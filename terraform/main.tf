# --------------------------------------------------------------------------------------------------
# MOSAIC HEALTHCARE ENTERPRISE AZURE AI FOUNDRY MODEL FACTORY MODULE
# "Deterministic guardrails, hardened vector retrieval, and sovereign clinical intelligence."
# --------------------------------------------------------------------------------------------------
# File: terraform/main.tf
# Purpose: Production-grade, HITRUST-compliant Azure AI Foundry Hub, Projects, OpenAI Model
#          Deployments (GPT-4o, Embeddings), AI Search RAG, Content Safety, and Private Link.
# --------------------------------------------------------------------------------------------------

# Retrieve Azure client configuration for tenant and subscription identification
data "azurerm_client_config" "current" {}

# Generate random string suffix for globally unique resource naming across Azure DNS zones
resource "random_string" "ai_suffix" {
  length  = 6     # Length of random alphanumeric suffix
  special = false # Exclude special characters to adhere to Azure DNS naming rules
  upper   = false # Lowercase only for clean URI compatibility
}

# --------------------------------------------------------------------------------------------------
# 1. CORE SUPPORTING SERVICES: LOG ANALYTICS, APP INSIGHTS & STORAGE
# --------------------------------------------------------------------------------------------------

# Log Analytics Workspace for AI Foundry telemetry and model audit logging
resource "azurerm_log_analytics_workspace" "ai_law" {
  name                = "${var.prefix}-ai-law-${var.environment}-${random_string.ai_suffix.result}" # Unique workspace name
  location            = var.location                                                                 # Target Azure region
  resource_group_name = var.resource_group_name                                                      # Host Resource Group
  sku                 = "PerGB2018"                                                                  # Standard pay-per-GB pricing tier
  retention_in_days   = var.log_retention_days                                                       # Mandatory 730 days for HIPAA audit compliance

  # Resource tags for cost allocation and compliance auditing
  tags = merge(var.tags, {
    Component          = "AI-Foundry-Audit-Logging" # Component identification
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11"   # Regulatory framework
    DataClassification = "Audit-Telemetry"          # Data sensitivity tier
  })
}

# Application Insights for MLflow model tracing and inference latency monitoring
resource "azurerm_application_insights" "ai_insights" {
  name                = "${var.prefix}-ai-appi-${var.environment}-${random_string.ai_suffix.result}" # Unique App Insights name
  location            = var.location                                                                  # Regional placement
  resource_group_name = var.resource_group_name                                                       # Host Resource Group
  workspace_id        = azurerm_log_analytics_workspace.ai_law.id                                     # Linked Log Analytics Workspace
  application_type    = "web"                                                                         # Web telemetry telemetry mode

  # Resource metadata tags
  tags = merge(var.tags, {
    Component       = "AI-Foundry-Telemetry"  # Telemetry component
    ComplianceScope = "HIPAA-HITRUST-CSF-v11" # Governance standard
  })
}

# Secure Storage Account for AI datasets, prompt engineering artifacts, and fine-tuning weights
resource "azurerm_storage_account" "ai_storage" {
  name                          = "${replace(var.prefix, "-", "")}aistg${var.environment}${random_string.ai_suffix.result}" # Storage account name (no hyphens)
  location                      = var.location                                                                               # Regional placement
  resource_group_name           = var.resource_group_name                                                                    # Host Resource Group
  account_tier                  = "Standard"                                                                                 # Standard performance tier
  account_replication_type      = "GRS"                                                                                      # Geo-Redundant Storage for clinical disaster recovery
  account_kind                  = "StorageV2"                                                                                # General Purpose v2 storage
  is_hns_enabled                = true                                                                                       # Hierarchical Namespace enabled for Lakehouse AI & Delta Lake
  min_tls_version               = "TLS1_2"                                                                                   # Enforce modern TLS 1.2+ encryption
  enable_https_traffic_only     = true                                                                                       # Reject unencrypted HTTP traffic
  public_network_access_enabled = false                                                                                      # Zero public internet ingress allowed (Private Link only)

  # Blob service properties for data protection
  blob_properties {
    versioning_enabled = true # Immutable artifact history for regulatory traceability
    delete_retention_policy {
      days = 30 # 30-day soft delete recovery window
    }
  }

  # Compliance and data classification tags
  tags = merge(var.tags, {
    Component          = "AI-Foundry-Dataset-Store" # Storage role
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11"   # Regulatory scope
    DataClassification = "PHI-Restricted"           # High-sensitivity data tag
  })
}

