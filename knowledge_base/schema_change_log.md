# Schema Change Log — v1.0 → v1.1

**Document:** Schema Migration Record
**Date:** 2026-06-05
**Author:** Senior Knowledge Architect
**Change Basis:** Schema Stress Test validated against 5 European green hydrogen projects (Normand'Hy, Masshylia, Holland Hydrogen I, Hamburg Green Hydrogen Hub, HyDeal España)
**Status:** Approved — Schema v1.1 is FROZEN for Gold Dataset v1 construction

---

## Table of Contents

1. [Change Summary](#1-change-summary)
2. [Fields Removed (Category C)](#2-fields-removed-category-c)
3. [Fields Added](#3-fields-added)
4. [Fields Reclassified (Mandatory ↔ Optional)](#4-fields-reclassified-mandatory--optional)
5. [Mandatory Fields Comparison](#5-mandatory-fields-comparison)
6. [Schema Impact Matrix](#6-schema-impact-matrix)
7. [Migrating v1.0 Data to v1.1](#7-migrating-v10-data-to-v11)

---

## 1. Change Summary

| Metric | v1.0 | v1.1 | Delta |
|--------|------|------|-------|
| Total fields (logical, excluding `sources[]` sub-fields and `rag_metadata`) | 58 | **64** | +6 net |
| Mandatory fields | 14 | **16** | +2 net |
| Optional fields | 44 | **48** | +4 net |
| Block count | 10 | **11** | +1 (Data Management) |
| Expected avg. completeness (operational/construction) | 51.7% | **~65%** | +13.3 pp |
| Expected avg. completeness (planned) | 31.6% | **~40%** | +8.4 pp |

**Net effect:** The v1.1 schema has 6 more total fields than v1.0, but 4 unreachable fields were removed and 10 actionable fields were added. The expected completeness for public-data projects rises because the removed fields were never populatable, while new fields are all based on analyst-provided metadata.

---

## 2. Fields Removed (Category C)

Four fields were removed following the stress test findings. All had 0% fill rate across the 5 projects tested.

### 2.1 `financial.expected_irr_percent`

| Attribute | Value |
|-----------|-------|
| **v1.0 location** | Financial Block, field #51 |
| **v1.0 mandatory** | No |
| **Fill rate (5 projects)** | **0%** — never published |
| **Reason for removal** | IRR is commercially confidential and never disclosed by project developers. It is a financial modeling output, not a data collection input. If IRR estimation becomes a Copilot feature in the future, it should live in a separate `financial_model` entity with explicit methodology and assumptions. |
| **Migration note** | Simply delete from the schema. No projects had this populated, so no data loss. |

### 2.2 `financial.capex_breakdown_available`

| Attribute | Value |
|-----------|-------|
| **v1.0 location** | Financial Block, field #47 |
| **v1.0 mandatory** | No |
| **Fill rate (5 projects)** | **0%** — always false for public data |
| **Reason for removal** | This was a pipeline-internal flag, not a data collection field. For public-source projects, the answer is always `false`. The existence of entries in the `cost_library/` already indicates whether a CAPEX breakdown is available. This redundancy adds no retrieval value. |
| **Migration note** | Delete from the schema. If needed at runtime, derive from `cost_library/` cross-reference index. |

### 2.3 `power.expected_capacity_factor_percent`

| Attribute | Value |
|-----------|-------|
| **v1.0 location** | Power Supply Block, field #28 |
| **v1.0 mandatory** | No |
| **Fill rate (5 projects)** | **0%** — never published for electrolyzer projects |
| **Reason for removal** | Capacity factor depends on renewable resource quality, PPA terms, and operational strategy — all of which are commercially sensitive. This is an engineering modeling parameter, not a data collection field. If needed for the Copilot, it should be an assumed value in a `technical_assumptions` entity with transparent defaults per renewable type and region. |
| **Migration note** | Delete from the schema. No data loss. |

### 2.4 `technology.stack_pressure_type`

| Attribute | Value |
|-----------|-------|
| **v1.0 location** | Technology Block, field #15 |
| **v1.0 mandatory** | No |
| **Fill rate (5 projects)** | **0%** — never stated in project press releases |
| **Reason for removal** | This is inherently a technology property, not a project-specific fact. All PEM stacks are inherently pressurized; all Alkaline stacks are inherently atmospheric (with few exceptions). This information belongs on the Technology Knowledge Card (`TC-PEM-001`, `TC-ALK-001`), not on every project entry. Every project already links to a technology card via `technology_card_ref`, so this field was redundant. |
| **Migration note** | Delete from project schema. Ensure this field is populated on both Technology Cards (`TC-PEM-001` and `TC-ALK-001`). Reading it should happen via FK join, not copy. |

---

## 3. Fields Added

Ten new fields were added based on the stress test recommendations. All address gaps identified during real-world data collection.

### New Block: Data Management (6 new fields)

The stress test revealed that v1.0 lacked any metadata about data quality, freshness, and project maturity granularity. These 6 fields form a new **Data Management Block** placed after Core Identity and before Location.

#### 3.1 `data_completeness_tier`

| Attribute | Value |
|-----------|-------|
| **Data type** | `enum: tier_1_basic \| tier_2_intermediate \| tier_3_detailed \| tier_4_full` |
| **Mandatory** | **Yes** |
| **Block** | Data Management |
| **Rationale** | The stress test showed projects vary wildly in completeness (24% to 60%). A completeness tier enables: (1) Users to filter for "only projects with financial data" or "only projects with detailed technical data"; (2) RAG agents to qualify their confidence based on data richness of retrieved projects; (3) Analysts to prioritize backfill efforts. |
| **Tier definitions** | See `database_architecture_v1.1.md` §4.2.3 for full tier criteria |

#### 3.2 `project_phase_at_collection`

| Attribute | Value |
|-----------|-------|
| **Data type** | `enum: pre_feasibility \| feasibility \| pre_fid \| post_fid \| construction \| commissioning \| operational` |
| **Mandatory** | **Yes** |
| **Block** | Data Management |
| **Rationale** | The existing `status` field (operational/under_construction/planned) is too coarse. A project "planned" could be at pre-feasibility (10% complete) or post-FID awaiting construction (80% complete). This field enables precise filtering by the project's actual maturity at data collection time, which strongly correlates with data completeness. The stress test showed planned projects averaged 30.2% vs. under-construction at 58.0%. |

#### 3.3 `last_data_update`

| Attribute | Value |
|-----------|-------|
| **Data type** | `string` (ISO 8601 datetime) |
| **Mandatory** | **Yes** |
| **Block** | Data Management |
| **Rationale** | `rag_metadata.last_indexed` tracks the embedding pipeline, not the data itself. A project might have been indexed yesterday but last updated 2 years ago. This business-level field enables stale-data detection, update scheduling triggers, and retrieval-time freshness filtering. Critical for an industrial Copilot where using outdated CAPEX or timeline data could lead to incorrect feasibility conclusions. |

#### 3.4 `narrative_summary`

| Attribute | Value |
|-----------|-------|
| **Data type** | `string` (max 2000 characters) |
| **Mandatory** | **Yes** |
| **Block** | Data Management |
| **Rationale** | THE single most important field for RAG embedding quality. A human-written 3–5 sentence summary captures the project's essence — what, where, how big, who, for what purpose — in natural language that embedding models understand. The stress test showed that structured fields (like `capacity.electrolyzer_capacity_mw: 200`) embed poorly compared to natural text ("a 200 MW PEM electrolyzer producing 28,000 tonnes per year"). This field is the primary source for `rag_metadata.text_for_embedding`. |

#### 3.5 `is_first_of_a_kind`

| Attribute | Value |
|-----------|-------|
| **Data type** | `boolean` |
| **Mandatory** | No |
| **Block** | Data Management |
| **Rationale** | First-of-a-kind (FOAK) projects carry elevated risk across technical, cost, and schedule dimensions. The risk library references FOAK status as a key applicability filter. This field enables: (1) "Show me only FOAK projects for risk benchmarking"; (2) Weighting CAPEX estimates higher for non-FOAK projects. Definition: FOAK = first project at this scale for this technology in this region, OR first project by this developer, OR using novel technical configuration. |

#### 3.6 `related_project_ids`

| Attribute | Value |
|-----------|-------|
| **Data type** | `string[]` |
| **Mandatory** | No |
| **Block** | Data Management |
| **Rationale** | Projects don't exist in isolation. Normand'Hy is related to ELYgator (same developer, same technology). Holland Hydrogen I is related to Hollandse Kust Noord (same developer, power source). This field enables graph-traversal queries: "Find all projects in Shell's hydrogen portfolio" or "Show projects sharing infrastructure with HH1." Populate with `project_id` references. |

### New Sub-Fields in Existing Blocks (4 new fields)

#### 3.7 `location.coordinates_verified`

| Attribute | Value |
|-----------|-------|
| **Data type** | `boolean` |
| **Mandatory** | No |
| **Block** | Location (sub-field of `location`) |
| **Rationale** | The stress test found that ALL 5 projects had coordinates, but ALL were analyst-estimated from city/industrial zone names — not from official project documentation. Default: `false`. This field distinguishes geolocated facts from analyst estimates, which matters for map-based visualizations and proximity queries. |

#### 3.8 `technology.technology_selection_status`

| Attribute | Value |
|-----------|-------|
| **Data type** | `enum: confirmed \| announced \| not_selected` |
| **Mandatory** | No |
| **Block** | Technology (sub-field of `technology`) |
| **Rationale** | The stress test found that for pre-FID projects (Masshylia, HyDeal España), the technology type was ambiguous or not yet selected. A project might announce "PEM" but later switch to Alkaline. This field distinguishes: `confirmed` = contract signed with OEM; `announced` = publicly stated intention but no contract; `not_selected` = technology not yet chosen. |

#### 3.9 `financial.capex_confidence`

| Attribute | Value |
|-----------|-------|
| **Data type** | `enum: official \| media_report \| analyst_estimate \| calculated` |
| **Mandatory** | No |
| **Block** | Financial (sub-field of `financial`) |
| **Rationale** | The stress test showed CAPEX data of widely varying quality: official Air Liquide figures vs. media-estimated Shell figures vs. analyst-calculated per-kW values. This field enables: (1) Weighted averaging for CAPEX estimation (higher weight for `official`); (2) Filtering "only use official CAPEX for benchmarking." |

#### 3.10 `financial.capex_per_kw_method`

| Attribute | Value |
|-----------|-------|
| **Data type** | `enum: stated \| calculated_total_div_mw` |
| **Mandatory** | No |
| **Block** | Financial (sub-field of `financial`) |
| **Rationale** | The stress test found that `capex_per_kw_eur` was always present but 80% of values were calculated (total CAPEX ÷ MW) rather than stated by the developer. Stated vs. calculated per-kW values have different meanings: a stated per-kW value often reflects stack-only cost, while a calculated value reflects all-in cost. This field makes the derivation transparent. |

---

## 4. Fields Reclassified (Mandatory ↔ Optional)

### 4.1 `power.renewable_type`: **Mandatory → Optional**

| Attribute | Value |
|-----------|-------|
| **v1.0 status** | **Yes (Mandatory)** |
| **v1.1 status** | **No (Optional)** |
| **Fill rate (5 projects)** | 60% |
| **Reason** | Two of five projects (Normand'Hy, Hamburg Green Hydrogen Hub) are grid-connected without a dedicated renewable source. Making this field mandatory forces data fabricators or false assumptions. Grid-connected projects with grid-mix electricity are valid green hydrogen configurations — the renewable type is simply "grid_mix" or unknown. |
| **Affected projects** | Normand'Hy, HGHH — these would have been invalid under v1.0 mandatory constraint. |

### 4.2 All Other Mandatory Fields — Unchanged

The following v1.0 mandatory fields remain mandatory in v1.1 (stress test validated ≥80% public availability):

- `project_id` — 100%
- `project_name` — 100%
- `status` — 100%
- `location.country` — 100%
- `location.region_classification` — 100%
- `technology.type` — 60% (borderline, but essential for filtering — kept mandatory with `technology_selection_status` flag)
- `capacity.electrolyzer_capacity_mw` — 100%
- `offtake.primary_application` — 100%
- `stakeholders.developer` — 100%
- `sources[]` — 100%

---

## 5. Mandatory Fields Comparison

### v1.0 Mandatory Fields (14)
```
1.  project_id
2.  project_name
3.  status
4.  location.country
5.  location.region_classification
6.  technology.type
7.  capacity.electrolyzer_capacity_mw
8.  power.renewable_type              ← DEMOTED in v1.1
9.  offtake.primary_application
10. stakeholders.developer
11. sources[].source_id
12. sources[].source_type
13. sources[].title
14. sources[].confidence
(rag_metadata fields are pipeline-populated, not manually entered)
```

### v1.1 Mandatory Fields (16)
```
1.  project_id
2.  project_name
3.  status
4.  location.country
5.  location.region_classification
6.  technology.type
7.  capacity.electrolyzer_capacity_mw
8.  offtake.primary_application
9.  stakeholders.developer
10. data_completeness_tier          ← NEW
11. project_phase_at_collection      ← NEW
12. last_data_update                 ← NEW
13. narrative_summary                ← NEW
14. sources[].source_id
15. sources[].source_type
16. sources[].title
(rag_metadata.text_for_embedding and rag_metadata.keywords remain pipeline-populated mandatory)
```

---

## 6. Schema Impact Matrix

This matrix shows which blocks were affected by the v1.1 changes.

```
Block              | Removed | Added | Mandatory Δ | Net Δ | Risk to Existing Data
-------------------|---------|-------|-------------|-------|----------------------
Core Identity      | 0       | 0     | 0           | 0     | None
Data Management    | — (new) | +6    | +4          | +6    | None (new block)
Location           | 0       | +1    | 0           | +1    | None (optional add)
Technology         | -1      | +1    | 0           | 0     | stack_pressure_type data lost if populated (none found)
Capacity           | 0       | 0     | 0           | 0     | None
Power Supply       | -1      | 0     | -1          | -1    | capacity_factor data lost if populated (none found)
Water Supply       | 0       | 0     | 0           | 0     | None
Hydrogen Offtake   | 0       | 0     | 0           | 0     | None
Stakeholders       | 0       | 0     | 0           | 0     | None
Financial          | -2      | +2    | 0           | 0     | irr + breakdown data lost if populated (none found)
Timeline           | 0       | 0     | 0           | 0     | None
Source Traceability| 0       | 0     | 0           | 0     | None
RAG Metadata       | 0       | 0     | 0           | 0     | None
-------------------|---------|-------|-------------|-------|----------------------
TOTAL              | -4      | +10   | +3 / -1     | +6    | Zero risk (all removed fields had 0% fill)
```

---

## 7. Migrating v1.0 Data to v1.1

### 7.1 Migration Script (Conceptual)

Since no Gold Dataset exists yet, this section is a forward-looking specification for when v1.0 test data is migrated.

```
FOR each v1.0 project reference JSON:
  1. DELETE field: technology.stack_pressure_type
  2. DELETE field: financial.expected_irr_percent
  3. DELETE field: financial.capex_breakdown_available
  4. DELETE field: power.expected_capacity_factor_percent
  5. ADD block: data_management:
     a. data_completeness_tier ← calculate from filled optional fields
     b. project_phase_at_collection ← derive from status + timeline
     c. last_data_update ← set to current datetime
     d. narrative_summary ← generate from key fields (human review required)
     e. is_first_of_a_kind ← set to null (requires analyst judgment)
     f. related_project_ids ← set to [] (requires analyst research)
  6. ADD field: location.coordinates_verified ← set to false (all were estimated)
  7. ADD field: technology.technology_selection_status ← derive from manufacturer presence
  8. ADD field: financial.capex_confidence ← derive from source confidence
  9. ADD field: financial.capex_per_kw_method ← set to "calculated_total_div_mw" (default)
  10. IF power.renewable_type is null: no action (now allowed by optional status)
  11. VALIDATE against v1.1 schema
```

### 7.2 Migration Status

| Project | v1.0 Completeness | v1.1 Completeness (est.) | Migration Complexity |
|---------|-------------------|--------------------------|---------------------|
| Normand'Hy | 58.6% | ~62% | Low — CAPEX confidence inferrable; narrative summary writeable from known fields |
| Masshylia | 36.2% | ~42% | Low — pre-FID project; tier and phase easily set |
| Holland Hydrogen I | 60.3% | ~65% | Low — best-documented project, richest narrative |
| Hamburg Green Hydrogen Hub | 55.2% | ~60% | Low — similar to Normand'Hy profile |
| HyDeal España | 24.1% | ~32% | Low — giga-scale aspirational, appropriately tier_1 |

**Conclusion:** Migration from v1.0 to v1.1 is zero-risk. No data will be lost because all removed fields had 0% fill rate in tested projects. All new fields can be populated from existing structured data or analyst judgment.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Knowledge Architect | Initial change log for v1.0 → v1.1 migration |
