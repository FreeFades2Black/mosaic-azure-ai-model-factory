# AI Governance, Content Safety & HIPAA Regulation

## 1. Multi-Tiered AI Regulation Matrix

| Gate | Validation Rule | Mandatory Threshold | Action on Failure |
| :--- | :--- | :--- | :--- |
| **Prompt Shield** | Jailbreak & Injection Scan | 0 Injections Detected | Block request & log incident to Sentinel |
| **Content Safety** | Hate, Violence, Self-Harm, Sexual | Severity Level = 0 | Block inference & quarantine |
| **PHI / HIPAA** | SSN, MRN, Phone, Email, DOB | 0 Cleartext PHI Tokens | Redact token & raise audit alert |
| **Groundedness** | Vector Context Alignment Score | Score $\ge 4.00 / 5.00$ | Reject response & trigger human review |

## 2. Running the Policy Gate

```bash
python -m pytest tests/test_groundedness_gate.py -v
```
