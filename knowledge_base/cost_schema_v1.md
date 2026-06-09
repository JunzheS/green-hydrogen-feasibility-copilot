# Cost Record Schema v1 — Green Hydrogen Project CAPEX

**Document:** Cost Record Structure Specification
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Industrial Project Controller
**Schema Version:** 1.0.0
**Parent Architecture:** database_architecture_v1.1.md §7
**Taxonomy Reference:** cost_taxonomy_framework.md
**Enhances:** Original cost template with PMO-grade estimation fields

---

## 1. Schema Definition

### 1.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 1 | `cost_id` | `string` | Unique identifier. Format: `CS-{CATEGORY}-{NNN}`. Example: `CS-STK-001` | **Yes** |
| 2 | `cost_name` | `string` | Descriptive name (max 200 chars). Format: `{Technology} {Cost Item} — {Cost Basis} — {Scale} MW — {Region} {Year}`. Example: "PEM Electrolyzer Stack — Installed Cost — 100 MW — Europe 2024" | **Yes** |
| 3 | `cost_category` | `enum` | `electrolyzer_system` \| `electrical_infrastructure` \| `water_systems` \| `hydrogen_processing` \| `civil_construction` \| `thermal_management` \| `instrumentation_controls` \| `indirect_owners_costs` | **Yes** |
| 4 | `cost_subcategory` | `enum` | Subcategory code per cost_taxonomy_framework.md §2. Example: `01.1_electrolyzer_stack` | **Yes** |
| 5 | `cost_basis` | `enum` | `equipment_only` \| `installed_cost` \| `epc_total` \| `all_in`. See §1.2. | **Yes** |
| 6 | `cost_version` | `string` | Semantic version. Example: `1.0.0` | **Yes** |
| 7 | `cost_status` | `enum` | `draft` \| `reviewed` \| `published` \| `superseded` | **Yes** |
| 8 | `supersedes` | `string` | Previous cost_id if this replaces an older entry | No |
| 9 | `last_review_date` | `string` | ISO 8601 date of last review | **Yes** |

### 1.2 Cost Basis Definitions

