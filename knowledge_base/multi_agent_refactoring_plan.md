# Multi-Agent Refactoring Plan — M10A

**Document:** Migration Strategy from Integrated Agent to Multi-Agent Architecture
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Current State:** Single integrated Preliminary Feasibility Agent (M9)
**Target State:** Four-agent architecture with PM Review gate

---

## 1. Migration Overview

### 1.1 The Migration in One Diagram

```
CURRENT (M9)                          FUTURE (M10A)

Preliminary Feasibility Agent         Agent 1: Knowledge Retrieval
├── Query Normalizer          →       ├── Query Normalizer
├── P1: Project Matching      →       ├── Project Matching Engine
├── P2: Technology Assessment →       ├── Technology Card Lookup
├── P3: Risk Assessment       →       └── Source Aggregation
├── P4: Cost Assessment       →
├── Evidence Aggregator       →       Agent 2: Technical Assessment
└── Report Composer           →       ├── Technology Suitability
                                       ├── Scale Assessment
                                       ├── Performance Analysis
                                       └── Reference Comparison

                                      Agent 3: Risk & Economic Assessment
                                      ├── Risk Filtering & Scoring
                                      ├── CAPEX Estimation
                                      ├── OPEX Estimation (new)
                                      └── LCOH Assessment (new)

                                      Agent 4: PM Review
                                      ├── Evidence Quality Gates
                                      ├── Cross-Dimension Consistency
                                      ├── Gap Prioritization
                                      └── Gate Review Report
```

### 1.2 What Moves Where

| Current Component (M9) | Future Agent | Change |
|------------------------|-------------|--------|
| Query Normalizer | Agent 1 | Promoted — becomes Agent 1's entry point |
| P1 — Project Matching | Agent 1 | Extracted — becomes Agent 1's core capability |
| P2 — Technology Assessment | Agent 2 | Extracted — becomes Agent 2's core capability |
| P3 — Risk Assessment | Agent 3 (Risk sub-module) | Extracted — enhanced with residual risk scoring |
| P4 — Cost Assessment | Agent 3 (Cost sub-module) | Extracted — enhanced with OPEX/LCOH integration |
| Evidence Aggregator | Agent 4 | Transformed — from mechanical collection to quality judgment |
| Report Composer | Agent 4 | Transformed — from template fill to gate review report |

### 1.3 What Is NEW

| Capability | Owner Agent | Status |
|-----------|------------|--------|
| OPEX estimation | Agent 3 | Architecture designed (M9A); needs OPEX Library population |
| LCOH calculation | Agent 3 | Architecture designed (M9A); needs OPEX Library |
| Cross-dimension consistency check | Agent 4 | NEW — Agent 4 reviews Agent 2 and Agent 3 outputs for contradictions |
| PM Gate review methodology | Agent 4 | NEW — structured gate review per PMBOK phase-gate |
| Agent-to-agent communication | All | NEW — message passing protocol |
| Confidence calibration | Agent 4 | NEW — adjusts confidence scores based on source quality and dimension consistency |

---

## 2. Detailed Component Mapping

### 2.1 Agent 1 — Knowledge Retrieval

**Extracted from:** P1 Project Matching + Query Normalizer + Source Aggregation logic

| Current Component | Reusability | Changes Needed |
|------------------|-------------|---------------|
| Query Normalizer (industry→offtake mapping, country normalization) | **100%** — logic is fully defined, no changes | Remove from Preliminary Agent; promote to Agent 1 entry point |
| 5-dimension weighted similarity scoring | **100%** — validated across 10 test cases (M5 + M9) | None. Proven methodology. |
| Top-6 project ranking with rationale | **100%** | Add project_reference_ids[] in output for Agent 2 consumption |
| Technology Card lookup | **100%** | Add to Agent 1 scope (currently P2 logic) |
| Source aggregation (collect from retrieved items) | **80%** — collection logic reusable | Remove quality-scoring logic (moves to Agent 4) |
| Degradation handling (missing fields, no matches) | **100%** | None |

**Agent 1 Input:** `{ country, industry, technology, capacity_mw, target_cod }`
**Agent 1 Output:**
```json
{
  "similar_projects": [{ "project_id", "score", "rationale" } × 6],
  "technology_cards": ["TC-PEM-001"],
  "sources_collected": [{ "source_id", "level", "score" } × N]
}
```

### 2.2 Agent 2 — Technical Assessment

**Extracted from:** P2 Technology Assessment

