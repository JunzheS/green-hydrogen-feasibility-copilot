"""Technology Comparison Engine — side-by-side PEM vs Alkaline assessment.

Reuses existing Technology Cards, Cost Library, Risk Library, and LCOH Module.
No new data collection or methodology changes.
"""
from src.main import FeasibilityEngine
from src.loaders.technology_loader import load_all_technology_cards, get_card_for_technology


def _extract(row: dict, card) -> dict:
    """Extract comparison-relevant fields from a single assessment result."""
    tech_assess = row.get("technology_assessment", {})
    capex = row.get("capex_assessment", {}).get("total", {})
    lcoh = row.get("lcoh_assessment", {})
    risks = row.get("risk_assessment", {}).get("top_risks", [])
    pm = row.get("pm_review", {})

    top_risk_name = risks[0].get("risk_name", "")[:70] if risks else "None"

    return {
        "trl": f"TRL {tech_assess.get('trl','')}/9 - {tech_assess.get('commercial_maturity','')}",
        "suitability": tech_assess.get("application_suitability", ""),
        "capex_per_kw": capex.get("central_eur_per_kw", 0),
        "capex_eur_m": capex.get("central_eur_m", 0),
        "capex_range": f"EUR {capex.get('p10_eur_m',0):.0f}M - EUR {capex.get('p90_eur_m',0):.0f}M",
        "lcoh": lcoh.get("central_eur_per_kg", 0),
        "lcoh_range": f"EUR {lcoh.get('p10_eur_per_kg',0):.2f} - EUR {lcoh.get('p90_eur_per_kg',0):.2f}/kg",
        "dominant_driver": lcoh.get("dominant_driver", "").replace("_", " ").title(),
        "top_risk": top_risk_name,
        "gate": pm.get("gate_outcome", ""),
        "max_scale": f"{tech_assess.get('max_proven_mw',0)} MW" if tech_assess.get("max_proven_mw") else "N/A",
        "efficiency": f"{card.system_efficiency_kwh_per_kg} kWh/kg" if card else "N/A",
        "stack_life": f"{card.stack_lifetime_hours:,} hrs" if card else "N/A",
        "output_pressure": f"{card.output_pressure_bar} bar" if card else "N/A",
        "purity": f"{card.hydrogen_purity_percent}%" if card else "N/A",
        "ramp_rate": f"{card.ramp_rate_pct_per_second}%/s" if card else "N/A",
        "min_load": f"{card.min_load_percent}%" if card else "N/A",
    }


def compare_technologies(query: dict, engine: FeasibilityEngine) -> dict:
    """Run the same assessment for both technologies and return side-by-side results."""
    pem_query = query.copy()
    alk_query = query.copy()
    pem_query["technology"] = "PEM"
    alk_query["technology"] = "Alkaline"

    pem_result = engine.run(**pem_query)
    alk_result = engine.run(**alk_query)

    cards = load_all_technology_cards()
    pem_card = get_card_for_technology(cards, "PEM")
    alk_card = get_card_for_technology(cards, "Alkaline")

    pem_data = _extract(pem_result, pem_card)
    alk_data = _extract(alk_result, alk_card)

    return {
        "PEM": pem_data,
        "Alkaline": alk_data,
        "recommended_applications": {
            "PEM": ["Refinery (high purity)", "Mobility (fuel cell grade)", "Solar-coupled projects", "Space-constrained brownfield sites"],
            "Alkaline": ["Ammonia (lowest CAPEX)", "Large-scale baseload (>200 MW)", "Steady renewable profiles (offshore wind)", "Cost-sensitive markets"],
        },
        "delta": {
            "capex_per_kw": round(pem_data["capex_per_kw"] - alk_data["capex_per_kw"], 0),
            "lcoh": round(pem_data["lcoh"] - alk_data["lcoh"], 2),
        }
    }
