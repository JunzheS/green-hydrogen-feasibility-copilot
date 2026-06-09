"""LCOH engine — levelized cost of hydrogen estimation.

Implements lcoh_methodology_framework.md exactly.
"""
from src.models.data_models import TechnologyCard, Query


def calculate_lcoh(query: Query, card: TechnologyCard, capex_result: dict,
                   electricity_price_eur_per_mwh: float = 40,
                   full_load_hours: int = 4500,
                   wacc: float = 0.07,
                   project_life_years: int = 20) -> dict:
    """Calculate LCOH with waterfall decomposition and sensitivity tornado."""

    total_capex_eur_per_kw = capex_result["total"]["central_eur_per_kw"]
    total_capex_m = capex_result["total"]["central_eur_m"]

    # Annual H₂ production
    annual_h2_kg = query.capacity_mw * 1000 * full_load_hours / card.system_efficiency_kwh_per_kg

    # Capital Recovery Factor
    crf = (wacc * (1 + wacc) ** project_life_years) / ((1 + wacc) ** project_life_years - 1)
    capex_annual_eur = total_capex_m * 1_000_000 * crf
    capex_per_kg = capex_annual_eur / annual_h2_kg if annual_h2_kg > 0 else 0

    # Electricity
    electricity_per_kg = card.system_efficiency_kwh_per_kg * electricity_price_eur_per_mwh / 1000

    # Stack replacement (sinking fund)
    stack_repl_annual = query.capacity_mw * 1000 * card.stack_replacement_eur_per_kw / (card.stack_lifetime_hours / full_load_hours)
    stack_repl_per_kg = stack_repl_annual / annual_h2_kg if annual_h2_kg > 0 else 0

    # Maintenance (from Technology Card OPEX proxy)
    maintenance_per_kg = 0.30 if "PEM" in card.technology_type.upper() else 0.23

    # Labor
    labor_eur_per_kg = 0.18 if "PEM" in card.technology_type.upper() else 0.17

    # Other OPEX (water, insurance, land, regulatory)
    other_opex_per_kg = 0.25

    total_opex_per_kg = electricity_per_kg + stack_repl_per_kg + maintenance_per_kg + labor_eur_per_kg + other_opex_per_kg
    total_lcoh = capex_per_kg + total_opex_per_kg

    # Decomposition
    decomposition = [
        {"component": "CAPEX contribution", "eur_per_kg": round(capex_per_kg, 2), "pct": round(capex_per_kg / total_lcoh * 100, 0) if total_lcoh > 0 else 0},
        {"component": "Electricity", "eur_per_kg": round(electricity_per_kg, 2), "pct": round(electricity_per_kg / total_lcoh * 100, 0) if total_lcoh > 0 else 0},
        {"component": "Stack Replacement", "eur_per_kg": round(stack_repl_per_kg, 2), "pct": round(stack_repl_per_kg / total_lcoh * 100, 0) if total_lcoh > 0 else 0},
        {"component": "Maintenance", "eur_per_kg": round(maintenance_per_kg, 2), "pct": round(maintenance_per_kg / total_lcoh * 100, 0) if total_lcoh > 0 else 0},
        {"component": "Labor", "eur_per_kg": round(labor_eur_per_kg, 2), "pct": round(labor_eur_per_kg / total_lcoh * 100, 0) if total_lcoh > 0 else 0},
        {"component": "Other OPEX", "eur_per_kg": round(other_opex_per_kg, 2), "pct": round(other_opex_per_kg / total_lcoh * 100, 0) if total_lcoh > 0 else 0},
    ]

    # Tornado sensitivity
    tornado = [
        {"driver": "Electricity ±€15/MWh", "impact": f"±€{round(card.system_efficiency_kwh_per_kg * 15 / 1000, 2)}/kg"},
        {"driver": "Capacity factor ±1,000 hrs", "impact": f"±€{round(capex_per_kg * 1000 / full_load_hours, 2)}/kg"},
        {"driver": f"CAPEX ±€{round(total_capex_eur_per_kw * 0.20, 0)}/kW", "impact": f"±€{round(capex_per_kg * 0.20, 2)}/kg"},
        {"driver": "System efficiency ±5 kWh/kg", "impact": f"±€{round(electricity_price_eur_per_mwh * 5 / 1000, 2)}/kg"},
        {"driver": "WACC ±2%", "impact": f"±€{round(capex_per_kg * 0.15, 2)}/kg"},
    ]

    # P10/P90 scenarios
    p10_lcoh = calculate_scenario(query, card, capex_result, electricity_price_eur_per_mwh * 0.75, int(full_load_hours * 1.22), wacc * 0.7)
    p90_lcoh = calculate_scenario(query, card, capex_result, electricity_price_eur_per_mwh * 1.50, int(full_load_hours * 0.78), wacc * 1.3)

    return {
        "central_eur_per_kg": round(total_lcoh, 2),
        "p10_eur_per_kg": round(p10_lcoh, 2),
        "p90_eur_per_kg": round(p90_lcoh, 2),
        "decomposition": decomposition,
        "tornado": tornado,
        "dominant_driver": "electricity_price" if electricity_per_kg > capex_per_kg else "capex",
        "assumptions": {
            "electricity_price_eur_per_mwh": electricity_price_eur_per_mwh,
            "full_load_hours": full_load_hours,
            "wacc_pct": wacc * 100,
            "project_life_years": project_life_years,
        },
        "data_quality_note": (
            "OPEX uses Technology Card proxy data (Class C). "
            "OPEX Library not populated. LCOH is CLASS D (PRELIMINARY). "
            "Do not use for investment decisions."
        ),
    }


def calculate_scenario(query: Query, card: TechnologyCard, capex_result: dict,
                       electricity_price: float, hours: int, wacc: float) -> float:
    """Quick scenario LCOH calculation."""
    total_capex_eur_per_kw = capex_result["total"]["central_eur_per_kw"]
    total_capex_m = total_capex_eur_per_kw * query.capacity_mw * 1000 / 1_000_000
    annual_h2_kg = query.capacity_mw * 1000 * hours / card.system_efficiency_kwh_per_kg
    crf = (wacc * (1 + wacc) ** 20) / ((1 + wacc) ** 20 - 1)
    capex_annual = total_capex_m * 1_000_000 * crf
    capex_per_kg = capex_annual / annual_h2_kg if annual_h2_kg > 0 else 0
    electricity_per_kg = card.system_efficiency_kwh_per_kg * electricity_price / 1000
    return capex_per_kg + electricity_per_kg + 0.85  # rough OPEX
