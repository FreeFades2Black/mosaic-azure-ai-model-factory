"""Tests for fine-tuning orchestrator."""
import pytest
from src.fine_tuning.fine_tune_runner import FineTuningOrchestrator, FineTuningJobSpec

def test_fine_tuning_payload_generation():
    orchestrator = FineTuningOrchestrator()
    spec = FineTuningJobSpec(
        base_model="gpt-4o-mini-2024-07-18",
        model_suffix="mosaic-clinical-v1",
        n_epochs=4,
        batch_size=8,
        learning_rate_multiplier=1.2
    )

    assert orchestrator.validate_spec(spec) is True
    payload = orchestrator.build_submission_payload(spec)

    assert payload["model"] == "gpt-4o-mini-2024-07-18"
    assert payload["suffix"] == "mosaic-clinical-v1"
    assert payload["hyperparameters"]["n_epochs"] == 4
    assert payload["hyperparameters"]["batch_size"] == 8

def test_fine_tuning_validation_failure():
    orchestrator = FineTuningOrchestrator()
    with pytest.raises(ValueError):
        orchestrator.validate_spec(FineTuningJobSpec(n_epochs=50))
