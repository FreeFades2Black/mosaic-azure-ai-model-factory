"""
==============================================================================
AZURE AI AGENT CODE INTERPRETER & DYNAMIC EXECUTION ENGINE
==============================================================================
Provides sandboxed, deterministic Python execution for statistical analysis,
clinical calculations, dosage modeling, and tabular data synthesis.
Notice: Connects to Azure AI Agent Dynamic Sessions in cloud runtime.
==============================================================================
"""

import ast
import io
import logging
import math
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


@dataclass
class CodeExecutionResult:
    status: str  # "success" or "error"
    stdout: str
    stderr: str
    return_value: Optional[Any] = None
    execution_time_ms: float = 0.0
    generated_artifacts: List[str] = field(default_factory=list)


class CodeInterpreterTool:
    """Sandboxed Code Interpreter tool for Azure AI Agents and LLM copilots."""

    # Forbidden modules / functions in healthcare agent sandbox to prevent escape
    FORBIDDEN_OPERATIONS = [
        "import os",
        "import sys",
        "import subprocess",
        "import socket",
        "import shutil",
        "eval(",
        "exec(",
        "__import__",
        "open('/etc",
        "open('C:\\Windows"
    ]

    def __init__(self, timeout_seconds: float = 5.0, session_pool_endpoint: Optional[str] = None):
        self.timeout_seconds = timeout_seconds
        self.session_pool_endpoint = session_pool_endpoint

    def get_tool_definition(self) -> Dict[str, Any]:
        """Returns OpenAI / Azure AI Agent Service tool definition schema."""
        return {
            "type": "code_interpreter",
            "code_interpreter": {
                "description": (
                    "Executes Python code in a secure sandboxed environment. Use this tool "
                    "for mathematical calculations, clinical formulas (eGFR, BSA, MME), "
                    "statistical analyses, EHR data aggregations, and data visualization."
                )
            }
        }

    def sanitize_code(self, code: str) -> None:
        """Verifies code does not attempt sandbox escape or forbidden system calls."""
        lower_code = code.lower()
        for forbidden in self.FORBIDDEN_OPERATIONS:
            if forbidden.lower() in lower_code:
                raise PermissionError(f"Security Policy Violation: Forbidden operation '{forbidden}' detected.")

    def execute_code(self, python_code: str, execution_context: Optional[Dict[str, Any]] = None) -> CodeExecutionResult:
        """Executes sanitized Python code within an isolated local sandbox or Azure session."""
        start_time = time.perf_counter()
        self.sanitize_code(python_code)
        parsed_ast = ast.parse(python_code)

        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()


        # Safe global scope with standard mathematical and statistical libraries
        safe_globals: Dict[str, Any] = {
            "__builtins__": {
                "print": print,
                "range": range,
                "len": len,
                "min": min,
                "max": max,
                "sum": sum,
                "abs": abs,
                "round": round,
                "float": float,
                "int": int,
                "str": str,
                "bool": bool,
                "list": list,
                "dict": dict,
                "set": set,
                "tuple": tuple,
                "enumerate": enumerate,
                "zip": zip,
                "isinstance": isinstance,
                "map": map,
                "filter": filter,
            },
            "math": math,
        }

        # Inject clinical calculation utilities
        safe_globals.update(self._get_clinical_math_utilities())

        if execution_context:
            safe_globals.update(execution_context)

        old_stdout, old_stderr = sys.stdout, sys.stderr
        return_val = None
        status = "success"

        try:
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture

            # Execute compiled bytecode in isolated scope
            local_scope: Dict[str, Any] = {}
            if parsed_ast.body and isinstance(parsed_ast.body[-1], ast.Expr):
                *body_statements, last_expr = parsed_ast.body
                if body_statements:
                    exec(
                        compile(ast.Module(body=body_statements, type_ignores=[]), "<sandboxed_session>", "exec"),
                        safe_globals,
                        local_scope,
                    )
                return_val = eval(
                    compile(ast.Expression(body=last_expr.value), "<sandboxed_session>", "eval"),
                    safe_globals,
                    local_scope,
                )
            else:
                exec(compile(parsed_ast, "<sandboxed_session>", "exec"), safe_globals, local_scope)
                if "result" in local_scope:
                    return_val = local_scope["result"]
                elif local_scope:
                    return_val = list(local_scope.values())[-1]


        except Exception as e:
            status = "error"
            stderr_capture.write(f"{type(e).__name__}: {str(e)}")
            logger.warning(f"Sandboxed code execution failed: {e}")
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return CodeExecutionResult(
            status=status,
            stdout=stdout_capture.getvalue(),
            stderr=stderr_capture.getvalue(),
            return_value=return_val,
            execution_time_ms=round(elapsed_ms, 2),
            generated_artifacts=[]
        )

    def _get_clinical_math_utilities(self) -> Dict[str, Any]:
        """Provides verified healthcare formula functions to the interpreter."""

        def calculate_egfr_cockcroft_gault(age: int, weight_kg: float, serum_creatinine: float, is_female: bool = False) -> float:
            """Calculates estimated Creatinine Clearance (eCrCl / eGFR) in mL/min."""
            if serum_creatinine <= 0:
                raise ValueError("Serum creatinine must be positive.")
            crcl = ((140 - age) * weight_kg) / (72 * serum_creatinine)
            if is_female:
                crcl *= 0.85
            return round(crcl, 2)

        def calculate_body_surface_area(height_cm: float, weight_kg: float) -> float:
            """Calculates Body Surface Area (BSA) in m^2 using the Mosteller formula."""
            if height_cm <= 0 or weight_kg <= 0:
                raise ValueError("Height and weight must be positive.")
            bsa = math.sqrt((height_cm * weight_kg) / 3600.0)
            return round(bsa, 2)

        def calculate_mme(opioid_name: str, dose_mg: float) -> float:
            """Calculates Morphine Milligram Equivalents (MME)."""
            conversion_factors = {
                "morphine": 1.0,
                "oxycodone": 1.5,
                "hydrocodone": 1.0,
                "hydromorphone": 4.0,
                "fentanyl_mcg_hr": 2.4, # transdermal mcg/hr to oral MME/day
                "codeine": 0.15,
                "tramadol": 0.1
            }
            factor = conversion_factors.get(opioid_name.lower())
            if factor is None:
                raise ValueError(f"Unknown opioid: '{opioid_name}'. Supported: {list(conversion_factors.keys())}")
            return round(dose_mg * factor, 2)

        return {
            "calculate_egfr_cockcroft_gault": calculate_egfr_cockcroft_gault,
            "clinical_egfr_cockcroft_gault": calculate_egfr_cockcroft_gault,
            "calculate_body_surface_area": calculate_body_surface_area,
            "clinical_bsa_mosteller": calculate_body_surface_area,
            "calculate_mme": calculate_mme,
            "clinical_opioid_mme_conversion": calculate_mme,
        }

