# Knowledge Asset Map

**Date:** 2026-06-09
**Total Assets:** 18 asset classes, ~300+ individual records

---

## Asset Inventory

| # | Asset Class | Count | Schema | Implementation | Agent Usage | UI Visibility | Status |
|---|-------------|-------|--------|----------------|-------------|--------------|--------|
| 1 | **Project References** | 82 | database_architecture_v1.1.md | ✅ Loaded | Agent 1 (matching) Project loader | 03_Reference_Projects.py | ✅ |
| 2 | **Technology Cards (PEM)** | 1 | technology_card_template.json | ✅ Loaded | Agent 2 (assessment) Technology loader | 04_Technology_Assessment.py | ✅ |
| 3 | **Technology Cards (Alkaline)** | 1 | technology_card_template.json | ✅ Loaded | Agent 2 (assessment) Technology loader | 04_Technology_Assessment.py | ✅ |
| 4 | **SOEC/AEM Tech Cards** | 0 | technology_card_template.json | ❌ Not created | — | — | ❌ Gap |
| 5 | **Risk Records** | 30 | risk_schema_v1.md | ✅ Loaded | Agent 3 (filtering) Risk loader | 05_Risk_Assessment.py | ✅ |
| 6 | **Cost Records** | 30 | cost_schema_v1.md | ✅ Loaded | Agent 3 (CAPEX) Cost loader | 06_CAPEX_LCOH.py | ✅ |
| 7 | **OPEX Records** | 0 | opex_schema_v1.md | ❌ Not populated | — (LCOH uses proxies) | — | ❌ Gap |
| 8 | **Project Match Breakdown** | Calculated | — | ✅ Generated | Agent 1 → enriched | 03_Reference_Projects.py | ✅ |
| 9 | **Executive Insights** | 5/assessment | — | ✅ Generated | Agent 4 (insights) | 02_Assessment_Report.py | ✅ |
| 10 | **Risk Consequences** | 10/assessment | — | ✅ Generated | Agent 3 → enriched | 05_Risk_Assessment.py | ✅ |
| 11 | **Gate Justifications** | 1/assessment | — | ✅ Generated | Agent 4 | 02_Assessment_Report.py | ✅ |
| 12 | **Technology Comparisons** | 1/assessment | — | ✅ Generated | Tech comparison engine | 09_Technology_Comparison.py | ✅ |
| 13 | **Agent Trace Records** | 6/assessment | agent_memory_schema_v1.json | ❌ Designed | — | 07_Agent_Trace.py (static display only) | ⚠️ Partial |
| 14 | **Contradiction Records** | Detected | contradiction_detection_framework.md | ❌ Not integrated | — | — | ❌ Gap |
| 15 | **OEM Records** | Embedded in projects | — | ⚠️ Partial (in narrative) | Not directly queried | Not shown | ⚠️ Underused |
| 16 | **Developer Records** | Embedded in projects | — | ⚠️ Partial (in stakeholders) | Not directly queried | Not shown | ⚠️ Underused |
| 17 | **Source Documents Library** | 200+ cited | source_governance_framework.md | ⚠️ Sources cited in JSON | Referenced only | Not directly browsable | ⚠️ Underused |
| 18 | **Architecture Documents** | 69 .md files | — | ✅ Complete | Reference only | Not in UI | ⚠️ Underused |

---

## Asset Utilization Summary

```
Projects (82)     ████████████████████████████████████████ 100% — loaded, queried, displayed
Tech Cards (2)    ████████████████████████████████████████ 100% — loaded, queried, displayed
Risks (30)        ████████████████████████████████████████ 100% — loaded, filtered, displayed
Costs (30)        ████████████████████████████████████████ 100% — loaded, scaled, displayed
OPEX (0)          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0% — not populated
Insights          ████████████████████████████████████████ 100% — generated, displayed
Comparisons       ████████████████████████████████████████ 100% — generated, displayed
Agent Trace       ████████████████████░░░░░░░░░░░░░░░░░░░░  50% — static display, no persistence
OEM Data          ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  15% — stored in projects, not queried
Developer Data    ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  15% — stored in projects, not queried
Source Library    ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  10% — cited, not browsable
Architecture Docs ████████████████████████████████░░░░░░░░  70% — complete but external
```

## Gap Assets (Not Created)

| Asset | Priority | Effort | Impact |
|-------|----------|--------|--------|
| SOEC/AEM Technology Cards | LOW | 2 days | Enables comparison for 4 projects |
| OPEX Library | HIGH | 5 days | Upgrades LCOH from Class D to Class C |
| Persisted Agent Memory | MEDIUM | 3 days | Enables audit trail and learning |
| Contradiction Detection | MEDIUM | 2 days | Hardens Agent 4 quality review |
| OEM/Developer Index | LOW | 1 day | Enables developer portfolio retrieval |
| Source Document Browser | LOW | 2 days | Makes source governance visible |
