# PM Memory Review Framework — Agent 4 Integration

**Document:** PM Agent Memory Review Methodology
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect & PMO Lead
**Agent:** Agent 4 — PM Review
**Reads:** MEM-A1, MEM-A2, MEM-A3 (immutable, read-only)
**Writes:** MEM-A4 + annotations on upstream memories

---

## 1. PM Agent Memory Responsibilities

### 1.1 What Agent 4 Reviews

Agent 4 reviews BOTH the agent outputs (from agent_interface_specification.md) AND the agent memories (from agent_memory_interfaces.md). The combination is essential — the output tells WHAT was concluded; the memory tells WHY.

```
Agent Output:  "PEM suitability for steel: HIGH"       ← WHAT
Agent Memory:  "Evidence: TC-PEM-001 §applications.     ← WHY
                Assumption: DRI pressure 10-20 bar.     
                Confidence: 0.68 (GOOD).                
                Limiting factor: No operational steel    
                PEM reference."                         
```

### 1.2 The Four Review Questions

Agent 4 answers these four questions for every agent, every session:

| Q | Question | Memory Sources |
|---|----------|---------------|
| **Q1** | **What evidence supports this conclusion?** | `knowledge_sources_used` + `evidence_ids` |
| **Q2** | **What assumptions are weak?** | `assumptions[]` (filtered for HIGH impact_if_wrong) |
| **Q3** | **What conflicts exist?** | `contradictions_detected[]` + cross-agent comparison |
| **Q4** | **What confidence level is justified?** | `confidence` (self-assessed) vs. Agent 4 calibration |

---

## 2. Review Methodology

### 2.1 Step 1 — Evidence Audit

```
FOR each memory (MEM-A1, A2, A3):
  COUNT evidence_ids
  CLASSIFY by level (A/B/C/D)
  IDENTIFY decisions with <2 evidence citations
  IDENTIFY decisions relying solely on Class D evidence
  FLAG as EVIDENCE GAP if any decision lacks adequate support

OUTPUT → final_review_memory.evidence_audit
```

**Example finding:**
```
EVIDENCE GAP [MEM-A3 DEC-A3-010]:
  LCOH central estimate uses Technology Card OPEX proxies (Class C).
  OPEX Library not populated. No Class A or B OPEX data exists.
  → Agent 4 annotation: "LCOH confidence capped at LOW. Class D estimate."
```

### 2.2 Step 2 — Assumption Stress Test

```
FOR each memory:
  IDENTIFY assumptions where impact_if_wrong ≥ HIGH
  FOR each HIGH-impact assumption:
    CHECK: Is the assumption validated by another agent?
    CHECK: Would the conclusion change if the assumption were wrong?
    RATE: assumption robustness (ROBUST / SENSITIVE / CRITICAL)

OUTPUT → final_review_memory.assumption_stress_test
```

**Example finding:**
```
CRITICAL ASSUMPTION [MEM-A3 ASM-A3-001]:
  "Electricity price: €40/MWh" — impact_if_wrong: HIGH (±€0.83/kg LCOH).
  NOT validated by any other agent.
  LCOH changes from €4.78 → €5.33/kg if electricity is €50/MWh.
  → Agent 4 annotation: "SENSITIVITY ANALYSIS REQUIRED for electricity price."
```

### 2.3 Step 3 — Conflict Resolution

See contradiction_detection_framework.md for the complete methodology. Agent 4 executes the detection algorithm and resolves or escalates.

### 2.4 Step 4 — Confidence Calibration

```
FOR each agent:
  CALIBRATED = Agent.self_assessed × Consistency_Factor × Source_Quality_Factor

  Consistency_Factor:
    1.00 = No contradictions with other agents
    0.85 = Minor inconsistencies with other agents
    0.70 = Material inconsistency (corrected by Agent 4)

  Source_Quality_Factor:
    1.00 = ≥70% Level A+B sources
    0.85 = 50-69% Level A+B
    0.70 = <50% Level A+B

FINAL overall_confidence = MIN(calibrated_A1, calibrated_A2, calibrated_A3)
```

---

## 3. Agent 4 Memory Structure

### MEM-A4: `mem_a4_pm_review.json`

```json
{
  "memory_id": "MEM-20260605-A4",
  "session_id": "SES-20260605-0001",
  "agent_name": "Agent 4 — PM Review",
  "assessment_type": "pm_review",

  "decisions": [
    {
      "decision_id": "DEC-A4-001",
      "type": "gate_outcome",
      "statement": "GATE: PROCEED WITH CAUTION. 3 conditions for advancement.",
      "rationale": "Technology and references are GOOD. Economics is ADEQUATE — limited by OPEX data gap. One contradiction resolved (FOAK scope).",
      "conditions": ["COND-001: Resolve steel offtake application risk", "COND-002: Obtain OEM quotation", "COND-003: Monitor Normand'Hy commissioning"],
      "confidence": "MEDIUM"
    }
  ],

  "evidence_audit": {
    "total_evidence_citations": 47,
    "level_distribution": { "A": 12, "B": 24, "C": 11, "D": 0 },
    "gaps_found": 2,
    "gaps": [
      { "memory_ref": "MEM-A3 DEC-A3-010", "issue": "LCOH uses Class D proxy data" }
    ]
  },

  "assumption_stress_test": {
    "assumptions_reviewed": 9,
    "critical_found": 1,
    "critical": [
      { "memory_ref": "MEM-A3 ASM-A3-001", "assumption": "Electricity €40/MWh", "sensitivity": "CRITICAL — ±€0.83/kg LCOH" }
    ]
  },

  "contradiction_registry": {
    "total_differences": 2,
    "contradictions": 0,
    "trade_offs": 2,
    "information_gaps": 1,
    "escalations": 0
  },

  "confidence_calibration": {
    "agent_1_self": 0.64, "agent_1_calibrated": 0.64,
    "agent_2_self": 0.68, "agent_2_calibrated": 0.68,
    "agent_3_self": 0.58, "agent_3_calibrated": 0.52,
    "overall_calibrated": 0.52,
    "calibration_rationale": "Agent 3 downgraded: OPEX data uses Class D proxies. Consistency high across all agents (no contradictions)."
  }
}
```

---

## 4. Annotations (PM Comments on Upstream Memories)

Agent 4 can annotate upstream memories without modifying them. Annotations are stored in `final_review_memory.json`:

```json
{
  "annotation_id": "ANN-20260605-001",
  "target_memory": "MEM-A2",
  "target_decision": "DEC-A2-004",
  "annotation_type": "evidence_gap | assumption_weak | confidence_override | note",
  "content": "FOAK for application determination is correct, but confidence could be improved by adding at least one analogous reference (e.g., PEM→ammonia as industrial gas precedent).",
  "severity": "LOW",
  "action_required": false
}
```

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect & PMO Lead |
