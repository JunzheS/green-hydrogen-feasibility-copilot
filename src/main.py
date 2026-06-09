#!/usr/bin/env python3
"""
Green Hydrogen Project Feasibility Copilot — Executable Engine v1.0

Single-command execution:
    python -m src.main

Or import programmatically:
    from src.main import FeasibilityEngine
    engine = FeasibilityEngine()
    report = engine.run(country="France", industry="Steel", technology="PEM", capacity_mw=100, target_cod=2029)
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.loaders.project_loader import load_all_projects
from src.loaders.technology_loader import load_all_technology_cards, get_card_for_technology
from src.loaders.risk_loader import load_all_risks
from src.loaders.cost_loader import load_all_costs
from src.engines.matching_engine import rank_projects
from src.engines.technical_assessment_engine import assess_technology
from src.engines.risk_assessment_engine import assess_risks
from src.engines.cost_assessment_engine import estimate_capex
from src.engines.lcoh_engine import calculate_lcoh
from src.engines.pm_review_engine import review_assessment
from src.models.data_models import Query, Technology
from src.utils.helpers import normalise_country, normalise_industry, get_industry_matches
from src.engines.executive_insights_engine import generate_insights, generate_gate_justification, generate_risk_consequences, generate_project_match_breakdown


class FeasibilityEngine:
    """Main orchestrator for the Green Hydrogen Project Feasibility Copilot."""

    def __init__(self):
        print("=" * 65)
        print("  GREEN HYDROGEN PROJECT FEASIBILITY COPILOT")
        print("  Executable Engine v1.0")
        print("=" * 65)
        print()
        print("Loading knowledge base...")
        self.projects = load_all_projects()
        print(f"  [OK] {len(self.projects)} project records loaded")
        self.tech_cards = load_all_technology_cards()
        print(f"  [OK] {len(self.tech_cards)} technology cards loaded ({', '.join(self.tech_cards.keys())})")
        self.risks = load_all_risks()
        print(f"  [OK] {len(self.risks)} risk records loaded")
        self.costs = load_all_costs()
        print(f"  [OK] {len(self.costs)} cost records loaded")
        print()

    def run(self, country: str, industry: str, technology: str,
            capacity_mw: float, target_cod: int,
            electricity_price: float = 40, full_load_hours: int = 4500) -> dict:
        """
        Execute a complete pre-feasibility assessment.

        Returns a structured report dict with all sections.
        """
        # --- Normalize query ---
        norm_country = normalise_country(country)
        norm_industry = normalise_industry(industry)
        offtake_matches = get_industry_matches(norm_industry)
        primary_offtake = offtake_matches[0][0] if offtake_matches else norm_industry

        tech_enum = Technology.PEM if "PEM" in technology.upper() else (
            Technology.ALKALINE if "ALK" in technology.upper() else Technology.PEM
        )

        query = Query(
            country=norm_country, industry=norm_industry,
            technology=technology, capacity_mw=capacity_mw,
            target_cod=target_cod,
            technology_enum=tech_enum, offtake=primary_offtake,
        )

        # --- Agent 1: Project Matching ---
        ranked = rank_projects(query, self.projects)

        # --- Agent 2: Technology Assessment ---
        card = get_card_for_technology(self.tech_cards, technology)
        if not card:
            return {"error": f"No technology card found for '{technology}'."}
        tech_assessment = assess_technology(query, card, self.projects)

        # --- Agent 3: Risk Assessment ---
        risk_assessment = assess_risks(
            query, self.risks,
            foak_scale=tech_assessment.get("is_foak_for_scale", False),
            foak_app=tech_assessment.get("is_foak_for_application", False),
        )

        # --- Agent 3: Cost Assessment ---
        capex_estimate = estimate_capex(
            query, self.costs,
            is_foak_app=tech_assessment.get("is_foak_for_application", False),
            is_foak_scale=tech_assessment.get("is_foak_for_scale", False),
        )

        # --- Agent 3: LCOH Assessment ---
        lcoh_estimate = calculate_lcoh(
            query, card, capex_estimate,
            electricity_price_eur_per_mwh=electricity_price,
            full_load_hours=full_load_hours,
        )

        # --- Build agent outputs for PM review ---
        matching_output = {
            "ranked_projects": [
                {
                    "rank": m.rank,
                    "project_id": m.project.project_id,
                    "project_name": m.project.project_name,
                    "country": m.project.country,
                    "technology": m.project.technology,
                    "capacity_mw": m.project.capacity_mw,
                    "status": m.project.status,
                    "primary_offtake": m.project.primary_offtake,
                    "composite_score": m.composite_score,
                    "tech_score": m.tech_score,
                    "industry_score": m.industry_score,
                    "capacity_score": m.capacity_score,
                    "country_score": m.country_score,
                    "maturity_score": m.maturity_score,
                    "tier": m.tier,
                    "rationale": m.rationale,
                }
                for m in ranked
            ],
            "total_scored": len(ranked),
            "query_offtake": primary_offtake,
        }

        # --- Agent 4: PM Review ---
        pm_review = review_assessment(
            query.__dict__, matching_output, tech_assessment,
            risk_assessment, capex_estimate, lcoh_estimate,
        )

        # --- Executive Intelligence ---
        assessment_payload = {
            "query": {
                "country": norm_country, "industry": norm_industry,
                "technology": technology, "capacity_mw": capacity_mw,
                "target_cod": target_cod,
                "offtake": primary_offtake,
            },
            "similar_projects": matching_output,
            "technology_assessment": tech_assessment,
            "risk_assessment": risk_assessment,
            "capex_assessment": capex_estimate,
            "lcoh_assessment": lcoh_estimate,
            "pm_review": pm_review,
        }
        executive_insights = generate_insights(assessment_payload)
        gate_justification = generate_gate_justification(pm_review, tech_assessment, risk_assessment, query.__dict__)
        risk_consequences = generate_risk_consequences(risk_assessment)
        project_breakdown = generate_project_match_breakdown(matching_output.get("ranked_projects", []))

        return {
            "query": {
                "country": norm_country, "industry": norm_industry,
                "technology": technology, "capacity_mw": capacity_mw,
                "target_cod": target_cod,
                "offtake": primary_offtake,
            },
            "similar_projects": matching_output,
            "technology_assessment": tech_assessment,
            "risk_assessment": risk_assessment,
            "capex_assessment": capex_estimate,
            "lcoh_assessment": lcoh_estimate,
            "pm_review": pm_review,
            "executive_insights": executive_insights,
            "gate_justification": gate_justification,
            "risk_consequences": risk_consequences,
            "project_match_breakdown": project_breakdown,
        }


def _safe(text: str) -> str:
    """Replace Unicode characters that can't be encoded in cp1252 (Windows console)."""
    replacements = {
        '—': '--', '–': '-', '’': "'", '‘': "'",
        '“': '"', '”': '"', '…': '...',
        'é': 'e', 'è': 'e', 'ê': 'e',
        'à': 'a', 'ô': 'o', 'ö': 'o',
        'ü': 'u', 'û': 'u',
        'É': 'E', 'È': 'E',
        '₂': '2',  # subscript 2 (H2)
        '²': '2',  # superscript 2
        '≤': '<=', '≥': '>=', '±': '+/-',
        '°': 'deg',  # degree symbol
        'μ': 'u',  # micro
        '™': '(TM)',
        '€': 'EUR',
    }
    result = text
    for k, v in replacements.items():
        result = result.replace(k, v)
    return result.encode('ascii', errors='replace').decode('ascii')


