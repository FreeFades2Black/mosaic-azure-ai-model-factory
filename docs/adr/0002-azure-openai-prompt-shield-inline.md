# ADR-0002: Azure AI Content Safety & Prompt Shield Inline Guardrails

**Status:** Accepted  
**Date:** 2026-06-21  
**Lead Architect:** William Free Hall (Free) <whall4.wh@gmail.com>

## 1. Context & Operational Challenge
Deploying LLMs in clinical decision support introduces risks of indirect prompt injection attacks (e.g. malicious instructions embedded within patient clinical notes or external lab PDFs).

## 2. Options Considered
* **Option A: Client-Side Regex Heuristics and Keyword Blacklists**
  - *Evaluation:* Zero API latency overhead, but trivially bypassed by adversarial linguistic obfuscation, Base64 encodings, or roleplay prompts.
* **Option B: Managed Azure AI Content Safety Prompt Shields (Spotlight Analysis)**
  - *Evaluation:* Machine learning models analyze prompt and document chunks for indirect injection attacks, returning a risk classification score before LLM processing.

## 3. Decision & Trade-Off Accepted
We adopted **Option B (Azure Prompt Shields)**.  
**Trade-Off Accepted:** Incurs an additional 35ms network latency budget per inference request and an API cost ($0.75 per 1,000 text records). We accept the latency cost to prevent unauthorized prompt override or data exfiltration.
