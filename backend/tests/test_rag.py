from app.rag.ingest import ingest
from app.rag.retrieve import retrieve

def test_rag_ingest():
    """Test ingestion chunks and indexes knowledge docs."""
    count = ingest()
    assert count > 0


def test_rag_retrieve():
    """Test retrieval finds relevant GST compliance citations."""
    results = retrieve("GST invoice rules and mandatory details")
    assert isinstance(results, list)
    assert len(results) > 0
    top = results[0]
    assert "title" in top
    assert "content" in top
    assert "similarity" in top
    assert top["similarity"] >= 0.4