| Current Component | Reusability | Changes Needed |
|------------------|-------------|---------------|
| TRL/Maturity assessment | **100%** | None. TC-PEM-001/TC-ALK-001 §maturity |
| Performance parameter retrieval | **100%** | None. TC §performance |
| Application suitability scoring | **100%** | None. TC §applications.suitability_per_application |
| Scale assessment (within/beyond proven range) | **100%** | None — logic from reasoning_logic.md §2.3 |
| Advantages/Limitations contextualization | **100%** | None |

**Agent 2 Input:** `{ technology, capacity_mw, industry, target_cod, similar_projects[] }` (projects from Agent 1)
**Agent 2 Output:**
```json
{
  "technology_verdict": {
    "trl": 8, "maturity": "early_commercial",
    "scale_status": "within_proven_range",
    "application_suitability": { "level": "high", "rationale": "..." },
    "is_foak": false
  },
  "performance_summary": { "efficiency_kwh_per_kg": 55, "stack_lifetime_hours": 65000, "output_pressure_bar": 30 },
  "key_advantages": ["..."], "key_limitations": ["..."],
  "reference_comparison": [{ "project_id", "comparison_note" }],
  "confidence": "HIGH"
}
```

### 2.3 Agent 3 — Risk & Economic Assessment

**Extracted from:** P3 Risk Assessment + P4 Cost Assessment + M9A OPEX/LCOH architecture

| Current Component | Reusability | Changes Needed |
|------------------|-------------|---------------|
| Risk filtering by technology + scale + phase | **100%** | None. Risk Library applicability fields directly support this. |
| RPN ranking + top-N selection per category | **100%** | Add residual risk scoring (P×I×D post-mitigation) |
| Mitigation evidence linking to Gold Dataset | **100%** | None |
| CAPEX record selection + scaling | **100%** | None. Cost Library + scaling_methodology proven. |
| Learning curve adjustment | **100%** | None |
| CAPEX range with confidence | **100%** | None |
| OPEX estimation | **0%** (new) | Build from M9A opex_taxonomy + Technology Card opex_breakdown. Requires OPEX Library population. |
| LCOH decomposition + sensitivity | **0%** (new) | Build from M9A lcoh_methodology + sensitivity_framework |

**Agent 3 Input:** `{ technology, capacity_mw, industry, target_cod, country, technology_verdict }` (tech verdict from Agent 2)
**Agent 3 Output:**
```json
{
  "risk_assessment": {
    "risks_by_category": { "technical": [...], "financial": [...] },
    "top_risks": [{ "risk_id", "rpn", "class", "mitigation" } × 8],
    "risk_evidence_quality": { "with_project_evidence": 6, "total": 8 }
  },
  "capex_assessment": {
    "breakdown": [{ "category", "eur_per_kw", "eur_m", "confidence" } × 8],
    "total_central": 157, "range": { "p10": 120, "p90": 210 },
    "weighted_confidence": 0.62
  },
  "opex_assessment": {
    "breakdown": [{ "category", "eur_per_kg" } × 5],
    "total_eur_per_kg": 3.05
  },
  "lcoh_assessment": {
    "central": 4.78, "range": { "p10": 3.10, "p90": 6.90 },
    "tornado": [{ "driver": "electricity", "impact": "±0.83" }],
    "dominant_driver": "electricity_price"
  },
  "confidence": "MEDIUM"
}
```

### 2.4 Agent 4 — PM Review

**Transformed from:** Evidence Aggregator + Report Composer (with significant NEW capability)

| Current Component | Reusability | Changes Needed |
|------------------|-------------|---------------|
| Source de-duplication | **100%** | None |
| Evidence quality scoring | **80%** | Enhance with cross-dimension consistency check |
| Knowledge gap detection | **80%** | Enhance with gap prioritization severity |
| Report composition | **60%** | Transform from template fill to gate review with assessment commentary |
| Cross-dimension consistency | **0%** (NEW) | Compare Agent 2 technology verdict vs Agent 3 risk profile — do they agree? |
| Gate review methodology | **0%** (NEW) | PMBOK phase-gate adapted for pre-feasibility assessment |
| Confidence calibration | **0%** (NEW) | Adjust agent confidence based on source quality and dimension agreement |

**Agent 4 Input:** `{ query, agent_1_output, agent_2_output, agent_3_output }`
**Agent 4 Output:** Full 8-section gate review report (see pm_agent_design.md)

---

## 3. Reusable Components — Consolidated View

