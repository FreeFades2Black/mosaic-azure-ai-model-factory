"""
==============================================================================
CLINICAL DOCUMENT CHUNKER & VECTOR PREPARATION PIPELINE
==============================================================================
Splits clinical protocol documents into semantically coherent chunks.
==============================================================================
"""

import hashlib
import re
from dataclasses import dataclass
from typing import List


@dataclass
class ClinicalDocumentChunk:
    chunk_id: str
    protocol_id: str
    title: str
    department: str
    content: str


class DocumentChunker:
    """Chunks clinical documents with sliding window overlap."""

    def __init__(self, chunk_size: int = 400, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, protocol_id: str, title: str, department: str) -> List[ClinicalDocumentChunk]:
        """Splits text into chunks preserving sentence boundaries."""
        words = text.split()
        if not words:
            return []

        chunks = []
        start = 0
        idx = 0

        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk_text = " ".join(words[start:end])
            chunk_hash = hashlib.sha256(f"{protocol_id}_{idx}_{chunk_text[:30]}".encode()).hexdigest()[:12]

            chunks.append(
                ClinicalDocumentChunk(
                    chunk_id=f"chk_{protocol_id}_{chunk_hash}",
                    protocol_id=protocol_id,
                    title=title,
                    department=department,
                    content=chunk_text
                )
            )
            idx += 1
            if end == len(words):
                break
            start += self.chunk_size - self.overlap

        return chunks
