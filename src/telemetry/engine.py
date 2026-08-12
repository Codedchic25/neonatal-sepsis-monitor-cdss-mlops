"""NICU Sepsis Monitor AI - Bio-Mathematical Telemetry Engine.

This module provides deterministic pharmacokinetic evaluation models for neonatal sepsis
biomarker progression, accounting for acute renal failure blockages and supportive
non-pharmacological therapeutic accelerators.

Author: Dr. Cojocaru & AI Engineering Team
Compliance: PEP 8, PEP 257, Google Python Style Guide
"""

import math
from typing import Final

# --- INFANT PROFILES CONFIGURATION (Real Pharmacokinetics) ---
# Keys use absolute technical tokens to ensure universal language decoupling.
INFANT_PROFILES: Final[dict[str, dict[str, float]]] = {
    "preterm_28w": {
        "base_pcr_slope": 12.0,
        "base_pct_slope": 1.9,
        "t12_pcr": 24.0,
        "t12_pct": 30.0,
    },
    "term_neonate": {
        "base_pcr_slope": 4.5,
        "base_pct_slope": 0.8,
        "t12_pcr": 19.0,
        "t12_pct": 24.0,
    },
}


def generate_telemetry_step(
    profile_name: str,
    last_pcr: float,
    last_pct: float,
    antibiotics_administered: bool,
    kangaroo_active: bool = False,
    nutrition_type: str = "None",
    music_active: bool = False,
    aki_level: str = "normal",
    **kwargs,
) -> tuple[float, float]:
    """Evaluates first-order pharmacokinetic decay or pathological accumulation.

    Compounds physiological biomarkers based on clinical interventions, active
    family-centered supportive therapies, and dynamic kidney filtration restrictions.
    Maintains absolute test suite backward compatibility via kwargs reflection.

    Args:
        profile_name: The gestational state selection string from the interface.
        last_pcr: The previous iteration's C-Reactive Protein value in mg/L.
        last_pct: The previous iteration's Procalcitonin value in ng/mL.
        antibiotics_administered: Active boolean status of antimicrobial protocols.
        kangaroo_active: Boolean indicator marking physical skin-to-skin contact.
        nutrition_type: String token specifying breast milk or standard formula.
        music_active: Reactive state indicator for womb auditory emulation.
        aki_level: Categorical evaluation state marking kidney function stability.
        **kwargs: Catchall keyword arguments mapping legacy unit testing parameters.

    Returns:
        A tuple containing the newly calculated (pcr_level, pct_level) float values.
    """
    # Defensive programming: Enforce strict positive operational baselines for inputs
    current_pcr = max(0.0, last_pcr)
    current_pct = max(0.0, last_pct)
    dt = 1.0  # Time step resolution mapped to exactly +1 hour

    # Dynamic token clean mapping to decouple business logic from multi-language UI strings
    clean_profile = "term_neonate"
    if "preterm" in profile_name.lower() or profile_name == "Preterm":
        clean_profile = "preterm_28w"

    prof = INFANT_PROFILES[clean_profile]

    # Intercept and map legacy testing kidney status parameters dynamically from kwargs or ui state
    clean_aki = "normal"
    legacy_renal = kwargs.get("renal_function_status", "").lower()
    aki_lower = aki_level.lower()

    if "mild" in legacy_renal or "mild" in aki_lower:
        clean_aki = "mild"
    elif "severe" in legacy_renal or "severe" in aki_lower or "anuria" in aki_lower:
        clean_aki = "severe"

    if antibiotics_administered:
        # Resolve AKI biological half-life extension coefficients
        alpha_aki = 1.0
        if clean_aki == "mild":
            alpha_aki = 1.25  # +25% delayed glomerular filtration extension
        elif clean_aki == "severe":
            alpha_aki = 2.50  # 60% metabolic clearance collapse boundary

        # Calculate elimination constants based on mathematical kinetics (k = ln(2) / t1/2)
        k_pcr = math.log(2) / (prof["t12_pcr"] * alpha_aki)
        k_sn_pct = math.log(2) / (prof["t12_pct"] * alpha_aki)

        # Apply active supportive care compounding acceleration constants (+3%, +3%, +4%)
        fcc_clearance_bonus = 1.0
        if kangaroo_active:
            fcc_clearance_bonus += 0.03
        if music_active:
            fcc_clearance_bonus += 0.03
        if nutrition_type in ["Donated", "Own"]:
            fcc_clearance_bonus += 0.04

        # Execute first-order exponential clearance step calculations
        pcr_new = max(1.0, current_pcr * math.exp(-k_pcr * dt * fcc_clearance_bonus))
        pct_new = max(0.1, current_pct * math.exp(-k_sn_pct * dt * fcc_clearance_bonus))
    else:
        # Pathological linear accumulation trend during active untreated sepsis frames
        alpha_accumulation = 1.0
        if clean_aki == "mild":
            alpha_accumulation = 1.15
        elif clean_aki == "severe":
            alpha_accumulation = 1.40

        pcr_new = current_pcr + (prof["base_pcr_slope"] * alpha_accumulation)
        pct_new = current_pct + (prof["base_pct_slope"] * alpha_accumulation)

    return round(pcr_new, 1), round(pct_new, 2)
