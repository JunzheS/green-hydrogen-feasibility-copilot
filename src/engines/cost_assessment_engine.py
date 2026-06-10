"""Cost assessment engine -- CAPEX estimation using taxonomy-based breakdown.

Matches the methodology validated in M9: select a total CAPEX benchmark,
apply scaling/learning, then apportion to categories using cost taxonomy percentages.
"""
import math
from typing import Optional

from src.models.data_models import CostRecord, Query


# Category percentage breakdown from cost_taxonomy_framework.md Section 4
TAXONOMY_PCT = {
    "PEM": {
        "01 Electrolyzer System": 32,
        "02 Electrical Infrastructure": 14,
        "03 Water Systems": 4,
        "04 Hydrogen Processing": 9,
        "05 Civil & Construction": 10,
        "06 Thermal Management": 3,
        "07 I&C": 4,
        "08 Indirect & Owner's": 24,
    },
    "Alkaline": {
        "01 Electrolyzer System": 28,
        "02 Electrical Infrastructure": 15,
        "03 Water Systems": 3,
        "04 Hydrogen Processing": 12,
        "05 Civil & Construction": 13,
        "06 Thermal Management": 3,
        "07 I&C": 4,
        "08 Indirect & Owner's": 22,
    },
}

# Confidence class weights
CONFIDENCE_WEIGHTS: dict[str, float] = {
    "A_actual_cost": 1.0, "B_contracted_price": 0.80,
    "C_industry_benchmark": 0.60, "D_analyst_estimate": 0.40,
}

# Per-category scaling exponents (cost_scaling_methodology.md)
SCALING_EXPONENTS: dict[str, float] = {
    "electrolyzer_system": 0.90,
    "electrical_infrastructure": 0.45,
    "water_systems": 0.85,
    "hydrogen_processing": 0.75,
    "civil_construction": 0.80,
    "thermal_management": 0.80,
    "instrumentation_controls": 0.65,
    "indirect_owners_costs": 0.55,
}


def _select_total_record(technology: str, scale_mw: float,
                         all_costs: list[CostRecord]) -> Optional[CostRecord]:
    """Select the best all-in total CAPEX benchmark record."""
    tech_upper = technology.upper()
    candidates = []

    for c in all_costs:
        if c.cost_basis != "all_in":
            continue
        ct = c.technology_type.upper()
        if "TECHNOLOGY_AGNOSTIC" not in ct and tech_upper not in ct:
            continue
        candidates.append(c)

    if not candidates:
        # Fall back to installed_cost records
        for c in all_costs:
            if "all" not in c.cost_subcategory.lower():
                continue
            ct = c.technology_type.upper()
            if "TECHNOLOGY_AGNOSTIC" not in ct and tech_upper not in ct:
                continue
            candidates.append(c)

    if not candidates:
        return None

    candidates.sort(key=lambda c: (
        1 if c.project_reference_id else 0,
        -abs(c.project_scale_mw - scale_mw)
    ), reverse=True)
    return candidates[0]


def _scale_to_target(eur_per_kw: float, record: CostRecord, target_mw: float) -> float:
    """Scale a per-kW cost value to target capacity.

    For per-kW costs: Cost_kW_B = Cost_kW_A * (Scale_B/Scale_A)^(n-1)
    This ensures scale-up decreases per-kW (economies of scale) and
    scale-down increases per-kW (small-plant penalty).
    """
    if record.project_scale_mw <= 0 or target_mw <= 0:
        return eur_per_kw
    exponent = SCALING_EXPONENTS.get(record.cost_category, 0.85)
    # For all-in totals, use a blended exponent (plant-level, not category-level)
    if record.cost_basis == "all_in":
        exponent = 0.80
    ratio = target_mw / record.project_scale_mw
    per_kw_exponent = exponent - 1.0  # per-kW scaling exponent is (n-1)
    return eur_per_kw * (ratio ** per_kw_exponent)


def _apply_learning(eur_per_kw: float, record: CostRecord, target_year: int) -> float:
    """Apply technology learning curve."""
    lr = record.learning_rate_percent
    if not lr or lr <= 0 or target_year <= record.cost_year:
        return eur_per_kw
    if "PEM" in record.technology_type.upper():
        doublings = (target_year - record.cost_year) / 3.5
    else:
        doublings = (target_year - record.cost_year) / 4.5
    if doublings <= 0:
        return eur_per_kw
    return eur_per_kw * ((1.0 - lr / 100.0) ** doublings)


