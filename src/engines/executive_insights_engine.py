"""Executive Insights Engine — converts assessment data into consulting-grade PM decision support."""
from __future__ import annotations


def generate_insights(assessment: dict) -> list[dict]:
    insights = []
    tech = assessment.get("technology_assessment", {})
    capex = assessment.get("capex_assessment", {})
    lcoh = assessment.get("lcoh_assessment", {})
    risk = assessment.get("risk_assessment", {})
    query = assessment.get("query", {})
    projects = assessment.get("similar_projects", {}).get("ranked_projects", [])

    # INS-001: Cost driver dominance
    lcoh_decomp = lcoh.get("decomposition", [])
    elec_share = 0
    for d in lcoh_decomp:
        if "electricity" in d.get("component", "").lower():
            elec_share = d.get("pct", 0)
            break
    if elec_share > 0:
        tornado = lcoh.get("tornado", [])
        sensitivity = tornado[0].get("impact", "EUR 0.55/kg") if tornado else "EUR 0.55/kg per EUR 10/MWh"
        insights.append({
            "id": "INS-001",
            "icon": "⚡",
            "label": "COST",
            "title": "Electricity Cost Dominates LCOH",
            "observation": f"Electricity represents {elec_share:.0f}% of the levelized cost. At EUR {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)}/MWh, this is EUR 2.20/kg of the total EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg.",
            "business_impact": "Electricity price has approximately 4x more impact on project economics than CAPEX accuracy. A EUR 10/MWh change swings LCOH by ~EUR 0.55/kg.",
            "recommendation": "Secure a fixed-price renewable PPA for at least 70% of consumption before FEED completion. Target EUR 35/MWh or below."
        })

    # INS-002: Technology maturity
    foak_app = tech.get("is_foak_for_application", False)
    foak_scale = tech.get("is_foak_for_scale", False)
    if foak_app or foak_scale:
        details = []
        if foak_app: details.append(f"application ({query.get('industry','')}) has no operational reference")
        if foak_scale: details.append(f"scale ({query.get('capacity_mw','')} MW) exceeds largest proven deployment")
        insights.append({
            "id": "INS-002", "icon": "⚠️", "label": "TECH",
            "title": "First-of-a-Kind Risk Identified",
            "observation": f"This project is first-of-a-kind for {' and '.join(details)}.",
            "business_impact": "FOAK status adds 10-20% CAPEX contingency and requires higher debt service coverage. Expect extended lender due diligence (6-12 months).",
            "recommendation": "Partner with an EPC contractor with hydrogen track record. Budget 20% contingency. Engage lenders at pre-feasibility stage."
        })
    else:
        insights.append({
            "id": "INS-002", "icon": "✅", "label": "TECH",
            "title": "Technology Risk is Manageable",
            "observation": f"{tech.get('technology_name','')} at TRL {tech.get('trl','')}. {query.get('capacity_mw','')} MW is within proven deployment range.",
            "business_impact": "Standard project finance structure applicable. No technology risk premium required. Lender confidence expected to be high.",
            "recommendation": "Proceed with standard project finance. Reference: Normand'Hy (200 MW PEM under construction)."
        })

    # INS-003: Risk profile
    top_risks = risk.get("top_risks", [])
    if top_risks:
        high = [r for r in top_risks if r.get("risk_class") in ("high", "critical")]
        medium = [r for r in top_risks if r.get("risk_class") == "medium"]
        hc = len(high); mc = len(medium)
        insights.append({
            "id": "INS-003", "icon": "\U0001f6a8", "label": "RISK",
            "title": f"{hc} Critical and {mc} Medium Priority Risks",
            "observation": f"Of {risk.get('total_filtered',0)} assessed risks: {hc} high/critical, {mc} medium, {risk.get('risk_count_by_class',{}).get('low',0)} low.",
            "business_impact": f"{'Executive attention needed for high risks.' if hc > 0 else 'Standard project management processes are sufficient.'} Top risk: {top_risks[0].get('risk_name','')}.",
            "recommendation": f"{'Appoint dedicated risk owners and hold monthly reviews.' if hc > 0 else 'Standard quarterly risk review is adequate.'}"
        })

    # INS-004: Reference coverage
    if projects:
        direct_matches = sum(1 for p in projects if p.get("primary_offtake") == query.get("offtake", ""))
        total = len(projects)
        pct = round(direct_matches / total * 100) if total else 0
        if pct < 20:
            insights.append({
                "id": "INS-004", "icon": "\U0001f50d", "label": "BENCH",
                "title": "Limited Industry Benchmarking Data",
                "observation": f"Only {direct_matches} of {total} matched references share the same offtake ({query.get('offtake','')}).",
                "business_impact": "Benchmark confidence is reduced. Cost and risk estimates rely on cross-industry extrapolation.",
                "recommendation": "Commission a targeted benchmarking study. Consider expanding the reference dataset."
            })
        else:
            insights.append({
                "id": "INS-004", "icon": "\U0001f50d", "label": "BENCH",
                "title": "Strong Industry Benchmarks Available",
                "observation": f"{direct_matches} of {total} matched references share the same offtake — a solid basis for comparison.",
                "business_impact": "Reduces estimation uncertainty. Supports lender confidence.",
                "recommendation": "Use matched references as primary benchmarks. Highlight alignment in lender presentations."
            })

    # INS-005: CAPEX confidence
    capex_m = capex.get("total", {}).get("central_eur_m", 0)
    capex_kw = capex.get("total", {}).get("central_eur_per_kw", 0)
    p10 = capex.get("total", {}).get("p10_eur_m", 0)
    p90 = capex.get("total", {}).get("p90_eur_m", 0)
    conf_label = capex.get("weighted_confidence_label", "")
    spread = (p90 - p10) if p90 and p10 else 0
    insights.append({
        "id": "INS-005", "icon": "\U0001f4b0", "label": "CAPEX",
        "title": f"CAPEX: EUR {capex_m:.0f}M (EUR {capex_kw:.0f}/kW)",
        "observation": f"P10-P90 range: EUR {p10:.0f}M to EUR {p90:.0f}M. Spread: EUR {spread:.0f}M ({conf_label} confidence).",
        "business_impact": f"{'Range is tight enough for budget planning.' if conf_label == 'GOOD' else 'Range requires contingency planning.'} An OEM quotation could reduce uncertainty by 30-40%.",
        "recommendation": "Obtain a budget quotation from Siemens Energy or ITM Power to upgrade confidence to Class B."
    })
    return insights


