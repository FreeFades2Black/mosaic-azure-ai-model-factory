# Architecture & Topology Deep Dive: Azure AI Foundry Model Factory

## 1. Enterprise Architecture Overview

The **Mosaic Azure AI Model Factory** establishes an automated, security-hardened environment for training, fine-tuning, vector-grounding, and deploying clinical Artificial Intelligence models within Microsoft Azure.

```mermaid
graph TD
    subgraph "Clinical Applications & Ingress"
        EHR["EHR Interoperability Stream (FHIR R4 / HL7 v2)"]
        CopilotApp["Clinical Copilot Application (HTTPS / TLS 1.3)"]
    end

    subgraph "Azure AI Foundry Enterprise Hub (East US 2)"
        AIHub["Azure AI Foundry Hub<br/>(Tenant: 18795ad0-94b5-4aa9-bea9-d3f5daa93cf6)"]
        AIProject["Clinical Agent Project<br/>(mosaic-clinical-agent-project)"]
        AIHub --> AIProject

        subgraph "Foundation Model Deployments"
            GPT4o["GPT-4o Multi-Modal Model (100K TPM)"]
            EmbeddingModel["text-embedding-3-large (3,072-D)"]
        end

        subgraph "Retrieval-Augmented Generation & Safety"
            AISearch["Azure AI Search<br/>(HNSW Vector Index + Semantic Ranker)"]
            SafetyShield["Azure AI Content Safety<br/>(Prompt Shield + Harm Severity=0)"]
            PHIScan["HIPAA PHI Redactor<br/>(Zero-Leak Enforcement)"]
        end

        subgraph "Cryptographic & Storage Subsystem"
            Storage["Azure Data Lake Storage Gen2<br/>(Checkpoints & JSONL Datasets)"]
            KeyVault["Azure Key Vault (Premium)<br/>(FIPS 140-2 Level 3 HSM CMK)"]
            LAW["Log Analytics Workspace<br/>(730-Day Immutable Audit Trail)"]
        end
    end

    CopilotApp --> SafetyShield
    SafetyShield -->|Pass| PHIScan
    PHIScan -->|Pass| GPT4o
    AISearch -->|Context Grounding| GPT4o
    EmbeddingModel --> AISearch
    GPT4o --> Storage
    GPT4o --> KeyVault
    GPT4o --> LAW
```

## 2. Component Taxonomy & Security Guarantees

| Component | Azure Service Resource | Security & Compliance Guarantee |
| :--- | :--- | :--- |
| **Governance Hub** | `azurerm_ai_foundry` | Role-Based Access Control (RBAC), Entra ID Managed Identity, Disallow Public Network Access. |
| **Inference Engine** | `azurerm_cognitive_account` (OpenAI) | GlobalStandard TPM scaling, CMK Encryption at Rest, TLS 1.3 in Transit. |
| **Vector Index** | `azurerm_search_service` | 3,072-dimension HNSW cosine indexing with deep learning Semantic Reranking. |
| **Safety Guardrail** | `azurerm_cognitive_account` (ContentSafety) | Prompt Shield against jailbreaks and zero-tolerance harm scoring (Hate/Violence/Self-Harm=0). |
| **Audit Pipeline** | `azurerm_log_analytics_workspace` | Diagnostic log streaming with 730-day retention for HIPAA § 164.312 compliance. |
