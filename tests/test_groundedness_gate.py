"""Tests for groundedness scoring and multi-gate regulation."""
import pytest
from src.evaluation.groundedness_evaluator import GroundednessEvaluator
from src.evaluation.model_regulation_gate import ModelRegulationGate

def test_groundedness_high_overlap():
    evaluator = GroundednessEvaluator()
    context = (
        "Under Mosaic Clinical Protocol Section 4.2, standard antibiotic prophylaxis requires "
        "intravenous Cefazolin (2g to 3g adjusted for patient weight >= 120kg) combined with "
        "Metronidazole (500mg IV) administered within 60 minutes prior to surgical incision."
    )
    response = (
        "Under Mosaic Clinical Protocol Section 4.2, standard antibiotic prophylaxis requires "
        "intravenous Cefazolin (2g to 3g) combined with Metronidazole (500mg IV) administered "
        "within 60 minutes prior to surgical incision."
    )
    result = evaluator.evaluate(response, context)
    assert result.passed is True
    assert result.score >= 4.0

def test_groundedness_hallucination():
    evaluator = GroundednessEvaluator()
    context = "Stroke care pathways indicate IV rtPA Alteplase within 4.5 hours of symptom onset."
    response = "You should administer high dose Morphine and immediate experimental chemotherapy."
    result = evaluator.evaluate(response, context)
    assert result.passed is False
    assert result.score < 4.0

def test_full_regulation_gate_pass():
    gate = ModelRegulationGate()
    prompt = "What is the stroke treatment window?"
    context = "Alteplase is indicated within 4.5 hours of verified symptom onset."
    response = "According to protocols, Alteplase is indicated within 4.5 hours of verified symptom onset."

    report = gate.run_full_evaluation(prompt, response, context)
    assert report.overall_passed is True
    assert report.content_safety_passed is True
    assert report.prompt_shield_passed is True
    assert report.phi_scan_passed is True
    assert report.groundedness_passed is True
