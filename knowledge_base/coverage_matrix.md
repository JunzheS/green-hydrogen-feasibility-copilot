# Gold Dataset Coverage Matrix — Sprint 2

**Date:** 2026-06-09
**Total Projects:** 50 (from 10)

---

## Country Distribution

| Country | Count | Target | Status |
|---------|-------|--------|--------|
| France | 18 | ≥15 | ✅ |
| Germany | 9 | — | ✅ |
| Portugal | 4 | — | ✅ |
| Spain | 3 | — | ✅ |
| Netherlands | 3 | — | ✅ |
| Denmark | 3 | — | ✅ |
| Belgium | 3 | — | ✅ |
| Sweden | 2 | — | ✅ |
| Italy | 2 | — | ✅ |
| Austria | 1 | — | ✅ |
| Serbia | 1 | — | ✅ |
| Chile | 1 | — | ✅ |

## Technology Distribution

| Technology | Count | Target | Status |
|-----------|-------|--------|--------|
| PEM | 28 | 20-25 | ✅ (slightly above) |
| Alkaline | 12 | 20-25 | ⚠️ Below target |
| PEM+Alkaline | 6 | — | ✅ |
| SOEC | 3 | 2-3 | ✅ |
| AEM | 1 | 1-2 | ✅ |
| **Total** | **50** | **50** | ✅ |

## Offtake Distribution

| Offtake | Count | Before Sprint 2 | Delta |
|---------|-------|----------------|-------|
| refinery | 16 | 6 | +10 |
| industrial_heat | 12 | 1 | +11 |
| steel | 7 | 1 | +6 |
| ammonia | 5 | 1 | +4 |
| mobility | 4 | 1 | +3 |
| export | 2 | 0 | +2 |
| methanol | 2 | 0 | +2 |
| chemicals | 1 | 0 | +1 |
| grid_injection | 1 | 0 | +1 |

## Status Distribution

| Status | Count |
|--------|-------|
| operational | 18 |
| under_construction | 12 |
| planned | 20 |
| decommissioned | 0 |

## Project Scale Distribution

| Scale | Range | Count |
|-------|-------|-------|
| Small | <10 MW | 10 |
| Medium | 10-100 MW | 15 |
| Large | 100-500 MW | 13 |
| Very Large | >500 MW | 7 |
| Giga | >1 GW | 3 |
| Manufacturing | N/A | 2 |

## Score Verification: "No matching reference project"

All 5 validation cases return at least 3 projects matching. H2V Dunkerque Phase 1 (GA-PR-015) is now the top match for France/Steel/PEM queries — a direct steel-offtake PEM reference that did not exist in Sprint 1.

## French Project Detail

| ID | Name | MW | Tech | Offtake | Status |
|----|------|-----|------|---------|--------|
| GA-PR-001 | Normand'Hy | 200 | PEM | refinery | under_construction |
| GA-PR-002 | Masshylia | 20 | PEM | refinery | planned |
| GA-PR-011 | Lhyfe Bouin | 1 | PEM | mobility | operational |
| GA-PR-012 | Lhyfe Buleon | 5 | PEM | industrial_heat | operational |
| GA-PR-013 | Lhyfe Bessieres | 5 | PEM | industrial_heat | operational |
| GA-PR-014 | Green Horizon | 100 | PEM | ammonia | planned |
| GA-PR-015 | H2V Dunkerque P1 | 200 | PEM | steel | under_construction |
| GA-PR-016 | H4 Marseille Fos | 390 | PEM+ALK | export | planned |
| GA-PR-021 | Genvia SLIND | 1 | SOEC | steel | under_construction |
| GA-PR-028 | Grandpuits | 20 | PEM | refinery | under_construction |
| GA-PR-031 | DH2 Dunkirk | 400 | ALK | steel | planned |
| GA-PR-032 | Sunrhyse/Hy2gen | 5 | PEM | industrial_heat | planned |
| GA-PR-036 | Verso Energy | 200 | PEM+ALK | refinery | planned |
| GA-PR-037 | Seine Axis Mobility | 50 | PEM | mobility | planned |
| GA-PR-041 | LHC Methanol | 20 | PEM | methanol | planned |
| GA-PR-045 | Engie H2 | 100 | PEM | refinery | planned |
| GA-PR-048 | McPhy Belfort | 300 | ALK | industrial_heat | operational |
| GA-PR-050 | Territoires d'Industrie | 15 | PEM | industrial_heat | operational |
