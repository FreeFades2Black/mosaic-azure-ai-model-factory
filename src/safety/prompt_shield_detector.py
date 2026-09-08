"""
==============================================================================
AZURE AI PROMPT SHIELD & JAILBREAK DETECTOR
==============================================================================
Detects adversarial prompt injections and system instruction overrides.
==============================================================================
"""

import logging
import re
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class PromptShieldResult:
    is_safe: bool
    jailbreak_detected: bool
    indirect_attack_detected: bool
    trigger_patterns: List[str]


class PromptShieldDetector:
    """Scans incoming user prompts and retrieved RAG context for prompt injections."""

    ADVERSARIAL_PATTERNS = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"disregard\s+(all\s+)?guidelines",
        r"you\s+are\s+now\s+in\s+DAN\s+mode",
        r"system\s*:\s*override",
        r"reveal\s+(your\s+)?system\s+prompt",
        r"bypass\s+(safety|content)\s+filters",
        r"roleplay\s+as\s+an\s+unrestricted\s+AI",
        r"output\s+all\s+confidential\s+data"
    ]

    def scan_prompt(self, prompt: str) -> PromptShieldResult:
        """Evaluates whether a prompt contains adversarial override patterns."""
        matched = []
        for pattern in self.ADVERSARIAL_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                matched.append(pattern)

        jailbreak = len(matched) > 0
        is_safe = not jailbreak

        return PromptShieldResult(
            is_safe=is_safe,
            jailbreak_detected=jailbreak,
            indirect_attack_detected=False,
            trigger_patterns=matched
        )
