# --------------------------------------------------------------------------------------------------
# MOSAIC HEALTHCARE ENTERPRISE AZURE AI FOUNDRY MODULE
# Output Values for Downstream Application & Pipeline Integration
# --------------------------------------------------------------------------------------------------
# File: terraform/outputs.tf
# Purpose: Expose critical endpoints, resource IDs, and identity principals for AI SDK pipelines.
# --------------------------------------------------------------------------------------------------

# Azure AI Foundry Hub Resource ID
output "ai_foundry_hub_id" {
  value       = azurerm_ai_foundry.hub.id                         # Fully qualified Hub ID
  description = "Fully qualified Resource ID of the Azure AI Foundry Hub."
}

# Azure AI Foundry Hub Workspace Name
output "ai_foundry_hub_name" {
  value       = azurerm_ai_foundry.hub.name                       # AI Hub Name
  description = "Name of the provisioned Azure AI Foundry Hub workspace."
}

# Azure AI Foundry Clinical Project Resource ID
output "ai_foundry_project_id" {
  value       = azurerm_ai_foundry_project.clinical_project.id    # Clinical Project ID
  description = "Resource ID of the Clinical Agent AI Foundry Project."
}

# Azure OpenAI Cognitive Account ID
output "openai_account_id" {
  value       = azurerm_cognitive_account.openai.id               # OpenAI Resource ID
  description = "Resource ID of the Azure OpenAI cognitive account."
}

# Azure OpenAI Inference Endpoint HTTPS URI
output "openai_endpoint" {
  value       = azurerm_cognitive_account.openai.endpoint         # Inference Endpoint URL
  description = "Primary HTTPS endpoint URI for Azure OpenAI model inferencing."
}

# Managed Identity Principal ID for Azure OpenAI
output "openai_principal_id" {
  value       = azurerm_cognitive_account.openai.identity[0].principal_id # Identity Principal ID
  description = "Managed Service Identity (MSI) Principal ID for Azure OpenAI account."
}

# GPT-4o Model Deployment Name
output "gpt4o_deployment_name" {
  value       = azurerm_cognitive_deployment.gpt4o.name           # GPT-4o deployment name
  description = "Deployment name for the GPT-4o multi-modal foundation model."
}

# Text Embedding Model Deployment Name
output "embedding_deployment_name" {
  value       = azurerm_cognitive_deployment.embedding.name       # Embedding model deployment name
  description = "Deployment name for the text-embedding-3-large vectorization model."
}

# Azure AI Search Service Name
output "ai_search_service_name" {
  value       = azurerm_search_service.rag_search.name            # Search service name
  description = "Name of the provisioned Azure AI Search Service."
}

# Azure AI Search Vector Index Endpoint URI
output "ai_search_endpoint" {
  value       = "https://${azurerm_search_service.rag_search.name}.search.windows.net" # Vector index endpoint URL
  description = "HTTPS endpoint URI for the Azure AI Search RAG vector index."
}

# Azure AI Content Safety Service Endpoint URI
output "content_safety_endpoint" {
  value       = azurerm_cognitive_account.content_safety.endpoint # Content Safety API endpoint URL
  description = "HTTPS endpoint for Azure AI Content Safety real-time harm evaluation."
}

# Secure Storage Account Name for AI Checkpoints
output "ai_storage_account_name" {
  value       = azurerm_storage_account.ai_storage.name           # Storage account name
  description = "Name of the storage account used for AI datasets and fine-tuning weights."
}

# Foundry IQ Enterprise Knowledge Base Endpoint
output "foundry_iq_knowledge_base_endpoint" {
  value       = "https://${azurerm_ai_foundry.hub.name}.services.ai.azure.com/iq/v1/kb" # Foundry IQ KB endpoint
  description = "HTTPS endpoint URI for the Foundry IQ Enterprise Context Knowledge Base."
}

# Model Context Protocol (MCP) Server Endpoint for Agent Tooling
output "foundry_iq_mcp_server_endpoint" {
  value       = "https://${azurerm_ai_foundry.hub.name}.services.ai.azure.com/mcp/v1" # Foundry IQ MCP endpoint
  description = "Standard Model Context Protocol (MCP) JSON-RPC 2.0 / SSE endpoint for agent tool connections."
}