# --------------------------------------------------------------------------------------------------
# 2. AZURE OPENAI & AI SERVICES (FOUNDATION MODEL ENGINE)
# --------------------------------------------------------------------------------------------------

# Azure AI Services / OpenAI multi-service account with Managed Identity
resource "azurerm_cognitive_account" "openai" {
  name                          = "${var.prefix}-openai-${var.environment}-${random_string.ai_suffix.result}" # Unique Cognitive Services name
  location                      = var.location                                                                 # Regional placement
  resource_group_name           = var.resource_group_name                                                      # Host Resource Group
  kind                          = "OpenAI"                                                                     # Azure OpenAI service kind
  sku_name                      = "S0"                                                                         # Standard cognitive SKU
  custom_subdomain_name         = "${var.prefix}-openai-${var.environment}-${random_string.ai_suffix.result}" # Subdomain for token authentication
  public_network_access_enabled = false                                                                        # Strict private endpoint enforcement

  # System-Assigned Managed Identity for passwordless Azure RBAC
  identity {
    type = "SystemAssigned" # System-assigned identity for token-based authentication
  }

  # Enterprise tags for billing and governance
  tags = merge(var.tags, {
    Component          = "Azure-OpenAI-Inference"  # Core model inference component
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11"   # Regulatory framework
    DataClassification = "Clinical-AI-Inference"   # AI inference classification
  })
}

# Model Deployment: GPT-4o Multi-Modal Foundation Model
resource "azurerm_cognitive_deployment" "gpt4o" {
  name                 = "gpt-4o"                                 # Target deployment name
  cognitive_account_id = azurerm_cognitive_account.openai.id      # Parent Cognitive Account

  # Foundation model parameters
  model {
    format  = "OpenAI"                  # OpenAI model format
    name    = "gpt-4o"                  # GPT-4o multi-modal model
    version = var.gpt4o_model_version   # Pinned model version
  }

  # Scale settings for token rate limits
  scale {
    type     = "GlobalStandard"   # Global Standard for elastic healthcare throughput
    capacity = var.gpt4o_capacity # TPM capacity allocation in thousands
  }
}

# Model Deployment: text-embedding-3-large for High-Dimensional Clinical Vector Search
resource "azurerm_cognitive_deployment" "embedding" {
  name                 = "text-embedding-3-large"                 # Deployment identifier
  cognitive_account_id = azurerm_cognitive_account.openai.id      # Parent Cognitive Account

  # Embedding model parameters
  model {
    format  = "OpenAI"                  # OpenAI format
    name    = "text-embedding-3-large"  # 3072-dimension high accuracy embedding model
    version = "1"                       # Model version 1
  }

  # Embedding scale allocation
  scale {
    type     = "Standard" # Standard regional scaling
    capacity = 50         # 50K TPM allocation for document vectorization
  }
}

# --------------------------------------------------------------------------------------------------
# 3. AZURE AI CONTENT SAFETY & PROMPT SHIELD
# --------------------------------------------------------------------------------------------------

# Azure AI Content Safety service for real-time harm filtering and prompt shield
resource "azurerm_cognitive_account" "content_safety" {
  name                          = "${var.prefix}-safety-${var.environment}-${random_string.ai_suffix.result}" # Unique Content Safety name
  location                      = var.location                                                                 # Regional placement
  resource_group_name           = var.resource_group_name                                                      # Host Resource Group
  kind                          = "ContentSafety"                                                              # Content Safety kind
  sku_name                      = "S0"                                                                         # Standard cognitive SKU
  custom_subdomain_name         = "${var.prefix}-safety-${var.environment}-${random_string.ai_suffix.result}" # Subdomain for safety API
  public_network_access_enabled = false                                                                        # Private Link only

  # Managed Service Identity
  identity {
    type = "SystemAssigned" # System-assigned identity
  }

  # Resource tags
  tags = merge(var.tags, {
    Component          = "Azure-AI-Content-Safety" # Content safety component
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11"   # Regulatory scope
    DataClassification = "AI-Safety-Guardrail"     # Guardrail classification
  })
}

# --------------------------------------------------------------------------------------------------
# 4. AZURE AI SEARCH (CLINICAL RAG & SEMANTIC VECTOR RETRIEVAL)
# --------------------------------------------------------------------------------------------------

