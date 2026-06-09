"""Technical assessment engine — technology readiness, suitability, scale check."""
from typing import Optional

from src.models.data_models import TechnologyCard, ProjectReference, Query


def assess_technology(query: Query, card: TechnologyCard,
                      reference_projects: list[ProjectReference]) -> dict:
    """Produce a structured technology assessment."""
    # === TRL & Maturity ===
    trl = card.trl
    maturity = card.commercial_maturity
    trl_rationale = (
        f"TRL {trl} — {maturity}. "
        f"{'Proven at >100 MW single-plant scale.' if trl >= 8 else 'Still in demonstration phase.'}"
    )

    # === Scale check ===
    max_proven = _max_project_capacity(reference_projects, card.technology_type)
    scale_status, scale_detail, is_foak_scale = _check_scale(query.capacity_mw, max_proven)

    # === Application suitability ===
    app_info = card.suitability_scores.get(query.offtake or query.industry, {})
    suitability = app_info.get("suitability", "medium")
    app_rationale = app_info.get("rationale", f"No specific suitability data for '{query.offtake}' in Technology Card.")
    app_refs = app_info.get("reference_project_ids", [])

    # === FOAK determination ===
    app_refs_in_dataset = [r for r in reference_projects if r.project_id in app_refs]
    is_foak_app = len(app_refs_in_dataset) == 0 and suitability != "not_recommended"

    # === Performance relevance ===
    perf_notes = _performance_notes(query, card)

    return {
        "technology_name": card.technology_name,
        "technology_id": card.technology_id,
        "trl": trl,
        "trl_rationale": trl_rationale,
        "commercial_maturity": maturity,
        "scale_status": scale_status,
        "scale_detail": scale_detail,
        "max_proven_mw": max_proven,
        "is_foak_for_scale": is_foak_scale,
        "is_foak_for_application": is_foak_app,
        "foak_rationale": (
            f"First-of-a-kind for APPLICATION: no operational {card.technology_type} plant "
            f"has supplied a {query.offtake} facility."
        ) if is_foak_app else "Not first-of-a-kind.",
        "application_suitability": suitability,
        "application_rationale": app_rationale,
        "application_reference_projects": app_refs,
        "performance_notes": perf_notes,
        "key_advantages": _contextual_advantages(card, query),
        "key_limitations": _contextual_limitations(card, query),
        "confidence": "GOOD" if trl >= 8 and suitability == "high" else "ADEQUATE",
    }


def _max_project_capacity(projects: list[ProjectReference], tech: str) -> float:
    """Find max capacity among projects matching the technology (pure match only, exclude hybrids)."""
    tech_upper = tech.upper()
    max_mw = 0.0
    for p in projects:
        ptech = p.technology.upper()
        if tech_upper in ptech and "PEM+ALK" not in ptech:
            if p.capacity_mw > max_mw:
                max_mw = p.capacity_mw
    # If no pure matches found, include hybrids as fallback
    if max_mw == 0.0:
        for p in projects:
            ptech = p.technology.upper()
            if tech_upper in ptech or "PEM+ALK" in ptech:
                if p.capacity_mw > max_mw:
                    max_mw = p.capacity_mw
    return max_mw


def _check_scale(query_mw: float, max_proven: float) -> tuple[str, str, bool]:
    if max_proven == 0:
        return "unknown", "No reference projects found.", True
    if query_mw <= max_proven:
        return (
            "within_proven_range",
            f"Query scale ({query_mw} MW) is within proven deployment range (max {max_proven} MW).",
            False,
        )
    return (
        "beyond_proven_range",
        f"Query scale ({query_mw} MW) exceeds largest known deployment ({max_proven} MW). FOAK for scale.",
        True,
    )


def _performance_notes(query: Query, card: TechnologyCard) -> list[str]:
    notes = []
    notes.append(f"System efficiency: {card.system_efficiency_kwh_per_kg} kWh/kg H₂")
    notes.append(f"Stack lifetime: {card.stack_lifetime_hours:,} hours (~{card.stack_lifetime_hours // 8000} years at 8,000 hr/yr)")
    notes.append(f"Output pressure: {card.output_pressure_bar} bar — {'matches' if card.output_pressure_bar >= 20 else 'below'} typical industrial offtake pressure")
    notes.append(f"H₂ purity: {card.hydrogen_purity_percent}%")
    notes.append(f"Dynamic response: {card.ramp_rate_pct_per_second}%/s ramp, {card.min_load_percent}% min load, {card.cold_start_minutes} min cold start")
    return notes


def _contextual_advantages(card: TechnologyCard, query: Query) -> list[str]:
    """Select up to 5 most relevant advantages for this query context."""
    return card.advantages[:5]


def _contextual_limitations(card: TechnologyCard, query: Query) -> list[str]:
    """Select up to 5 most relevant limitations for this query context."""
    return card.limitations[:5]
