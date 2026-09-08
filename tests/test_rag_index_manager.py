"""Tests for RAG index manager and document chunker."""
import pytest
from src.rag.search_index_manager import SearchIndexManager, SearchIndexConfig
from src.rag.document_chunker import DocumentChunker

def test_search_index_schema():
    manager = SearchIndexManager()
    schema = manager.build_schema()

    assert schema["name"] == "mosaic-clinical-protocols-index"
    assert len(schema["fields"]) >= 5
    assert schema["vectorSearch"]["profiles"][0]["algorithm"] == "hnsw-cosine"
    assert "semantic" in schema

def test_document_chunker():
    chunker = DocumentChunker(chunk_size=10, overlap=2)
    sample_text = "This is a clinical protocol for surgical antibiotic prophylaxis in hospital acute care."
    chunks = chunker.chunk_text(sample_text, "PROT_01", "Surgical Prophylaxis", "Surgery")

    assert len(chunks) >= 1
    assert chunks[0].protocol_id == "PROT_01"
    assert chunks[0].department == "Surgery"
