# Migration Risk Assessment — Multi-Agent Refactoring

**Document:** Risk Assessment for M9 → M10A Migration
**Date:** 2026-06-05
**Author:** Lead AI Solution Architect
**Methodology:** FMEA adapted for software architecture migration

---

## 1. Risk Register

### R-MIG-001: Determinism Loss in Multi-Agent Message Passing

| Attribute | Detail |
|-----------|--------|
| **Severity** | **CRITICAL** — M9 validation proved the reasoning logic produces correct, consistent results. If multi-agent refactoring introduces nondeterminism, all validation is invalidated. |
| **Probability** | **LOW** — All reasoning is deterministic (weighted sums, table lookups, mathematical formulas). No ML models, no random sampling. The migration is mechanical extraction, not algorithm change. |
| **Detectability** | **HIGH** — Bit-exact comparison of M9 pipeline outputs vs. M10A agent outputs for same inputs. Any deviation is immediately detectable. |
| **RPN** | **1 (LOW)** — Low probability + high detectability = manageable |
| **Mitigation** | (1) Run M9 and M10A side-by-side on all 5 validation cases. (2) Require bit-exact match for all numerical outputs (similarity scores, RPN, CAPEX €/kW). (3) Accept minor formatting differences in narrative text only. (4) Automate regression testing: 5 cases × 4 agents = 20 test assertions per build. |
| **Contingency** | If determinism cannot be guaranteed in Phase 1 (Agent 1 extraction), abort migration and retain single-agent architecture. The single agent is proven and production-ready. |

---

### R-MIG-002: OPEX/LCOH Module Premature Integration

| Attribute | Detail |
|-----------|--------|
| **Severity** | **HIGH** — Agent 3's LCOH module uses Technology Card OPEX proxies instead of populated OPEX Library data. This could produce misleading LCOH estimates that appear more authoritative than they are. |
| **Probability** | **HIGH** — OPEX Library is not yet populated (planned for Sprint 2). Agent 3 WILL use proxy data initially. |
| **Detectability** | **MODERATE** — The `data_quality_note` field flags this, but users may overlook it. |
| **RPN** | **9 (MEDIUM)** |
| **Mitigation** | (1) ALL LCOH output from Agent 3 is labeled "CLASS D — PRELIMINARY" until OPEX Library has ≥20 populated records. (2) Agent 4 enforces: if OPEX Library population <20 records, LCOH confidence capped at LOW. (3) LCOH sensitivity analysis always uses wider ranges (±40%) until OPEX Library is populated. (4) Gate report explicitly states: "LCOH estimate is based on industry proxy data, not project-specific OPEX benchmarks." |
| **Contingency** | Defer LCOH module to post-OPEX-Library sprint if proxy-based estimates prove misleading in validation. |

---

### R-MIG-003: Agent 4 Overreach — PM Agent Exceeds Review Mandate

| Attribute | Detail |
|-----------|--------|
| **Severity** | **HIGH** — If Agent 4 makes de-facto project approval/rejection decisions (e.g., "DO NOT PROCEED" when the evidence merely suggests caution), it violates the Copilot's core boundary: agents advise, humans decide. |
| **Probability** | **MEDIUM** — Agent 4's gate review methodology has explicit rules (§3 of pm_agent_design.md), but edge cases may produce overly assertive gate outcomes. |
| **Detectability** | **MODERATE** — Detection requires human review of gate outcomes against evidence. |
| **RPN** | **9 (MEDIUM)** |
| **Mitigation** | (1) Agent 4's GATE OUTCOME is always labeled "RECOMMENDATION — FOR HUMAN REVIEW". (2) Gate outcomes are based on evidence quality, not project merit. A project with GOOD evidence gets PROCEED regardless of whether the PM thinks it's a good investment. (3) Agent 4 must cite specific evidence from Agents 1-3 for every condition. (4) Test: feed Agent 4 identical evidence quality scores but different project profiles → gate outcome should depend ONLY on evidence quality. |
| **Contingency** | If Agent 4 produces a DO NOT PROCEED that a human PM overrides with valid rationale, recalibrate gate thresholds. |

---

### R-MIG-004: Knowledge Base Race Condition — Agent Reads Stale Data

| Attribute | Detail |
|-----------|--------|
| **Severity** | **MEDIUM** — In a single-agent system, the knowledge base is read once at query time. In multi-agent, Agent 2 could read a Technology Card that gets updated between Agent 1's read and Agent 2's read. |
| **Probability** | **LOW** — Knowledge base updates are batch operations (Sprint releases), not real-time. The window for inconsistency is hours during a release, not seconds during a query. |
| **Detectability** | **LOW** — Silent inconsistency: Agent 1 returns a project list that references TC-PEM-001 v1.0, but Agent 2 reads TC-PEM-001 v1.1 with different TRL/cost data. |
| **RPN** | **2 (LOW)** |
| **Mitigation** | (1) Knowledge base version snapshot: Orchestrator records knowledge_base_version at query start. All agents use the same snapshot. (2) Knowledge base version is included in every agent output for auditability. (3) Batch releases only — no hot-patching of individual files. |
| **Contingency** | If stale reads become a problem (e.g., due to more frequent updates), implement file locking or a simple read-committed snapshot. |

---

### R-MIG-005: Inter-Agent Message Schema Evolution Breaking Backward Compatibility

