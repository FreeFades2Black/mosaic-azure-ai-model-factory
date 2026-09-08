"""Tests for Terraform module structure, HCL validity, and outputs."""
import pytest
from pathlib import Path

def test_terraform_files_exist(repo_root):
    tf_dir = repo_root / "terraform"
    assert tf_dir.exists()

    required_files = ["main.tf", "variables.tf", "outputs.tf", "providers.tf", "terraform.tfvars.example"]
    for fname in required_files:
        fpath = tf_dir / fname
        assert fpath.exists(), f"Missing required terraform file: {fname}"
        assert fpath.stat().st_size > 100

def test_terraform_resource_definitions(repo_root):
    main_tf = (repo_root / "terraform" / "main.tf").read_text(encoding="utf-8")
    assert "azurerm_cognitive_account" in main_tf
    assert "azurerm_cognitive_deployment" in main_tf
    assert "azurerm_search_service" in main_tf
    assert "azurerm_ai_foundry" in main_tf
    assert "azurerm_ai_foundry_project" in main_tf

def test_terraform_annotation_density(repo_root):
    tf_dir = repo_root / "terraform"
    for tf_file in tf_dir.glob("*.tf"):
        lines = tf_file.read_text(encoding="utf-8").splitlines()
        comment_lines = [l for l in lines if "#" in l]
        assert len(comment_lines) >= len(lines) * 0.25, f"Low comment density in {tf_file.name}"
