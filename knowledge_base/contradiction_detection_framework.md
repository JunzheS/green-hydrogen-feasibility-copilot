# Contradiction Detection Framework v1.0

**Document:** Cross-Agent Output Analysis
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Purpose:** Classify and resolve differences between agent outputs

---

## 1. Why This Matters

In a multi-agent system, agents work with different knowledge sources and reasoning methods. They WILL produce outputs that appear to conflict. The question is not whether differences occur — it's whether the system can classify, explain, and resolve them correctly.

**A system that treats every difference as a contradiction will cry wolf. A system that ignores genuine contradictions will produce inconsistent assessments.**

---

## 2. Four-Part Classification

### 2.1 Classification Matrix

| Classification | Definition | Example | Action |
|---------------|-----------|---------|--------|
| **CONTRADICTION** | Two agents assert mutually exclusive facts about the same dimension | Agent 2: "Not FOAK for scale." Agent 3: "FOAK premium applied for scale." | **ESCALATE to Agent 4 for resolution.** Record in contradiction registry. |
| **TRADE-OFF** | Two agents describe different dimensions of a multi-faceted reality | Agent 2: "PEM recommended for dynamic response." Agent 3: "PEM has higher CAPEX than Alkaline." | **NOT a contradiction.** Record as trade-off in PM review. No escalation needed. |
| **INFORMATION GAP** | One agent has data another lacks; outputs differ because knowledge bases differ | Agent 2: TC-PEM-001 rates steel suitability HIGH. Agent 3: No steel-offtake project evidence for risk assessment. | **NOT a contradiction.** Flag as knowledge gap. Prioritize for data collection. |
| **ESCALATION REQUIRED** | Agents disagree on a material fact that affects the gate outcome | Agent 2: "FOAK for application only." Agent 3: "Applied FOAK premium to BOTH scale and application (double-counted)." | **ESCALATE to Agent 4 for immediate resolution.** Gate decision deferred pending resolution. |

---

## 3. Detection Rules

### 3.1 Cross-Dimension Comparison Pairs

Agent 4 systematically compares these output pairs:

| Pair | Check | Contradiction If... | Trade-Off If... |
|------|-------|--------------------|--------------------|
| **A2.FOAK vs A3.FOAK_premium** | Does Agent 3's FOAK premium scope match Agent 2's FOAK determination? | A2 says "not FOAK for scale" AND A3 applies FOAK premium to scale cost categories | A2 says "FOAK for application" AND A3 applies FOAK premium to application-related costs |
| **A2.suitability vs A3.risk_profile** | Does the risk profile reflect the suitability rating? | A2 says "HIGH suitability" AND A3 identifies 5 HIGH probability risks for this application | A2 says "HIGH suitability" AND A3 identifies 2-3 MEDIUM risks — normal for any project |
| **A1.references vs A3.risk_evidence** | Are the reference projects cited as risk evidence? | A1 returns 6 projects AND A3 says "no project evidence for top risks" | A1 returns 6 projects AND A3's risk evidence is from 3 different projects (Agent 1 ranked them lower) |
| **A2.scale_status vs A3.capex_scale** | Are scaling adjustments consistent with scale assessment? | A2 says "beyond proven scale" AND A3 applies NO FOAK premium | A2 says "within proven scale" AND A3 applies standard nth-of-a-kind scaling |
| **A3.capex vs A3.lcoh** | Is the CAPEX contribution to LCOH internally consistent? | CAPEX annualized ≠ CRF × CAPEX_total within ±10% | Minor rounding differences |
| **A2.purity vs A3.purification_cost** | Is purification cost consistent with purity assessment? | A2 says "PEM 99.99% purity native" AND A3 includes €50/kW deoxo purification cost | A2 says "PEM 99.99% purity" AND A3 includes €20/kW TSA drying only (consistent — drying is separate from purification) |

### 3.2 Detection Algorithm

```
Agent 4 loads Agent 1, 2, 3 memories
FOR each comparison pair in §3.1:
  EXTRACT values from agent memories
  COMPARE values using pair-specific logic
  CLASSIFY using the 4-part matrix
  RECORD in contradiction registry
  
IF any CONTRADICTION or ESCALATION_REQUIRED:
  FLAG gate outcome for review
  DO NOT auto-resolve — present to human PM
  
IF only TRADE-OFF and INFORMATION_GAP:
  NOTE in PM review
  Proceed with gate assessment
```

---

## 4. Worked Examples

### Example A: FOAK Scope Disagreement (Classification: TRADE-OFF)

```
AGENT 2 MEMORY:
  DEC-A2-002: "Scale status: WITHIN proven range (max 200 MW under construction). FOAK for scale: FALSE."
  DEC-A2-004: "FOAK for APPLICATION: TRUE. No PEM plant has supplied DRI steel furnace."

AGENT 3 MEMORY:
  DEC-A3-009: "FOAK adjustment: +5% contingency for steel application novelty (per Agent 2 FOAK finding)."

ANALYSIS:
  Agent 2 says: Not FOAK for SCALE, but FOAK for APPLICATION.
  Agent 3 says: Applied FOAK premium for APPLICATION only.
  
  VERDICT: TRADE-OFF. Both agents agree on the facts. Agent 2 decomposed FOAK into 
  scale + application dimensions. Agent 3 applied the FOAK premium to the correct dimension
  (application, not scale). No contradiction.

RECORDED AS: CTR-A2A3-001 — TRADE-OFF. FOAK scope correctly differentiated by both agents.
```

