# Enterprise Deployment Playbook: Azure AI Foundry

## 1. Prerequisites

- Azure CLI authenticated to target tenant (`az login`).
- OpenTofu v1.6+ or Terraform v1.6+.
- Python 3.10+ virtual environment.

## 2. Step-by-Step Deployment

```bash
# 1. Navigate to terraform directory
cd terraform

# 2. Copy and customize variables
cp terraform.tfvars.example terraform.tfvars

# 3. Initialize OpenTofu
tofu init

# 4. Plan and review changes
tofu plan -out=tfplan

# 5. Apply infrastructure
tofu apply tfplan
```
