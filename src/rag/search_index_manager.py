"""
==============================================================================
AZURE AI SEARCH VECTOR INDEX & SEMANTIC RANKER MANAGER
==============================================================================
Defines the schema and vector search configuration for clinical protocol RAG.
==============================================================================
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class SearchIndexConfig:
    index_name: str = "mosaic-clinical-protocols-index"
    embedding_dimensions: int = 3072  # text-embedding-3-large
    algorithm_name: str = "hnsw-cosine"
    semantic_config_name: str = "clinical-semantic-config"


class SearchIndexManager:
    """Manages Azure AI Search index schemas and HNSW vector profiles."""

    def __init__(self, config: SearchIndexConfig = SearchIndexConfig()):
        self.config = config

    def build_schema(self) -> Dict[str, Any]:
        """Generates the full index definition payload."""
        return {
            "name": self.config.index_name,
            "fields": [
                {"name": "id", "type": "Edm.String", "key": True, "searchable": False},
                {"name": "protocol_id", "type": "Edm.String", "searchable": True, "filterable": True},
                {"name": "title", "type": "Edm.String", "searchable": True, "filterable": True},
                {"name": "department", "type": "Edm.String", "searchable": True, "filterable": True, "facetable": True},
                {"name": "content", "type": "Edm.String", "searchable": True},
                {
                    "name": "content_vector",
                    "type": "Collection(Edm.Single)",
                    "searchable": True,
                    "dimensions": self.config.embedding_dimensions,
                    "vectorSearchProfile": "clinical-vector-profile"
                }
            ],
            "vectorSearch": {
                "profiles": [
                    {
                        "name": "clinical-vector-profile",
                        "algorithm": self.config.algorithm_name
                    }
                ],
                "algorithms": [
                    {
                        "name": self.config.algorithm_name,
                        "kind": "hnsw",
                        "parameters": {
                            "m": 4,
                            "efConstruction": 400,
                            "efSearch": 500,
                            "metric": "cosine"
                        }
                    }
                ]
            },
            "semantic": {
                "configurations": [
                    {
                        "name": self.config.semantic_config_name,
                        "prioritizedFields": {
                            "titleField": {"fieldName": "title"},
                            "contentFields": [{"fieldName": "content"}]
                        }
                    }
                ]
            }
        }
