# Future Learning Readiness — Architecture Preparation v1.0

**Document:** Learning Capability Design (Implementation NOT in scope)
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Status:** ARCHITECTURE PREPARATION ONLY — No autonomous learning, no self-modifying behavior

---

## 1. What This Document IS

This document identifies **structural hooks** in the Decision Traceability Layer that could eventually support machine learning, pattern discovery, and agent self-improvement. It does NOT:

- Implement any learning algorithm
- Modify agent behavior based on past sessions
- Create feedback loops
- Enable autonomous system evolution

It IS a **forward-compatibility design** — ensuring that when the Copilot is ready for learning capabilities, the memory layer already contains the structured data needed.

---

## 2. Learning-Ready Data Structures

### 2.1 What the Memory Layer Already Provides

The memory schema captures structured, labeled data suitable for future training:

| Memory Field | Future Learning Use |
|-------------|-------------------|
| `decisions[].statement` + `decisions[].confidence` | Labeled training data: "For query profile X, decision Y was made with confidence Z" |
| `evidence_ids[]` | Feature attribution: which evidence sources correlate with high-confidence vs. low-confidence decisions |
| `assumptions[].impact_if_wrong` | Sensitivity training: which assumptions most frequently drive incorrect conclusions |
| `contradictions_detected[]` | Error pattern discovery: which agent pairings most frequently produce contradictions |
| `confidence.self_assessed` vs PM Agent `calibrated` | Calibration training: learn systematic over/under-confidence patterns per agent |
| `warnings[]` | Gap prediction: train a model to predict knowledge gaps before they're encountered |

### 2.2 Session Index as Training Corpus

The `session_index.json` accumulates structured metadata:

```json
{
  "session_id": "SES-20260605-0001",
  "query": { "country": "France", "industry": "Steel", "technology": "PEM", "capacity_mw": 100 },
  "timestamp": "2026-06-05T14:30:00Z",
  "gate_outcome": "PROCEED_WITH_CAUTION",
  "overall_confidence": 0.52,
  "contradictions_found": 0,
  "gaps_found": 3,
  "agent_1_score": 0.64, "agent_2_score": 0.68, "agent_3_score": 0.52, "agent_4_score": 0.52
}
```

After 100+ sessions, this becomes a training corpus for:
- Predicting gate outcomes from query profiles
- Identifying query profiles that systematically produce low confidence
- Detecting which knowledge base gaps most frequently cause problems

---

## 3. Five Future Learning Capabilities (Architecture Supports)

### 3.1 Knowledge Refinement

**What:** Use historical session data to identify systematic gaps and prioritize knowledge base expansion.

**Architecture hook:** The `warnings[]` and `gaps[]` fields in agent memories accumulate gap data. After 50 sessions, the system could:
- Rank gaps by frequency: "Steel offtake gap appeared in 12 of 50 sessions — highest priority for Gold Dataset Sprint 3"
- Identify "gap clusters": "Queries with industry=X AND capacity=Y consistently produce low confidence"

**What's needed to implement:** A simple analytics pipeline over session_index.json. No ML required — just frequency counting.

### 3.2 Pattern Discovery

**What:** Discover correlations between query profiles and assessment outcomes.

**Architecture hook:** The structured `query → decisions` mapping in each session memory creates a labeled dataset:
```
Query(FR, Steel, PEM, 100MW, 2029) → Gate(PROCEED_WITH_CAUTION, 0.52)
Query(DE, Industrial, ALK, 300MW, 2030) → Gate(PROCEED, 0.65)
Query(ES, Refinery, PEM, 20MW, 2028) → Gate(PROCEED, 0.68)
```

After enough sessions, simple regression could predict: "For this query profile, expect confidence ~0.55 — the limiting factor is likely [offtake novelty] based on historical patterns."

**What's needed:** A decision tree or logistic regression trained on session data. The structured memory format means NO data preprocessing is needed — the features are already extracted.

