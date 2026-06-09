# Retrieval Agent Revalidation — Sprint 3

**Date:** 2026-06-09
**Dataset:** 82 projects (from 50)

---

## Revalidation Results

| Case | Query | Top Match | Score | Previous Score | Delta |
|------|-------|-----------|-------|---------------|-------|
| 1 | France, Steel, PEM, 100 MW | **H2V Dunkerque Phase 1** | **0.96** | 0.96 | — |
| 2 | Germany, Ind H2, ALK, 300 MW | **Holland Hydrogen I** | **0.93** | 0.93 | — |
| 3 | Spain, Refinery, PEM, 20 MW | **TotalEnergies Grandpuits** | **0.95** | 0.93 | +0.02 |
| 4 | Belgium, Chemicals, ALK, 25 MW | **Hyoffwind** | **0.75** | 0.75 | — |
| 5 | Portugal, Ind H2, PEM, 100 MW | **Galp Sines** | **1.00** | 1.00 | — |

## New Benchmark Scenarios

| # | Query | Top Match | Score | Match Quality |
|---|-------|-----------|-------|-------------|
| 6 | France, Chemicals, ALK, 100 MW | Hyport Green Ammonia / Plug Power (DK) | 0.89 | Good — chemicals ALK cross-match |
| 7 | Sweden, Steel, ALK, 500 MW | H2 Green Steel - Boden | **0.98** | **Excellent** — direct steel ALK match |
| 8 | France, Methanol, PEM, 50 MW | LHC Methanol (France) | 0.85 | Good — direct methanol match |
| 9 | Germany, Alkaline, 100 MW, P2X | Uniper H2 Maasvlakte | 0.84 | Good |
| 10 | Norway, Ammonia, ALK, 24 MW | Yara Porsgrunn | 0.89 | Excellent — same country+tech+offtake |

## Quality Improvements vs Sprint 2

| Metric | Sprint 2 | Sprint 3 | Improvement |
|--------|----------|----------|-------------|
| Direct match score (avg) | 0.82 | 0.87 | +0.05 |
| Direct steel-ofktake matches | 2 | 4 | +2 |
| Direct chemical/methanol matches | 0 | 4 | +4 |
| Countries covered | 12 | 18 | +6 |
| Alkaline coverage | 12 | 25 | +13 |
| Operational references | 18 | 27 | +9 |
| "No match" cases | 0 | 0 | — |
| Cross-industry extrapolation | 2 cases | 0 cases | Eliminated |

## No "No Matching Reference" Cases

All 10 test cases return at least 3 relevant projects. Direct matches are now available for steel, chemicals, and methanol queries that previously required cross-industry extrapolation.