| Attribute | Detail |
|-----------|--------|
| **Severity** | **MEDIUM** — If Agent 3's output schema adds a new required field, Agent 4 breaks because it expects the old schema. |
| **Probability** | **MEDIUM** — Schema evolution is inevitable as agents mature. |
| **Detectability** | **HIGH** — Schema validation at message receipt immediately detects mismatches. |
| **RPN** | **6 (LOW)** |
| **Mitigation** | (1) All inter-agent messages carry a `schema_version` field. (2) All agents validate incoming messages against expected schema before processing. (3) Schema changes follow ADDITIVE ONLY rule — new fields are optional with defaults; no field removals without version bump. (4) Integration tests validate full message chain for every schema change. |
| **Contingency** | If breaking change is unavoidable, bump schema major version. Old agents reject messages with unsupported major versions → graceful error, not silent corruption. |

---

### R-MIG-006: Performance Degradation — Multi-Agent Slower Than Single Agent

| Attribute | Detail |
|-----------|--------|
| **Severity** | **LOW** — The Copilot is not a real-time system. Pre-feasibility reports are generated on demand. A 10-second response vs 3-second is acceptable. |
| **Probability** | **MEDIUM** — Message serialization/deserialization between 4 agents adds overhead vs. in-process function calls. |
| **Detectability** | **HIGH** — Timing instrumentation per agent. |
| **RPN** | **2 (LOW)** |
| **Mitigation** | (1) Target: <10 seconds end-to-end. (2) If >10 seconds, profile per-agent. (3) Agents 1-3 are I/O-bound (reading JSON files), not CPU-bound — file caching eliminates most latency. |
| **Contingency** | If performance is unacceptable (>30 seconds), revert to single-agent with modular architecture (same code, no message passing). |

---

### R-MIG-007: Agent 1-3 Extraction Introduces Bugs in Previously Validated Logic

| Attribute | Detail |
|-----------|--------|
| **Severity** | **HIGH** — Logic that worked in M9 may break when extracted into standalone agents with different runtime contexts. |
| **Probability** | **MEDIUM** — Any code extraction carries refactoring risk. |
| **Detectability** | **HIGH** — Deterministic outputs enable exact comparison with M9 baselines. |
| **RPN** | **6 (LOW)** |
| **Mitigation** | (1) Phase 1-3 each include regression testing against M9 outputs. (2) No phase advances until agent output matches M9 pipeline output exactly. (3) Test suite: 5 validation cases × all pipeline outputs = 20+ assertions. |
| **Contingency** | Phase-level rollback: if Agent 2 extraction introduces bugs, revert to M9 P2 logic and retry extraction with smaller, more testable increments. |

---

## 2. Risk Summary Matrix

| ID | Risk | P | I | D | RPN | Class |
|----|------|---|---|---|-----|-------|
| R-MIG-001 | Determinism loss | 1 | 5 | 1 | 5 | LOW |
| R-MIG-002 | OPEX/LCOH premature integration | 5 | 4 | 3 | 60 | HIGH |
| R-MIG-003 | Agent 4 overreach | 3 | 4 | 3 | 36 | MEDIUM |
| R-MIG-004 | Knowledge base race condition | 1 | 3 | 3 | 9 | LOW |
| R-MIG-005 | Schema backward compatibility | 3 | 3 | 1 | 9 | LOW |
| R-MIG-006 | Performance degradation | 3 | 1 | 1 | 3 | LOW |
| R-MIG-007 | Extraction bugs | 3 | 4 | 1 | 12 | LOW |

**Overall migration risk: MEDIUM.** One HIGH risk (R-MIG-002 — OPEX/LCOH premature integration) is mitigated by explicit labeling and Agent 4 confidence capping. All other risks are LOW and well-mitigated.

---

## 3. Go/No-Go Criteria per Migration Phase

| Phase | Go Criteria | No-Go Triggers |
|-------|------------|---------------|
| **Phase 1 (Agent 1 extraction)** | Agent 1 output matches M9 P1 output on all 5 test cases | Any numerical output differs from M9 baseline |
| **Phase 2 (Agent 2 extraction)** | Agent 2 output matches M9 P2 output; Agent 1→2 message passing works | Technology verdict differs from M9; message passing fails |
| **Phase 3 (Agent 3 extraction)** | Agent 3 output matches M9 P3+P4 outputs; LCOH estimates within M9A validation range | CAPEX differs from M9; LCOH outside documented ranges |
| **Phase 4 (Agent 4 integration)** | Agent 4 report ≥ M9 report quality; cross-dimension consistency check functions; gate review produces actionable conditions | Agent 4 makes unsupported PROCEED/DO NOT PROCEED decisions; report quality degrades vs M9 |

---

## 4. Overall Migration Recommendation

**PROCEED WITH CAUTION.** The migration is fundamentally low-risk: 85% of logic is reused without change, all reasoning is deterministic (enabling exact regression testing), and the single-agent architecture is a proven fallback. The only material concern is OPEX/LCOH premature integration (R-MIG-002), which is managed through explicit labeling and confidence capping.

**Fallback:** If any phase fails its Go criteria, the single-agent Preliminary Feasibility Agent (M9) remains production-ready. The multi-agent architecture is an enhancement, not a dependency.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect | Migration risk assessment |
