# Schema Freeze Report — Project Reference Schema v1.1

**Document:** Official Schema Freeze Confirmation
**Date:** 2026-06-05
**Author:** Senior Knowledge Architect
**Freeze Scope:** Project Reference Database Schema v1.1 (database_architecture_v1.1.md §4)
**Freeze Duration:** Gold Dataset v1 construction (30 projects, estimated 6–8 weeks)
**Approval Authority:** Knowledge Architecture Review Board

---

## 1. Freeze Declaration

**The Project Reference Schema v1.1 is hereby FROZEN.**

This freeze applies to the schema defined in [database_architecture_v1.1.md](database_architecture_v1.1.md) §4. No additions, removals, reclassifications, or data-type changes to the Project Reference Schema are permitted during the freeze period.

The following are **NOT frozen** and may evolve independently:
- Technology Knowledge Card Schema ([database_architecture_v1.1.md](database_architecture_v1.1.md) §5)
- Risk Database Schema (§6)
- Cost Database Schema (§7)
- RAG Metadata block fields (pipeline-populated, may evolve with embedding model)
- Index structures (new derived indexes may be added)
- Embedding/chunking strategies
- Retrieval routing logic

---

## 2. Frozen Schema Summary

### 2.1 Schema Identity

| Attribute | Value |
|-----------|-------|
| Schema name | Project Reference Database Schema v1.1 |
| Schema version | 1.1.0 |
| Parent schema | v1.0.0 (database_architecture.md) |
| Authoritative document | database_architecture_v1.1.md |
| Authoritative template | templates/project_reference_template_v1.1.json |
| Stress test basis | schema_review_report.md (5 European projects) |
| Change log | schema_change_log.md |

### 2.2 Schema Dimensions

| Metric | Value |
|--------|-------|
| Total logical fields | 64 (excluding `sources[]` and `rag_metadata` sub-fields) |
| Blocks | 12 (Core Identity, Data Management, Location, Technology, Capacity, Power Supply, Water Supply, Hydrogen Offtake, Stakeholders, Financial, Timeline, Source Traceability) + RAG Metadata |
| Mandatory fields | 16 |
| Optional fields | 48 |
| Controlled vocabularies | 14 enum sets |
| Expected completeness (operational/under construction) | ~65% |
| Expected completeness (planned/pre-FID) | ~35–40% |
| Category A fields (essential) | 16 mandatory + 2 pipeline |
| Category B fields (optional) | 40 |
| Category C fields (archive-level, rarely available) | 6 |

### 2.3 Mandatory Fields (16)

The following 16 fields are frozen as mandatory. All must be populated for `published` status.

| # | Field | Rationale |
|---|-------|-----------|
| 1 | `project_id` | System identifier; 100% availability |
| 2 | `project_name` | Universal; primary display label |
| 3 | `status` | Core filter; 100% availability |
| 4 | `data_management.data_completeness_tier` | Retrieval quality gating |
| 5 | `data_management.project_phase_at_collection` | Maturity-based filtering |
| 6 | `data_management.last_data_update` | Staleness detection |
| 7 | `data_management.narrative_summary` | Primary RAG embedding source |
| 8 | `location.country` | Core filter; 100% availability |
| 9 | `location.region_classification` | Regional filtering |
| 10 | `technology.type` | Technology filtering |
| 11 | `capacity.electrolyzer_capacity_mw` | Scale filtering; 100% availability |
| 12 | `offtake.primary_application` | Application filtering; 100% availability |
| 13 | `stakeholders.developer` | Developer filtering; 100% availability |
| 14 | `sources[]` (source_id, source_type, title) | Source traceability |
| 15 | `rag_metadata.text_for_embedding` | Pipeline-generated; vector search |
| 16 | `rag_metadata.keywords` | Pipeline-generated; hybrid search |

---

## 3. Freeze Validation

### 3.1 Design Validation

| Validation | Status | Evidence |
|-----------|--------|----------|
| Schema stress-tested against real data | ✅ PASS | 5 European projects; 58 fields scored; see schema_review_report.md |
| No unreachable mandatory fields | ✅ PASS | All 16 mandatory fields have ≥60% public availability confirmed by stress test |
| No removed fields with populated data | ✅ PASS | 4 removed fields had 0% fill rate; zero data loss risk |
| All new fields have clear population path | ✅ PASS | 10 new fields are analyst-populated from structured data or expert judgment |
| Controlled vocabularies complete | ✅ PASS | 14 enum sets defined; no ambiguous values |
| Source traceability block validated | ✅ PASS | All 5 test projects had multiple traceable sources |
| RAG embedding field validated | ✅ PASS | `narrative_summary` design confirmed by stress test as superior to structured concatenation |
| Cross-reference strategy complete | ✅ PASS | FK links defined; index structure specified |
| Template matches schema | ✅ PASS | `project_reference_template_v1.1.json` validated against schema definition |
| Change log complete | ✅ PASS | schema_change_log.md documents every modification with rationale |

### 3.2 Stress Test Validation Summary

| Project | Status | v1.0 Completeness | v1.1 Estimated Completeness | Delta |
|---------|--------|-------------------|-----------------------------|-------|
| Normand'Hy (FR) | under_construction | 58.6% | ~62% | +3.4 pp |
| Masshylia (FR) | planned | 36.2% | ~42% | +5.8 pp |
| Holland Hydrogen I (NL) | under_construction | 60.3% | ~65% | +4.7 pp |
| Hamburg Green Hydrogen Hub (DE) | under_construction | 55.2% | ~60% | +4.8 pp |
| HyDeal España (ES) | planned | 24.1% | ~32% | +7.9 pp |
| **Average** | | **46.9%** | **~52.2%** | **+5.3 pp** |