### Example B: Double-Counted FOAK (Classification: CONTRADICTION)

```
AGENT 2 MEMORY:
  DEC-A2-002: "Scale status: WITHIN proven range. FOAK for scale: FALSE."

AGENT 3 MEMORY:
  DEC-A3-009: "FOAK adjustment: +5% contingency for FOAK scale AND +5% for steel application novelty."

ANALYSIS:
  Agent 2 says: NOT FOAK for scale.
  Agent 3 says: Applied FOAK premium for scale (+5%) AND application (+5%).
  
  VERDICT: CONTRADICTION. Agent 3 has applied a FOAK premium for scale that Agent 2 
  explicitly determined is not applicable. Total FOAK premium is double-counted.

RECORDED AS: CTR-A2A3-002 — CONTRADICTION. Agent 3 applied scale FOAK premium despite 
Agent 2 determining scale is within proven range.

RESOLUTION: Agent 4 flags this. Corrected CAPEX removes +5% scale FOAK. 
Recalculated total: €150M (was €157M).
```

### Example C: Technology Recommendation vs. Cost Penalty (Classification: TRADE-OFF)

```
AGENT 2 MEMORY:
  DEC-A2-003: "PEM suitability for mobility: HIGH (purity, pressure, dynamics)."

AGENT 3 MEMORY:
  DEC-A3-011: "PEM LCOH is €0.18/kg higher than Alkaline at this scale."

ANALYSIS:
  Agent 2 says: PEM is technically well-suited.
  Agent 3 says: PEM costs more.
  
  VERDICT: TRADE-OFF. These are different dimensions of a project decision.
  Technology suitability is not the same as economic optimality. Many projects
  knowingly pay a premium for technical advantages (purity, dynamics, smaller footprint).
  
  This is the single most common "apparent contradiction" in pre-feasibility assessments.
  It is NEVER a contradiction — it's a design trade-off that the project team must resolve.

RECORDED AS: CTR-A2A3-003 — TRADE-OFF. Technical suitability vs. cost. 
Standard multi-dimensional project trade-off.
```

### Example D: Missing Risk Evidence (Classification: INFORMATION GAP)

```
AGENT 1 MEMORY:
  DEC-A1-002 through A1-007: "Top 6 projects: Normand'Hy (refinery), REFHYNE II (refinery), 
  Galp Sines (refinery), Masshylia (refinery), Puertollano (ammonia), HGHH (industrial_heat)."

AGENT 3 MEMORY:
  DEC-A3-001: "RK-FIN-002 Offtake Risk (RPN 30). No project evidence for steel offtake."

ANALYSIS:
  Agent 1 says: 6 projects retrieved, none with steel offtake.
  Agent 3 says: No project evidence for steel offtake risk.
  
  VERDICT: INFORMATION GAP. Both agents correctly identify the same absence.
  The Gold Dataset has no steel-offtake project. This is a knowledge base limitation,
  not an agent error.

RECORDED AS: GAP-A1A3-001 — INFORMATION GAP. Steel offtake not represented in Gold Dataset.
```

---

## 5. Contradiction Registry Format

```json
{
  "contradiction_id": "CTR-{session_date}-NNN",
  "session_id": "SES-YYYYMMDD-NNNN",
  "agents_involved": ["Agent 2", "Agent 3"],
  "classification": "contradiction | trade_off | information_gap | escalation_required",
  "description": "Agent 2 determined scale is within proven range. Agent 3 applied FOAK scale premium.",
  "agent_2_position": { "memory_ref": "MEM-A2 DEC-A2-002", "value": "FOAK for scale: FALSE" },
  "agent_3_position": { "memory_ref": "MEM-A3 DEC-A3-009", "value": "FOAK scale premium: +5%" },
  "resolution": "Agent 4 removed scale FOAK premium. CAPEX recalculated.",
  "resolved_by": "Agent 4",
  "resolved_at": "2026-06-05T14:30:30Z",
  "material_impact": "CAPEX reduced from €157M to €150M (−4.5%)"
}
```

---

## 6. Escalation Thresholds

| Condition | Escalation Level | Action |
|-----------|-----------------|--------|
| **Any CONTRADICTION found** | Gate Review | Agent 4 must resolve before gate decision. Resolution recorded in contradiction registry. |
| **CONTRADICTION affecting >5% of CAPEX or >2 risk classes** | Human Review | Agent 4 cannot auto-resolve. Flag for PM review with both agent positions presented. |
| **ESCALATION REQUIRED** | Immediate | Gate decision deferred. Both agent outputs preserved. Human PM must decide. |
| **>3 TRADE-OFFS on same dimension** | Gate Review | Agent 4 notes pattern. May indicate a poorly defined dimension that needs schema refinement. |
| **INFORMATION GAP on a critical dimension** | Gate Review | Gap included in gate conditions. Does not block PROCEED WITH CAUTION. |

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect |
