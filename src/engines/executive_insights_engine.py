"""Executive Insights Engine — transforms assessment data into actionable PM insights.

Converts raw assessment outputs into decision-support intelligence.
No new knowledge bases, no new data collection, no methodology changes.
"""
from __future__ import annotations


def generate_insights(assessment: dict) -> list[dict]:
    """Generate 3-5 key insights from a completed assessment."""
    insights = []
    tech = assessment.get("technology_assessment", {})
    capex = assessment.get("capex_assessment", {})
    lcoh = assessment.get("lcoh_assessment", {})
    risk = assessment.get("risk_assessment", {})
    pm = assessment.get("pm_review", {})
    query = assessment.get("query", {})
    projects = assessment.get("similar_projects", {}).get("ranked_projects", [])

    # Insight 1: Cost driver dominance
    lcoh_decomp = lcoh.get("decomposition", [])
    elec_share = 0
    for d in lcoh_decomp:
        if "electricity" in d.get("component", "").lower():
            elec_share = d.get("pct", 0)
            break
    if elec_share > 0:
        is_dominant = elec_share > 40
        insights.append({
            "id": "INS-001",
            "title": "Electricity Cost Dominance",
            "observation": f"Electricity contributes {elec_share:.0f}% of LCOH at the assumed electricity price of EUR {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)}/MWh.",
            "business_impact": f"A {'higher' if is_dominant else 'substantial'} electricity price directly erodes project margins more than any other single factor{' — a 10 EUR/MWh increase adds EUR {} per kg to LCOH'.format(lcoh.get('tornado',[{}])[0].get('impact','')) if is_dominant else ''}.",
            "reasoning": f"Based on LCOH decomposition from lcoh_methodology_framework.md using {lcoh.get('decomposition',[{}])[0].get('pct',0):.0f}% CAPEX contribution vs {elec_share:.0f}% electricity.",
            "recommendation": "Secure a long-term fixed-price renewable PPA covering at least 70% of expected consumption before FEED completion. Target electricity price should be at or below the assumed price in this assessment."
        })

    # Insight 2: Technology maturity and risk
    foak_app = tech.get("is_foak_for_application", False)
    foak_scale = tech.get("is_foak_for_scale", False)
    if foak_app or foak_scale:
        foak_detail = []
        if foak_app:
            foak_detail.append(f"the application ({query.get('industry','')}) has no operational reference with this technology")
        if foak_scale:
            foak_detail.append(f"the scale ({query.get('capacity_mw','')} MW) exceeds the largest known deployment")
        insights.append({
            "id": "INS-002",
            "title": "First-of-a-Kind Risk Premium",
            "observation": f"This project is first-of-a-kind for {' and '.join(foak_detail)}.",
            "business_impact": "FOAK projects carry a 10-20% CAPEX premium and 20-30% schedule contingency over nth-of-a-kind equivalents. Lenders typically require higher debt service coverage ratios.",
            "reasoning": f"FOAK determination from Technology Card {tech.get('technology_id','')}. FOAK premium of {'+5% for application' if foak_app else ''}{' +10% for scale' if foak_scale else ''}{' +5% total' if (foak_app and not foak_scale) else ' +10% total' if foak_scale else ''} applied to CAPEX contingency.",
            "recommendation": "Partner with an experienced EPC contractor with relevant hydrogen delivery track record. Budget 15-25% CAPEX contingency. Engage lenders early to align on technology risk perception."
        })
    else:
        insights.append({
            "id": "INS-002",
            "title": "Technology Maturity Confirmed",
            "observation": f"{tech.get('technology_name','')} is at TRL {tech.get('trl','')} ({tech.get('commercial_maturity','')}). The project at {query.get('capacity_mw','')} MW is within proven deployment range.",
            "business_impact": "Within-proven-scale technology reduces financing risk. Lenders are more likely to accept technology risk at this TRL.",
            "reasoning": f"TRL assessed in {tech.get('technology_id','')}. Proven scale derived from Gold Dataset projects with matching technology.",
            "recommendation": "Proceed with standard project finance structure. No technology risk premium required from lenders."
        })

    # Insight 3: Risk exposure
    top_risks = risk.get("top_risks", [])
    if top_risks:
        high_risks = [r for r in top_risks if r.get("risk_class") in ("high", "critical")]
        medium_risks = [r for r in top_risks if r.get("risk_class") == "medium"]
        high_count = len(high_risks)
        med_count = len(medium_risks)
        risk_verb = "CRITICAL" if high_count > 0 else "notable" if med_count > 0 else "manageable"
        insights.append({
            "id": "INS-003",
            "title": f"Risk Profile: {high_count} High{'/Critical' if high_count > 0 else ''} Risks Identified",
            "observation": f"Of {risk.get('total_filtered',0)} risks assessed, {high_count} are {'high/critical' if high_count else ''}{' and ' if high_count and med_count else ''}{med_count} are medium priority.",
            "business_impact": f"This is a {'significant' if high_count > 0 else 'moderate' if med_count > 2 else 'manageable'} risk exposure. {'Executive attention required for high/critical risks.' if high_count else 'Standard project management processes are sufficient.'}",
            "reasoning": f"Risks filtered by technology ({query.get('technology','')}), scale ({query.get('capacity_mw','')} MW), and phase (pre-feasibility). Scored using FMEA methodology (P x I x D).",
            "recommendation": f"{'Assign dedicated risk owners for high/critical risks. Schedule monthly risk review.' if high_count > 0 else 'Standard quarterly risk review is adequate.'} {'Address top risk: ' + top_risks[0].get('risk_name','') + '.' if top_risks else ''}"
        })

    # Insight 4: Reference project coverage
    if projects:
        same_offtake = sum(1 for p in projects if p.get("primary_offtake") == query.get("offtake", ""))
        total = len(projects)
        coverage_pct = round(same_offtake / total * 100) if total > 0 else 0
        if coverage_pct < 20:
            insights.append({
                "id": "INS-004",
                "title": "Limited Direct Reference Coverage",
                "observation": f"Only {same_offtake} of {total} matched reference projects share the same offtake ({query.get('offtake','')}) as this project.",
                "business_impact": "Limited direct references increase uncertainty in cost benchmarking and risk assessment for this specific application. Cross-industry extrapolation introduces estimation error.",
                "reasoning": f"From project matching: {coverage_pct}% of top-matched projects share the offtake. Matching methodology cross-references via industry groups.",
                "recommendation": f"Commission a focused benchmarking study targeting {query.get('offtake','')}-specific projects. Consider broadening the Gold Dataset to include {query.get('offtake','')}-type offtake projects."
            })
        else:
            insights.append({
                "id": "INS-004",
                "title": "Strong Reference Coverage",
                "observation": f"{same_offtake} of {total} matched projects share the same offtake application, providing solid benchmarking basis.",
                "business_impact": "Strong reference coverage reduces estimation uncertainty and supports lender confidence during project financing.",
                "reasoning": f"Of the top {total} matched projects, {same_offtake} have matching offtake.",
                "recommendation": "Use the matched reference projects as primary benchmarks in the feasibility study. Highlight offtake alignment in lender presentation."
            })

    # Insight 5: FOAK vs nth-of-a-kind economics
    capex_central = capex.get("total", {}).get("central_eur_per_kw", 0)
    capex_p10 = capex.get("total", {}).get("p10_eur_m", 0)
    capex_p90 = capex.get("total", {}).get("p90_eur_m", 0)
    confidence = capex.get("weighted_confidence_label", "")
    insights.append({
        "id": "INS-005",
        "title": f"CAPEX Estimation: {confidence} Confidence",
        "observation": f"CAPEX estimated at EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M (EUR {capex_central:.0f}/kW) with a P10-P90 range of EUR {capex_p10:.0f}M to EUR {capex_p90:.0f}M.",
        "business_impact": f"The {'tight' if confidence == 'GOOD' else 'moderate' if confidence == 'ADEQUATE' else 'wide'} range reflects {'strong' if confidence == 'GOOD' else 'adequate' if confidence == 'ADEQUATE' else 'limited'} cost data confidence. A EUR {(capex_p90 - capex_p10) if capex_p90 and capex_p10 else 0:.0f}M spread between P10 and P90 represents {'manageable' if confidence == 'GOOD' else 'material' if confidence == 'ADEQUATE' else 'significant'} financial uncertainty.",
        "reasoning": f"AACE Class 4 estimate with weighted confidence of {capex.get('weighted_confidence',0):.2f}. Based on Cost Library benchmarks from IEA GHR 2025 and IRENA 2024.",
        "recommendation": f"Obtain an OEM budget quotation for the electrolyser stack to upgrade cost confidence from {'D' if confidence == 'ADEQUATE' else 'C'} to Class B. This will narrow the CAPEX range by an estimated 10-15%."
    })

    return insights