def estimate_capex(query: Query, all_costs: list[CostRecord],
                   is_foak_app: bool = False, is_foak_scale: bool = False) -> dict:
    """Produce CAPEX estimate with taxonomy-based category breakdown."""

    # Select best total CAPEX benchmark
    total_record = _select_total_record(query.technology, query.capacity_mw, all_costs)
    if not total_record:
        return {"error": "No total CAPEX benchmark record found.", "breakdown": [], "total": {}}

    # Scale to target capacity
    central_total_eur_per_kw = _scale_to_target(
        total_record.eur_per_kw, total_record, query.capacity_mw)
    central_total_eur_per_kw = _apply_learning(
        central_total_eur_per_kw, total_record, query.target_cod)

    # FOAK premium: +5% for application, +10% for scale
    foak_mult = 1.0
    if is_foak_scale:
        foak_mult += 0.10
    elif is_foak_app:
        foak_mult += 0.05
    central_total_eur_per_kw *= foak_mult

    # Get taxonomy percentages for this technology
    tech_key = "PEM" if "PEM" in query.technology.upper() else "Alkaline"
    pct = TAXONOMY_PCT.get(tech_key, TAXONOMY_PCT["PEM"])

    # Build breakdown
    category_keys = list(pct.keys())
    breakdown = []
    total_central_m = central_total_eur_per_kw * query.capacity_mw / 1000

    for cat_name in category_keys:
        cat_pct = pct[cat_name]
        eur_per_kw = round(central_total_eur_per_kw * cat_pct / 100, 0)
        eur_m = round(total_central_m * cat_pct / 100, 1)
        breakdown.append({
            "category": cat_name,
            "eur_per_kw": eur_per_kw,
            "eur_m": eur_m,
            "pct_of_total": cat_pct,
            "confidence": "C" if cat_name != "08 Indirect & Owner's" else ("D" if is_foak_app else "C"),
            "cost_id": total_record.cost_id,
        })

    # Range (P10-P90) — V1.1 fix: apply same scale + learn + FOAK as central
    # Previously P10/P90 used raw record bounds, causing Central > P90
    # when target scale differed from reference scale (e.g., 5 MW query
    # against 100 MW benchmark: Central scaled to €14M but P90 stuck at €10M).
    if total_record.eur_per_kw_low > 0:
        low_eur_per_kw = _scale_to_target(total_record.eur_per_kw_low, total_record, query.capacity_mw)
        low_eur_per_kw = _apply_learning(low_eur_per_kw, total_record, query.target_cod)
    else:
        low_eur_per_kw = central_total_eur_per_kw * 0.75
    if total_record.eur_per_kw_high > 0:
        high_eur_per_kw = _scale_to_target(total_record.eur_per_kw_high, total_record, query.capacity_mw)
        high_eur_per_kw = _apply_learning(high_eur_per_kw, total_record, query.target_cod)
    else:
        high_eur_per_kw = central_total_eur_per_kw * 1.35
    low_total_m = round(low_eur_per_kw * query.capacity_mw / 1000 * foak_mult, 0)
    high_total_m = round(high_eur_per_kw * query.capacity_mw / 1000 * foak_mult, 0)

    # Weighted confidence
    cw = CONFIDENCE_WEIGHTS.get(total_record.confidence_level, 0.50)

    # ── V1.1: Industrial Development Budget (validation layer) ──
    industrial_budget = _estimate_industrial_budget(
        central_total_eur_per_kw, query.capacity_mw, query.target_cod,
        total_record.cost_year, tech_key,
        is_foak_app=is_foak_app, is_foak_scale=is_foak_scale)

    return {
        "breakdown": breakdown,
        "total": {
            "central_eur_per_kw": round(central_total_eur_per_kw, 0),
            "central_eur_m": round(total_central_m, 0),
            "p10_eur_m": low_total_m,
            "p90_eur_m": high_total_m,
        },
        "aace_class": "Class 4 (feasibility, +/-20-30%)",
        "weighted_confidence": round(cw, 2),
        "weighted_confidence_label": (
            "GOOD" if cw >= 0.60 else "ADEQUATE" if cw >= 0.40 else "LIMITED"
        ),
        "benchmark_record": total_record.cost_id,
        "foak_multiplier": foak_mult,
        "industrial_budget": industrial_budget,
    }


