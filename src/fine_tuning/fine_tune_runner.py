"""
==============================================================================
AZURE AI FOUNDRY FINE-TUNING ORCHESTRATOR
==============================================================================
Submits, tracks, and manages supervised fine-tuning (SFT / LoRA) jobs in Azure.
==============================================================================
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class FineTuningJobSpec:
    base_model: str = "gpt-4o-mini-2024-07-18"
    model_suffix: str = "mosaic-clinical-v1"
    training_file: str = "synthetic_clinical_finetune.jsonl"
    validation_file: Optional[str] = None
    n_epochs: int = 3
    batch_size: int = 4
    learning_rate_multiplier: float = 1.0
    seed: int = 42
    integrations: list = field(default_factory=lambda: [{"type": "azure_ai_foundry_logging"}])


class FineTuningOrchestrator:
    """Manages Azure AI Foundry model fine-tuning job lifecycle."""

    def __init__(self, endpoint: str = "https://mosaic-openai-prod.openai.azure.com/"):
        self.endpoint = endpoint

    def build_submission_payload(self, spec: FineTuningJobSpec) -> Dict[str, Any]:
        """Builds the REST / SDK submission payload for Azure OpenAI Fine-Tuning."""
        payload = {
            "model": spec.base_model,
            "training_file": spec.training_file,
            "suffix": spec.model_suffix,
            "seed": spec.seed,
            "hyperparameters": {
                "n_epochs": spec.n_epochs,
                "batch_size": spec.batch_size,
                "learning_rate_multiplier": spec.learning_rate_multiplier,
            },
            "integrations": spec.integrations,
        }
        if spec.validation_file:
            payload["validation_file"] = spec.validation_file
        return payload

    def validate_spec(self, spec: FineTuningJobSpec) -> bool:
        """Ensures fine-tuning job parameters satisfy enterprise safety bounds."""
        if spec.n_epochs < 1 or spec.n_epochs > 20:
            raise ValueError(f"Epochs ({spec.n_epochs}) must be between 1 and 20.")
        if spec.batch_size < 1 or spec.batch_size > 64:
            raise ValueError(f"Batch size ({spec.batch_size}) must be between 1 and 64.")
        if spec.learning_rate_multiplier <= 0:
            raise ValueError("Learning rate multiplier must be positive.")
        if not spec.training_file:
            raise ValueError("Training file path cannot be empty.")
        return True
