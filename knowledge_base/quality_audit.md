# Gold Dataset Quality Audit — Sprint 2

**Date:** 2026-06-09
**Total Records:** 50

---

## Schema Compliance

| Field | Completion Rate | Notes |
|-------|-----------------|-------|
| project_id | 50/50 (100%) | GA-PR-001 through GA-PR-050 |
| project_name | 50/50 (100%) | All named |
| status | 50/50 (100%) | 3 status values used |
| country | 50/50 (100%) | 12 countries |
| technology.type | 50/50 (100%) | 5 technology types |
| capacity.electrolyzer_capacity_mw | 50/50 (100%) | Range: 0.5 MW to 7400 MW |
| offtake.primary_application | 50/50 (100%) | 9 distinct offtake types |
| stakeholders.developer | 50/50 (100%) | Identified for all |
| narrative_summary | 50/50 (100%) | All have summaries |
| sources | 50/50 (100%) | At least 1 source per project |
| coordinates | 50/50 (100%) | All estimated; coordinates_verified=false |

## Source Quality

| Level | Count | % | Change from Sprint 1 |
|-------|-------|---|---------------------|
| A (Official primary source) | 27 | 54% | +2% |
| B (Authoritative industry) | 8 | 16% | -11% |
| C (Professional media) | 15 | 30% | +10% |
| D (Unverified) | 0 | 0% | 0% |

## Matching Quality — Readmission

| Case | Query | Top Match | Score | Notes |
|------|-------|-----------|-------|-------|
| 1 | France, Steel, PEM, 100 MW | H2V Dunkerque Phase 1 | 0.96 | Direct steel-offtake match ✅ |
| 2 | Germany, Ind H2, ALK, 300 MW | Holland Hydrogen I | 0.93 | Same as Sprint 1 ✅ |
| 3 | Spain, Refinery, PEM, 20 MW | Puertollano | 0.84 | Operational reference ✅ |
| 4 | Belgium, Chemicals, ALK, 25 MW | Hyoffwind | 0.75 | Country match ✅ |
| 5 | Portugal, Ind H2, PEM, 100 MW | Galp Sines | 1.00 | Perfect match maintained ✅ |

## Coverage Requirements

| Requirement | Target | Actual | Status |
|-------------|--------|--------|--------|
| Total projects | 50 | 50 | ✅ |
| France | ≥15 | 18 | ✅ |
| PEM | 20-25 | 28 | ⚠️ (slightly above) |
| Alkaline | 20-25 | 12 | ⚠️ Below target |
| SOEC | 2-3 | 3 | ✅ |
| AEM | 1-2 | 1 | ✅ |
| Steel references | ≥3 | 7 | ✅ |
| Chemical references | ≥3 | 3 | ✅ |

## Regression Tests

| Test Suite | Result |
|-----------|--------|
| Engine loads 50 projects | ✅ |
| All 5 cases match to relevant projects | ✅ |
| No "No matching reference project" | ✅ |
| 35/35 test assertions passing | ✅ |