def _estimate_industrial_budget(
    reference_eur_per_kw: float,
    capacity_mw: float,
    target_cod: int,
    cost_year: int,
    tech_key: str,
    is_foak_app: bool = False,
    is_foak_scale: bool = False,
) -> dict:
    """V1.1: Estimate Industrial Development Budget.

    Expands the Reference Benchmark CAPEX (nth-of-a-kind, overnight, 2025 EUR)
    to a Total Investment Requirement reflecting first-project reality:

      Industrial Budget = Reference CAPEX
                         × FOAK_factor
                         × IDC_factor
                         × Scope_factor
                         × Escalation_factor

    All factors are documented and traceable to methodology documents.
    Calibrated for PEM; extended to Alkaline with reduced FOAK factors.
    NOT validated for SOEC or AEM.

    Reference: industrial_budget_methodology.md (Sprint 5D)
    """
    # ── FOAK Factor ──
    # Source: cost_assessment_engine.py FOAK multipliers + cost_scaling_methodology.md §5.2
    # PEP: +10% scale FOAK, +5% application FOAK, +5% developer first-project
    if tech_key == "PEM":
        foak_scale_factor = 0.10 if is_foak_scale else 0.0
        foak_app_factor = 0.05 if is_foak_app else 0.0
        developer_factor = 0.05  # conservative: assume first project by developer
        foak_mult = 1.0 + foak_scale_factor + foak_app_factor + developer_factor
    elif tech_key == "Alkaline":
        # Alkaline is more mature (TRL 9): reduced FOAK premiums
        # Source: cost_scaling_methodology.md §5.2 — Alkaline FOAK is 5-15% vs PEM 15-25%
        foak_scale_factor = 0.05 if is_foak_scale else 0.0
        foak_app_factor = 0.03 if is_foak_app else 0.0
        developer_factor = 0.03
        foak_mult = 1.0 + foak_scale_factor + foak_app_factor + developer_factor
    else:
        # SOEC, AEM: not validated — return null
        return {
            "available": False,
            "reason": (
                f"Industrial Development Budget is calibrated for PEM and Alkaline only. "
                f"{tech_key} lacks sufficient reference data for FOAK, IDC, and scope factors."
            ),
        }

    # ── IDC Factor (Interest During Construction) ──
    # Source: standard project finance — 3-year construction, 7% WACC on 50% drawdown
    # IDC ≈ (1 + WACC/2)^years − 1 ≈ (1.035)^3 − 1 ≈ 0.109 → factor 1.10
    idc_factor = 1.10

    # ── Scope Expansion Factor ──
    # Source: industry_feedback_validation_report.md §3.2 Explanation 3
    # Bulk H₂ buffer storage: +3-5%, extended commissioning: +3-5%, owner's internal: +2-3%
    # Blended: ~10% for pre-FEED stage scope uncertainty
    scope_factor = 1.10

    # ── Escalation Factor (2025 EUR → Year-of-Expenditure EUR) ──
    # Source: standard construction cost escalation at 3%/year
    # European chemical plant construction inflation: 2.5–3.5%/year (IHS Markit, 2024)
    years_to_cod = max(0, target_cod - cost_year)
    escalation_rate = 0.03
    escalation_factor = (1.0 + escalation_rate) ** years_to_cod

    # ── Compute ──
    total_multiplier = foak_mult * idc_factor * scope_factor * escalation_factor
    industrial_eur_per_kw = round(reference_eur_per_kw * total_multiplier, 0)
    industrial_eur_m = round(industrial_eur_per_kw * capacity_mw / 1000, 0)

    reference_eur_m = round(reference_eur_per_kw * capacity_mw / 1000, 0)

    return {
        "available": True,
        "technology_calibration": f"{tech_key}-calibrated",
        "industrial_eur_per_kw": industrial_eur_per_kw,
        "industrial_eur_m": industrial_eur_m,
        "reference_eur_m": reference_eur_m,
        "delta_pct": round((industrial_eur_m / reference_eur_m - 1.0) * 100, 0) if reference_eur_m > 0 else 0,
        "factors": {
            "foak_multiplier": round(foak_mult, 2),
            "foak_scale": is_foak_scale,
            "foak_application": is_foak_app,
            "developer_first_project": True,  # conservative assumption
            "idc_factor": idc_factor,
            "idc_assumption": "3-year construction, 7% WACC, 50% drawdown",
            "scope_factor": scope_factor,
            "scope_items": [
                "Bulk H₂ buffer storage (8-24 hour)",
                "Extended commissioning and performance testing",
                "Owner's internal development and project management",
                "Initial spares and first-fill consumables",
                "Pre-FEED scope contingency (~10% on BOP)",
            ],
            "escalation_factor": round(escalation_factor, 3),
            "escalation_rate_pct": 3.0,
            "escalation_years": years_to_cod,
            "cost_year": cost_year,
            "target_cod": target_cod,
            "total_multiplier": round(total_multiplier, 3),
        },
        "note": (
            "The Industrial Development Budget is a planning estimate for TOTAL investment "
            "requirement including FOAK premium, interest during construction, broader "
            "scope items, and cost escalation to year of expenditure. It is NOT a "
            "like-for-like comparison with the Reference Benchmark CAPEX (which is "
            "nth-of-a-kind, overnight, constant 2025 EUR). Use for budget planning, "
            "not for technology cost comparison."
        ),
    }
