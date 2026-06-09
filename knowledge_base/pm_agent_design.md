# PM Agent Design — Project Manager Review Agent v1.0

**Document:** Agent Design Specification
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect & PMO Lead
**Agent:** Agent 4 — PM Review (the "Gatekeeper")

---

## 1. Agent Identity

### 1.1 Who Is Agent 4?

The PM Review Agent is the **quality gate** of the multi-agent system. It does not perform original research or generate new assessments — it reviews, validates, and integrates the outputs of Agents 1-3. It acts like a **senior project manager reviewing work prepared by junior consultants.**

```
Agent 1 (Junior Consultant — Research):
  "Here are 6 similar projects, ranked by relevance."

Agent 2 (Junior Consultant — Technical):
  "Here's the technology assessment. PEM is suitable, TRL 8, 100 MW is within range."

Agent 3 (Junior Consultant — Risk & Cost):
  "Here are the top 8 risks. CAPEX range is €120-210M. LCOH is €3.10-6.90/kg."

Agent 4 (Senior PM — Review):
  "Agent 2 says technology is proven but Agent 3 identifies steel offtake novelty as a risk — 
   cross-check: does the technology verdict account for application novelty? (YES, flagged as 
   FOAK for application). Evidence quality is GOOD for technology but ADEQUATE for economics — 
   I'm downgrading overall confidence. I see 3 critical gaps. My recommendation: PROCEED WITH 
   CAUTION — resolve steel offtake risk before advancing to feasibility."
```

### 1.2 What Agent 4 DOES

| ✅ | Description |
|----|-------------|
| Review Agent 1-3 outputs for completeness and consistency |
| Cross-check dimensions for contradictions |
| Evaluate evidence quality per dimension |
| Identify and prioritize knowledge gaps |
| Calibrate confidence based on evidence quality and dimension agreement |
| Determine project maturity (readiness for next phase) |
| Generate gate review report with conditions for advancement |
| Flag when agents disagree and request human review |

### 1.3 What Agent 4 DOES NOT Do

| ❌ | Why Not |
|----|---------|
| Approve or reject projects | Gate recommendation is "conditions for approval", not approval itself |
| Override Agent 1-3 technical judgments | Agent 4 reviews quality, not substance |
| Fill knowledge gaps | Agent 4 identifies gaps; does not invent data to fill them |
| Make investment decisions | Decision authority is with human project governance |

---

## 2. Review Methodology

### 2.1 The Four-Dimension Review

Agent 4 reviews the output of each upstream agent across three criteria and one cross-cutting dimension:

```
                Completeness    Consistency    Source Quality
Agent 1 Output      ✓               ✓               ✓
Agent 2 Output      ✓               ✓               ✓
Agent 3 Output      ✓               ✓               ✓
                              ↓
                    CROSS-DIMENSION CONSISTENCY
                    (Do Agent 1, 2, 3 agree?)
```

### 2.2 Completeness Check

For each agent output, verify all mandatory fields are present:

| Agent | Check | Fail Condition | Action |
|-------|-------|---------------|--------|
| Agent 1 | ≥3 similar projects returned | <3 projects with score ≥0.30 | Flag "narrow reference base" gap |
| Agent 1 | Technology Card retrieved | No card found for specified technology | Error — cannot proceed |
| Agent 2 | Application suitability assessed | Industry not in suitability_per_application | Flag "unassessed application" gap |
| Agent 2 | Scale assessment complete | scale_status not set | Flag "scale assessment missing" |
| Agent 3 | ≥1 risk per category | Any category empty | Flag "risk coverage gap" |
| Agent 3 | CAPEX total with range | Missing p10 or p90 | Flag "incomplete CAPEX" |
| Agent 3 | LCOH decomposition | Missing decomposition | Flag "LCOH not decomposed" |

### 2.3 Consistency Check

Cross-check Agent outputs for contradictions:

| Check | Compare | Contradiction Example | Action |
|-------|---------|----------------------|--------|
| **Technology vs Risk** | Agent 2: "TRL 8, proven at scale" ↔ Agent 3 risk assessment includes RK-TEC-001 (PEM degradation) | No contradiction — both correct. But check: does Agent 3's risk assessment appropriately reflect Agent 2's FOAK flags? | If Agent 2 says "not FOAK" but Agent 3 applies FOAK premium → flag inconsistency |
| **Technology vs Cost** | Agent 2: "within proven scale" ↔ Agent 3 CAPEX applies FOAK premium | If Agent 2 says "within proven scale" AND Agent 3 applies FOAK cost premium → inconsistency | Flag: "Agent 2 and 3 disagree on FOAK status" |
| **Projects vs Risks** | Agent 1 projects have risk evidence ↔ Agent 3 risk assessment claims "no project evidence" | If Agent 1 returns projects where a risk materialized, but Agent 3 says no evidence → inconsistency | Flag: "Risk evidence exists in Gold Dataset but not cited" |
| **Cost vs LCOH** | Agent 3 CAPEX contribution to LCOH ↔ Agent 3 LCOH decomposition CAPEX share | Should agree within ±10% | Flag if mismatch >10% |
| **Scale self-consistency** | Agent 1 project scales ↔ Agent 2 scale assessment | Agent 1's top project is 200 MW; Agent 2 says "300 MW within proven range" | Flag if Agent 2 scale assessment contradicts Agent 1 reference projects |

### 2.4 Evidence Quality Calibration

Agent 4 recalculates evidence quality with an **inter-dimension adjustment**:

