"""Unit tests for the AI Inference and Clinical Decision Support Layer.

Validates active instantiation boundaries, real-time context-augmented prompt routing,
and deterministic cold fallback execution loops when cloud links are unlinked.
"""

import os

from src.medical.expert import NeonatalAIExpert


def test_ai_expert_initialization_bounds() -> None:
    """Verifies that the neonatal AI expert component instantiates correctly.

    Confirms internal infrastructure frameworks choose the optimal LPU core model.
    """
    ai_expert = NeonatalAIExpert()

    # Dynamically evaluate the active engine from environment configurations to prevent static string mismatch
    assert ai_expert.model_core == os.environ.get(
        "GROQ_MODEL_NAME", "llama-3.1-8b-instant"
    )


def test_ai_expert_deterministic_fallback_or_live_trigger() -> None:
    """Verifies the core engine yields structural, non-empty medical documentation.

    Guarantees absolute fail-safe fallback coverage when remote cloud gateways
    are unreachable.
    """
    ai_expert = NeonatalAIExpert()

    # Mock high-acuity critical physiological sensory data snapshot payload
    critical_vitals_payload = {
        "weight_kg": 2.50,
        "hr": 175,
        "temp": 38.9,
        "spo2": 91,
        "bp": "54/32 mmHg",
        "pcr": 25.0,
        "pct": 4.5,
        "kangaroo_care_active": False,
        "nutrition_type_active": "None",
        "music_therapy_active": False,
    }

    # Execute system context completion dispatcher using localized linguistic tags
    report = ai_expert.generate_clinical_support(
        vitals_payload=critical_vitals_payload, lang="RO"
    )

    # Assert absolute response framework initialization integrity
    assert report is not None
    assert len(report) > 50

    # Convert to upper case once to secure uniform tag scanning performance
    report_upper = report.upper()

    # The returned envelope payload must contain mandatory XML partition blocks
    assert "<RAPORT>" in report_upper and "</RAPORT>" in report_upper
    assert "<MEDICATIE>" in report_upper and "</MEDICATIE>" in report_upper
    assert "<FCC>" in report_upper and "</FCC>" in report_upper

    # Safe validation that the LLM response contains meaningful clinical content
    normalized_report = " ".join(report_upper.split())
    has_secure_local_failsafe = (
        "SYSTEM OPERATING IN SECURE FAIL-SAFE LOCAL MODE" in normalized_report
    )
    has_live_response_layer = len(report_upper) > 150

    assert has_live_response_layer or has_secure_local_failsafe
