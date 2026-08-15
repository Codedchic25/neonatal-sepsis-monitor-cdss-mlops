"""Unit tests for the First-Order Telemetry Clearance Engine algorithms.

Validates baseline constant properties and mild renal complication adjustments
modulating metabolic biological degradation half-lives.
"""

import pytest

from src.telemetry.engine import generate_telemetry_step


def test_mild_acute_kidney_injury_clearance_retention() -> None:
    """Verifies that Mild AKI slows down the first-order clearance degradation path."""
    pcr_start = 50.0
    last_pct = 8.0

    # Execution A: Baseline normal clearance profile
    _, pct_normal = generate_telemetry_step(
        profile_name="Term Neonate / Nou-nascut la Termen",
        last_pcr=pcr_start,
        last_pct=last_pct,
        antibiotics_administered=True,
        aki_level="normal",
    )

    # Execution B: Mild Acute Kidney Injury (AKI) delayed filtration (+25% half-life extension)
    _, pct_mild_aki = generate_telemetry_step(
        profile_name="Term Neonate / Nou-nascut la Termen",
        last_pcr=pcr_start,
        last_pct=last_pct,
        antibiotics_administered=True,
        aki_level="Mild AKI",
    )

    # Mild AKI must stall clearance, retaining more toxic markers in blood than normal filtration
    assert pct_mild_aki > pct_normal
    # FIXED: Aligned reference with exact formula value 7.817 (7.82) instead of mistyped 7.85
    assert pct_mild_aki == pytest.approx(7.82, abs=0.02)  # 8 * e^(-ln(2)/(24 * 1.25))
