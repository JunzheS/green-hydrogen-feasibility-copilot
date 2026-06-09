# Agent Memory Architecture — Decision Traceability Layer v1.0

**Document:** Memory System Architecture
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Purpose:** Structured, immutable audit trail for multi-agent pre-feasibility assessments
**Scope:** Traceability and explainability — NOT conversational memory, NOT vector memory, NOT autonomous learning

---

## 1. What This Is (And What It Isn't)

### 1.1 This IS

| ✅ | Description |
|----|-------------|
| A **structured decision log** — immutable records of what each agent did |
| An **audit trail** — every conclusion traceable to its evidence and assumptions |
| A **confidence tracker** — how confidence evolved across agents |
| An **explainability foundation** — enables answering "why was this conclusion reached?" |
| A **contradiction registry** — records where agents' outputs diverge |
| A **future-learning enabler** — structured data that could eventually train better agents |

### 1.2 This IS NOT

| ❌ | Clarification |
|----|--------------|
| Conversational memory | Does not remember past chats with users |
| Vector / RAG memory | Does not embed and retrieve memories semantically |
| Long-term learning system | Does not modify agent behavior based on past sessions |
| Agent knowledge base | Does not store Gold Dataset or Technology Cards — it references them |
| Human-readable narrative | Machines write it; machines and auditors read it |
| Self-modifying | No agent can change its own past memory |

---

## 2. Architecture Overview

### 2.1 The Three Memory Layers

```
SESSION MEMORY (1 per user query — container)
├── Created: at query start by Orchestrator
├── Immutable: after session closes
├── Contains: session metadata + link to all agent memories
│
├── AGENT MEMORY (1 per agent execution — 4 per session)
│   ├── MEM-A1: Agent 1 — Knowledge Retrieval
│   ├── MEM-A2: Agent 2 — Technical Assessment
│   ├── MEM-A3: Agent 3 — Risk & Economic Assessment
│   └── MEM-A4: Agent 4 — PM Review
│
└── FINAL REVIEW MEMORY (1 per session — Agent 4's synthesis)
    ├── Cross-agent consistency report
    ├── Contradiction registry
    ├── Confidence calibration log
    └── Gate decision rationale
```

### 2.2 Memory Lifecycle

```
TIME ──────────────────────────────────────────────────────────────►

T0: User submits query
    └─ ORCHESTRATOR creates SESSION MEMORY
       session_id = "SES-20260605-0001"
       status = "in_progress"

T1: Agent 1 executes
    └─ ORCHESTRATOR creates MEM-A1 container
    └─ AGENT 1 populates MEM-A1 with retrieval decisions
    └─ MEM-A1 status = "complete"
    └─ AGENT 1 output → ORCHESTRATOR → AGENT 2

T2: Agent 2 executes
    └─ ORCHESTRATOR creates MEM-A2 container
    └─ AGENT 2 reads MEM-A1 (READ ONLY — cannot modify)
    └─ AGENT 2 populates MEM-A2 with technology decisions
    └─ MEM-A2 status = "complete"

T3: Agent 3 executes
    └─ ORCHESTRATOR creates MEM-A3 container
    └─ AGENT 3 reads MEM-A1, MEM-A2 (READ ONLY)
    └─ AGENT 3 populates MEM-A3 with risk + economic decisions
    └─ MEM-A3 status = "complete"

T4: Agent 4 executes
    └─ ORCHESTRATOR creates MEM-A4 + FINAL REVIEW containers
    └─ AGENT 4 reads MEM-A1, MEM-A2, MEM-A3 (READ ONLY)
    └─ AGENT 4 populates MEM-A4 with review decisions
    └─ AGENT 4 populates FINAL REVIEW with cross-agent synthesis
    └─ MEM-A4 status = "complete"

T5: Session closes
    └─ SESSION MEMORY status = "complete"
    └─ ALL MEMORIES BECOME IMMUTABLE
    └─ Stored as JSON files in knowledge_base/memory/sessions/{session_id}/
```

---

## 3. Memory Storage

### 3.1 File Structure

```
knowledge_base/memory/
├── sessions/
│   └── {session_id}/
│       ├── session_memory.json          ← SESSION container
│       ├── mem_a1_retrieval.json        ← Agent 1 memory
│       ├── mem_a2_technical.json        ← Agent 2 memory
│       ├── mem_a3_risk_economic.json    ← Agent 3 memory
│       ├── mem_a4_pm_review.json        ← Agent 4 memory
│       └── final_review_memory.json     ← Cross-agent synthesis
│
├── index/
│   └── session_index.json              ← Maps session_id → timestamp + query summary
│
└── templates/
    └── agent_memory_schema_v1.json       ← Schema template
```