### 3.3 Retrieval Optimization

**What:** Tune the project matching similarity weights based on actual PM feedback.

**Architecture hook:** The `decisions[].confidence` field for project ranking decisions, cross-referenced with the PM Agent's calibration:
- If Agent 1 consistently self-assesses confidence at 0.70 but PM calibrates to 0.55 for certain query types → the similarity weights need tuning for those query profiles
- If certain country/industry combinations consistently produce low-ranked results → the matching algorithm could learn adjusted weights

**What's needed:** Weight optimization using the session data as a loss function: minimize the gap between Agent 1 self-assessed confidence and Agent 4 calibrated confidence.

### 3.4 Future Skill Generation

**What:** Use accumulated session patterns to generate new agent capabilities automatically.

**Architecture hook:** The structured memory format records every reasoning step. After sufficient sessions:
- Common PM Agent annotations ("EVIDENCE GAP", "WEAK ASSUMPTION") could become automated pre-flight checks in Agents 1-3
- Frequently escalated contradictions could become new detection rules in Agent 4
- Successful resolution patterns could become standard operating procedures

**Example:** If Agent 4 consistently annotates "OPEX Class D — confidence capped" on Agent 3 outputs, a future version of Agent 3 could self-check: "Is my LCOH using only Class D data? If yes, auto-cap confidence at LOW before Agent 4 review."

**What's needed:** Rule extraction from annotation patterns — a form of program synthesis from operational data.

### 3.5 Confidence Calibration Training

**What:** Train agents to self-assess confidence more accurately.

**Architecture hook:** Each session records:
- `confidence.self_assessed` (what the agent thought)
- `confidence.calibrated` (what Agent 4 determined)

After 50+ sessions per agent, the calibration gap becomes measurable:
- Agent 3 systematically overestimates by 0.06 (mean self-assessed 0.58 → PM calibrated 0.52)
- Agent 1 is well-calibrated (mean gap 0.00)
- Agent 2 slightly underestimates (mean gap +0.02)

A simple calibration model could adjust future self-assessments automatically.

**What's needed:** Isotonic regression or Platt scaling on the self-assessed vs. calibrated pairs.

---

## 4. What We Explicitly Do NOT Support (Yet)

| Capability | Why Not Yet |
|-----------|------------|
| **Reinforcement learning — agent improves from feedback** | Requires a reward signal. The PM Agent's gate outcome could eventually serve as a reward, but we have no mechanism for "was this gate decision correct?" until projects actually proceed to construction. |
| **Unsupervised clustering of query profiles** | Interesting but not actionable yet. Knowing that "PEM+Steel queries cluster together" doesn't help until we can say "and that cluster has systematically different outcomes." |
| **Automated knowledge base expansion** | Agents should NEVER modify the knowledge base autonomously. Knowledge base updates require human validation per the Source Governance Framework. |
| **Model-based agent replacement** | All current reasoning is rules-based and deterministic. Replacing with learned models would break determinism and auditability — unacceptable without a parallel validation framework. |
| **Federated learning across Copilot instances** | The Copilot is local and file-based. Multi-instance coordination is architecturally incompatible with the current design. |

---

## 5. Activation Roadmap (When Learning Is Appropriate)

| Phase | Condition | Capability to Activate |
|-------|----------|----------------------|
| **NOW (M10B-0)** | Memory layer built | Data collection only — structured audit trail |
| **M11** | ≥50 sessions accumulated | Gap frequency analytics (3.1), confidence calibration training (3.5) |
| **M12** | ≥100 sessions + regression validation | Retrieval weight optimization (3.3), pattern discovery (3.2) |
| **M13+** | ≥200 sessions + human-validated patterns | PM annotation → pre-flight checks (3.4), contradiction rule extraction |
| **Future** | TBD — requires operational project feedback loop | Reinforcement learning from actual project outcomes |

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect |
