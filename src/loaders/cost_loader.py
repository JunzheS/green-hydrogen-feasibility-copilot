"""Load Cost Library JSON records."""
import json
from pathlib import Path

from src.config.paths import COST_LIBRARY_DIR, COST_CATEGORIES
from src.models.data_models import CostRecord


def _safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return default
    return d if d is not None else default


def load_cost_record(filepath: Path) -> CostRecord:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    cost_data = raw.get("cost_data", {})
    context = raw.get("context", {})
    confidence = raw.get("confidence", {})
    drivers = raw.get("cost_drivers", {})

    return CostRecord(
        cost_id=raw.get("cost_id", ""),
        cost_name=raw.get("cost_name", ""),
        cost_category=raw.get("cost_category", ""),
        cost_subcategory=raw.get("cost_subcategory", ""),
        cost_basis=raw.get("cost_basis", ""),
        eur_per_kw=cost_data.get("eur_per_kw", 0),
        eur_per_kw_low=cost_data.get("eur_per_kw_low", 0),
        eur_per_kw_high=cost_data.get("eur_per_kw_high", 0),
        cost_year=cost_data.get("cost_year", 2025),
        technology_type=context.get("technology_type", "technology_agnostic"),
        project_scale_mw=context.get("project_scale_mw", 100),
        scale_is_extrapolated=context.get("scale_is_extrapolated", False),
        confidence_level=confidence.get("level", "C_industry_benchmark"),
        percentage_of_total_capex=cost_data.get("percentage_of_total_capex"),
        learning_rate_percent=drivers.get("learning_rate_percent"),
        project_reference_id=context.get("project_reference_id"),
        greenfield_or_brownfield=context.get("greenfield_or_brownfield"),
        sensitivity_to_scale=drivers.get("sensitivity_to_scale"),
    )


def load_all_costs() -> list[CostRecord]:
    costs: list[CostRecord] = []
    if not COST_LIBRARY_DIR.exists():
        return costs
    for category in COST_CATEGORIES:
        cat_dir = COST_LIBRARY_DIR / category
        if not cat_dir.exists():
            continue
        for fp in sorted(cat_dir.glob("CS-*.json")):
            try:
                costs.append(load_cost_record(fp))
            except Exception as e:
                print(f"  [WARN] Failed to load {fp.name}: {e}")
    return costs
