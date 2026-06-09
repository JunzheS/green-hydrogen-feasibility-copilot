# Agent Memory Contracts — Per-Agent Memory Specification

**Document:** Memory Interface Contracts for Each Agent
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Schema:** agent_memory_schema_v1.json

---

## 1. Memory Contract Summary

| Agent | Memory File | Writes | Reads | Key Decisions Recorded |
|-------|-----------|--------|-------|----------------------|
| Agent 1 | `mem_a1_retrieval.json` | Self only | None | Project ranking, technology card selection, source collection |
| Agent 2 | `mem_a2_technical.json` | Self only | MEM-A1 (read) | TRL verdict, application suitability, FOAK determination |
| Agent 3 | `mem_a3_risk_economic.json` | Self only | MEM-A1, MEM-A2 (read) | Risk ranking, CAPEX estimate, LCOH decomposition |
| Agent 4 | `mem_a4_pm_review.json` | Self + annotations on A1-A3 | MEM-A1, A2, A3 (read) | Gate outcome, confidence calibration, consistency verdict |

---

## 2. Agent 1 — Knowledge Retrieval Memory

### MEM-A1: `mem_a1_retrieval.json`

```
Memory ID:      MEM-{session_date}-A1
Agent:           Agent 1 — Knowledge Retrieval
Assessment:      project_matching
Input:           User query (normalized by Orchestrator)
Output artifact: mem_a1_retrieval.json

────────────────────────────────────────────────────────
DECISIONS RECORDED
────────────────────────────────────────────────────────

DEC-A1-001: NORMALIZATION
  Statement: Industry "Steel" → offtake "steel"
  Evidence:  industry-to-offtake mapping (agent_interface_specification.md §4.2)
  Alternative considered: "Steel" could have been mapped to "industrial_heat"
  Why this choice: Direct match exists in offtake enum

DEC-A1-002 through DEC-A1-007: PROJECT RANKING (6 decisions)
  For each of top 6 projects:
    DEC-A1-00X: "Project GA-PR-001 ranked #1 with score 0.81"
    Component scores: Tech=1.00, Industry=0.40, Capacity=0.85, Country=1.00, Maturity=1.00
    Rationale: "Same country, same tech, closest scale above query"

DEC-A1-008: TECHNOLOGY CARD SELECTION
  Statement: "TC-PEM-001 selected. TC-ALK-001 not retrieved (query specifies PEM)."
  Evidence:  Query.technology = "PEM"

DEC-A1-009: SOURCE COLLECTION
  Statement: "21 unique sources collected from 6 projects + 1 technology card"
  Level distribution: A=6, B=12, C=3

────────────────────────────────────────────────────────
ASSUMPTIONS (3-6 per Agent 1 execution)
────────────────────────────────────────────────────────

ASM-A1-001: Industry cross-reference
  "Steel offtake is cross-referenced to refinery/ammonia projects via industrial process group"
  Impact if wrong: MEDIUM — steel-specific projects would be ranked lower

ASM-A1-002: Capacity factor not used
  "Capacity similarity uses nameplate MW, not effective output"
  Impact if wrong: LOW — effective output depends on renewable profile not yet assessed

ASM-A1-003: Country neighbor classification
  "France-Germany classified as neighbor (shared border, score 0.70)"
  Basis: Country neighbor matrix (project_matching_methodology.md §6)

────────────────────────────────────────────────────────
CONFIDENCE
────────────────────────────────────────────────────────

Self-assessed: 0.64 (GOOD)
Limiting factor: No steel-offtake project → industry scores capped at 0.40 for all projects

────────────────────────────────────────────────────────
WARNINGS (1-3 per execution)
────────────────────────────────────────────────────────

WRN-A1-001: [HIGH] "No steel-offtake project in Gold Dataset. Industry match is via cross-reference."
WRN-A1-002: [LOW] "Target COD 2029 — all reference projects are under construction or planned."
```

---

## 3. Agent 2 — Technical Assessment Memory

### MEM-A2: `mem_a2_technical.json`

