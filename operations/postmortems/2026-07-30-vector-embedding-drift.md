# Incident Post-Mortem: Vector Dimensionality Drift During Clinical Knowledge Base Re-Index

**Incident Date:** 2026-07-30  
**Impact Duration:** 24 minutes  
**Severity:** SEV-2  
**Root Cause:** A background re-indexing pipeline updated embedding generation from `text-embedding-ada-002` (1536 dims) to `text-embedding-3-small` (1536 dims with 512-dim truncation) without updating the HNSW search index schema, causing vector dimension mismatch exceptions in the clinical RAG pipeline.

## Timeline
* **11:00 UTC:** Re-index pipeline started batch indexing 50,000 clinical monographs with truncated 512-dim vectors.
* **11:04 UTC:** RAG query service threw `InvalidVectorDimensionError: expected 1536, received 512`.
* **11:12 UTC:** Incident response confirmed query embedding client was still generating full 1536-dim vectors.
* **11:18 UTC:** Schema rolled back; query service updated to enforce 1536-dim normalization contract across all environments.
* **11:24 UTC:** Index health restored; RAG query validation passed.

## Corrective Actions
1. Created unit test `test_rag_embeddings.py` asserting strict 1536-dimension contract validation before upserting into Azure AI Search.
2. Added pre-flight schema assertion verifying index vector dimensionality matches model output configuration.
