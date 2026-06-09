#!/usr/bin/env python3
"""Execution demonstration -- prints structured intermediate + final output."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.main import FeasibilityEngine

engine = FeasibilityEngine()
report = engine.run(country="France", industry="Steel", technology="PEM", capacity_mw=100, target_cod=2029)

# --- Intermediate Outputs ---
print("=== INTERMEDIATE OUTPUTS ===")
print()

print("--- Query ---")
print(json.dumps(report["query"], indent=2))
print()

print("--- Agent 1: Project Matching (top 6 ranked) ---")
for p in report["similar_projects"]["ranked_projects"]:
    print(f"  #{p['rank']} {p['project_name']} ({p['project_id']})")
    print(f"     {p['country']} | {p['capacity_mw']} MW {p['technology']} | {p['status']} | {p['primary_offtake']}")
    print(f"     Score: {p['composite_score']:.2f} ({p['tier']})")
    print(f"     {p['rationale'][:120]}")
print()

print("--- Agent 2: Technology Assessment ---")
tech = report["technology_assessment"]
print(f"  TRL: {tech['trl']} -- {tech['commercial_maturity']}")
print(f"  Application suitability: {tech['application_suitability']} -- {tech['application_rationale'][:120]}")
print(f"  Scale status: {tech['scale_status']} (max proven: {tech['max_proven_mw']} MW)")
print(f"  FOAK scale: {tech['is_foak_for_scale']} | FOAK app: {tech['is_foak_for_application']}")
print(f"  Confidence: {tech['confidence']}")
print()

print("--- Agent 3: Risk Assessment ---")
risk = report["risk_assessment"]
print(f"  Risks filtered: {risk['total_filtered']}")
print(f"  By class: {risk['risk_count_by_class']}")
for r in risk["top_risks"][:5]:
    print(f"  [{r['risk_class'].upper()}] {r['risk_id']} RPN={r['rpn']} (P={r['probability']} I={r['impact']} D={r['detectability']})")
    print(f"     {r['risk_name'][:90]}")
print()

print("--- Agent 3: CAPEX Assessment ---")
capex = report["capex_assessment"]
print(f"  Central: EUR {capex['total']['central_eur_m']}M ({capex['total']['central_eur_per_kw']} EUR/kW)")
print(f"  Range: EUR {capex['total']['p10_eur_m']}M - EUR {capex['total']['p90_eur_m']}M")
print(f"  Confidence: {capex['weighted_confidence_label']} ({capex['weighted_confidence']})")
for b in capex["breakdown"]:
    print(f"  {b['category']:30s} EUR {b['eur_per_kw']:>6.0f}/kW  {b['eur_m']:>7.1f}M  {b['pct_of_total']:>5.1f}%  [{b['confidence']}]")
print()

print("--- Agent 3: LCOH Assessment ---")
lcoh = report["lcoh_assessment"]
print(f"  Central: EUR {lcoh['central_eur_per_kg']}/kg (P10: EUR {lcoh['p10_eur_per_kg']} - P90: EUR {lcoh['p90_eur_per_kg']})")
print(f"  Dominant driver: {lcoh['dominant_driver']}")
for d in lcoh["decomposition"]:
    print(f"  {d['component']:25s} EUR {d['eur_per_kg']:>6.2f}/kg  ({d['pct']:>3.0f}%)")
print()

print("--- Agent 4: PM Review ---")
pm = report["pm_review"]
print(f"  Gate: {pm['gate_outcome']}")
print(f"  Confidence: {pm['overall_confidence']['label']} ({pm['overall_confidence']['score']:.2f})")
print(f"  Dimensions: P={pm['dimension_scores']['project_references']['quality']} "
      f"T={pm['dimension_scores']['technology']['quality']} "
      f"R={pm['dimension_scores']['risk']['quality']} "
      f"E={pm['dimension_scores']['economics']['quality']}")
print(f"  Critical gaps: {len(pm['critical_gaps'])} | Important gaps: {len(pm['important_gaps'])}")
if pm['conditions']:
    print("  Conditions:")
    for i, c in enumerate(pm['conditions'][:3], 1):
        print(f"    {i}. {c[:120]}")

print()
print("=" * 65)
print("  EXECUTION COMPLETE -- All 4 agents produced output")
print("=" * 65)
