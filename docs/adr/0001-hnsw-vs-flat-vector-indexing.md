# ADR-0001: Hierarchical Navigable Small World (HNSW) vs Flat Cosine Search for Clinical RAG

**Status:** Accepted  
**Date:** 2026-06-08  
**Lead Architect:** William Free Hall (Free) <whall4.wh@gmail.com>

## 1. Context & Operational Challenge
Our clinical retrieval-augmented generation (RAG) system indexes over 2.5 million medical guidelines, pharmacology monographs, and patient histories. We needed a vector search index offering sub-50ms query latencies without exceeding memory budgets.

## 2. Options Considered
* **Option A: Exhaustive Flat Cosine Search (Exact Nearest Neighbor)**
  - *Evaluation:* 100% recall accuracy, but search latency scales linearly (`O(N)`), reaching 850ms per query at 2.5 million vectors.
* **Option B: Hierarchical Navigable Small World (HNSW) Graph Indexing**
  - *Evaluation:* Approximate Nearest Neighbor (ANN) search achieves logarithmic query time (`O(log N)`), executing in 12ms with 98.6% recall accuracy at `M=16, efConstruction=200`.

## 3. Decision & Trade-Off Accepted
We adopted **Option B (HNSW Indexing)**.  
**Trade-Off Accepted:** Increases vector index memory consumption by ~25% and index build times, but delivers a 70x query throughput increase required for real-time clinician assistance.
