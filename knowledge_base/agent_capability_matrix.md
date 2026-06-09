# Agent Capability Matrix

**Date:** 2026-06-09

---

## Agent 1 — Knowledge Retrieval

| Dimension | Detail |
|-----------|--------|
| **Implementation** | ✅ Fully implemented in matching_engine.py |
| **Inputs** | country, industry, technology, capacity_mw, target_cod |
| **Outputs** | Top-6 ranked projects with scores, tier, rationale |
| **Knowledge Sources** | Gold Dataset (82 projects) |
| **Reasoning Methods** | 5-dimension weighted sum (tech 30%, industry 25%, capacity 25%, country 15%, maturity 5%) |
| **Score Breakdown** | ✅ Technology, Industry, Capacity, Country, Maturity per project |
| **Degradation** | ✅ Missing field, unknown country, extreme capacity |
| **Limitations** | No semantic/vector similarity — structured only. No developer/OEM indexing. |
| **Unused Potential** | Could match by developer, OEM, or site characteristics. Could cluster similar projects. |

## Agent 2 — Technical Assessment

| Dimension | Detail |
|-----------|--------|
| **Implementation** | ✅ Fully implemented in technical_assessment_engine.py |
| **Inputs** | technology, capacity_mw, industry, target_cod, similar_projects[] |
| **Outputs** | TRL, suitability, scale status, FOAK flags, performance notes, advantages, limitations |
| **Knowledge Sources** | TC-PEM-001, TC-ALK-001 |
| **Reasoning Methods** | Direct card lookup + max-proven-scale comparison |
| **Limitations** | No SOEC/AEM card. No cost-benefit estimation. Advantages/limitations are static text. |
| **Unused Potential** | Could use project-specific degradation data. Could compare against operational performance data from Gold Dataset. |

## Agent 3 — Risk & Economic Assessment

| Dimension | Detail |
|-----------|--------|
| **Implementation** | ✅ Fully implemented across risk_assessment_engine.py, cost_assessment_engine.py, lcoh_engine.py |
| **Inputs** | technology, capacity_mw, country, industry, target_cod, technology_verdict (FOAK flags) |
| **Outputs** | Risk ranking, CAPEX breakdown, LCOH decomposition, sensitivity tornado |
| **Knowledge Sources** | Risk Library (30), Cost Library (30), TC cost profiles |
| **Reasoning Methods** | FMEA filtering + taxonomy-based CAPEX breakdown + LCOH formula |
| **Strengths** | Multi-dimensional output. Technology-differentiated. FOAK-aware. |
| **Limitations** | Risk costs not scaled to project size. No Monte Carlo. LCOH uses Class D OPEX proxies. |
| **Unused Potential** | OPEX Library would upgrade LCOH. Risk cost scaling would enable risk-adjusted CAPEX. Monte Carlo would provide probabilistic ranges. |

## Agent 4 — PM Review

| Dimension | Detail |
|-----------|--------|
| **Implementation** | ✅ Fully implemented in pm_review_engine.py + executive_insights_engine.py |
| **Inputs** | All Agent 1-3 outputs |
| **Outputs** | Gate outcome, dimension scores, gaps, conditions, decision rationale, 5 insights |
| **Knowledge Sources** | Upstream agent outputs, evidence quality calculations |
| **Reasoning Methods** | Evidence quality scoring, cross-dimension consistency check, confidence calibration |
| **Strengths** | Deterministic, transparent, condition-generation. Insight generation automates 80% of a PM review. |
| **Limitations** | Contradiction detection not integrated. Memory layer not persisted. No escalation for cross-agent disagreements. |
| **Unused Potential** | Contradiction detection algorithm exists (framework) but not called. Memory layer would provide multi-session learning. |

## Cross-Agent Capabilities

| Capability | Exists? | Used? | UI Visible? |
|-----------|---------|-------|-------------|
| Project matching | ✅ | ✅ | ✅ 03_Reference_Projects.py |
| Score breakdown | ✅ | ✅ | ✅ 03 (project cards) |
| Technology comparison | ✅ | ✅ | ✅ 09_Technology_Comparison.py |
| Risk heatmap (5x5) | ✅ | ✅ | ✅ 05_Risk_Assessment.py |
| Risk consequence analysis | ✅ | ✅ | ✅ 05 (register table) |
| CAPEX breakdown chart | ✅ | ✅ | ✅ 06_CAPEX_LCOH.py |
| LCOH waterfall chart | ✅ | ✅ | ✅ 06_CAPEX_LCOH.py |
| Tornado sensitivity | ✅ | ✅ | ✅ 06 (bar chart) |
| Executive insights | ✅ | ✅ | ✅ 02_Assessment_Report.py |
| Gate justification (pros/cons) | ✅ | ✅ | ✅ 02_Assessment_Report.py |
| Next action generation | ✅ | ✅ | ✅ 02_Assessment_Report.py |
| Assessment snapshot | ✅ | ✅ | ✅ 02_Assessment_Report.py |
| Agent trace timeline | ✅ | ✅ | ✅ 07_Agent_Trace.py |
| PDF report export | ✅ | ✅ | ✅ 02 (download button) |
| Assessment history | ✅ | ✅ | ✅ 08_Assessment_History.py |
| Contradiction detection | ⚠️ Designed | ❌ Not integrated | ❌ Not shown |
| Memory persistence | ⚠️ Designed | ❌ Not integrated | ❌ Not shown |
| OPEX Library | ❌ Not built | — | — |
| Technology score breakdown | ✅ | ✅ | ✅ 03_Reference_Projects.py |
| OEM/developer indexing | ⚠️ Partial | ❌ Not queried | ❌ Not shown |

## Key Finding

**All 4 agents are fully implemented and integrated.** No agent is purely "designed" — every planned agent exists in code. The gap is not in agent creation but in:

1. **Data population** (OPEX, regional multipliers, memory persistence)
2. **Advanced reasoning** (contradiction detection, Monte Carlo)
3. **UI exposure** (contradiction detection results, OEM/developer filtering)
