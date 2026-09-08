"""
==============================================================================
MULTI-GATE MODEL REGULATION & COMPLIANCE GATE ENGINE
==============================================================================
Runs full test matrices against AI Foundry agents before promotion to production.
==============================================================================
"""

import logging
from dataclasses import dataclass
from typing import Dict, List, Optional

from ..safety.content_safety_shield import ContentSafetyShield
from ..safety.prompt_shield_detector import PromptShieldDetector
from ..safety.phi_scanner import PHIScanner
from .groundedness_evaluator import GroundednessEvaluator

logger = logging.getLogger(__name__)


@dataclass
class EvaluationReport:
    overall_passed: bool
    content_safety_passed: bool
    prompt_shield_passed: bool
    phi_scan_passed: bool
    groundedness_passed: bool
    groundedness_score: float
    violations: List[str]


class ModelRegulationGate:
    """Orchestrates comprehensive safety and quality gate checks."""

    def __init__(self):
        self.content_safety = ContentSafetyShield()
        self.prompt_shield = PromptShieldDetector()
        self.phi_scanner = PHIScanner()
        self.groundedness = GroundednessEvaluator()

    def run_full_evaluation(self, prompt: str, response: str, context: str) -> EvaluationReport:
        """Runs prompt safety, response safety, PHI scan, and groundedness evaluations."""
        violations = []

        # 1. Prompt Shield Gate
        prompt_res = self.prompt_shield.scan_prompt(prompt)
        if not prompt_res.is_safe:
            violations.append(f"Prompt injection detected: {prompt_res.trigger_patterns}")

        # 2. Content Safety Gate
        safety_res = self.content_safety.evaluate_text(response)
        if not safety_res.passed:
            violations.append(f"Content safety harm detected: {safety_res.flagged_categories}")

        # 3. PHI / HIPAA Scanner Gate
        phi_res = self.phi_scanner.scan_and_redact(response)
        if not phi_res.passed:
            violations.append(f"HIPAA PHI detected: {phi_res.detected_types} ({phi_res.violations_count} occurrences)")

        # 4. Groundedness / Hallucination Gate
        ground_res = self.groundedness.evaluate(response, context)
        if not ground_res.passed:
            violations.append(f"Groundedness score {ground_res.score:.2f} below mandatory threshold 4.00")

        overall_passed = len(violations) == 0

        return EvaluationReport(
            overall_passed=overall_passed,
            content_safety_passed=safety_res.passed,
            prompt_shield_passed=prompt_res.is_safe,
            phi_scan_passed=phi_res.passed,
            groundedness_passed=ground_res.passed,
            groundedness_score=ground_res.score,
            violations=violations
        )
