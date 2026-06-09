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

    # Range (P10-P90 based on total_record low/high)
    low_eur_per_kw = total_record.eur_per_kw_low if total_record.eur_per_kw_low > 0 else total_record.eur_per_kw * 0.75
    high_eur_per_kw = total_record.eur_per_kw_high if total_record.eur_per_kw_high > 0 else total_record.eur_per_kw * 1.35
    low_total_m = round(low_eur_per_kw * query.capacity_mw / 1000 * foak_mult, 0)
    high_total_m = round(high_eur_per_kw * query.capacity_mw / 1000 * foak_mult, 0)

    # Weighted confidence
    cw = CONFIDENCE_WEIGHTS.get(total_record.confidence_level, 0.50)

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
    }