def generate_gate_justification(pm: dict, tech: dict, risk: dict, query: dict) -> dict:
    """Generate a structured gate justification with decision, why, and conditions."""
    gate = pm.get("gate_outcome", "INSUFFICIENT DATA")
    dims = pm.get("dimension_scores", {})
    dim_labels = {
        "project_references": "Reference Projects",
        "technology": "Technology",
        "risk": "Risk",
        "economics": "Economics"
    }

    reasons = []
    for key, label in dim_labels.items():
        d = dims.get(key, {})
        quality = d.get("quality", "INADEQUATE")
        reasons.append(f"{label}: {quality}")

    decision_text = {
        "PROCEED": "The project meets all assessment criteria. Proceed to feasibility study.",
        "PROCEED WITH CAUTION": "The project is fundamentally viable but has identified gaps that must be addressed before advancing to feasibility stage.",
        "DO NOT PROCEED": "The project has significant barriers that prevent advancement in its current form.",
        "INSUFFICIENT DATA": "The knowledge base does not contain enough information to assess this project profile."
    }

    conditions = pm.get("conditions", [])
    if tech.get("is_foak_for_application"):
        conditions.append(f"Resolve first-of-a-kind risk for {query.get('industry','')} application: commission technology qualification study before FEED.")
    if tech.get("is_foak_for_scale"):
        conditions.append(f"Resolve first-of-a-kind risk for {query.get('capacity_mw','')} MW scale: obtain OEM confirmation of manufacturing capability.")
    if not conditions:
        conditions.append("Proceed to feasibility study with standard project governance.")

    return {
        "decision": gate,
        "rationale": decision_text.get(gate, "Assessment incomplete."),
        "dimension_summary": reasons,
        "conditions": conditions[:5]
    }


