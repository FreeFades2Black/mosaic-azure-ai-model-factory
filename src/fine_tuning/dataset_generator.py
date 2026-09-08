"""
==============================================================================
SYNTHETIC CLINICAL DATASET GENERATOR FOR MODEL FINE-TUNING
==============================================================================
Generates synthetic, HIPAA-compliant JSONL training sets conforming to the
Azure OpenAI / Azure AI Foundry Chat Completion dataset format.
==============================================================================
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class SyntheticDatasetGenerator:
    """Generates synthetic domain-adapted training pairs for LLM fine-tuning."""

    SYSTEM_PROMPT = (
        "You are an enterprise clinical decision support intelligence agent developed "
        "for Mosaic Healthcare. You provide evidence-based guidance adhering to HITRUST "
        "and HIPAA safety controls. You never invent patient records or output PHI."
    )

    SAMPLE_DATA: List[Dict[str, str]] = [
        {
            "query": "What is the surgical antimicrobial prophylaxis guideline for clean-contaminated colorectal procedures?",
            "response": (
                "Per Mosaic Clinical Protocol Section 4.2, standard antibiotic prophylaxis requires IV Cefazolin "
                "(2g to 3g adjusted for patient weight >= 120kg) combined with Metronidazole (500mg IV) administered "
                "within 60 minutes prior to surgical incision."
            )
        },
        {
            "query": "What is the confirmed treatment window for IV Alteplase in acute ischemic stroke?",
            "response": (
                "According to Mosaic Stroke Care Pathways, intravenous recombinant tissue plasminogen activator "
                "(IV rtPA / Alteplase 0.9 mg/kg, max 90 mg) is indicated within 4.5 hours of verified symptom onset "
                "following non-contrast cranial CT excluding intracranial hemorrhage."
            )
        },
        {
            "query": "What is the initial hemodynamic resuscitation protocol for adult Diabetic Ketoacidosis (DKA)?",
            "response": (
                "Per Mosaic ICU Endocrinology Protocol, initial fluid resuscitation begins with 0.9% Normal Saline "
                "at 1,000 to 1,500 mL/hr during the first 1-2 hours, followed by continuous low-dose regular insulin "
                "(0.1 units/kg/hr) once serum potassium is verified > 3.3 mEq/L."
            )
        },
        {
            "query": "Outline the diagnostic criteria and initial management for suspected hospital-acquired pneumonia (HAP).",
            "response": (
                "Suspected HAP requires new or progressive pulmonary infiltrate on chest radiograph presenting >= 48 hours "
                "after admission plus >= 2 clinical criteria (fever > 38°C, purulent sputum, leukocytosis). Initial empiric "
                "therapy includes IV Piperacillin-Tazobactam (4.5g q6h) or Cefepime (2g q8h) plus MRSA coverage with Vancomycin."
            )
        },
        {
            "query": "What are the emergency magnesium sulfate infusion parameters for severe preeclampsia with severe features?",
            "response": (
                "For severe preeclampsia seizure prophylaxis, administer Magnesium Sulfate 4g to 6g IV loading dose over "
                "20 minutes, followed by a continuous maintenance infusion of 1g to 2g per hour for 24 hours postpartum, "
                "with hourly monitoring of patellar reflexes and respiratory rate."
            )
        }
    ]

    def __init__(self, system_prompt: Optional[str] = None):
        self.system_prompt = system_prompt or self.SYSTEM_PROMPT

    def generate_jsonl(self, output_file: str, samples: Optional[List[Dict[str, str]]] = None) -> str:
        """Writes synthetic chat completion conversation records to a JSONL file."""
        target_path = Path(output_file)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        data = samples or self.SAMPLE_DATA

        records = []
        for item in data:
            record = {
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": item["query"]},
                    {"role": "assistant", "content": item["response"]}
                ]
            }
            records.append(record)

        with open(target_path, "w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec) + "\n")

        logger.info(f"Generated {len(records)} synthetic fine-tuning samples at '{target_path}'.")
        return str(target_path)
