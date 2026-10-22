"""Knowledge retrieval module for FinPilot RAG."""

from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any, Optional

from app.config import (
    CHROMA_DIR,
    DATA_DIR,
    KNOWLEDGE_DIR,
    RAG_MIN_SIMILARITY,
    RAG_TOP_K,
)

_STOPWORDS = {
    "a", "an", "the", "and", "or", "in", "on", "at", "to", "for", "of", "with",
    "is", "are", "was", "were", "what", "how", "when", "where", "which", "who",
    "does", "do", "can", "should", "under", "about", "rules", "rule", "india",
    "kya", "hai", "ka", "ki", "ke", "ko", "mein", "se", "aur", "ya", "par",
}


def _tokenize(text: str) -> list[str]:
    """Extract lowercase alpha tokens, skipping common stopwords."""
    words = re.findall(r"\b[a-zA-Z0-9_\u0900-\u097F]{2,}\b", text.lower())
    return [w for w in words if w not in _STOPWORDS]


def _fallback_search(
    query: str,
    chunks: list[dict[str, Any]],
    top_k: int,
    min_similarity: float,
) -> list[dict[str, Any]]:
    """Term-frequency BM25-style keyword search over chunked knowledge."""
    q_tokens = _tokenize(query)
    if not q_tokens:
        return []

    scored: list[tuple[float, dict[str, Any]]] = []

    for chunk in chunks:
        content = chunk.get("content", "")
        title = chunk.get("section_title", "")
        doc_title = chunk.get("doc_title", "")

        c_tokens = _tokenize(content)
        t_tokens = set(_tokenize(title + " " + doc_title))

        if not c_tokens:
            continue

        # Score matching tokens
        match_count = 0
        title_matches = 0
        for token in q_tokens:
            count = c_tokens.count(token)
            if count > 0:
                match_count += math.log(1 + count)
            if token in t_tokens:
                title_matches += 1

        if match_count == 0 and title_matches == 0:
            continue

        # Calculate normalized similarity
        q_len = max(len(q_tokens), 1)
        coverage = min(1.0, (match_count + (title_matches * 1.5)) / q_len)
        # Scaled between 0.45 and 0.95
        sim = 0.45 + (coverage * 0.5)
        sim = min(0.98, round(sim, 3))

        if sim >= min_similarity:
            scored.append((
                sim,
                {
                    "title": chunk.get("section_title") or chunk.get("doc_title", "Document"),
                    "content": content,
                    "source": chunk.get("source_file", "knowledge"),
                    "similarity": sim,
                },
            ))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:top_k]]


def retrieve(
    query: str,
    top_k: Optional[int] = None,
    min_similarity: Optional[float] = None,
) -> list[dict[str, Any]]:
    """Retrieve relevant knowledge sections for a question.

    Returns:
        List of dicts:
            [{"title": str, "content": str, "source": str, "similarity": float}]
    """
    if not query or not query.strip():
        return []

    k = top_k if top_k is not None else RAG_TOP_K
    min_sim = min_similarity if min_similarity is not None else RAG_MIN_SIMILARITY

    # 1. Try ChromaDB if available
    try:
        import chromadb

        if CHROMA_DIR.exists():
            client = chromadb.PersistentClient(path=str(CHROMA_DIR))
            collection = client.get_collection(name="finpilot_compliance")
            results = collection.query(query_texts=[query], n_results=k)

            output: list[dict[str, Any]] = []
            if results and results.get("documents") and results["documents"][0]:
                docs = results["documents"][0]
                metas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(docs)
                distances = results["distances"][0] if results.get("distances") else [0.0] * len(docs)

                for doc, meta, dist in zip(docs, metas, distances):
                    # Chroma returns L2 or cosine distance; convert to similarity [0, 1]
                    sim = max(0.0, min(1.0, 1.0 - (float(dist) / 2.0)))
                    sim = round(sim, 3)
                    if sim >= min_sim:
                        title = meta.get("section_title") or meta.get("doc_title", "Compliance Note")
                        output.append({
                            "title": title,
                            "content": doc,
                            "source": meta.get("source_file", "knowledge"),
                            "similarity": sim,
                        })

                if output:
                    return output
    except Exception:
        pass

    # 2. Fallback to local JSON index
    index_file = DATA_DIR / "knowledge_index.json"
    chunks: list[dict[str, Any]] = []

    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                chunks = json.load(f)
        except Exception:
            chunks = []

    # If index not yet written, dynamically parse data/knowledge
    if not chunks and KNOWLEDGE_DIR.exists():
        from app.rag.ingest import _chunk_markdown

        for md_path in KNOWLEDGE_DIR.glob("*.md"):
            chunks.extend(_chunk_markdown(md_path.read_text(encoding="utf-8"), md_path.name))

    return _fallback_search(query, chunks, top_k=k, min_similarity=min_sim)
