# OPEX Record Schema v1 — Green Hydrogen Project Operating Costs

**Document:** OPEX Record Structure
**Date:** 2026-06-05
**Author:** Hydrogen Economist & Industrial Cost Engineer

---

## 1. Schema Definition

### Core Identity

| # | Field | Type | Description | M |
|---|-------|------|-------------|---|
| 1 | `opex_id` | `string` | Unique ID. Format: `OX-{CATEGORY}-{NNN}`. Example: `OX-ELC-001` | **Yes** |
| 2 | `opex_name` | `string` | Descriptive name. Format: `{Category} — {Detail} — {Tech} {Scale} MW — {Region} {Year}` | **Yes** |
| 3 | `opex_category` | `enum` | `electricity` \| `stack_replacement` \| `maintenance` \| `labor` \| `water_consumables` \| `insurance` \| `land_facilities` \| `regulatory_compliance` \| `other` | **Yes** |
| 4 | `opex_subcategory` | `string` | Per opex_taxonomy_framework.md (e.g., `O3.1_preventive_maintenance`) | **Yes** |
| 5 | `opex_unit` | `enum` | `eur_per_kg_h2` \| `eur_per_kw_per_year` \| `eur_per_year` \| `eur_per_mwh` \| `percent_of_total_opex` | **Yes** |
| 6 | `opex_version` | `string` | Semantic version | **Yes** |
| 7 | `opex_status` | `enum` | `draft` \| `reviewed` \| `published` | **Yes** |
| 8 | `last_review_date` | `string` | ISO 8601 | **Yes** |

### OPEX Data

| # | Field | Type | Description | M |
|---|-------|------|-------------|---|
| 9 | `opex_data.value` | `number` | Central estimate in `opex_unit` | **Yes** |
| 10 | `opex_data.value_low` | `number` | P10 or minimum | No |
| 11 | `opex_data.value_high` | `number` | P90 or maximum | No |
| 12 | `opex_data.cost_year` | `integer` | Year of cost data | **Yes** |
| 13 | `opex_data.percentage_of_opex` | `number` | This category's share of total OPEX (%) | No |
| 14 | `opex_data.percentage_of_lcoh` | `number` | This category's contribution to LCOH (%) | No |

### Context

| # | Field | Type | Description | M |
|---|-------|------|-------------|---|
| 15 | `context.technology_type` | `enum` | `PEM` \| `Alkaline` \| `technology_agnostic` | **Yes** |
| 16 | `context.project_scale_mw` | `number` | Reference plant scale | **Yes** |
| 17 | `context.full_load_hours_per_year` | `number` | Assumed operating hours for €/kg conversion | No |
| 18 | `context.electricity_price_assumption_eur_per_mwh` | `number` | For electricity OPEX records | No |
| 19 | `context.project_reference_id` | `string` | FK → Gold Dataset | No |

### Confidence

| # | Field | Type | Description | M |
|---|-------|------|-------------|---|
| 20 | `confidence.level` | `enum` | `A_actual` \| `B_contracted` \| `C_benchmark` \| `D_estimate` | **Yes** |
| 21 | `confidence.rationale` | `string` | Justification | **Yes** |

### Cost Drivers & Sensitivity

| # | Field | Type | Description |
|---|-------|------|-------------|
| 22 | `sensitivity.primary_driver` | `string` | Main factor driving this cost |
| 23 | `sensitivity.lcoh_impact_per_unit_change` | `string` | Example: "±€0.55/kg per ±€10/MWh electricity price" |
| 24 | `sensitivity.scale_dependency` | `enum` | `strong` \| `moderate` \| `weak` \| `none` |

### Sources & Integration (same pattern as Cost Library)

---

## 2. Mandatory Fields (16)

1-4. `opex_id`, `opex_name`, `opex_category`, `opex_subcategory`
5. `opex_unit`, 6-7. `opex_version`, `opex_status`, 8. `last_review_date`
9. `opex_data.value`, 12. `opex_data.cost_year`
15-16. `context.technology_type`, `context.project_scale_mw`
20-21. `confidence.level`, `confidence.rationale`
22. `sensitivity.primary_driver`
Plus `sources[]` (minimum 1 with source_id, type, title, confidence)

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Hydrogen Economist & Industrial Cost Engineer |