```
Base_Evidence_Score = Σ(source_level_weight × reliability) / count  [from Agent 1]
Adjusted_Score = Base_Evidence_Score × Consistency_Factor

Consistency_Factor:
  1.00 = All dimensions consistent (no contradictions found)
  0.85 = Minor inconsistencies (1-2 non-material contradictions)
  0.70 = Moderate inconsistencies (3+ contradictions OR 1 material)
  0.50 = Major inconsistency (Agent outputs fundamentally disagree → flag for human review)
```

---

## 3. Gate Review Methodology

### 3.1 PMBOK Phase-Gate Adaptation

The PM Agent applies a pre-feasibility gate review per PMBOK principles:

```
GATE 1 — PRE-FEASIBILITY ASSESSMENT

Gate Question: "Is there sufficient information to proceed to feasibility study?"

Assessment Dimensions:
  D1 — Project References: Are there credible reference projects?
  D2 — Technology: Is the technology proven for this application and scale?
  D3 — Risk: Are key risks identified and understood?
  D4 — Economics: Is the indicative CAPEX/LCOH range acceptable?

Gate Outcomes:
  ✅ PROCEED — All dimensions GOOD or better; no critical gaps
  ⚠️ PROCEED WITH CAUTION — Most dimensions GOOD; 1-2 critical gaps identified
  ❌ DO NOT PROCEED — Multiple dimensions INADEQUATE; >3 critical gaps
  🔄 INSUFFICIENT DATA — Cannot assess ≥2 dimensions (knowledge base too sparse)
```

### 3.2 Dimension Scoring Rubric

| Score | Criteria |
|-------|----------|
| **GOOD** | Evidence quality ≥0.60, ≥3 relevant references, dimension internally consistent |
| **ADEQUATE** | Evidence quality 0.40-0.59, 1-2 relevant references, minor inconsistencies |
| **INADEQUATE** | Evidence quality <0.40, no relevant references, major gaps |
| **NOT ASSESSED** | Agent did not produce output for this dimension |

### 3.3 Conditions for Advancement

If the gate outcome is PROCEED WITH CAUTION, Agent 4 generates specific, actionable conditions:

```
Example:
  □ COND-001: Resolve steel offtake application risk through:
    - Engage at least 1 steelmaker for offtake term sheet
    - Commission technology qualification study for PEM→DRI integration
  □ COND-002: Upgrade cost confidence:
    - Obtain OEM indicative stack quotation (Siemens Energy or ITM Power)
    - This upgrades CAPEX from Class C to Class B for the electrolyzer category
  □ COND-003: Close knowledge base gaps:
    - Add at least 1 operational PEM project >50 MW to Gold Dataset when available
```

---

## 4. Confidence Calibration Logic

### 4.1 Agent 4 Override Rules

Agent 4 may override individual agent confidence levels:

| Condition | Override |
|-----------|----------|
| Agent claims HIGH confidence but has <3 independent sources | Downgrade to MEDIUM |
| Agent claims HIGH confidence but cross-dimension inconsistency found | Downgrade to MEDIUM |
| Agent claims LOW confidence but other agents' outputs corroborate | Upgrade to MEDIUM (with note) |
| Critical knowledge gap exists in the agent's dimension | Cap confidence at MEDIUM regardless of agent's self-assessment |

### 4.2 Overall Project Confidence

```
Overall_Confidence = MIN(
  Agent_1_Adjusted_Confidence,
  Agent_2_Adjusted_Confidence,
  Agent_3_Adjusted_Confidence
) × Cross_Dimension_Factor
```

The weakest dimension determines the ceiling. A project with GOOD technology and GOOD references but INADEQUATE economics cannot have HIGH overall confidence.

---

## 5. Gate Review Report Structure

The PM Agent produces the final 8-section report (inheriting the M9 template) with these PM-specific additions:

### §0 — Gate Review Summary (NEW)

```
GATE: Pre-Feasibility Assessment
GATE OUTCOME: ⚠️ PROCEED WITH CAUTION
OVERALL CONFIDENCE: MEDIUM

DIMENSION REVIEW:
  D1 Project References:  ✅ GOOD (0.64)
  D2 Technology:           ✅ GOOD (0.68)
  D3 Risk:                 ⚠️ ADEQUATE (0.58)
  D4 Economics:            ⚠️ ADEQUATE (0.52)

CONSISTENCY: No contradictions found across agent outputs.

CRITICAL GAPS (3):
  1. No steel-offtake PEM reference in Gold Dataset
  2. No Class A/B cost data (all industry benchmarks)
  3. OPEX Library not populated — LCOH uses proxy data

CONDITIONS FOR ADVANCEMENT (3):
  □ COND-001: Resolve steel offtake application risk
  □ COND-002: Obtain OEM indicative stack quotation
  □ COND-003: Monitor Normand'Hy commissioning (2026) for operational PEM cost data
```

### §1-§8: Standard report sections (inherited from M9 template), with PM annotations where Agents disagree or gaps exist.

---

## 6. Escalation Rules

| Situation | Agent 4 Action |
|-----------|---------------|
| Two agents produce contradictory outputs on a material fact | Flag as "CONSISTENCY ISSUE — HUMAN REVIEW REQUIRED". Do not resolve automatically. |
| All three agents return HIGH confidence | Gate = PROCEED. Report ready for stakeholder review. |
| Any agent returns INSUFFICIENT DATA error | Gate = INSUFFICIENT DATA. Generate focused data collection plan. |
| Critical risk identified (RPN ≥81) | Flag in Gate Summary. If combined with ADEQUATE+ evidence, may still PROCEED WITH CAUTION. |
| Knowledge base completely empty for a dimension | Gate = INSUFFICIENT DATA. Prioritize knowledge base population. |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect & PMO Lead | PM Agent design |