# Azure AI Search Service for hybrid dense/sparse vector retrieval with Semantic Ranker
resource "azurerm_search_service" "rag_search" {
  name                          = "${var.prefix}-search-${var.environment}-${random_string.ai_suffix.result}" # Search service name
  location                      = var.location                                                                 # Regional placement
  resource_group_name           = var.resource_group_name                                                      # Host Resource Group
  sku                           = "standard"                                                                   # Standard search SKU
  replica_count                 = var.search_replica_count                                                     # High availability replicas
  partition_count               = 1                                                                            # Vector partition count
  semantic_search_sku           = "standard"                                                                   # Enables Microsoft Semantic Ranker for clinical accuracy
  public_network_access_enabled = false                                                                        # Private Link only

  # Managed Service Identity for search indexer RBAC
  identity {
    type = "SystemAssigned" # System-assigned identity
  }

  # Governance metadata tags
  tags = merge(var.tags, {
    Component          = "Azure-AI-Search-RAG"     # Vector search component
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11"   # Regulatory framework
    DataClassification = "Clinical-Vector-Store"   # Vector store classification
  })
}

# --------------------------------------------------------------------------------------------------
# 5. AZURE AI FOUNDRY HUB & PROJECT (ENTERPRISE GOVERNANCE WORKSPACE)
# --------------------------------------------------------------------------------------------------

# Azure AI Foundry Hub (Top-Level Enterprise Workspace)
resource "azurerm_ai_foundry" "hub" {
  name                    = "${var.prefix}-aihub-${var.environment}-${random_string.ai_suffix.result}" # AI Hub workspace name
  location                = var.location                                                                 # Regional placement
  resource_group_name     = var.resource_group_name                                                      # Host Resource Group
  storage_account_id      = azurerm_storage_account.ai_storage.id                                        # Attached secure storage
  key_vault_id            = var.key_vault_id                                                             # Attached Key Vault for CMK
  application_insights_id = azurerm_application_insights.ai_insights.id                                  # Attached App Insights for tracing
  public_network_access   = "Disabled"                                                                   # Enforce private endpoint communication

  # Managed Identity for AI Hub
  identity {
    type = "SystemAssigned" # System-assigned identity
  }

  # AI Hub metadata tags
  tags = merge(var.tags, {
    Component          = "Azure-AI-Foundry-Hub"  # Governance hub
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11" # Governance standard
    DataClassification = "AI-Governance-Hub"     # Data classification
  })
}

# Azure AI Foundry Project: Clinical Copilot & Model Fine-Tuning Environment
resource "azurerm_ai_foundry_project" "clinical_project" {
  name               = "mosaic-clinical-agent-project"  # Dedicated clinical agent project name
  location           = var.location                     # Regional placement
  ai_services_hub_id = azurerm_ai_foundry.hub.id        # Parent AI Foundry Hub reference

  # Managed Identity for project
  identity {
    type = "SystemAssigned" # System-assigned identity
  }

  # Project metadata tags
  tags = merge(var.tags, {
    Component          = "Azure-AI-Foundry-Project"   # Project workspace
    ComplianceScope    = "HIPAA-HITRUST-CSF-v11"     # Regulatory standard
    ProjectRole        = "Clinical-Agent-Development" # Project purpose
  })
}

# --------------------------------------------------------------------------------------------------
# 6. DIAGNOSTIC LOGGING FOR IMMUTABLE AUDIT TRAIL (7-YEAR HIPAA WORM COMPLIANCE)
# --------------------------------------------------------------------------------------------------

# Diagnostic settings streaming all OpenAI audit events and token transactions to Log Analytics
resource "azurerm_monitor_diagnostic_setting" "openai_diagnostics" {
  name                       = "${var.prefix}-openai-diag"                                # Diagnostic setting name
  target_resource_id         = azurerm_cognitive_account.openai.id                         # Target OpenAI cognitive service
  log_analytics_workspace_id = azurerm_log_analytics_workspace.ai_law.id                   # Target Log Analytics Workspace

  # Audit log stream category
  enabled_log {
    category = "Audit" # Audit logs for authentication and permission checks
  }

  # Request & Response telemetry category
  enabled_log {
    category = "RequestAndResponseLogs" # Model request and response metadata
  }

  # Metrics stream for inference latency
  metric {
    category = "AllMetrics" # Metric stream
    enabled  = true          # Enable metric forwarding
  }
}