The completeness improvement comes from 10 new fields that are populatable (analyst-supplied) replacing 4 fields that were never populatable.

---

## 4. Frozen Artifacts Inventory

The following files constitute the frozen schema baseline. All are committed to the knowledge base repository.

| # | File | Type | Status |
|---|------|------|--------|
| 1 | [database_architecture_v1.1.md](database_architecture_v1.1.md) | Architecture specification | **FROZEN** |
| 2 | [templates/project_reference_template_v1.1.json](templates/project_reference_template_v1.1.json) | Data entry template | **FROZEN** |
| 3 | [schema_change_log.md](schema_change_log.md) | Migration record | **FROZEN** |
| 4 | [schema_freeze_report.md](schema_freeze_report.md) | Freeze confirmation (this document) | **FROZEN** |
| 5 | [schema_review_report.md](schema_review_report.md) | Stress test evidence | Reference (historical) |
| 6 | [database_architecture.md](database_architecture.md) | v1.0 specification | Reference (superseded) |
| 7 | [templates/project_reference_template.json](templates/project_reference_template.json) | v1.0 template | Reference (superseded) |

---

## 5. Gold Dataset v1 Construction Parameters

### 5.1 Entry Requirements

Every project reference submitted for inclusion in Gold Dataset v1 MUST:

1. Conform to the frozen [project_reference_template_v1.1.json](templates/project_reference_template_v1.1.json)
2. Have all 16 mandatory fields populated
3. Have at least one source with `confidence: "high"`
4. Pass automated schema validation
5. Pass second-analyst review
6. Be saved to the correct status subfolder under `project_references/`

### 5.2 Quality Gates

| Gate | When | Criteria | Pass Threshold |
|------|------|----------|---------------|
| **G1: Schema conformance** | On submission | Valid JSON; all mandatory fields present; enum values in range | 100% |
| **G2: Source quality** | On submission | ≥1 source with confidence `high` | Mandatory |
| **G3: Tier assignment** | On submission | Correct tier per §4.2.3 criteria | Analyst review |
| **G4: Narrative quality** | On submission | 3–5 sentences; covers what/where/who/how-big/for-what | Analyst review |
| **G5: Cross-reference integrity** | After indexing | All FK references resolve | 100% |
| **G6: Duplicate detection** | Before publish | No duplicate project_id or same-name + same-location | 0 duplicates |

### 5.3 Target Mix (30 Projects)

| Dimension | Target |
|-----------|--------|
| **By status:** 5 operational, 10 under construction, 12 planned, 2 decommissioned/cancelled, 1 uncategorized | |
| **By technology:** 12 PEM, 12 Alkaline, 4 PEM+Alkaline, 2 unknown | |
| **By region:** 15 Europe, 5 MENA, 4 Asia-Pacific, 2 North America, 2 Latin America, 1 China, 1 India | |
| **By scale:** 5 small (<10 MW), 10 medium (10-100 MW), 12 large (100-500 MW), 3 very large (>500 MW) | |
| **By tier:** ≥20 at tier_2_intermediate+, ≤10 at tier_1_basic | |

---

## 6. Change Request Log (During Freeze)

Schema changes discovered as necessary during Gold Dataset construction should be logged here. They will be evaluated for inclusion in Schema v1.2 after the freeze lifts.

| CR ID | Date | Field(s) | Issue | Proposed Resolution | Priority | Status |
|-------|------|----------|-------|---------------------|----------|--------|
| — | — | — | No change requests filed | — | — | — |

---

## 7. Freeze Lift Conditions

The schema freeze will be lifted when ALL of the following conditions are met:

- [ ] Gold Dataset v1 reaches 30 projects with quality gates G1–G6 passed
- [ ] Cross-reference index is complete and validated
- [ ] Embedding pipeline has run successfully on all 30 projects
- [ ] RAG retrieval quality benchmarks measured (Precision@10, Recall@10 for 6 standard query types)
- [ ] Knowledge Quality Engineer reviews construction experience and files Schema v1.2 scope proposal
- [ ] At least 2 Copilot prototype queries return useful results

**Estimated freeze lift date:** 2026-07-18 (6 weeks from freeze)

---

## 8. Signatures

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Senior Knowledge Architect | — | 2026-06-05 | *Schema designed, stress-tested, and frozen* |
| Knowledge Quality Engineer | — | 2026-06-05 | *Stress test validated; Category A/B/C classification confirmed* |
| Gold Dataset Lead (TBD) | — | — | *Awaiting appointment* |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Knowledge Architect | Initial freeze report; Schema v1.1 frozen for Gold Dataset v1 |

---

### Statement of Record

**This freeze report confirms that the Project Reference Database Schema v1.1, as defined in database_architecture_v1.1.md §4 and embodied in templates/project_reference_template_v1.1.json, is the single authoritative schema for all Gold Dataset v1 project reference entries.**

**The schema was stress-tested against 5 real-world European green hydrogen projects with public-source data. All removed fields had 0% public fill rate. All added fields address validated gaps identified during the stress test. The mandatory field set is achievable for 100% of projects at any maturity stage.**

**No schema modifications are permitted during Gold Dataset construction. Change requests will be logged and evaluated for Schema v1.2.**

**Gold Dataset v1 construction may now begin.**
