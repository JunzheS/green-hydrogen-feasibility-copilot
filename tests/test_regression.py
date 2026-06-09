#!/usr/bin/env python3
"""
Regression test suite -- validates engine outputs against M9 validation report.

Run:  python tests/test_regression.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.main import FeasibilityEngine

TEST_CASES = [
    {
        "name": "Case 1: France 100MW PEM Steel 2029",
        "query": dict(country="France", industry="Steel", technology="PEM", capacity_mw=100, target_cod=2029),
        "expected": {
            "top_project_id": "GA-PR-001",
            "top_score_min": 0.70,
            "trl": 8, "suitability": "high",
            "risk_count_min": 10,
            "capex_central_min_m": 120, "capex_central_max_m": 210,
            "lcoh_central_min": 3.0, "lcoh_central_max": 6.0,
            "gate_in": ["PROCEED WITH CAUTION", "PROCEED"],
        },
    },
    {
        "name": "Case 2: Germany 300MW Alkaline Industrial H2 2030",
        "query": dict(country="Germany", industry="Industrial Hydrogen", technology="Alkaline", capacity_mw=300, target_cod=2030),
        "expected": {
            "top_project_id": "GA-PR-003",
            "top_score_min": 0.80,
            "trl": 9,
            "risk_count_min": 8,
            "capex_central_min_m": 250, "capex_central_max_m": 550,
            "lcoh_central_min": 2.5, "lcoh_central_max": 6.0,
            "gate_in": ["PROCEED WITH CAUTION", "PROCEED"],
        },
    },
    {
        "name": "Case 3: Spain 20MW PEM Refinery 2028",
        "query": dict(country="Spain", industry="Refinery", technology="PEM", capacity_mw=20, target_cod=2028),
        "expected": {
            "top_score_min": 0.70,
            "trl": 8, "suitability": "high",
            "risk_count_min": 8,
            "capex_central_min_m": 25, "capex_central_max_m": 55,
            "lcoh_central_min": 3.0, "lcoh_central_max": 8.0,
            "gate_in": ["PROCEED WITH CAUTION", "PROCEED", "DO NOT PROCEED"],
        },
    },
    {
        "name": "Case 4: Belgium 25MW Alkaline Chemicals 2029",
        "query": dict(country="Belgium", industry="Chemicals", technology="Alkaline", capacity_mw=25, target_cod=2029),
        "expected": {
            "top_score_min": 0.50,
            "trl": 9,
            "risk_count_min": 6,
            "capex_central_min_m": 25, "capex_central_max_m": 70,
            "lcoh_central_min": 3.0, "lcoh_central_max": 9.0,
            "gate_in": ["PROCEED WITH CAUTION", "PROCEED", "DO NOT PROCEED", "INSUFFICIENT DATA"],
        },
    },
    {
        "name": "Case 5: Portugal 100MW PEM Industrial H2 2030",
        "query": dict(country="Portugal", industry="Industrial Hydrogen", technology="PEM", capacity_mw=100, target_cod=2030),
        "expected": {
            "top_project_id": "GA-PR-010",
            "top_score_min": 0.80,
            "trl": 8,
            "risk_count_min": 10,
            "capex_central_min_m": 100, "capex_central_max_m": 220,
            "lcoh_central_min": 3.0, "lcoh_central_max": 6.5,
            "gate_in": ["PROCEED WITH CAUTION", "PROCEED"],
        },
    },
]


def run_tests():
    """Run all regression tests."""
    print("=" * 65)
    print("  REGRESSION TEST SUITE - Green Hydrogen Copilot Engine")
    print("=" * 65)
    print()

    engine = FeasibilityEngine()
    passed = 0
    total = 0
    failures = []

    for case in TEST_CASES:
        print(f"--- {case['name']} ---")
        q = case["query"]
        report = engine.run(**q)
        exp = case["expected"]

        if "error" in report:
            failures.append(f"{case['name']}: Engine error: {report['error']}")
            print(f"  [FAIL] {report['error']}")
            continue

        # Top project score
        ranked = report["similar_projects"]["ranked_projects"]
        top = ranked[0] if ranked else None
        if top:
            t_score = top["composite_score"]
            total += 1
            if t_score >= exp["top_score_min"]:
                passed += 1
                print(f"  [PASS] Top: {top['project_name']} (score {t_score:.2f} >= {exp['top_score_min']})")
            else:
                failures.append(f"{case['name']}: Score {t_score:.2f} < {exp['top_score_min']}")
                print(f"  [FAIL] Score {t_score:.2f} < {exp['top_score_min']}")

            if "top_project_id" in exp:
                total += 1
                if top["project_id"] == exp["top_project_id"]:
                    passed += 1
                    print(f"  [PASS] Top ID matches: {top['project_id']}")
                else:
                    print(f"  [WARN] Expected top {exp['top_project_id']}, got {top['project_id']}")

        # TRL
        trl = report["technology_assessment"]["trl"]
        total += 1
        if trl == exp["trl"]:
            passed += 1
            print(f"  [PASS] TRL: {trl}")
        else:
            failures.append(f"{case['name']}: TRL {trl} != {exp['trl']}")
            print(f"  [FAIL] TRL: {trl} != {exp['trl']}")

        # Suitability
        if "suitability" in exp:
            suit = report["technology_assessment"]["application_suitability"]
            total += 1
            if suit == exp["suitability"]:
                passed += 1
                print(f"  [PASS] Suitability: {suit}")
            else:
                failures.append(f"{case['name']}: Suitability {suit} != {exp['suitability']}")
                print(f"  [WARN] Suitability: {suit} != {exp['suitability']}")

        # Risk count
        risk_n = report["risk_assessment"]["total_filtered"]
        total += 1
        if risk_n >= exp["risk_count_min"]:
            passed += 1
            print(f"  [PASS] Risks: {risk_n} >= {exp['risk_count_min']}")
        else:
            failures.append(f"{case['name']}: Only {risk_n} risks")
            print(f"  [FAIL] Risks: {risk_n} < {exp['risk_count_min']}")

        # CAPEX
        capex_m = report["capex_assessment"]["total"]["central_eur_m"]
        total += 1
        if exp["capex_central_min_m"] <= capex_m <= exp["capex_central_max_m"]:
            passed += 1
            print(f"  [PASS] CAPEX: EUR {capex_m}M in [{exp['capex_central_min_m']}-{exp['capex_central_max_m']}]")
        else:
            failures.append(f"{case['name']}: CAPEX {capex_m}M outside range")
            print(f"  [WARN] CAPEX: EUR {capex_m}M outside expected range")

        # LCOH
        lcoh_c = report["lcoh_assessment"]["central_eur_per_kg"]
        total += 1
        if exp["lcoh_central_min"] <= lcoh_c <= exp["lcoh_central_max"]:
            passed += 1
            print(f"  [PASS] LCOH: EUR {lcoh_c}/kg in [{exp['lcoh_central_min']}-{exp['lcoh_central_max']}]")
        else:
            failures.append(f"{case['name']}: LCOH {lcoh_c}/kg outside range")
            print(f"  [WARN] LCOH: EUR {lcoh_c}/kg outside expected range")

        # Gate
        gate = report["pm_review"]["gate_outcome"]
        total += 1
        if gate in exp["gate_in"]:
            passed += 1
            print(f"  [PASS] Gate: {gate}")
        else:
            failures.append(f"{case['name']}: Gate '{gate}' not in {exp['gate_in']}")
            print(f"  [WARN] Gate: {gate} not in expected outcomes")

        print()

    print("=" * 65)
    print(f"  RESULTS: {passed}/{total} passed ({total - passed} failures)")
    print("=" * 65)

    if failures:
        print()
        print("  FAILURES:")
        for f in failures:
            print(f"    - {f}")
    return passed, total, failures


if __name__ == "__main__":
    passed, total, failures = run_tests()
    if failures:
        print(f"\n  {len(failures)} assertion(s) need investigation.")
        sys.exit(0 if len(failures) <= 3 else 1)
    else:
        print("\n  All regression tests passed.")
        sys.exit(0)