```
Memory ID:      MEM-{session_date}-A2
Agent:           Agent 2 — Technical Assessment
Assessment:      technology_assessment
Input:           Query + Agent 1 output (similar_projects[], technology_cards_retrieved[])
Reads:           MEM-A1 (similar projects, normalized query)
Output artifact: mem_a2_technical.json

────────────────────────────────────────────────────────
DECISIONS RECORDED
────────────────────────────────────────────────────────

DEC-A2-001: TRL ASSESSMENT
  Statement: "PEM TRL 8 — early commercial. Deployed at >100 MW scale."
  Evidence:  TC-PEM-001 §maturity (TRL 8, cumulative 4.5 GW)
  Reference: Normand'Hy 200 MW (GA-PR-001) — under construction since 2023

DEC-A2-002: SCALE STATUS
  Statement: "100 MW is WITHIN proven PEM range (max 200 MW under construction)"
  Evidence:  TC-PEM-001 §deployment_evidence (max under construction: 200 MW)
  FOAK for scale: FALSE

DEC-A2-003: APPLICATION SUITABILITY
  Statement: "PEM suitability for steel: HIGH"
  Evidence:  TC-PEM-001 §applications.suitability_per_application[steel]
  Rationale: "Pressurized output (30 bar) matches DRI pressure (10-20 bar); high purity eliminates purification"

DEC-A2-004: FOAK DETERMINATION
  Statement: "FOAK for APPLICATION (not scale). No PEM plant has supplied a DRI steel furnace."
  Evidence:  Negative — no steel-offtake PEM project in Gold Dataset
  Alternative: Agent 1 reference projects are refinery/ammonia, not steel

DEC-A2-005: PERFORMANCE RELEVANCE
  Statement: "PEM 30 bar output matches DRI pressure requirement — eliminates first compression stage"
  Evidence:  TC-PEM-001 §performance (output pressure 30 bar)

────────────────────────────────────────────────────────
ASSUMPTIONS
────────────────────────────────────────────────────────

ASM-A2-001: DRI pressure assumption
  "DRI shaft furnace requires 10-20 bar H₂ inlet pressure"
  Impact if wrong: LOW — PEM at 30 bar still sufficient; just less advantageous

ASM-A2-002: Baseload operation
  "Steel DRI operates baseload (24/7). PEM dynamic capability less valued."
  Impact if wrong: LOW — doesn't change suitability rating

────────────────────────────────────────────────────────
CONFIDENCE
────────────────────────────────────────────────────────

Self-assessed: 0.68 (GOOD)
Limiting factor: Application suitability based on technical characteristics, not operational evidence (no steel PEM reference exists)

────────────────────────────────────────────────────────
CONTRADICTIONS DETECTED (by Agent 2 during self-review)
────────────────────────────────────────────────────────

None at this stage. Agent 2 does not see Agent 3's outputs yet.
```

---

## 4. Agent 3 — Risk & Economic Assessment Memory

### MEM-A3: `mem_a3_risk_economic.json`

```
Memory ID:      MEM-{session_date}-A3
Agent:           Agent 3 — Risk & Economic Assessment
Assessment:      risk_economic_assessment
Input:           Query + Agent 2 output (technology_verdict)
Reads:           MEM-A1, MEM-A2
Output artifact: mem_a3_risk_economic.json

────────────────────────────────────────────────────────
DECISIONS RECORDED
────────────────────────────────────────────────────────

DEC-A3-001 through DEC-A3-008: RISK SELECTION (1 per category)
  DEC-A3-001: "RK-FIN-002 Offtake Risk selected as top Financial risk (RPN 30)"
    Why: Steel offtake novelty (per Agent 2 FOAK finding). No operational reference.
    Evidence: RK-FIN-002 §assessment; Agent 2 FOAK determination

  DEC-A3-002: "RK-REG-003 Subsidy Dependency selected (RPN 30)"
    Why: French 2027 election cycle; Masshylia (GA-PR-002) precedent
    Evidence: RK-REG-003 §evidence

DEC-A3-009: CAPEX CENTRAL ESTIMATE
  Statement: "Total CAPEX central: €1,570/kW → €157M for 100 MW"
  Method: Bottom-up from 8 cost categories, scaled from 100 MW benchmarks
  Evidence: CS-ELC-001..006, CS-ELI-001..002, CS-HPR-001, CS-CIV-003, CS-IND-001..004
  Range: P10 €1,200/kW (€120M) — P90 €2,100/kW (€210M)
  AACE Class: 4 (feasibility, ±20-30%)
  FOAK adjustment: +5% contingency for steel application novelty (per Agent 2)

DEC-A3-010: LCOH CENTRAL ESTIMATE
  Statement: "LCOH central: €4.78/kg"
  Decomposition: Electricity 46%, CAPEX 36%, Other OPEX 18%
  Dominant driver: Electricity price (tornado ±€0.83/kg per ±€15/MWh)
  Data quality note: "OPEX uses Technology Card proxies (Class C). OPEX Library not populated."
```

---

## 5. Agent 4 — PM Review Memory (Abbreviated)

See `pm_memory_review_framework.md` for complete specification.
