# Operational Runbook: Azure OpenAI Tokens-Per-Minute (TPM) 429 Throttling Triage

**Severity:** P2 / AI Inference Degraded  
**Target Systems:** Azure OpenAI Service, Model Gateway, Redis Rate Limiter

## Diagnostic Workflow

### 1. Check Azure Monitor for OpenAI 429 Errors
```bash
az cognitiveservices account show \
  --name mosaic-openai-prod \
  --resource-group mosaic-ai-rg \
  --query 'properties.provisionedModelCapacities'
```

### 2. Inspect Client-Side Rate Limiter Telemetry
```bash
python -m src.fine_tune_runner --check-tpm-consumption
```

### 3. Step-by-Step Remediation
1. **Activate Multi-Region Model Gateway Fallback:**
   Route overflow inference traffic from `eastus` to secondary `swedencentral` deployment:
   ```bash
   python -m src.fine_tune_runner --set-fallback-region swedencentral
   ```
2. **Dynamically Adjust Client Token Bucket:**
   Reduce client batch concurrency from 32 to 16 workers in `.env`:
   ```bash
   sed -i 's/MAX_CONCURRENT_INFERENCE=32/MAX_CONCURRENT_INFERENCE=16/' .env
   ```
