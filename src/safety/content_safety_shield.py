"""
==============================================================================
AZURE AI CONTENT SAFETY EVALUATION SHIELD
==============================================================================
Enforces zero-tolerance safety policies across Hate, Violence, Self-Harm & Sexual.
==============================================================================
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ContentSafetyResult:
    passed: bool
    hate_score: int
    violence_score: int
    self_harm_score: int
    sexual_score: int
    flagged_categories: List[str]


class ContentSafetyShield:
    """Evaluates text against Microsoft Azure AI Content Safety policy thresholds."""

    # Zero-tolerance threshold in healthcare AI (0 = Safe, 2 = Low, 4 = Medium, 6 = High)
    MAX_ALLOWABLE_SEVERITY = 0

    HARMFUL_TRIGGERS: Dict[str, List[str]] = {
        "Hate": ["hate speech", "discrimination", "supremacy", "slur"],
        "Violence": ["assault", "homicide", "detonate bomb", "lethal attack"],
        "SelfHarm": ["suicide instructions", "overdose intentionally", "self-mutilation"],
        "Sexual": ["explicit erotica", "non-consensual content"]
    }

    def evaluate_text(self, text: str) -> ContentSafetyResult:
        """Evaluates text content and returns categorized severity levels."""
        lower_text = text.lower()
        hate = 0
        violence = 0
        self_harm = 0
        sexual = 0
        flagged = []

        for term in self.HARMFUL_TRIGGERS["Hate"]:
            if term in lower_text:
                hate = 4
                flagged.append("Hate")

        for term in self.HARMFUL_TRIGGERS["Violence"]:
            if term in lower_text:
                violence = 4
                flagged.append("Violence")

        for term in self.HARMFUL_TRIGGERS["SelfHarm"]:
            if term in lower_text:
                self_harm = 4
                flagged.append("SelfHarm")

        for term in self.HARMFUL_TRIGGERS["Sexual"]:
            if term in lower_text:
                sexual = 4
                flagged.append("Sexual")

        passed = (
            hate <= self.MAX_ALLOWABLE_SEVERITY
            and violence <= self.MAX_ALLOWABLE_SEVERITY
            and self_harm <= self.MAX_ALLOWABLE_SEVERITY
            and sexual <= self.MAX_ALLOWABLE_SEVERITY
        )

        return ContentSafetyResult(
            passed=passed,
            hate_score=hate,
            violence_score=violence,
            self_harm_score=self_harm,
            sexual_score=sexual,
            flagged_categories=flagged
        )
