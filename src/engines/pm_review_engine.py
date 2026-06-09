"""PM Review engine — gate decision, evidence quality, confidence calibration."""
from src.models.data_models import GateOutcome


def review_assessment(query: dict, matching_result: dict, tech_result: dict,
                      risk_result: dict, capex_result: dict, lcoh_result: dict) -> dict:
    """Agent 4 — PM Review. Quality-gate the outputs of Agents 1-3."""

    # === D1: Project References ===
    proj_quality = _assess_project_quality(matching_result)

    # === D2: Technology ===
    tech_quality = _assess_technology_quality(tech_result)

    # === D3: Risk ===
    risk_quality = _assess_risk_quality(risk_result)

    # === D4: Economics ===
    econ_quality = _assess_economics_quality(capex_result, lcoh_result)

    # === Cross-consistency checks ===
    issues = _check_consistency(tech_result, capex_result)

    # === Knowledge gaps ===
    gaps = _identify_gaps(matching_result, tech_result, risk_result, lcoh_result)

    # === Confidence calibration ===
    calibrated = _calibrate_confidence(proj_quality, tech_quality, risk_quality, econ_quality)

    # === Gate decision ===
    gate, conditions = _gate_decision(proj_quality, tech_quality, risk_quality, econ_quality, gaps)

    return {
        "gate_outcome": gate.value,
        "overall_confidence": calibrated,
        "dimension_scores": {
            "project_references": {"quality": proj_quality["label"], "confidence": proj_quality["score"]},
            "technology": {"quality": tech_quality["label"], "confidence": tech_quality["score"]},
            "risk": {"quality": risk_quality["label"], "confidence": risk_quality["score"]},
            "economics": {"quality": econ_quality["label"], "confidence": econ_quality["score"]},
        },
        "conditions": conditions,
        "critical_gaps": gaps["critical"],
        "important_gaps": gaps["important"],
        "consistency_issues": issues,
        "calibration_rationale": calibrated["rationale"],
    }


def _assess_project_quality(matching: dict) -> dict:
    projects = matching.get("similar_projects", matching.get("ranked_projects", []))
    n = len(projects)
    avg_score = sum(p.get("composite_score", p.get("similarity_score", 0)) for p in projects) / n if n > 0 else 0
    if n >= 5 and avg_score >= 0.70:
        return {"label": "GOOD", "score": 0.70}
    elif n >= 3 and avg_score >= 0.50:
        return {"label": "GOOD", "score": 0.60}
    elif n >= 2 and avg_score >= 0.30:
        return {"label": "ADEQUATE", "score": 0.45}
    return {"label": "INADEQUATE", "score": 0.25}


def _assess_technology_quality(tech: dict) -> dict:
    trl = tech.get("trl", 2)
    suit = tech.get("application_suitability", "low")
    if trl >= 8 and suit == "high":
        return {"label": "GOOD", "score": 0.70}
    elif trl >= 7:
        return {"label": "GOOD", "score": 0.60}
    elif trl >= 5:
        return {"label": "ADEQUATE", "score": 0.45}
    return {"label": "INADEQUATE", "score": 0.25}


def _assess_risk_quality(risk: dict) -> dict:
    top_risks = risk.get("top_risks", [])
    with_evidence = sum(1 for r in top_risks if r.get("reference_projects"))
    n = len(top_risks) if top_risks else 1
    ratio = with_evidence / n
    if ratio >= 0.70:
        return {"label": "GOOD", "score": 0.65}
    elif ratio >= 0.40:
        return {"label": "ADEQUATE", "score": 0.50}
    return {"label": "ADEQUATE", "score": 0.40}


def _assess_economics_quality(capex: dict, lcoh: dict) -> dict:
    wc = capex.get("weighted_confidence", 0.50)
    if wc >= 0.60:
        return {"label": "GOOD", "score": 0.65}
    elif wc >= 0.40:
        return {"label": "ADEQUATE", "score": 0.50}
    return {"label": "ADEQUATE", "score": 0.35}


def _check_consistency(tech: dict, capex: dict) -> list[str]:
    issues = []
    foak_app = tech.get("is_foak_for_application", False)
    foak_scale = tech.get("is_foak_for_scale", False)
    if not foak_scale and capex.get("foak_applied", False):
        issues.append("Agent 2 determined NOT FOAK for scale, but FOAK premium was applied to CAPEX.")
    return issues


def _identify_gaps(matching: dict, tech: dict, risk: dict, lcoh: dict) -> dict:
    critical, important = [], []

    projects = matching.get("similar_projects", matching.get("ranked_projects", []))
    same_industry = [p for p in projects if _get_industry(p) == matching.get("query_offtake", "")]
    if not same_industry:
        critical.append(f"No reference projects with matching offtake ({matching.get('query_offtake', 'unknown')}) in Gold Dataset.")

    if tech.get("is_foak_for_application"):
        important.append(f"First-of-a-kind for application ({matching.get('query_offtake', '')}). No operational reference.")

    if lcoh.get("data_quality_note"):
        important.append("OPEX/LCOH uses Technology Card proxy data (Class D). OPEX Library not populated.")

    top_risks = risk.get("top_risks", [])
    without_evidence = [r for r in top_risks if not r.get("reference_projects")]
    if without_evidence:
        important.append(f"{len(without_evidence)} of {len(top_risks)} top risks lack Gold Dataset project evidence.")

    return {"critical": critical, "important": important}


def _calibrate_confidence(pj, tech, risk, econ) -> dict:
    scores = [pj["score"], tech["score"], risk["score"], econ["score"]]
    calibrated = min(scores)
    return {
        "score": round(calibrated, 2),
        "label": "GOOD" if calibrated >= 0.60 else "ADEQUATE" if calibrated >= 0.40 else "LIMITED",
        "rationale": f"Weakest dimension limits overall confidence at {calibrated:.2f}.",
    }


def _gate_decision(pj, tech, risk, econ, gaps) -> tuple[GateOutcome, list[str]]:
    conditions = []
    scores = {"GOOD": 3, "ADEQUATE": 2, "INADEQUATE": 1}
    total = scores.get(pj["label"], 0) + scores.get(tech["label"], 0) + scores.get(risk["label"], 0) + scores.get(econ["label"], 0)
    low_count = sum(1 for d in [pj, tech, risk, econ] if d["label"] == "INADEQUATE")

    if gaps["critical"]:
        conditions.extend(gaps["critical"])
    if gaps["important"]:
        conditions.extend(gaps["important"][:2])

    if low_count >= 2 or total <= 5:
        return GateOutcome.DO_NOT_PROCEED, conditions
    elif total <= 7 or gaps["critical"]:
        return GateOutcome.PROCEED_WITH_CAUTION, conditions
    elif total <= 11:
        return GateOutcome.PROCEED_WITH_CAUTION, conditions
    return GateOutcome.PROCEED, conditions


def _get_industry(project_dict: dict) -> str:
    p = project_dict.get("project", {})
    if hasattr(p, "primary_offtake"):
        return p.primary_offtake
    return project_dict.get("primary_offtake", "")
