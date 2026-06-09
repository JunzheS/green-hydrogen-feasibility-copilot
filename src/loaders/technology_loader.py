"""Load Technology Card JSON records."""
import json
from pathlib import Path
from typing import Optional

from src.config.paths import TECHNOLOGY_CARDS_DIR
from src.models.data_models import TechnologyCard


def _safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return default
    return d if d is not None else default


def load_technology_card(filepath: Path) -> TechnologyCard:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    maturity = raw.get("maturity", {})
    perf = raw.get("performance", {})
    cost = raw.get("cost_profile", {})
    apps = raw.get("applications", {})

    # Parse suitability scores
    suitability: dict[str, dict] = {}
    for entry in apps.get("suitability_per_application", []):
        app_name = entry.get("application", "")
        suitability[app_name] = {
            "suitability": entry.get("suitability", "medium"),
            "rationale": entry.get("rationale", ""),
            "reference_project_ids": entry.get("reference_project_ids", []),
        }

    return TechnologyCard(
        technology_id=raw.get("technology_id", ""),
        technology_name=raw.get("technology_name", ""),
        technology_type=raw.get("technology_type", ""),
        trl=maturity.get("trl_level", 8),
        commercial_maturity=maturity.get("commercial_maturity", ""),
        system_efficiency_kwh_per_kg=perf.get("system_efficiency_kwh_per_kg_h2", 55),
        stack_lifetime_hours=perf.get("stack_lifetime_hours", 65000),
        output_pressure_bar=perf.get("hydrogen_output_pressure_bar", 30),
        hydrogen_purity_percent=perf.get("hydrogen_output_purity_percent", 99.99),
        degradation_rate_pct_per_year=perf.get("stack_degradation_rate_percent_per_year", 1.0),
        ramp_rate_pct_per_second=perf.get("load_ramp_rate_percent_per_second", 10),
        min_load_percent=perf.get("min_load_percent", 5),
        cold_start_minutes=perf.get("cold_start_time_minutes", 15),
        capex_stack_central=cost.get("capex_eur_per_kw", {}).get("typical_central", 800),
        capex_stack_low=cost.get("capex_eur_per_kw", {}).get("typical_range_low", 600),
        capex_stack_high=cost.get("capex_eur_per_kw", {}).get("typical_range_high", 1100),
        learning_rate_pct=cost.get("learning_rate_percent_per_doubling", 15),
        stack_replacement_eur_per_kw=cost.get("stack_replacement_cost_eur_per_kw", 350),
        advantages=raw.get("advantages", []),
        limitations=raw.get("limitations", []),
        scaling_constraints=raw.get("scalability", {}).get("scaling_constraints", []),
        primary_applications=apps.get("primary_applications", []),
        suitability_scores=suitability,
    )


def load_all_technology_cards() -> dict[str, TechnologyCard]:
    cards: dict[str, TechnologyCard] = {}
    if not TECHNOLOGY_CARDS_DIR.exists():
        return cards
    for fp in TECHNOLOGY_CARDS_DIR.rglob("*.json"):
        try:
            card = load_technology_card(fp)
            cards[card.technology_type] = card
        except Exception as e:
            print(f"  [WARN] Failed to load {fp.name}: {e}")
    return cards


def get_card_for_technology(cards: dict[str, TechnologyCard], tech: str) -> Optional[TechnologyCard]:
    """Get the card matching a technology string (PEM, Alkaline, etc.)."""
    tech_upper = tech.upper()
    for t, card in cards.items():
        if t.upper() == tech_upper or tech_upper in t.upper():
            return card
    # fuzzy: "pem" in card type
    for t, card in cards.items():
        if tech_upper in t.upper():
            return card
    return None