| Component | % Reused | Origin | Destination |
|-----------|---------|--------|------------|
| Query Normalizer | 100% | Preliminary Agent | Agent 1 |
| 5-dimension similarity engine | 100% | M5 Retrieval Agent | Agent 1 |
| Technology Card query functions | 100% | Preliminary Agent P2 | Agent 1 + Agent 2 |
| Risk filtering & ranking logic | 100% | Preliminary Agent P3 | Agent 3 Risk Sub-module |
| Cost scaling with power law exponents | 100% | Preliminary Agent P4 | Agent 3 Cost Sub-module |
| Learning curve projection | 100% | Preliminary Agent P4 | Agent 3 Cost Sub-module |
| Source de-duplication | 100% | Preliminary Agent Evidence Aggregator | Agent 4 |
| Evidence quality scoring | 80% | Preliminary Agent Evidence Aggregator | Agent 4 (enhanced) |
| Knowledge gap detection | 80% | Preliminary Agent Evidence Aggregator | Agent 4 (enhanced) |
| Report template | 60% | Preliminary Agent Report Composer | Agent 4 (transformed) |

**Overall reuse: ~85% of validated logic.** The migration preserves all reasoning that was validated in the M9 5-case test.

---

## 4. Migration Roadmap — 4 Phases

### Phase 1: Extract Agent 1 (Week 1)

```
PREREQUISITE: None (Agent 1 is simplest — already a standalone service via M5)
TASKS:
  1. Promote Retrieval Agent (M5) from sub-component to standalone Agent 1
  2. Add Query Normalizer as Agent 1 entry point
  3. Add Technology Card lookup to Agent 1 scope (one extra function call)
  4. Define Agent 1 → Agent 2 output schema
  5. Test: Agent 1 independently produces project matches + tech card references
VALIDATION: Run Cases 1-5 (from M9 validation) through Agent 1 only.
           Verify top-6 projects match M9 results exactly (deterministic logic).
```

### Phase 2: Extract Agent 2 (Week 1-2)

```
PREREQUISITE: Agent 1 operational
TASKS:
  1. Extract P2 logic into standalone Agent 2
  2. Agent 2 receives technology + industry + capacity from Agent 1 output + original query
  3. Agent 2 performs: TRL assessment, scale assessment, application suitability, 
     advantages/limitations contextualization
  4. Define Agent 2 → Agent 3 output schema
  5. Test: Agent 2 independently produces technology verdict
VALIDATION: Same 5 cases. Technology verdict must match M9 P2 results.
```

### Phase 3: Extract Agent 3 (Week 2-3)

```
PREREQUISITE: Agents 1 and 2 operational
TASKS:
  1. Extract P3 (Risk) logic into Agent 3 Risk Sub-module
  2. Extract P4 (Cost) logic into Agent 3 Cost Sub-module
  3. Integrate M9A OPEX/LCOH methodology as Agent 3 LCOH Sub-module
  4. Agent 3 receives technology verdict from Agent 2 + original query
  5. Define Agent 3 → Agent 4 output schema
  6. Test: Risk + CAPEX results match M9 P3+P4 results.
     LCOH results are NEW — validate against M9A opex_lcoh_validation reference cases.
```

### Phase 4: Build & Integrate Agent 4 (Week 3-4)

```
PREREQUISITE: Agents 1, 2, 3 operational
TASKS:
  1. Build Agent 4 (PM Review) — see pm_agent_design.md
  2. Agent 4 receives all agent outputs + original query
  3. Implement cross-dimension consistency check
  4. Implement gate review methodology
  5. Implement confidence calibration
  6. Implement final report generation
  7. End-to-end integration test
VALIDATION: Full 5-case validation. Reports must be at least as informative as M9 reports.
           ADDITIONALLY: cross-dimension consistency, gate review assessment, confidence calibration.
```

---

## 5. Migration Risk Assessment Summary

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **Determinism loss** — multi-agent message passing introduces nondeterminism | HIGH | All reasoning logic is deterministic (no ML models). Agent outputs must be bit-exact matches to M9 pipeline outputs for identical inputs. |
| **OPEX/LCOH premature integration** — Agent 3 LCOH module uses unpopulated OPEX Library | MEDIUM | LCOH uses Technology Card OPEX breakdowns as proxies until OPEX Library is populated. Flag as Class D confidence. |
| **Agent 4 overreach** — PM Agent makes decisions it shouldn't | MEDIUM | Explicit boundary rules: Agent 4 reviews quality, never approves projects. Same boundary enforcement as M9. |
| **Integration complexity** — 4 agents with message passing vs 1 agent with function calls | LOW | Message schema is simple JSON. No async/non-blocking needed for current use case (all agents run sequentially on same query). |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect | Multi-agent refactoring plan |