def generate_gate_justification(pm: dict, tech: dict, risk: dict, query: dict) -> dict:
    gate = pm.get("gate_outcome", "INSUFFICIENT DATA")
    dims = pm.get("dimension_scores", {})
    labels = {"project_references": "References", "technology": "Tech", "risk": "Risk", "economics": "Economics"}
    reasons = [f"{labels[k]}: {d.get('quality','--')}" for k, d in dims.items()]
    conditions = list(pm.get("conditions", []))

    if tech.get("is_foak_for_application"):
        conditions.append(f"Resolve first-of-a-kind risk for {query.get('industry','')}: commission technology qualification study.")
    if not conditions:
        conditions.append("Proceed to feasibility study with standard project governance.")

    return {"decision": gate, "dimension_summary": reasons, "conditions": conditions[:5]}


def generate_risk_consequences(risk: dict) -> list[dict]:
    enhanced = []
    for r in risk.get("top_risks", [])[:10]:
        enhanced.append({
            "risk_id": r.get("risk_id", ""),
            "risk_name": r.get("risk_name", ""),
            "risk_class": r.get("risk_class", ""),
            "rpn": r.get("rpn", 0),
            "category": r.get("category", ""),
            "description": r.get("description", ""),
            "mitigation": r.get("mitigation", ""),
            "reference_projects": r.get("reference_projects", []),
        })
    return enhanced


def generate_project_match_breakdown(projects: list[dict]) -> list[dict]:
    enhanced = []
    for p in projects:
        breakdown = {k: f"{p.get(k.lower()+'_score',0)*100:.0f}%" for k in ["Technology","Industry","Capacity","Country","Maturity"]}
        breakdown["Technology"] = f"{p.get('tech_score',0)*100:.0f}%"
        breakdown["Industry"] = f"{p.get('industry_score',0)*100:.0f}%"
        breakdown["Capacity"] = f"{p.get('capacity_score',0)*100:.0f}%"
        breakdown["Country"] = f"{p.get('country_score',0)*100:.0f}%"
        breakdown["Maturity"] = f"{p.get('maturity_score',0)*100:.0f}%"
        enhanced.append({
            "rank": p.get("rank"), "project_name": p.get("project_name"), "project_id": p.get("project_id"),
            "country": p.get("country"), "technology": p.get("technology"), "capacity_mw": p.get("capacity_mw"),
            "status": p.get("status"), "offtake": p.get("primary_offtake"),
            "composite_score": p.get("composite_score"), "tier": p.get("tier"), "rationale": p.get("rationale"),
            "score_breakdown": breakdown,
        })
    return enhanced
