# V2 Roadmap Recommendation

**Date:** 2026-06-09
**Basis:** System audit (system_capability_audit.md), asset map (knowledge_asset_map.md), agent capabilities (agent_capability_matrix.md), utilization analysis (knowledge_utilization_report.md)

---

## Recommendation: Option E — Commercial/Product Readiness

**After completing a full system audit, the strongest development direction for Version 2 is Commercial/Product Readiness**, not knowledge expansion, agent reasoning enhancement, or data quality improvement.

### Rationale

The audit reveals that:

1. **The core reasoning engine is already production-quality.** All 4 agents are fully implemented, validated (35/35 tests), and documented. Additional agent reasoning would provide marginal improvement relative to effort.

2. **Knowledge coverage is sufficient for a commercial product.** 82 projects, 18 countries, 5 technologies, 9 offtake types. Adding more projects provides diminishing returns — the dataset already matches all 10 test cases directly without cross-industry extrapolation.

3. **The OPEX Library gap (Class D LCOH) is the only critical knowledge gap.** This one gap prevents LCOH from being production-ready, but it is a data population task, not an architecture task.

4. **The highest-ROI improvements are in usability, trust, and deployment — not in data.** The underutilized assets (OEM/developer data, contradiction detection, source library) can be exposed in the UI at low cost.

5. **Commercial readiness creates recruiter and client value.** A deployable, shareable product with multi-user support and polished UX generates more credibility than additional projects or algorithmic improvements.

---

## V2 Roadmap — Commercial Readiness

### Phase 1: Commercial Foundation (Highest Priority)

| Task | Effort | Impact | Rationale |
|------|--------|--------|-----------|
| **Streamlit Cloud deployment** | 1 hour | Demonstrate live product | Public URL for CV, LinkedIn, demos |
| **Multi-user session isolation** | 3 days | Sharing capability | Multiple simultaneous users |
| **Persistent session logs** | 2 days | Demo retention | Return to previous sessions |
| **Technology comparison landing page** | 0.5 days | First impression | Default for recruiter link |

### Phase 2: Trust & Transparency

| Task | Effort | Impact | Rationale |
|------|--------|--------|-----------|
| **OPEX Library population (30 records)** | 5 days | LCOH Class C | Eliminates largest disclaimer |
| **Contradiction detection integration** | 2 days | Quality signal | Agent 4 harder, more trustworthy |
| **Source library browser** | 2 days | Transparency | 200+ sources browsable in UI |

### Phase 3: Knowledge Utilization

| Task | Effort | Impact | Rationale |
|------|--------|--------|-----------|
| **OEM filtering page** | 1 day | OEM comparison | Hideen data exposed |
| **Developer portfolio view** | 1 day | Portfolio analysis | "All Shell/Air Liquide projects" |
| **Source quality weight in confidence** | 1 day | Better calibration | Existing data unused |

### Phase 4: Advanced Features

| Task | Effort | Impact | Rationale |
|------|--------|--------|-----------|
| **Memory layer (persistence)** | 3 days | Audit trail | Future learning enabler |
| **Quantitative risk integration** | 3 days | Risk CAPEX | Risk-adjusted cost estimates |
| **Multi-project portfolio** | 5 days | PMO capability | Portfolio comparison |

---

## Comparison of Options

| Option | Effort | Value | Risk | Verdict |
|--------|--------|-------|------|---------|
| **E. Commercial Readiness** | Medium | HIGH | Low | ✅ RECOMMENDED |
| A. Knowledge Expansion | Low | LOW (diminishing) | None | ❌ Low ROI at 82 projects |
| B. Quality Improvement | Medium | MEDIUM | None | ⏸ Good but lower than commercial |
| C. Agent Reasoning | HIGH | LOW-MEDIUM | Medium | ❌ Agents already validated |
| D. PM Decision Support | MEDIUM | MEDIUM | None | ⏸ Good, but overlaps commercial |

## Evidence Summary

### Why Not Knowledge Expansion?

The dataset at 82 projects with 18 countries already covers all major European markets. Adding more French projects (26 already) provides diminishing returns. The gap in Alkaline (25) is marginal. Expanding to MENA, China, or North America adds breadth but not depth for the current European-focused use case.

### Why Not Agent Reasoning Enhancement?

The 4-agent architecture is validated with 35/35 regression tests and produces consulting-grade output. Adding Monte Carlo simulation or quantitative risk integration would improve precision but the improvement would be invisible to a recruiter or client seeing the product for the first time.

### Why Commercial Readiness First?

A live demo at a public URL, visible to a recruiter in 30 seconds, creates more career value than any algorithmic improvement. The product is already "correct" — it now needs to be "adoptable." Commercial readiness enables:
- Sending a single link instead of code installation instructions
- Demo persistence (not ephemeral sessions)
- Trust signals (public URL, professional domain, multi-user support)

---

## V2 Release Criteria

| Criterion | Current | Target | Priority |
|-----------|---------|--------|----------|
| Public URL | ❌ Not deployed | share.streamlit.io | P0 |
| Multi-user sessions | ❌ Single user | Basic session isolation | P1 |
| LCOH confidence | Class D | Class C (OPEX Library) | P1 |
| Session persistence | ❌ Ephemeral | History across visits | P2 |
| Contradiction detection | ❌ Not integrated | Displayed in Agent 4 output | P2 |
| OEM/developer index | ❌ Hidden | Filterable pages | P2 |
| Regression tests | 35/35 | 50+ tests | P3 |
