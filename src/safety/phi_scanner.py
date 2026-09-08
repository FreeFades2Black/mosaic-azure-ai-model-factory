"""
==============================================================================
HIPAA PROTECTED HEALTH INFORMATION (PHI) SCANNER & REDACTOR
==============================================================================
Enforces zero-leak policies for SSNs, Medical Record Numbers (MRNs),
patient phone numbers, and email addresses.
==============================================================================
"""

import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class PHIScanResult:
    passed: bool
    violations_count: int
    detected_types: List[str]
    sanitized_text: str


class PHIScanner:
    """Detects and redacts HIPAA § 164.312 Safe Harbor PHI identifiers."""

    PATTERNS: Dict[str, str] = {
        "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
        "MRN": r"\bMRN\s*#?\s*\d{6,10}\b",
        "PHONE": r"\b(\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "DOB": r"\b(DOB|Date of Birth)\s*:\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
    }

    def scan_and_redact(self, text: str) -> PHIScanResult:
        """Identifies PHI tokens and returns redacted text with audit summary."""
        sanitized = text
        detected = []
        violations = 0

        for phi_type, regex in self.PATTERNS.items():
            matches = list(re.finditer(regex, sanitized, re.IGNORECASE))
            if matches:
                violations += len(matches)
                detected.append(phi_type)
                sanitized = re.sub(regex, f"[REDACTED_{phi_type}]", sanitized, flags=re.IGNORECASE)

        return PHIScanResult(
            passed=(violations == 0),
            violations_count=violations,
            detected_types=detected,
            sanitized_text=sanitized
        )
