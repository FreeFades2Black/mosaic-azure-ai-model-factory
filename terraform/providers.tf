# --------------------------------------------------------------------------------------------------
# TERRAFORM PROVIDERS & CONFIGURATION FOR AZURE AI FOUNDRY
# --------------------------------------------------------------------------------------------------
# File: terraform/providers.tf
# Purpose: Configure AzureRM and Random providers with required versions and feature flags.
# --------------------------------------------------------------------------------------------------

terraform {
  required_version = ">= 1.6.0" # Minimum OpenTofu / Terraform engine version

  # Required cloud provider definitions
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"       # HashiCorp AzureRM provider
      version = ">= 3.90.0, < 5.0.0"     # Tested version range
    }
    random = {
      source  = "hashicorp/random"        # HashiCorp Random provider for DNS suffixes
      version = ">= 3.5.0"                # Minimum random provider version
    }
  }
}

# Configure Azure Resource Manager provider features
provider "azurerm" {
  features {
    # Key Vault lifecycle rules
    key_vault {
      purge_soft_delete_on_destroy    = false # Prevent accidental destruction of cryptographic keys
      recover_soft_deleted_key_vaults = true  # Auto-recover soft-deleted vaults
    }
    # Cognitive Account lifecycle rules
    cognitive_account {
      purge_soft_delete_on_destroy = false # Prevent accidental deletion of AI models
    }
  }
}
