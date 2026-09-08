"""Pytest configuration and shared fixtures."""
import pytest
from pathlib import Path

@pytest.fixture
def repo_root():
    return Path(__file__).parent.parent.resolve()
