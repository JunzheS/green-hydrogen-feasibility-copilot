# Knowledge Utilization Report

**Date:** 2026-06-09
**Principle:** Knowledge that exists should be queried. Knowledge queried should be displayed. Knowledge displayed should be explained.

---

## Utilization by Asset Class

### Projects (82 records) — Utilization: 100%

| Stage | Status | Evidence |
|-------|--------|----------|
| Stored | ✅ | 82 JSON files in gold_dataset/ |
| Queried | ✅ | All loaded by project_loader.py |
| Used in reasoning | ✅ | Agent 1 matching, Agent 3 CAPEX scaling |
| Displayed to user | ✅ | 03_Reference_Projects.py + 02 (top match) |
| Explained | ✅ | Score breakdown, rationale, tie-back to query |

### Technology Cards (2 records) — Utilization: 100%

| Stage | Status |
|-------|--------|
| Stored | ✅ |
| Queried | ✅ |
| Used in reasoning | ✅ |
| Displayed | ✅ 04_Technology_Assessment.py |
| Explained | ✅ TRL rationale, suitability, performance notes |

### Risk Records (30 records) — Utilization: 100%

| Stage | Status |
|-------|--------|
| Stored | ✅ |
| Queried | ✅ |
| Used in reasoning | ✅ |
| Displayed | ✅ 05_Risk_Assessment.py |
| Explained | ✅ FMEA breakdown, mitigation, evidence references |

### Cost Records (30 records) — Utilization: 85%

| Stage | Status | Notes |
|-------|--------|-------|
| Stored | ✅ | |
| Queried | ✅ | |
| Used in reasoning | ✅ | CAPEX taxonomy breakdown |
| Displayed | ⚠️ Partial | Costs shown in EUR M/kW. Individual cost records not browseable. |
| Explained | ✅ | AACE class, confidence, scaling notes |

### Co-located/OEM Data (embedded in project records) — Utilization: 15%

| Stage | Status | Notes |
|-------|--------|-------|
| Stored | ⚠️ Partial | OEM and developer names in project records |
| Queried | ❌ | No OEM or developer indexing |
| Used in reasoning | ❌ | Not used in matching or analysis |
| Displayed | ❌ | Not extracted or shown separately |
| Explained | ❌ | Not explained |

**Hidden value:** The Gold Dataset contains developers, OEMs, EPC contractors, and financiers. This data is stored but never queried, aggregated, or displayed. A developer portfolio view ("all Shell projects") or OEM comparison view ("projects using Thyssenkrupp Nucera stacks") is not available.

### Executive Insights — Utilization: 100%

| Stage | Status |
|-------|--------|
| Stored | ✅ Generated per assessment |
| Queried | ✅ |
| Used in reasoning | ✅ |
| Displayed | ✅ 02_Assessment_Report.py |
| Explained | ✅ Observation, impact, reasoning, recommendation |

### Technology Comparisons — Utilization: 100%

| Stage | Status |
|-------|--------|
| Stored | ✅ Generated per comparison |
| Queried | ✅ |
| Used in reasoning | ✅ |
| Displayed | ✅ 09_Technology_Comparison.py |
| Explained | ✅ 17 parameters, delta metrics, applications |

### Source Documents Library (200+ citations) — Utilization: 20%

| Stage | Status | Notes |
|-------|--------|-------|
| Stored | ✅ | source_ids with title, author, URL, quality level |
| Queried | ⚠️ Partial | Referenced in risk/cost/project records |
| Used in reasoning | ❌ | Source quality not used to weight confidence |
| Displayed | ❌ | Source details not browseable in UI |
| Explained | ❌ | Not aggregated or searchable |

**Hidden value:** 200+ cited sources with quality levels (A/B/C/D). This is a structured library that could be made browseable. Source quality could dynamically weight confidence in Agent 4.

### Architecture Documents (69 .md files) — Utilization: 70%

| Stage | Status | Notes |
|-------|--------|-------|
| Stored | ✅ | Complete design documentation |
| Queried | ⚠️ Partial | Referenced via citation IDs in code |
| Used in reasoning | ❌ | Static reference only |
| Displayed | ❌ | Not in UI |
| Explained | ❌ | External to application |

---

## Non-Utilized Assets

| Asset | Storage | Current Use | Potential Use |
|-------|---------|-------------|---------------|
| **OEM data** (in projects) | JSON records | None | OEM filtering, comparison, manufacturing capacity analysis, supply chain risk assessment |
| **Developer data** (in projects) | JSON records | None | Developer portfolio view, developer experience weighting, lender presentation |
| **Source quality levels** (A/B/C/D) | Risk/cost records | None in Agent 4 | Could dynamically weight confidence calibration |
| **Contradiction detection framework** | contradiction_detection_framework.md | None | Could cross-check Agent 2 vs Agent 3 outputs in real-time |
| **Memory schema** | agent_memory_schema_v1.json | None | Per-assessment persistence, audit trail, session history |
| **Future learning readiness** (analytics) | future_learning_readiness.md | None | Gap frequency analysis, weight optimization from historical data |

---

## Utilization Score by Asset Class

```
Projects              ████████████████████████████████████ 100%
Tech Cards            ████████████████████████████████████ 100%
Risks                 ████████████████████████████████████ 100%
Costs                 ██████████████████████████████████░░  85%
Insights              ████████████████████████████████████ 100%
Comparisons           ████████████████████████████████████ 100%
Agent Trace           ████████████████████░░░░░░░░░░░░░░░  50%
OEM/Developer Data    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  15%
Source Library        █████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  20%
Architecture Docs     █████████████████████░░░░░░░░░░░░░░░  70%
Contradiction Detect  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10%
Memory Layer          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0%
```

## Recommendation

**Highest-ROI utilization improvement:** OEM/developer indexing and source library browsing would expose hidden knowledge at low implementation cost. Contradiction detection integration would harden Agent 4 with no new data collection.
