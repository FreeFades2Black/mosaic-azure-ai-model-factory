"""
==============================================================================
GROUNDEDNESS & HALLUCINATION EVALUATION ENGINE
==============================================================================
Scores agent responses against retrieved clinical context on a 1.0 to 5.0 scale.
==============================================================================
"""

import logging
import re
from dataclasses import dataclass
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class GroundednessResult:
    score: float
    passed: bool
    unsupported_claims: List[str]
    overlap_ratio: float


class GroundednessEvaluator:
    """Evaluates semantic grounding of LLM responses against RAG source context."""

    MIN_GROUNDEDNESS_THRESHOLD = 4.0

    def evaluate(self, response: str, context: str) -> GroundednessResult:
        """Computes key terminology and semantic overlap between response and context."""
        if not response or not context:
            return GroundednessResult(score=1.0, passed=False, unsupported_claims=["Empty context or response"], overlap_ratio=0.0)

        # Tokenize meaningful words (length >= 4)
        resp_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", response.lower()))
        ctx_words = set(re.findall(r"\b[a-zA-Z]{4,}\b", context.lower()))

        if not resp_words:
            return GroundednessResult(score=3.0, passed=False, unsupported_claims=[], overlap_ratio=0.0)

        overlap = resp_words.intersection(ctx_words)
        overlap_ratio = len(overlap) / len(resp_words)

        # Scale to 1.0 - 5.0 rating
        # 80%+ overlap maps to 4.5 - 5.0
        # 50%+ overlap maps to 3.5 - 4.5
        # <50% overlap maps to 1.0 - 3.5
        if overlap_ratio >= 0.70:
            score = 4.0 + (overlap_ratio - 0.70) / 0.30 * 1.0
        elif overlap_ratio >= 0.40:
            score = 3.0 + (overlap_ratio - 0.40) / 0.30 * 1.0
        else:
            score = 1.0 + (overlap_ratio / 0.40) * 2.0

        score = min(round(score, 2), 5.0)
        unsupported = list(resp_words - ctx_words)

        return GroundednessResult(
            score=score,
            passed=(score >= self.MIN_GROUNDEDNESS_THRESHOLD),
            unsupported_claims=unsupported[:5],
            overlap_ratio=round(overlap_ratio, 3)
        )
