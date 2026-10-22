"""Knowledge base ingestion pipeline for FinPilot RAG.

Reads Markdown documents from `data/knowledge/`, chunks them by sections,
and indexes them into ChromaDB (with local JSON/SQLite fallback).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from app.config import CHROMA_DIR, KNOWLEDGE_DIR
from app.db.engine import SessionLocal
from app.db.models import KnowledgeDoc


def _chunk_markdown(text: str, filename: str) -> list[dict[str, Any]]:
    """Split markdown text into semantic section chunks."""
    lines = text.strip().splitlines()
    doc_title = filename
    for line in lines:
        if line.startswith("# "):
            doc_title = line.lstrip("# ").strip()
            break

    chunks: list[dict[str, Any]] = []
    current_section = doc_title
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("## "):
            if current_lines:
                chunk_body = "\n".join(current_lines).strip()
                if chunk_body:
                    chunks.append({
                        "doc_title": doc_title,
                        "section_title": current_section,
                        "content": f"{current_section}\n\n{chunk_body}",
                        "source_file": filename,
                    })
                current_lines = []
            current_section = line.lstrip("# ").strip()
        else:
            current_lines.append(line)

    if current_lines:
        chunk_body = "\n".join(current_lines).strip()
        if chunk_body:
            chunks.append({
                "doc_title": doc_title,
                "section_title": current_section,
                "content": f"{current_section}\n\n{chunk_body}",
                "source_file": filename,
            })

    # If no headers found, chunk by paragraphs (max ~500 chars)
    if not chunks and text.strip():
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for idx, p in enumerate(paragraphs):
            chunks.append({
                "doc_title": doc_title,
                "section_title": f"{doc_title} (Part {idx + 1})",
                "content": p,
                "source_file": filename,
            })

    return chunks


def ingest() -> int:
    """Ingest all knowledge documents into ChromaDB and fallback index.

    Returns the total number of chunks indexed.
    """
    if not KNOWLEDGE_DIR.exists():
        print(f"Knowledge directory not found: {KNOWLEDGE_DIR}")
        return 0

    md_files = sorted(KNOWLEDGE_DIR.glob("*.md"))
    if not md_files:
        print(f"No markdown documents found in {KNOWLEDGE_DIR}")
        return 0

    all_chunks: list[dict[str, Any]] = []
    for md_path in md_files:
        content = md_path.read_text(encoding="utf-8")
        chunks = _chunk_markdown(content, md_path.name)
        all_chunks.extend(chunks)

    # 1. Update SQLite KnowledgeDoc table
    try:
        from app.db.engine import engine
        from app.db.models import Base
        Base.metadata.create_all(bind=engine)

        db = SessionLocal()
        try:
            for md_path in md_files:
                raw_text = md_path.read_text(encoding="utf-8")
                title = raw_text.split("\n", 1)[0].lstrip("# ").strip() or md_path.stem
                existing = db.query(KnowledgeDoc).filter_by(source_file=md_path.name).first()
                if existing:
                    existing.title = title
                    existing.content = raw_text
                else:
                    db.add(KnowledgeDoc(title=title, content=raw_text, source_file=md_path.name))
            db.commit()
        finally:
            db.close()
    except Exception as e:
        print(f"Warning: Could not sync to SQLite KnowledgeDoc: {e}")

    # 2. Save local JSON index (ultra-reliable fallback)
    index_file = CHROMA_DIR.parent / "knowledge_index.json"
    index_file.parent.mkdir(parents=True, exist_ok=True)
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    # 3. Try indexing in ChromaDB if available
    chroma_ok = False
    try:
        import chromadb

        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = client.get_or_create_collection(name="finpilot_compliance")

        ids = [f"{c['source_file']}_{i}" for i, c in enumerate(all_chunks)]
        documents = [c["content"] for c in all_chunks]
        metadatas = [
            {
                "doc_title": c["doc_title"],
                "section_title": c["section_title"],
                "source_file": c["source_file"],
            }
            for c in all_chunks
        ]

        # Upsert chunks
        collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
        chroma_ok = True
    except Exception as exc:
        print(f"Note: ChromaDB indexing skipped/fallback used ({exc})")

    mode_str = " (ChromaDB + Local Index)" if chroma_ok else " (Local Index)"
    print(f"[OK] Successfully ingested {len(all_chunks)} chunks from {len(md_files)} documents.{mode_str}")
    return len(all_chunks)


if __name__ == "__main__":
    ingest()