### 3.2 Immutability Guarantee

| Rule | Enforcement |
|------|------------|
| **Write-once per agent** | Each agent writes its own memory file ONCE. Subsequent writes to the same file are rejected by the Orchestrator. |
| **Read-only for downstream agents** | Agent 3 can read Agent 1 and 2's memories. It cannot modify them. |
| **No agent can modify its own past memory** | A new assessment = a new session. Memories are never updated retroactively. |
| **PM Agent can annotate, not edit** | Agent 4 can add annotations to Agent 1-3 memories (e.g., "EVIDENCE GAP: No Class A source cited") but cannot change the original agent's data. Annotations are stored in final_review_memory.json with reference to the original memory entry. |
| **Session closure = freeze** | Once Agent 4 completes, the Orchestrator hashes all 7 files and records the hash in session_memory.json. Any post-closure modification is detectable. |

---

## 4. Memory Flow Diagram

```
SESSION SES-20260605-0001 — "France 100MW PEM Steel 2029"
│
├─ MEM-A1 (Agent 1: Knowledge Retrieval)
│   input: { query }
│   evidence: [GA-PR-001..006], [TC-PEM-001]
│   decisions: "Top project: Normand'Hy (0.81)"
│   assumptions: ["Steel ≈ refinery (industrial group mapping)"]
│   confidence: 0.64
│
│   │ read by Agent 2 ──────────────────────────────┐
│   │                                               │
├─ MEM-A2 (Agent 2: Technical Assessment)            │
│   input: { query + Agent1.projects }              │
│   evidence: [TC-PEM-001 §§maturity,applications]   │
│   decisions: "TRL 8, suitable for steel, FOAK app"│
│   assumptions: ["DRI pressure = 10-20 bar"]        │
│   confidence: 0.68                                 │
│   contradictions_detected: []                       │
│                                                    │
│   │ read by Agent 3 ───────────────────────────────┤
│   │                                                │
├─ MEM-A3 (Agent 3: Risk & Economic Assessment)       │
│   input: { query + Agent2.verdict }                │
│   evidence: [RK-TEC-001..RK-ENV-001], [CS-ELC-001..]│
│   decisions: "Top risk: Offtake RPN 30, CAPEX €157M"│
│   assumptions: ["€40/MWh electricity", "20% contingency"]│
│   confidence: 0.58                                  │
│   contradictions_detected: ["Agent2 says not FOAK for scale; Agent3 applies FOAK for application — NOT a contradiction"]│
│                                                     │
│   │ read by Agent 4 ────────────────────────────────┘
│   │
├─ MEM-A4 (Agent 4: PM Review)
│   input: { query + A1+A2+A3 memories + outputs }
│   decisions: "GATE: PROCEED WITH CAUTION. 3 conditions."
│   cross_agent_consistency: PASS (1 noted difference, classified as trade-off)
│   confidence_calibration: "A3 self-assessed 0.58 → calibrated to 0.52 (OPEX data gap)"
│
└─ FINAL REVIEW MEMORY
    gate_outcome: "PROCEED WITH CAUTION"
    annotation_registry: [
      "MEM-A2: FOAK for application assertion — evidence gap noted (no operational steel PEM ref)",
      "MEM-A3: LCOH estimate uses Class D proxy data — capped confidence"
    ]
    session_hash: "sha256:abc123..."
```

---

## 5. Key Design Decisions

| Decision | Rationale |
|----------|----------|
| **Files, not database** | The Copilot is local and file-based. JSON files are human-readable, version-controllable, and require no server infrastructure. |
| **Immutable after session close** | Audit trail integrity. A session is a historical record, not a living document. |
| **Agent writes only its own memory** | Prevents contamination. Agent 3 cannot "fix" Agent 2's assumptions retroactively. |
| **PM can annotate, not edit** | Agent 4 is a reviewer, not a rewriter. Its observations are separate from the original agent's record. |
| **No vector embedding of memories** | This is a structured audit trail, not a retrieval system. If future learning needs embeddings, they can be derived from these structured files. |
| **Session-level granularity** | One session = one user query = one complete assessment. Memories are not at the individual function-call level (too granular) or project level (too coarse). |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect | Initial memory architecture |
