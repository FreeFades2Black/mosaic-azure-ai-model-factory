"""Tests for synthetic dataset generator."""
import json
import pytest
from src.fine_tuning.dataset_generator import SyntheticDatasetGenerator

def test_dataset_generator_output(tmp_path):
    generator = SyntheticDatasetGenerator()
    out_file = tmp_path / "test_data.jsonl"
    result_path = generator.generate_jsonl(str(out_file))

    assert out_file.exists()
    lines = out_file.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) >= 3

    for line in lines:
        data = json.loads(line)
        assert "messages" in data
        assert len(data["messages"]) == 3
        assert data["messages"][0]["role"] == "system"
        assert data["messages"][1]["role"] == "user"
        assert data["messages"][2]["role"] == "assistant"