| Basis | Scope | Typical Use |
|-------|-------|------------|
| `equipment_only` | Ex-works equipment price, no installation, no BOP | OEM budget quotes for stack modules |
| `installed_cost` | Equipment + direct installation (labor, materials, subcontractors) | Category-level benchmarks; stack installed cost |
| `epc_total` | Engineering, procurement, construction, commissioning | EPC contract value (excludes owner's costs and contingency) |
| `all_in` | EPC total + owner's costs + contingency + IDC | Total project CAPEX from Gold Dataset projects |

### 1.3 Cost Data Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 10 | `cost_data.eur_per_kw` | `number` | Central/point estimate (EUR/kW installed capacity) | **Yes** |
| 11 | `cost_data.eur_per_kw_low` | `number` | Low-end estimate (P10 or minimum). Use documented range, not arbitrary. | No |
| 12 | `cost_data.eur_per_kw_high` | `number` | High-end estimate (P90 or maximum) | No |
| 13 | `cost_data.eur_per_kg_per_day` | `number` | Alternate metric: EUR per kg/day H₂ production capacity | No |
| 14 | `cost_data.total_eur` | `number` | Absolute cost (EUR) for the stated scale. Computed: `eur_per_kw × scale_mw × 1000` | No |
| 15 | `cost_data.currency_original` | `string` | Original currency if not EUR (ISO 4217) | No |
| 16 | `cost_data.exchange_rate_used` | `number` | Exchange rate applied to convert to EUR | No |
| 17 | `cost_data.exchange_rate_date` | `string` | Date of exchange rate used (ISO 8601) | No |
| 18 | `cost_data.cost_year` | `integer` | Year of the original cost data (for inflation context) | **Yes** |
| 19 | `cost_data.is_inflation_adjusted` | `boolean` | Has this cost been adjusted for inflation to a base year? | No |
| 20 | `cost_data.inflation_base_year` | `integer` | Base year for inflation adjustment | No |
| 21 | `cost_data.escalation_rate_applied_percent` | `number` | Annual escalation/inflation rate applied | No |
| 22 | `cost_data.percentage_of_total_capex` | `number` | This item's share of total project CAPEX (%). Useful for top-down validation. | No |

### 1.4 Context Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 23 | `context.technology_type` | `enum` | `PEM` \| `Alkaline` \| `PEM+Alkaline` \| `technology_agnostic` | **Yes** |
| 24 | `context.project_scale_mw` | `number` | Project scale this cost applies to (MW) | **Yes** |
| 25 | `context.project_scale_category` | `enum` | `small_<10mw` \| `medium_10-100mw` \| `large_100-500mw` \| `very_large_>500mw` | No |
| 26 | `context.scale_is_extrapolated` | `boolean` | Is this cost extrapolated from data at a different scale? | **Yes** |
| 27 | `context.original_scale_mw` | `number` | If extrapolated, the original data's scale (MW) | No |
| 28 | `context.extrapolation_method` | `string` | If extrapolated: method used. Example: "Power law scaling with exponent 0.7" | No |
| 29 | `context.project_reference_id` | `string` | FK → Gold Dataset project ID (GA-PR-NNN) if from a specific project | No |
| 30 | `context.project_location_region` | `enum` | Region per Project Reference Schema. Default: `europe` | No |
| 31 | `context.project_country` | `string` | Specific country if relevant for labor/material cost context | No |
| 32 | `context.greenfield_or_brownfield` | `enum` | `greenfield` \| `brownfield` \| `expansion` \| `not_applicable` | No |
| 33 | `context.epc_contract_type` | `enum` | `lump_sum_turnkey` \| `epcm` \| `cost_plus` \| `multi_contract` \| `unknown` | No |

### 1.5 Estimation Maturity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 34 | `estimation.aace_class` | `enum` | `class_5_conceptual` \| `class_4_feasibility` \| `class_3_budget` \| `class_2_control` \| `class_1_definitive`. Per AACE 18R-97. | **Yes** |
| 35 | `estimation.expected_accuracy_range` | `string` | Example: "±30%" for Class 4, "±50%" for Class 5 | No |
| 36 | `estimation.estimation_method` | `string` | How was this estimate produced? Example: "OEM budget quotation (2024)", "IEA benchmark (2025 GHR)", "Project actual cost (EPC close-out, 2023)" | No |

### 1.6 Cost Confidence Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 37 | `confidence.level` | `enum` | `A_actual_cost` \| `B_contracted_price` \| `C_industry_benchmark` \| `D_analyst_estimate`. Per cost_confidence_framework.md. | **Yes** |
| 38 | `confidence.rationale` | `string` | Justification for confidence level. Example: "Based on audited actual installed cost from EPC close-out report (Project Alpha, 2024)" | **Yes** |
| 39 | `confidence.range_confidence_percent` | `number` | Confidence interval for low-high range. Example: 80 for P10-P90 range | No |
| 40 | `confidence.data_points_contributing` | `integer` | Number of independent data points behind this estimate | No |
| 41 | `confidence.verified_by_second_source` | `boolean` | Has a second independent source confirmed this? | No |
| 42 | `confidence.second_source_reference` | `string` | Source ID or description of verifying source | No |

### 1.7 Cost Drivers Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 43 | `cost_drivers.primary_drivers` | `string[]` | Main factors driving this cost. Example: `["Iridium spot price", "PFSA membrane cost", "Titanium machining cost"]` | No |
| 44 | `cost_drivers.sensitivity_to_scale` | `enum` | `high` \| `medium` \| `low` — how strongly does this cost scale with plant capacity? | No |
| 45 | `cost_drivers.scaling_exponent` | `number` | If known, the cost-capacity scaling exponent. 1.0 = linear; 0.6-0.8 typical for process equipment. | No |
| 46 | `cost_drivers.learning_rate_percent` | `number` | Technology learning rate (% cost reduction per doubling of cumulative deployed capacity) | No |
| 47 | `cost_drivers.regional_multiplier_notes` | `string` | Regional cost variation. Example: "China −20-30% vs Europe; North America +5-15%" | No |
| 48 | `cost_drivers.exclusions` | `string[]` | What is explicitly NOT included. Critical for preventing misuse in CAPEX aggregation. | **Yes** |
| 49 | `cost_drivers.inclusions` | `string[]` | What IS included (especially important when cost_basis is ambiguous). | No |

### 1.8 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 50 | `sources` | `object[]` | Array of source references. Inherits from Source Governance Framework. Minimum: source_id, source_type, source_quality_level, source_reliability_score, title, publication_date, retrieval_date, confidence. | **Yes** |

### 1.9 Integration Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 51 | `integration.technology_card_reference` | `string` | FK → Technology Card cost_profile section. Example: `TC-PEM-001.cost_profile` | No |
| 52 | `integration.risk_references` | `string[]` | FK → Risk Library entries where this cost is relevant to risk assessment. Example: `["RK-FIN-001"]` | No |
| 53 | `integration.related_cost_ids` | `string[]` | FK → related cost entries (e.g., stack cost + BOP cost = electrolyzer system cost) | No |

### 1.10 RAG Metadata Block

Standard embedding fields: `text_for_embedding`, `keywords`, `last_indexed`.

---

## 2. Mandatory Field Summary (22 fields)

1. `cost_id`, 2. `cost_name`, 3. `cost_category`, 4. `cost_subcategory`, 5. `cost_basis`, 6. `cost_version`, 7. `cost_status`, 8. `last_review_date`, 9. `cost_data.eur_per_kw`, 10. `cost_data.cost_year`, 11. `context.technology_type`, 12. `context.project_scale_mw`, 13. `context.scale_is_extrapolated`, 14. `estimation.aace_class`, 15. `confidence.level`, 16. `confidence.rationale`, 17. `cost_drivers.exclusions`, 18-22. `sources[]` (minimum: source_id, source_type, title, confidence)

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial PMO-enhanced cost record schema |
