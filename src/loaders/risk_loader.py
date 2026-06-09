"""Load Risk Library JSON records."""
import json
from pathlib import Path

from src.config.paths import RISK_LIBRARY_DIR, RISK_CATEGORIES
from src.models.data_models import RiskRecord


def _safe_get(d: dict, *keys, default=None):
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k)
        else:
            return default
    return d if d is not None else default


def load_risk_record(filepath: Path) -> RiskRecord:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)

    assessment = raw.get("assessment", {})
    applicability = raw.get("applicability", {})
    consequences = raw.get("consequences", {})
    mitigation = raw.get("mitigation", {})
    evidence = raw.get("evidence", {})

    # Extract mitigation summary from first action
    actions = mitigation.get("preventive_actions", [])
    mit_summary = actions[0].get("description", "")[:120] if actions else mitigation.get("strategy", "")

    # Extract consequence summary
    cons_schedule = consequences.get("schedule", {})
    cons_cost = consequences.get("cost", {})

    return RiskRecord(
        risk_id=raw.get("risk_id", ""),
        risk_name=raw.get("risk_name", ""),
        risk_category=raw.get("risk_category", ""),
        risk_subcategory=raw.get("risk_subcategory", ""),
        probability=assessment.get("probability", 3),
        impact=assessment.get("impact", 3),
        detectability=assessment.get("detectability", 3),
        rpn=assessment.get("risk_priority_number", 27),
        risk_class=assessment.get("risk_class", "medium"),
        description_summary=raw.get("description", {}).get("summary", ""),
        consequences_summary=f"{cons_schedule.get('impact', '')} delay, ~€{cons_cost.get('impact_eur', 0)//1_000_000}M cost" if cons_cost.get("impact_eur") else consequences.get("description", {}).get("description", "")[:150] if isinstance(consequences.get("description", {}), dict) else "",
        mitigation_summary=mit_summary,
        technology_types=applicability.get("technology_types", []),
        project_scales=applicability.get("project_scale", []),
        project_phases=applicability.get("project_phases", []),
        reference_project_ids=evidence.get("reference_project_ids", []),
        foak_only=applicability.get("first_of_a_kind_only", False),
    )


def load_all_risks() -> list[RiskRecord]:
    risks: list[RiskRecord] = []
    if not RISK_LIBRARY_DIR.exists():
        return risks
    for category in RISK_CATEGORIES:
        cat_dir = RISK_LIBRARY_DIR / category
        if not cat_dir.exists():
            continue
        for fp in sorted(cat_dir.glob("RK-*.json")):
            try:
                risks.append(load_risk_record(fp))
            except Exception as e:
                print(f"  [WARN] Failed to load {fp.name}: {e}")
    return risks
