# Mosaic Azure AI Model Factory: Enterprise Fine-Tuning, RAG & Model Regulation

[![Build & Test](https://github.com/FreeFades2Black/mosaic-azure-ai-model-factory/actions/workflows/test-and-lint.yml/badge.svg)](https://github.com/FreeFades2Black/mosaic-azure-ai-model-factory/actions/workflows/test-and-lint.yml)
[![AI Foundry Model Evaluation](https://github.com/FreeFades2Black/mosaic-azure-ai-model-factory/actions/workflows/ai-foundry-eval-gate.yml/badge.svg)](https://github.com/FreeFades2Black/mosaic-azure-ai-model-factory/actions/workflows/ai-foundry-eval-gate.yml)
[![Infrastructure](https://img.shields.io/badge/Infrastructure-Real%20Production%20Builds-2e7d32?style=flat&logo=microsoftazure)](terraform/)
[![Data](https://img.shields.io/badge/Data-Simulated%20%2F%20Synthetic-orange?style=flat)](#-infrastructure-integrity--data-classification-notice)
[![Compliance](https://img.shields.io/badge/Compliance-HITRUST%20CSF%20v11%20%7C%20HIPAA-purple?style=flat)](docs/GOVERNANCE_AND_SAFETY.md)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

---

## ℹ️ Infrastructure Integrity & Data Classification Notice

> - **Real Infrastructure & Cloud Builds:** The underlying cloud architecture, Terraform/OpenTofu blueprints, Microsoft Entra ID tenant connections, passwordless OIDC Workload Identity Federation, and Azure AI Foundry hub/project configurations in this repository are **100% real, operational, and deployed**.
> - **Simulated Data & Scenarios:** All clinical training pairs, protocol questions, patient records, harm score prompts, and evaluation matrices are **simulated / synthetic reference data** created for model benchmarking and governance testing. No live patient data or actual Protected Health Information (PHI) is hosted or transmitted.

---

## 📖 Executive Summary & System Overview

The **Mosaic Azure AI Model Factory** is an enterprise-grade framework designed to build, fine-tune, ground, and govern Artificial Intelligence models and autonomous clinical agents in Microsoft Azure.

Spanning **Azure AI Foundry (Hub & Projects)**, **Azure OpenAI Service**, **Azure AI Search (RAG)**, and **Azure AI Content Safety**, this repository delivers a complete Infrastructure as Code (IaC) and Python SDK toolchain engineered to meet strict **HITRUST CSF v11** and **HIPAA § 164.312** regulatory standards.

```mermaid
graph TD
    subgraph "Clinical Edge & Application Consumers"
        ClinicianApp["Clinical Copilot & Decision Support Web App<br/>(Private Endpoint / TLS 1.3)"]
        EHRStream["EHR Interoperability Stream<br/>(HL7 v2 / FHIR R4 Event Hubs)"]
    end

    subgraph "Azure AI Foundry Enterprise Hub (East US 2)"
        AIHub["Azure AI Foundry Hub<br/>(Tenant: 18795ad0-94b5-4aa9-bea9-d3f5daa93cf6)"]
        AIProject["Clinical Agent Project<br/>(mosaic-clinical-agent-project)"]
        AIHub --> AIProject

        subgraph "Foundation Model Deployments"
            GPT4o["GPT-4o Multi-Modal Model (100K TPM)"]
            EmbeddingModel["text-embedding-3-large (3,072-D)"]
        end

        subgraph "RAG Vector Index & Safety Guardrails"
            AISearch["Azure AI Search<br/>(HNSW Vector Index + Semantic Ranker)"]
            SafetyShield["Azure AI Content Safety<br/>(Prompt Shield + Severity=0)"]
            PHIScan["HIPAA PHI Scanner<br/>(Zero-Leak Enforcement)"]
        end

        subgraph "Storage & Cryptographic Foundation"
            Storage["Azure Data Lake Storage Gen2<br/>(Checkpoints & JSONL Datasets)"]
            KeyVault["Azure Key Vault (Premium)<br/>(FIPS 140-2 Level 3 HSM CMK)"]
            LAW["Log Analytics Workspace<br/>(730-Day Immutable Audit Trail)"]
        end
    end

    ClinicianApp --> SafetyShield
    SafetyShield -->|Pass| PHIScan
    PHIScan -->|Pass| GPT4o
    AISearch -->|Context Grounding| GPT4o
    EmbeddingModel --> AISearch
    GPT4o --> Storage
    GPT4o --> KeyVault
    GPT4o --> LAW
```

---

## 🏛️ Core Capabilities & Architecture Pillars

### 1. Automated Supervised Fine-Tuning (SFT / LoRA)
- **Synthetic Dataset Engine:** Generates chat-completion JSONL training sets with system prompts enforcing clinical protocol tone.
- **Hyperparameter Optimization:** Configurable epochs ($3 \text{ to } 5$), batch sizes, and learning rate multipliers ($0.8 \text{ to } 1.2$) to prevent catastrophic forgetting.
- **Automated Checkpointing:** Model weights stored in CMK-encrypted Geo-Redundant Storage (GRS).

### 2. High-Dimensional Hybrid Vector Search (RAG)
- **3,072-Dimension Embeddings:** Vectorized via `text-embedding-3-large`.
- **HNSW Vector Indexing:** Hierarchical Navigable Small World algorithm with Cosine distance metric.
- **Microsoft Semantic Ranker:** Re-ranks top-$50$ vector results using deep learning models to ensure maximum clinical relevance.

### 3. Multi-Tiered AI Governance & Safety Shields
- **Prompt Shield:** Detects adversarial injections, jailbreaks (DAN mode), and system overrides.
- **Content Safety Gate:** Zero-tolerance filtering across Hate, Violence, Self-Harm, and Sexual categories ($\text{Severity} = 0$).
- **HIPAA PHI Redactor:** Scans for SSNs, Medical Record Numbers (MRNs), phone numbers, and dates of birth.
- **Groundedness Evaluator:** Asserts response alignment to source documents with a mandatory threshold ($\text{Score} \ge 4.00 / 5.00$).

---

## 📂 Repository File Structure

```
mosaic-azure-ai-model-factory/
├── .github/
│   └── workflows/
│       ├── test-and-lint.yml           # Automated unit testing & linting
│       ├── ai-foundry-eval-gate.yml    # Model evaluation & Content Safety compliance gate
│       └── deploy-ai-infrastructure.yml# Automated OpenTofu/Terraform deployment via OIDC
├── terraform/
│   ├── main.tf                         # AI Foundry Hub, Projects, OpenAI, GPT-4o, Embeddings, AI Search, Content Safety
│   ├── variables.tf                    # Fully annotated variable schema with validation
│   ├── outputs.tf                      # Endpoints, IDs, principal mappings
│   ├── providers.tf                    # azurerm and random providers configuration
│   └── terraform.tfvars.example        # Sanitized enterprise deployment parameters
├── src/
│   ├── fine_tuning/
│   │   ├── dataset_generator.py        # Generates synthetic clinical JSONL datasets with HIPAA-safe records
│   │   └── fine_tune_runner.py         # Submits & tracks Azure AI Foundry fine-tuning jobs (LoRA / SFT)
│   ├── rag/
│   │   ├── search_index_manager.py     # Manages Azure AI Search vector indexes & Semantic Ranker configurations
│   │   └── document_chunker.py         # Ingestion, tokenization, and vector embedding pipeline
│   ├── safety/
│   │   ├── content_safety_shield.py    # Azure AI Content Safety evaluator (Hate, Violence, Self-Harm, Sexual)
│   │   ├── prompt_shield_detector.py   # Jailbreak and indirect prompt injection scanner
│   │   └── phi_scanner.py              # Zero-leak regex and NER identifier scanner for patient data
│   └── evaluation/
│       ├── groundedness_evaluator.py   # Groundedness & clinical truth scoring against vector context
│       └── model_regulation_gate.py    # Multi-gate automated policy enforcement engine
├── tests/
│   ├── conftest.py                     # Test fixtures and shared paths
│   ├── test_dataset_generator.py       # Validates JSONL formatting and HIPAA safety
│   ├── test_fine_tune_runner.py        # Validates fine-tuning payload generation and state tracking
│   ├── test_rag_index_manager.py       # Validates Azure AI Search schema and vector dimensions
│   ├── test_safety_and_phi.py          # Validates content safety harm scoring and PHI redactor
│   ├── test_groundedness_gate.py       # Validates groundedness evaluation thresholds (>= 4.0/5.0)
│   └── test_terraform_integrity.py     # Validates Terraform HCL syntax and line-by-line annotation density
├── docs/
│   ├── ARCHITECTURE.md                 # Deep-dive architecture notes, diagrams, and component interactions
│   ├── MODEL_FINE_TUNING_GUIDE.md      # Comprehensive fine-tuning playbook (LoRA vs SFT, hyperparameters)
│   ├── RAG_AND_VECTOR_SEARCH.md        # Azure AI Search HNSW indexing & Semantic Reranking reference
│   ├── GOVERNANCE_AND_SAFETY.md        # Content Safety thresholds, Prompt Shields, and HIPAA compliance
│   └── DEPLOYMENT_PLAYBOOK.md          # Step-by-step Azure CLI, OpenTofu, and OIDC deployment instructions
├── pyproject.toml                      # Modern packaging and pytest configuration
├── requirements.txt                    # Pinned Python dependencies
├── .gitignore                          # Standard git ignore rules
├── LICENSE                             # Apache 2.0 License
└── README.md                           # Master documentation
```

---

## 🚀 Quickstart & Execution Guide

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/FreeFades2Black/mosaic-azure-ai-model-factory.git
cd mosaic-azure-ai-model-factory
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Automated Test Suite
```bash
pytest tests/ -v
```

### 3. Generate Synthetic Clinical Fine-Tuning Dataset
```python
from src.fine_tuning.dataset_generator import SyntheticDatasetGenerator

generator = SyntheticDatasetGenerator()
dataset_file = generator.generate_jsonl("synthetic_clinical_finetune.jsonl")
print(f"Dataset generated at: {dataset_file}")
```

### 4. Deploy Infrastructure via OpenTofu / Terraform
```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
tofu init
tofu plan -out=tfplan
tofu apply tfplan
```

### 5. Run Full Governance & Model Evaluation Gate
```python
from src.evaluation.model_regulation_gate import ModelRegulationGate

gate = ModelRegulationGate()
prompt = "What is the stroke care thrombolytic therapy window?"
context = "Under Mosaic Stroke Care Pathways, intravenous Alteplase is indicated within 4.5 hours of symptom onset."
response = "Under Mosaic Stroke Care Pathways, intravenous Alteplase is indicated within 4.5 hours of symptom onset."

report = gate.run_full_evaluation(prompt, response, context)
print(f"Compliance Passed: {report.overall_passed}")
print(f"Groundedness Score: {report.groundedness_score} / 5.00")
```

---

## 📜 Compliance & Regulation Citations

- **HIPAA Security Rule (§ 164.312):** Enforces encryption in transit (TLS 1.3), encryption at rest (FIPS 140-2 Level 3 HSM CMK), and automated zero-leak PHI token redaction.
- **HITRUST CSF v11 (Domain 01.0 & 03.0):** Enforces role-based access control, system-assigned managed identities, and continuous model harm evaluation.
- **Microsoft Cloud Adoption Framework (CAF):** Implements subscription vending and hub-and-spoke private endpoint isolation for AI workloads.

---

## 📄 License

Licensed under the [Apache License, Version 2.0](LICENSE). Copyright © 2026 Mosaic Healthcare Enterprise Architecture Review Board. All rights reserved.