def generate_risk_consequences(risk: dict, risk_library: list | None = None) -> list[dict]:
    """Enrich risks with structured consequence data already present in the Risk Library."""
    enhanced = []
    for r in risk.get("top_risks", [])[:10]:
        enhanced.append({
            "risk_id": r.get("risk_id", ""),
            "risk_name": r.get("risk_name", ""),
            "risk_class": r.get("risk_class", ""),
            "rpn": r.get("rpn", 0),
            "probability": r.get("probability", 3),
            "impact": r.get("impact", 3),
            "detectability": r.get("detectability", 3),
            "category": r.get("category", ""),
            "description": r.get("description", ""),
            "mitigation": r.get("mitigation", ""),
            "reference_projects": r.get("reference_projects", []),
        })
    return enhanced


def generate_project_match_breakdown(projects: list[dict]) -> list[dict]:
    """Add score breakdown to each matched project."""
    enhanced = []
    for p in projects:
        breakdown = {
            "Technology": f"{p.get('tech_score', 0)*100:.0f}%",
            "Industry": f"{p.get('industry_score', 0)*100:.0f}%",
            "Capacity": f"{p.get('capacity_score', 0)*100:.0f}%",
            "Country": f"{p.get('country_score', 0)*100:.0f}%",
            "Maturity": f"{p.get('maturity_score', 0)*100:.0f}%",
        }
        enhanced.append({
            "rank": p.get("rank"),
            "project_name": p.get("project_name"),
            "project_id": p.get("project_id"),
            "country": p.get("country"),
            "technology": p.get("technology"),
            "capacity_mw": p.get("capacity_mw"),
            "status": p.get("status"),
            "offtake": p.get("primary_offtake"),
            "composite_score": p.get("composite_score"),
            "tier": p.get("tier"),
            "rationale": p.get("rationale"),
            "score_breakdown": breakdown,
        })
    return enhanced
