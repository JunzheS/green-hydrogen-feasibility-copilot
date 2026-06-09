"""Load Gold Dataset project records from JSON files."""
import json
from pathlib import Path
from typing import Optional

from src.config.paths import GOLD_DATASET_DIR
from src.models.data_models import ProjectReference


def _safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return default
    return d if d is not None else default


def load_project(filepath: Path) -> ProjectReference:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    loc = raw.get("location", {})
    tech = raw.get("technology", {})
    cap = raw.get("capacity", {})
    offtake = raw.get("offtake", {})
    fin = raw.get("financial", {})
    dm = raw.get("data_management", {})

    return ProjectReference(
        project_id=raw.get("project_id", ""),
        project_name=raw.get("project_name", ""),
        country=loc.get("country", ""),
        region=loc.get("region_classification", "europe"),
        technology=tech.get("type", ""),
        capacity_mw=cap.get("electrolyzer_capacity_mw", 0),
        status=raw.get("status", ""),
        primary_offtake=offtake.get("primary_application", ""),
        secondary_offtakes=offtake.get("secondary_applications", []),
        total_capex_eur=fin.get("total_capex_eur"),
        capex_per_kw_eur=fin.get("capex_per_kw_eur"),
        narrative_summary=dm.get("narrative_summary", ""),
        is_first_of_a_kind=dm.get("is_first_of_a_kind", False),
        data_completeness_tier=dm.get("data_completeness_tier", ""),
    )


def load_all_projects() -> list[ProjectReference]:
    projects: list[ProjectReference] = []
    if not GOLD_DATASET_DIR.exists():
        return projects
    for fp in sorted(GOLD_DATASET_DIR.glob("GA-PR-*.json")):
        try:
            projects.append(load_project(fp))
        except Exception as e:
            print(f"  [WARN] Failed to load {fp.name}: {e}")
    return projects


def get_project_by_id(projects: list[ProjectReference], project_id: str) -> Optional[ProjectReference]:
    for p in projects:
        if p.project_id == project_id:
            return p
    return None
