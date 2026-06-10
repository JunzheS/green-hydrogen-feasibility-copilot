"""Risk assessment engine — filter, rank, and contextualize risks."""
from src.models.data_models import RiskRecord, Query
from src.utils.helpers import get_scale_category

RISK_CATEGORIES = [
    "technical", "supply_chain", "grid_energy", "regulatory",
    "financial", "construction", "operational", "environmental",
]


def assess_risks(query: Query, all_risks: list[RiskRecord],
                 foak_scale: bool = False, foak_app: bool = False) -> dict:
    """Filter risks by technology, scale, and phase. Return top risks per category."""

    scale_cat = get_scale_category(query.capacity_mw)
    filtered: list[RiskRecord] = []

    for r in all_risks:
        # Technology filter — strict exact-match (V1.1 fix: no cross-technology leakage)
        # A risk tagged ["Alkaline"] must NOT appear for a PEM query.
        # A risk tagged ["PEM", "Alkaline"] applies to both.
        # A risk with empty technology_types is treated as technology-agnostic.
        risk_techs_upper = [t.upper() for t in r.technology_types]
        tech_query = query.technology.upper()
        if risk_techs_upper and tech_query not in risk_techs_upper:
            continue
        # Scale filter (loose — include if any scale matches or "any")
        scale_match = any(
            s == "any" or scale_cat in s or s in scale_cat
            for s in r.project_scales
        )
        if not scale_match and r.project_scales:
            continue
        # FOAK filter
        if r.foak_only and not (foak_scale or foak_app):
            continue
        filtered.append(r)

    # Group by category
    by_cat: dict[str, list[RiskRecord]] = {c: [] for c in RISK_CATEGORIES}
    for r in filtered:
        cat = r.risk_category
        if cat not in by_cat:
            cat = "technical"  # fallback
        by_cat[cat].append(r)

    # Sort each category by RPN descending, take top 2
    top_risks: list[RiskRecord] = []
    for cat in RISK_CATEGORIES:
        cat_risks = sorted(by_cat.get(cat, []), key=lambda r: r.rpn, reverse=True)
        top_risks.extend(cat_risks[:2])

    # Sort final list by RPN descending
    top_risks.sort(key=lambda r: r.rpn, reverse=True)

    return {
        "risks_by_category": {c: [
            {"risk_id": r.risk_id, "risk_name": r.risk_name, "rpn": r.rpn, "risk_class": r.risk_class}
            for r in sorted(by_cat.get(c, []), key=lambda x: x.rpn, reverse=True)[:3]
        ] for c in RISK_CATEGORIES if by_cat.get(c)},
        "top_risks": [
            {
                "risk_id": r.risk_id,
                "risk_name": r.risk_name,
                "category": r.risk_category,
                "subcategory": r.risk_subcategory,
                "probability": r.probability,
                "impact": r.impact,
                "detectability": r.detectability,
                "rpn": r.rpn,
                "risk_class": r.risk_class,
                "description": r.description_summary,
                "consequences": r.consequences_summary,
                "mitigation": r.mitigation_summary,
                "reference_projects": r.reference_project_ids,
            }
            for r in top_risks[:16]
        ],
        "risk_count_by_class": _count_by_class(filtered),
        "total_filtered": len(filtered),
    }


def _count_by_class(risks: list[RiskRecord]) -> dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for r in risks:
        cls = r.risk_class
        if cls in counts:
            counts[cls] += 1
    return counts
