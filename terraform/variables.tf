# --------------------------------------------------------------------------------------------------
# MOSAIC HEALTHCARE ENTERPRISE AZURE AI FOUNDRY MODULE
# Variable Definitions with Type Constraints & Regex Validation
# --------------------------------------------------------------------------------------------------
# File: terraform/variables.tf
# Purpose: Define strictly typed input variables for Azure AI Foundry, OpenAI, Search, and Hub.
# --------------------------------------------------------------------------------------------------

# Prefix variable for enterprise resource naming
variable "prefix" {
  type        = string                                                                    # String type constraint
  description = "Resource name prefix applied to all AI Foundry components (e.g., 'mosaic')." # Variable description
  default     = "mosaic"                                                                  # Default naming prefix

  # Regex validation ensuring lowercase alphanumeric characters and hyphens
  validation {
    condition     = can(regex("^[a-z0-9-]{2,10}$", var.prefix))                          # Length 2-10 regex
    error_message = "Prefix must consist of 2-10 lowercase alphanumeric characters and hyphens."
  }
}

# Environment variable for deployment stage
variable "environment" {
  type        = string                                                                    # String constraint
  description = "Target deployment lifecycle environment (prod, stage, dev, or sandbox)." # Stage description
  default     = "prod"                                                                    # Default to production

  # Allowed environment values
  validation {
    condition     = contains(["prod", "stage", "dev", "sandbox"], var.environment)        # Stage containment check
    error_message = "Environment must be one of: 'prod', 'stage', 'dev', 'sandbox'."
  }
}

# Regional location variable
variable "location" {
  type        = string                                                                    # String constraint
  description = "Target Azure primary region for AI Foundry resources (must support GPT-4o & AI Search)." # Region description
  default     = "eastus2"                                                                 # Default Azure region
}

# Parent Resource Group variable
variable "resource_group_name" {
  type        = string                                                                    # String constraint
  description = "Name of the parent Azure Resource Group housing the AI Foundry infrastructure." # RG name
}

# Key Vault Resource ID variable
variable "key_vault_id" {
  type        = string                                                                    # Full Resource ID constraint
  description = "Resource ID of the enterprise Azure Key Vault instance for CMK encryption and secrets." # Key Vault ID

  # Validation ensuring fully qualified Azure Resource ID format
  validation {
    condition     = can(regex("^/subscriptions/.+/resourceGroups/.+/providers/Microsoft.KeyVault/vaults/.+$", var.key_vault_id))
    error_message = "Key Vault ID must be a fully qualified Azure Resource ID."
  }
}

# Audit log retention variable
variable "log_retention_days" {
  type        = number                                                                    # Numeric retention window
  description = "Diagnostic and audit log retention window in days (730 days for HIPAA § 164.312)." # Retention days
  default     = 730                                                                       # 2-year retention default

  # Validation ensuring minimum healthcare compliance window
  validation {
    condition     = var.log_retention_days >= 365                                         # Minimum 365 days check
    error_message = "Healthcare audit log retention must be at least 365 days (730 recommended for HIPAA)."
  }
}

# Foundation model version tag
variable "gpt4o_model_version" {
  type        = string                                                                    # Version string
  description = "Target model version tag for GPT-4o foundation model in Azure AI Foundry." # Model version
  default     = "2024-11-20"                                                              # Pinned model version
}

# Foundation model capacity variable
variable "gpt4o_capacity" {
  type        = number                                                                    # Capacity in TPM thousands
  description = "Tokens-per-minute (TPM) capacity allocation in thousands for GPT-4o model deployment." # TPM allocation
  default     = 100                                                                       # 100K TPM default allocation

  # Capacity bounds check
  validation {
    condition     = var.gpt4o_capacity >= 10 && var.gpt4o_capacity <= 2000               # 10K to 2M TPM check
    error_message = "GPT-4o capacity must be between 10K TPM and 2,000K TPM."
  }
}

# Azure AI Search replica count variable
variable "search_replica_count" {
  type        = number                                                                    # Numeric replica count
  description = "Replica count for Azure AI Search Service for high availability and low latency query SLA." # Search replicas
  default     = 2                                                                         # High availability default

  # Replica bounds validation
  validation {
    condition     = var.search_replica_count >= 1 && var.search_replica_count <= 12        # 1 to 12 replicas check
    error_message = "Search replica count must be between 1 and 12."
  }
}

# Metadata tags variable
variable "tags" {
  type        = map(string)                                                               # Map of key-value tags
  description = "Enterprise metadata tags attached to all provisioned AI Foundry resources." # Tags description
  default = {
    Organization       = "Mosaic Healthcare System"                                       # Organization tag
    ArchitecturePillar = "AI-Foundry-Model-Regulation"                                    # Architecture pillar
    ComplianceStandard = "HITRUST-CSF-v11"                                                # Compliance standard
    SecurityTier       = "Tier-1-Clinical-Restricted"                                     # Security classification
  }
}
