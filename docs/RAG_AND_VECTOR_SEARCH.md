# RAG & Semantic Vector Search Guide: Azure AI Search

## 1. Vector Search Pipeline Architecture

```mermaid
graph LR
    Doc["Clinical Protocols & Manuals"] --> Chunker["Sliding Window Chunker (400 words)"]
    Chunker --> Embed["text-embedding-3-large (3072-D)"]
    Embed --> Index["Azure AI Search (HNSW Index)"]
    
    Query["Clinician Query"] --> EmbedQuery["Embed Query"]
    EmbedQuery --> Index
    Index --> TopK["Top-50 Vector Candidates"]
    TopK --> Semantic["Microsoft Semantic Ranker"]
    Semantic --> Context["Top-5 Reranked Chunks"]
    Context --> LLM["GPT-4o Generation"]
```

## 2. Index Configuration Reference

- **Vector Algorithm:** `HNSW` (Hierarchical Navigable Small World) with Cosine Metric.
- **Parameters:** `m=4`, `efConstruction=400`, `efSearch=500`.
- **Dimensions:** 3,072 dimensions matching `text-embedding-3-large`.
- **Semantic Configuration:** Prioritized fields (`title`, `content`) for deep learning re-ranking.