def print_report(report: dict):
    """Print a human-readable feasibility report to stdout."""
    if "error" in report:
        print(f"\n  ERROR: {report['error']}\n")
        return

    q = report["query"]
    tech = report["technology_assessment"]
    capex = report["capex_assessment"]
    lcoh = report["lcoh_assessment"]
    pm = report["pm_review"]
    risk = report["risk_assessment"]

    print()
    print("=" * 65)
    print("  PRELIMINARY FEASIBILITY ASSESSMENT REPORT")
    print("=" * 65)
    print()

    # §1 Executive Summary
    print("--- S1 EXECUTIVE SUMMARY ---")
    print(f"  Project: {q['capacity_mw']} MW {q['technology']} in {q['country']} for {q['industry']}")
    print(f"  Target COD: {q['target_cod']}")
    print(f"  Gate Outcome: {pm['gate_outcome']}")
    print(f"  Overall Confidence: {pm['overall_confidence']['label']} ({pm['overall_confidence']['score']:.2f})")
    print()

    # S2 Similar Projects
    print("--- S2 SIMILAR REFERENCE PROJECTS ---")
    for p in report["similar_projects"]["ranked_projects"]:
        print(f"  #{p['rank']} {p['project_name']} ({p['project_id']})")
        print(f"     {p['country']} | {p['capacity_mw']} MW {p['technology']} | {p['status']} | {p['primary_offtake']}")
        print(f"     Score: {p['composite_score']:.2f} ({p['tier']})")
        print(f"     {p['rationale'][:150]}")
        print()
    print(f"  Total projects scored: {report['similar_projects']['total_scored']}")
    print()

    # S3 Technology Assessment
    print("--- S3 TECHNOLOGY ASSESSMENT ---")
    print(f"  Technology: {tech['technology_name']} ({tech['technology_id']})")
    print(f"  {tech['trl_rationale']}")
    print(f"  Application suitability for {q['offtake']}: {tech['application_suitability'].upper()}")
    print(f"  {tech['application_rationale'][:200]}")
    print(f"  Scale status: {tech['scale_status']} (max proven: {tech['max_proven_mw']} MW)")
    print(f"  FOAK for application: {tech['is_foak_for_application']}")
    print()

    # S4 Key Risks
    print("--- S4 KEY RISKS ---")
    top = risk["top_risks"][:8]
    for r in top:
        print(f"  [{r['risk_class'].upper()}] {r['risk_id']} -- {r['risk_name'][:80]}")
        print(f"     RPN: {r['rpn']} (P={r['probability']} I={r['impact']} D={r['detectability']}) | {r['category']}")
        print(f"     Mitigation: {r['mitigation'][:120]}")
        print()
    print(f"  Total risks assessed: {risk['total_filtered']}")
    print()

    # S5 CAPEX
    print("--- S5 INDICATIVE CAPEX ASSESSMENT ---")
    t = capex["total"]
    print(f"  Central: EUR {t['central_eur_per_kw']}/kW -> EUR {t['central_eur_m']}M")
    print(f"  Range:   EUR {t['p10_eur_m']}M - EUR {t['p90_eur_m']}M")
    print(f"  AACE Class: {capex['aace_class']}")
    print(f"  Weighted Confidence: {capex['weighted_confidence_label']} ({capex['weighted_confidence']:.2f})")
    print()
    for b in capex["breakdown"]:
        print(f"  {b['category']:35s} EUR {b['eur_per_kw']:>6.0f}/kW  {b['eur_m']:>7.1f}M  {b['pct_of_total']:>5.1f}%  [{b['confidence']}]")
    print()

    # S6 LCOH
    print("--- S6 LCOH ASSESSMENT ---")
    print(f"  Central: EUR {lcoh['central_eur_per_kg']}/kg H2  (P10: EUR {lcoh['p10_eur_per_kg']} - P90: EUR {lcoh['p90_eur_per_kg']})")
    print(f"  Dominant driver: {lcoh['dominant_driver']}")
    print(f"  [!] {lcoh['data_quality_note'][:120]}")
    print()
    print("  LCOH Decomposition:")
    for d in lcoh["decomposition"]:
        print(f"    {d['component']:25s} EUR {d['eur_per_kg']:>6.2f}/kg  ({d['pct']:>3.0f}%)")
    print()
    print("  Sensitivity Tornado:")
    for t_item in lcoh["tornado"]:
        print(f"    {t_item['driver']:40s} {t_item['impact']}")
    print()

    # S7 Knowledge Gaps
    print("--- S7 KNOWLEDGE GAPS ---")
    for g in pm["critical_gaps"]:
        print(f"  [CRITICAL] {g[:150]}")
    for g in pm["important_gaps"]:
        print(f"  [IMPORTANT] {g[:150]}")
    if not pm["critical_gaps"] and not pm["important_gaps"]:
        print("  No significant knowledge gaps identified.")
    print()

    # S8 PM Review
    print("--- S8 GATE DECISION ---")
    print(f"  Gate: {pm['gate_outcome']}")
    if pm["conditions"]:
        print("  Conditions for advancement:")
        for i, c in enumerate(pm["conditions"][:5], 1):
            print(f"    {i}. {c[:150]}")
    print()
    print("=" * 65)
    print()


# ─── CLI Entry Point ───
if __name__ == "__main__":
    # Default: Case 1 from M9 validation
    engine = FeasibilityEngine()
    report = engine.run(
        country="France",
        industry="Steel",
        technology="PEM",
        capacity_mw=100,
        target_cod=2029,
    )
    print_report(report)
