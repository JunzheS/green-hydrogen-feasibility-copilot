# Green Hydrogen Project Feasibility Copilot — Knowledge Architecture v1.1

**Document Version:** 1.1.0
**Date:** 2026-06-05
**Status:** **FROZEN** — Gold Dataset v1 Construction Schema
**Author:** Senior Knowledge Architect
**Target System:** Local RAG-based Multi-Agent Copilot
**Predecessor:** database_architecture.md v1.0.0 (2026-06-05)
**Schema Review Basis:** Stress test against 5 European green hydrogen projects (see schema_review_report.md)
**Change Log:** See schema_change_log.md for detailed v1.0 → v1.1 modifications

---

## Table of Contents

1. [Overview & Design Principles](#1-overview--design-principles)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Folder Structure](#3-folder-structure)
4. [Schema 1: Project Reference Database v1.1](#4-schema-1-project-reference-database-v11)
5. [Schema 2: Technology Knowledge Card v1](#5-schema-2-technology-knowledge-card-v1)
6. [Schema 3: Risk Database v1](#6-schema-3-risk-database-v1)
7. [Schema 4: Cost Database v1](#7-schema-4-cost-database-v1)
8. [Cross-Reference Strategy](#8-cross-reference-strategy)
9. [RAG Integration Guidelines](#9-rag-integration-guidelines)
10. [Embedding & Chunking Strategy](#10-embedding--chunking-strategy)
11. [Indexing Architecture](#11-indexing-architecture)
12. [Governance & Maintenance](#12-governance--maintenance)
13. [Appendix: JSON Templates](#13-appendix-json-templates)

---

## 1. Overview & Design Principles

### 1.1 System Purpose

This knowledge architecture supports a **local RAG-based AI Copilot** that assists Project Managers, PMOs, and Engineering Consultants during **pre-feasibility assessment** of industrial green hydrogen projects. The system is scoped exclusively to **PEM (Proton Exchange Membrane)** and **Alkaline** electrolysis technologies.

### 1.2 Core Design Principles

| Principle | Description | Architectural Implication |
|-----------|-------------|---------------------------|
| **RAG-First** | Every schema is designed for embedding-based semantic retrieval | Rich textual fields, metadata for hybrid search filtering |
| **Filterability** | Users must slice data by technology, scale, region, maturity | Consistent categorical fields with controlled vocabularies |
| **Source Traceability** | Every fact links to its origin document | Mandatory `source` blocks in every entity |
| **Cross-Referencing** | Entities link bidirectionally (project → risks → costs → technology) | FK-based references with relationship indexes |
| **Cost-Aware** | CAPEX estimation is a core downstream task | Granular cost decomposition with confidence scoring |
| **Risk-Aware** | Risk analysis is a core downstream task | Structured risk taxonomy linked to real project evidence |
| **Scalable** | Schema must accommodate 1000+ projects, 200+ risks, 100+ cost entries | Normalized structure, index-ready fields |
| **Human-Readable** | JSON artifacts must be editable by domain experts without tooling | Flat structures where possible, clear field naming |
| **Technology-Scoped** | PEM and Alkaline only — no SOEC, AEM, or other technologies | Enum-constrained technology fields |
| **Data Honesty** | Distinguish stated facts from analyst estimates | `_verified`, `_confidence`, and `_method` sub-fields on estimated values |
| **Completeness-Aware** | Users must filter by data richness | `data_completeness_tier` on every entity |
| **Freshness-Tracked** | Stale data must be detectable | `last_data_update` on every entity; separate from pipeline `last_indexed` |
| **Narrative-Driven RAG** | Natural language summaries outperform structured fields for embedding | `narrative_summary` is mandatory; it feeds `text_for_embedding` |

### 1.3 What Changed in v1.1

This version incorporates findings from a stress test that attempted to populate the v1.0 Project Reference Schema using publicly available data for 5 European green hydrogen projects (Normand'Hy, Masshylia, Holland Hydrogen I, Hamburg Green Hydrogen Hub, HyDeal España). Key findings:

- **Average v1.0 completeness:** 43.6% (range: 24.1%–60.3%)
- **4 fields removed:** Fields with 0% public fill rate (IRR, capacity factor, CAPEX breakdown flag, stack pressure type)
- **10 fields added:** Data quality, narrative, and traceability fields
- **1 field demoted** from mandatory to optional: `power.renewable_type`

See [schema_change_log.md](schema_change_log.md) for the complete modification record.

### 1.4 Target Use Cases (RAG Queries)

| Use Case | Example Query | Primary Schema(s) |
|----------|--------------|-------------------|
| **Similar Project Lookup** | "Find PEM projects >50 MW in Europe operational after 2020" | Project Reference |
| **Technology Comparison** | "Compare PEM vs Alkaline stack lifetime and efficiency at 100 MW scale" | Technology Knowledge Card |
| **CAPEX Estimation** | "Estimate CAPEX range for a 200 MW Alkaline project in MENA region" | Cost Database + Project Reference |
| **Risk Identification** | "What are the top risks for first-of-a-kind PEM projects?" | Risk Database |
| **Feasibility Scoring** | "Score feasibility of a 50 MW PEM project with grid-connected solar in Chile" | All schemas (multi-agent orchestration) |
| **Report Generation** | "Generate a pre-feasibility summary comparing 3 reference projects" | Project Reference + Cost + Risk |

---

## 2. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     RAG QUERY ORCHESTRATOR                           │
│  (Agent Router: Query Classification → Schema Routing → Synthesis)  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │   PROJECT    │ │  TECHNOLOGY  │ │     RISK     │ │    COST    │ │
│  │  REFERENCES  │ │    CARDS     │ │   LIBRARY    │ │  LIBRARY   │ │
│  │   (JSON)     │ │   (JSON)     │ │   (JSON)     │ │  (JSON)    │ │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬─────┘ │
│         │                │                │                │       │
│  ┌──────┴────────────────┴────────────────┴────────────────┴─────┐ │
│  │                    HYBRID SEARCH INDEX                          │ │
│  │  ┌──────────────────┐  ┌──────────────────┐                    │ │
│  │  │ Vector Index     │  │ Keyword/Metadata │                    │ │
│  │  │ (embeddings/)    │  │ Index (indexes/) │                    │ │
│  │  └──────────────────┘  └──────────────────┘                    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │                   SOURCE DOCUMENTS                              │ │
│  │  (PDFs, spreadsheets, reports, papers — raw ingested files)    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.1 Data Flow

```
Source Documents → Ingestion Pipeline → Structured JSON Entities
                                          │
                                          ├→ Vector Embedding → embeddings/vectors/
                                          ├→ Metadata Extraction → embeddings/metadata/
                                          └→ Keyword Indexing → indexes/
```

### 2.2 v1.1 Filtering Enhancements

The v1.1 schema introduces filtering by data quality, enabling retrieval-time decisions:

```
Retrieval Query
  ├─ Filter: data_completeness_tier ≥ tier_2_intermediate (exclude sparse records)
  ├─ Filter: project_phase_at_collection IN [construction, operational] (mature projects only)
  ├─ Filter: last_data_update > 2025-01-01 (fresh data only)
  ├─ Filter: is_first_of_a_kind = false (exclude FOAK if benchmarking)
  └─ Filter: technology.technology_selection_status = confirmed (only firm data)
```

---

## 3. Folder Structure

```
/knowledge_base/
│
├── technology_cards/                  # Structured technology knowledge entries
│   ├── pem/                           # PEM electrolysis technology cards
│   │   └── {technology_id}.json       # e.g., TC-PEM-001.json
│   └── alkaline/                      # Alkaline electrolysis technology cards
│       └── {technology_id}.json       # e.g., TC-ALK-001.json
│
├── project_references/                # Structured project reference entries (v1.1 schema)
│   ├── operational/                   # Commissioned & producing hydrogen
│   │   └── {project_id}.json          # e.g., PR-OP-001.json
│   ├── under_construction/            # FID taken, under construction
│   │   └── {project_id}.json          # e.g., PR-UC-001.json
│   ├── planned/                       # Announced, pre-FID
│   │   └── {project_id}.json          # e.g., PR-PL-001.json
│   └── decommissioned/                # Shut down or cancelled (for lessons learned)
│       └── {project_id}.json          # e.g., PR-DC-001.json
│
├── risk_library/                      # Structured risk entries
│   ├── technical/                     # Technology & engineering risks
│   │   └── {risk_id}.json
│   ├── financial/                     # CAPEX, OPEX, funding risks
│   │   └── {risk_id}.json
│   ├── regulatory/                    # Permitting, policy, certification risks
│   │   └── {risk_id}.json
│   ├── operational/                   # O&M, supply chain, workforce risks
│   │   └── {risk_id}.json
│   ├── market/                        # Hydrogen demand, offtake, pricing risks
│   │   └── {risk_id}.json
│   └── environmental/                 # Water, land, emissions, social license risks
│       └── {risk_id}.json
│
├── cost_library/                      # Structured CAPEX cost entries
│   ├── electrolyzer_stack/            # Stack-specific costs
│   │   └── {cost_id}.json
│   ├── balance_of_plant/              # BOP: piping, instrumentation, controls
│   │   └── {cost_id}.json
│   ├── civil_works/                   # Site preparation, buildings, foundations
│   │   └── {cost_id}.json
│   ├── power_supply/                  # Transformer, rectifier, grid connection
│   │   └── {cost_id}.json
│   ├── water_treatment/               # Water purification, desalination if needed
│   │   └── {cost_id}.json
│   ├── hydrogen_processing/           # Compression, purification, drying
│   │   └── {cost_id}.json
│   ├── storage/                       # H₂ storage (tanks, caverns, pipelines)
│   │   └── {cost_id}.json
│   └── indirect_costs/                # EPC, owner's costs, contingency, commissioning
│       └── {cost_id}.json
│
├── reports/                           # Generated reports (output artifacts)
│   ├── feasibility_assessments/       # Generated pre-feasibility reports
│   ├── benchmarking/                  # Project comparison reports
│   └── risk_assessments/              # Generated risk assessment reports
│
├── source_documents/                  # Raw ingested source materials
│   ├── academic_papers/               # Peer-reviewed research papers (PDF)
│   ├── industry_reports/              # IEA, IRENA, BloombergNEF, WoodMac reports (PDF)
│   ├── project_data/                  # Press releases, investor presentations, EPC data
│   ├── standards/                     # ISO, IEC, ASME, CEN standards documents
│   └── news_articles/                 # Industry news, project announcements
│
├── indexes/                           # Keyword & metadata search indexes
│   ├── project_index.json             # Inverted index for project references
│   ├── technology_index.json          # Inverted index for technology cards
│   ├── risk_index.json                # Inverted index for risk library
│   ├── cost_index.json                # Inverted index for cost library
│   └── cross_reference_index.json     # Bidirectional relationship index
│
├── embeddings/                        # Vector embeddings for semantic search
│   ├── vectors/                       # FAISS / ChromaDB vector store files
│   │   ├── projects.faiss
│   │   ├── technologies.faiss
│   │   ├── risks.faiss
│   │   └── costs.faiss
│   └── metadata/                      # Embedding metadata & chunk maps
│       ├── chunks_projects.json
│       ├── chunks_technologies.json
│       ├── chunks_risks.json
│       └── chunks_costs.json
│
└── templates/                         # JSON schema templates for data entry
    ├── project_reference_template_v1.1.json    ← OFFICIAL Gold Dataset template
    ├── project_reference_template.json         ← v1.0 (archived reference only)
    ├── technology_card_template.json
    ├── risk_template.json
    └── cost_template.json
```

---

## 4. Schema 1: Project Reference Database v1.1

### 4.1 Purpose

Store structured references to real-world industrial green hydrogen projects. This schema is the **backbone** of the Copilot — it feeds similar-project lookup, CAPEX benchmarking, risk identification, and feasibility scoring.

**v1.1 Improvements over v1.0:**
- Removed 4 fields with 0% public fill rate (IRR, CAPEX breakdown flag, capacity factor, stack pressure type)
- Added 10 fields for data quality management and narrative enrichment
- Demoted `power.renewable_type` from mandatory to optional (60% public fill rate)
- Added a Data Management block for filtering by data richness and freshness

### 4.2 Schema Definition

#### 4.2.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 1 | `project_id` | `string` | Unique identifier, format: `PR-{STATUS}-{NNN}` (e.g., `PR-OP-001`) | **Yes** | A |
| 2 | `project_name` | `string` | Official project name | **Yes** | A |
| 3 | `alias_names` | `string[]` | Alternative names, former names, local names | No | B |
| 4 | `status` | `enum` | `operational` \| `under_construction` \| `planned` \| `decommissioned` \| `cancelled` | **Yes** | A |
| 5 | `status_detail` | `string` | Free-text status nuance (e.g., "75% of electrolyzers delivered; commissioning expected 2026") | No | B |

#### 4.2.2 Data Management Block *(NEW in v1.1)*

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 6 | `data_management.data_completeness_tier` | `enum` | `tier_1_basic` \| `tier_2_intermediate` \| `tier_3_detailed` \| `tier_4_full` | **Yes** | A |
| 7 | `data_management.project_phase_at_collection` | `enum` | `pre_feasibility` \| `feasibility` \| `pre_fid` \| `post_fid` \| `construction` \| `commissioning` \| `operational` | **Yes** | A |
| 8 | `data_management.last_data_update` | `string` | ISO 8601 datetime of last data change (business field, NOT pipeline field) | **Yes** | A |
| 9 | `data_management.narrative_summary` | `string` | Human-written 3–5 sentence project summary. Max 2000 chars. **Primary RAG embedding source.** | **Yes** | A |
| 10 | `data_management.is_first_of_a_kind` | `boolean` | Is this a first-of-a-kind project? (scale/tech/region/developer) | No | B |
| 11 | `data_management.related_project_ids` | `string[]` | FK references to related projects (shared developer, infrastructure, predecessor/successor) | No | B |

#### 4.2.3 Data Completeness Tier Criteria

| Tier | Criteria | Expected Completeness | Typical Projects |
|------|----------|----------------------|------------------|
| **tier_1_basic** | Identity + status + location + capacity + primary offtake filled | 25–40% | Pre-FID announced projects (e.g., HyDeal España, Masshylia) |
| **tier_2_intermediate** | Tier 1 + technology confirmed + timeline + developer + total CAPEX | 40–60% | Post-FID, pre-construction or under construction |
| **tier_3_detailed** | Tier 2 + stack count + power details + water details + offtaker names | 60–80% | Well-documented construction/operational projects (e.g., HH1) |
| **tier_4_full** | Tier 3 + CAPEX per kW + LCOH + storage details + lenders | 80%+ | Operational projects with published financials (rare) |

#### 4.2.4 Location Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 12 | `location.country` | `string` | Country (ISO 3166-1) | **Yes** | A |
| 13 | `location.region` | `string` | Sub-national region / state / province | No | B |
| 14 | `location.city` | `string` | Nearest city or industrial zone | No | B |
| 15 | `location.coordinates.lat` | `number` | Latitude (decimal degrees) | No | B |
| 16 | `location.coordinates.lon` | `number` | Longitude (decimal degrees) | No | B |
| 17 | `location.coordinates_verified` | `boolean` | Are coordinates from official project documentation? Default: `false` *(NEW in v1.1)* | No | B |
| 18 | `location.region_classification` | `enum` | `europe` \| `north_america` \| `latin_america` \| `mena` \| `sub_saharan_africa` \| `asia_pacific` \| `china` \| `india` \| `australia` \| `other` | **Yes** | A |

#### 4.2.5 Technology Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 19 | `technology.type` | `enum` | `PEM` \| `Alkaline` \| `PEM+Alkaline` (hybrid) | **Yes** | A |
| 20 | `technology.technology_selection_status` | `enum` | `confirmed` \| `announced` \| `not_selected` *(NEW in v1.1)* | No | B |
| 21 | `technology.electrolyzer_manufacturer` | `string` | Electrolyzer OEM name | No | B |
| 22 | `technology.electrolyzer_model` | `string` | Specific stack/module model if known | No | B |
| 23 | `technology.technology_card_ref` | `string` | Foreign key → `technology_cards/{technology_id}.json` | No | B |

> **v1.1 note:** `technology.stack_pressure_type` was removed. It is a technology-inherent property, not project-specific. Retrieve it via FK join to the Technology Card.

#### 4.2.6 Capacity Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 24 | `capacity.electrolyzer_capacity_mw` | `number` | Total electrolyzer nameplate capacity (MWₑ) | **Yes** | A |
| 25 | `capacity.electrolyzer_capacity_mw_source` | `enum` | `stated` \| `estimated` \| `calculated` | No | B |
| 26 | `capacity.hydrogen_output_kg_per_day` | `number` | Design H₂ output (kg/day) | No | B |
| 27 | `capacity.hydrogen_output_tons_per_year` | `number` | Design H₂ output (tons/year) | No | B |
| 28 | `capacity.number_of_stacks` | `integer` | Number of electrolyzer stacks | No | B |
| 29 | `capacity.stack_capacity_mw` | `number` | Individual stack rating (MWₑ) | No | B |

#### 4.2.7 Power Supply Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 30 | `power.renewable_type` | `enum` | `solar_pv` \| `onshore_wind` \| `offshore_wind` \| `solar_pv_wind_hybrid` \| `hydro` \| `grid_mix` \| `other` | No *(demoted in v1.1)* | B |
| 31 | `power.renewable_capacity_mw` | `number` | Dedicated renewable capacity (MW) | No | B |
| 32 | `power.grid_connection` | `boolean` | Is the project grid-connected? | No | B |
| 33 | `power.grid_connection_detail` | `string` | Description of grid connection arrangement | No | B |
| 34 | `power.ppa_structure` | `string` | Power purchase agreement structure (if known) | No | B |

> **v1.1 note:** `power.expected_capacity_factor_percent` was removed. It is an engineering modeling parameter, not a publicly documented field. If needed, use assumed defaults per technology/region in a separate `technical_assumptions` entity.

#### 4.2.8 Water Supply Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 35 | `water.source_type` | `enum` | `freshwater` \| `seawater_desalination` \| `brackish_desalination` \| `wastewater_recycled` \| `municipal` \| `other` | No | B |
| 36 | `water.consumption_cubic_m_per_hour` | `number` | Water consumption (m³/h). May be estimated from output. | No | C |
| 37 | `water.water_treatment_provider` | `string` | Water treatment EPC/OEM | No | B |

#### 4.2.9 Hydrogen Offtake Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 38 | `offtake.primary_application` | `enum` | `ammonia` \| `methanol` \| `refinery` \| `steel` \| `mobility` \| `grid_injection` \| `industrial_heat` \| `export` \| `other` | **Yes** | A |
| 39 | `offtake.secondary_applications` | `enum[]` | Secondary offtake uses | No | B |
| 40 | `offtake.offtaker_name` | `string` | Name of offtaker if known | No | B |
| 41 | `offtake.offtake_agreement_type` | `string` | Type of offtake agreement (rarely public; commercially sensitive) | No | C |
| 42 | `offtake.h2_storage_type` | `enum` | `compressed_gas` \| `liquid` \| `ammonia` \| `LOHC` \| `pipeline` \| `salt_cavern` \| `none` \| `other` | No | B |
| 43 | `offtake.h2_storage_capacity_kg` | `number` | H₂ storage capacity (kg). Very rarely public. | No | C |

#### 4.2.10 Project Stakeholders Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 44 | `stakeholders.developer` | `string` | Lead project developer | **Yes** | A |
| 45 | `stakeholders.developer_type` | `enum` | `utility` \| `oil_and_gas` \| `industrial_gas` \| `renewable_developer` \| `chemical_company` \| `consortium` \| `startup` \| `state_owned` \| `other` | No | B |
| 46 | `stakeholders.co_developers` | `string[]` | Co-developers / JV partners | No | B |
| 47 | `stakeholders.epc_contractor` | `string` | EPC contractor | No | B |
| 48 | `stakeholders.operations_operator` | `string` | O&M operator | No | B |
| 49 | `stakeholders.financial_advisors` | `string[]` | Financial advisors (rarely public) | No | C |
| 50 | `stakeholders.lenders` | `string[]` | Debt providers / lenders (rarely public except EIB/public banks) | No | C |

#### 4.2.11 Financial Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 51 | `financial.total_capex_eur` | `number` | Total project CAPEX (EUR) | No | B |
| 52 | `financial.capex_per_kw_eur` | `number` | CAPEX per kW installed (EUR/kW) | No | B |
| 53 | `financial.capex_per_kw_method` | `enum` | `stated` \| `calculated_total_div_mw` *(NEW in v1.1)* | No | B |
| 54 | `financial.capex_confidence` | `enum` | `official` \| `media_report` \| `analyst_estimate` \| `calculated` *(NEW in v1.1)* | No | B |
| 55 | `financial.capex_year_reference` | `integer` | Year of CAPEX data (for inflation adjustment) | No | B |
| 56 | `financial.funding_sources` | `string[]` | e.g., `["equity", "project_finance_debt", "eu_grant", "government_subsidy"]` | No | B |
| 57 | `financial.total_investment_decision_date` | `string` | FID date (ISO 8601 date or year) | No | B |
| 58 | `financial.lcoh_eur_per_kg` | `number` | Levelized cost of hydrogen (EUR/kg) if publicly stated. Rare. | No | C |

> **v1.1 removals:** `financial.expected_irr_percent` (never public) and `financial.capex_breakdown_available` (always false for public data; redundant with cost_library entries).

#### 4.2.12 Timeline Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 59 | `timeline.announcement_date` | `string` | Project announcement date (ISO 8601) | No | B |
| 60 | `timeline.fid_date` | `string` | Final investment decision date | No | B |
| 61 | `timeline.construction_start_date` | `string` | Construction start date | No | B |
| 62 | `timeline.commissioning_date` | `string` | Commissioning / COD date | No | B |
| 63 | `timeline.construction_duration_months` | `integer` | Construction duration (months). Calculable from dates above. | No | B |
| 64 | `timeline.current_operational_year` | `integer` | Current year of operation (if operational, N/A otherwise) | No | B |

#### 4.2.13 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 65 | `sources` | `object[]` | Array of source references | **Yes** | A |
| 65a | `sources[].source_id` | `string` | Unique source identifier | **Yes** | — |
| 65b | `sources[].source_type` | `enum` | `press_release` \| `investor_presentation` \| `industry_report` \| `academic_paper` \| `news_article` \| `government_announcement` \| `company_filing` \| `conference_presentation` \| `expert_interview` \| `database` | **Yes** | — |
| 65c | `sources[].title` | `string` | Source document title | **Yes** | — |
| 65d | `sources[].url` | `string` | URL (if publicly available) | No | — |
| 65e | `sources[].local_file_ref` | `string` | Relative path to local copy in `source_documents/` | No | — |
| 65f | `sources[].publication_date` | `string` | Date of source publication (ISO 8601) | No | — |
| 65g | `sources[].retrieval_date` | `string` | Date source was retrieved | **Yes** | — |
| 65h | `sources[].confidence` | `enum` | `high` \| `medium` \| `low` — reliability of this source | **Yes** | — |

#### 4.2.14 RAG Metadata Block

| # | Field Name | Data Type | Description | Mandatory | Tier |
|---|-----------|-----------|-------------|-----------|------|
| 66 | `rag_metadata.chunk_id` | `string` | Identifier for the chunked portion of this record | No | — |
| 67 | `rag_metadata.embedding_model` | `string` | Embedding model used (e.g., `text-embedding-3-large`) | No | — |
| 68 | `rag_metadata.embedding_version` | `string` | Version of embedding | No | — |
| 69 | `rag_metadata.last_indexed` | `string` | ISO 8601 timestamp of last embedding pipeline run | No | — |
| 70 | `rag_metadata.text_for_embedding` | `string` | Auto-generated concatenation of `narrative_summary` + key structured fields. Pipeline-populated. | **Yes** | — |
| 71 | `rag_metadata.keywords` | `string[]` | Controlled-vocabulary keywords for hybrid search | **Yes** | — |
| 72 | `rag_metadata.tags` | `string[]` | User-defined tags for flexible categorization | No | — |

### 4.3 Field Classification Summary (Category A / B / C)

| Category | Count | Description |
|----------|-------|-------------|
| **Category A (Essential)** | 16 mandatory + 2 pipeline | Fields with ≥80% public fill rate; primary retrieval/filter dimensions |
| **Category B (Optional)** | 46 fields | Fields with 20–79% fill rate; enrich retrieval quality when available |
| **Category C (Archive-level)** | 6 fields | Rarely available from public sources; kept for completeness but low retrieval impact |

### 4.4 Mandatory Fields (v1.1)

The following 16 fields MUST be populated for a record to reach `published` status:

1. `project_id`
2. `project_name`
3. `status`
4. `data_management.data_completeness_tier`
5. `data_management.project_phase_at_collection`
6. `data_management.last_data_update`
7. `data_management.narrative_summary`
8. `location.country`
9. `location.region_classification`
10. `technology.type`
11. `capacity.electrolyzer_capacity_mw`
12. `offtake.primary_application`
13. `stakeholders.developer`
14. `sources[]` (at minimum: source_id, source_type, title)
15. `rag_metadata.text_for_embedding` *(pipeline-populated)*
16. `rag_metadata.keywords` *(pipeline-populated)*

### 4.5 Controlled Vocabularies

#### Status Values
```
operational | under_construction | planned | decommissioned | cancelled
```

#### Data Completeness Tiers *(NEW in v1.1)*
```
tier_1_basic | tier_2_intermediate | tier_3_detailed | tier_4_full
```

#### Project Phase at Collection *(NEW in v1.1)*
```
pre_feasibility | feasibility | pre_fid | post_fid | construction | commissioning | operational
```

#### Technology Types
```
PEM | Alkaline | PEM+Alkaline
```

#### Technology Selection Status *(NEW in v1.1)*
```
confirmed | announced | not_selected
```

#### Region Classifications
```
europe | north_america | latin_america | mena | sub_saharan_africa |
asia_pacific | china | india | australia | other
```

#### Renewable Types
```
solar_pv | onshore_wind | offshore_wind | solar_pv_wind_hybrid | hydro | grid_mix | other
```

#### Primary Applications (Offtake)
```
ammonia | methanol | refinery | steel | mobility | grid_injection |
industrial_heat | export | other
```

#### CAPEX Confidence Levels *(NEW in v1.1)*
```
official | media_report | analyst_estimate | calculated
```

#### CAPEX per kW Method *(NEW in v1.1)*
```
stated | calculated_total_div_mw
```

#### Source Confidence
```
high | medium | low
```

### 4.6 RAG Chunking Strategy

Each project reference is stored as a **single JSON file** but is chunked for embedding as follows:

- **Chunk 1 (Identity + Data Management + Narrative):** Fields 1–11 — the richest semantic chunk; feeds most queries
- **Chunk 2 (Location + Technology):** Fields 12–23 — where and what technology
- **Chunk 3 (Capacity + Power + Water):** Fields 24–37 — technical specifications
- **Chunk 4 (Offtake + Stakeholders):** Fields 38–50 — commercial arrangements
- **Chunk 5 (Financial + Timeline):** Fields 51–64 — cost and schedule

Each chunk is embedded separately and linked via `project_id` + `chunk_id` reference in `rag_metadata`.

### 4.7 `text_for_embedding` Template (v1.1)

```
Generated from: {narrative_summary}. {project_name}. Status: {status} ({status_detail}).
Located in {location.country}, {location.region_classification}. Phase: {project_phase_at_collection}.
{technology.type} electrolysis ({technology_selection_status}), manufactured by {technology.electrolyzer_manufacturer}.
Capacity: {capacity.electrolyzer_capacity_mw} MW. Produces {capacity.hydrogen_output_tons_per_year} t/yr H₂.
Powered by {power.renewable_type} ({power.renewable_capacity_mw} MW). Water source: {water.source_type}.
Primary offtake: {offtake.primary_application} to {offtake.offtaker_name}.
Developed by {stakeholders.developer} ({stakeholders.developer_type}).
Total CAPEX: {financial.total_capex_eur} EUR ({financial.capex_per_kw_eur} EUR/kW, {financial.capex_confidence} confidence).
FID: {timeline.fid_date}. Expected COD: {timeline.commissioning_date}.
First-of-a-kind: {is_first_of_a_kind}. Completeness tier: {data_completeness_tier}.
Keywords: {keywords}. Tags: {tags}.
```

---

## 5. Schema 2: Technology Knowledge Card v1

*(Unchanged from v1.0 — see database_architecture.md §5 for the complete schema definition.)*

**v1.1 note:** `stack_pressure_type` was moved from the Project Reference Schema to the Technology Knowledge Card. When creating TC-PEM-001 and TC-ALK-001, ensure this field is populated with the correct technology-inherent pressure type.

---

## 6. Schema 3: Risk Database v1

*(Unchanged from v1.0 — see database_architecture.md §6 for the complete schema definition.)*

---

## 7. Schema 4: Cost Database v1

*(Unchanged from v1.0 — see database_architecture.md §7 for the complete schema definition.)*

**v1.1 note:** The cost database's `context.project_reference_id` FK now references a v1.1 project record. CAPEX confidence levels (`financial.capex_confidence`) on the project record should be consistent with `confidence.level` on cost entries linked to that project.

---

## 8. Cross-Reference Strategy

### 8.1 Relationship Map

```
┌──────────────────┐         ┌──────────────────────────────────────┐
│    TECHNOLOGY    │◄────────│     PROJECT REFERENCES (v1.1)         │
│      CARDS      │  FK     │                                      │
│                  │         │ related_project_ids[] (NEW)          │
│ technology_id ───┼─────────┤ technology_card_ref                  │
│                  │         │                                      │
└──────────────────┘         └───┬──────┬───────┬──────────────────┘
                                 │      │       │
                                 │ FK   │ FK    │ related_project_ids
                                 ▼      ▼       ▼
                        ┌──────────┐ ┌──────────┐
                        │   RISK   │ │   COST   │
                        │ LIBRARY  │ │ LIBRARY  │
                        │          │ │          │
                        │ reference│ │ project_ │
                        │ _project │ │ reference│
                        │ _ids[]   │ │ _id      │
                        └──────────┘ └──────────┘

┌──────────────────────────────────────────────────────────┐
│              CROSS-REFERENCE INDEX (v1.1)                │
│  (indexes/cross_reference_index.json)                   │
│                                                          │
│  Maps: project_id → [risk_ids, cost_ids, technology_id,  │
│                       related_project_ids]               │
│  Maps: risk_id    → [project_ids, technology_ids]        │
│  Maps: cost_id    → [project_ids, technology_ids]        │
│  Maps: developer  → [project_ids]  (NEW — derived index) │
└──────────────────────────────────────────────────────────┘
```

### 8.2 v1.1 Cross-Reference Enhancements

- `related_project_ids` enables graph traversal without querying by developer name
- `is_first_of_a_kind` enables risk-to-project linking for FOAK-specific risks
- Developer-based indexing enables portfolio view of multi-project developers

---

## 9. RAG Integration Guidelines

### 9.1 Retrieval Strategy

| Query Type | Retrieval Mode | Schema(s) Targeted | Top-K | v1.1 Enhancement |
|------------|---------------|-------------------|-------|-------------------|
| "Find similar projects" | Hybrid (semantic + metadata filter) | Project Reference | 10–20 | Filter by `data_completeness_tier`; prioritize `narrative_summary` match |
| "Compare technologies" | Semantic | Technology Knowledge Card | 2–5 | No change |
| "Identify risks for X" | Metadata-filtered semantic | Risk Database | 5–15 | Filter by `is_first_of_a_kind` applicability |
| "Estimate CAPEX for X" | Metadata-filtered semantic + aggregation | Cost Database | 10–30 | Weight by `financial.capex_confidence` |
| "Generate feasibility report" | Multi-hop | All schemas | Variable | Narrative-driven synthesis |
| "Answer specific question" | Semantic across all schemas | All schemas | 5–10 | Boost `narrative_summary` match results |

### 9.2 Hybrid Search Design

Combines:
1. **Vector Similarity:** Cosine similarity on `text_for_embedding` (now built from `narrative_summary`)
2. **Metadata Filtering:** Exact match / range / enum filters on structured fields
3. **Keyword Boost:** BM25-style keyword matching on `keywords` and `tags`
4. **Cross-Reference Expansion:** Following FK links to pull related entities
5. **Freshness Boost (NEW):** Boost results with `last_data_update` within 12 months
6. **Completeness Filter (NEW):** Exclude tier_1_basic results for high-confidence queries

### 9.3 v1.1 Retrieval Quality Expectations

| Query Complexity | v1.0 Precision@10 (est.) | v1.1 Precision@10 (est.) | Improvement Driver |
|-----------------|--------------------------|--------------------------|-------------------|
| Simple lookup (technology + region) | 0.80 | 0.85 | Completeness filtering removes noise |
| Intermediate (scale + offtake) | 0.65 | 0.75 | Narrative summary embedding |
| Complex (multi-criteria + CAPEX) | 0.45 | 0.60 | CAPEX confidence weighting |
| Report generation (multi-hop) | 0.35 | 0.50 | Narrative synthesis + cross-references |

---

## 10. Embedding & Chunking Strategy

*(No structural changes from v1.0; updated with `narrative_summary` as primary source.)*

### 10.1 `text_for_embedding` Construction (v1.1)

The `text_for_embedding` field is auto-generated by the pipeline from the `narrative_summary` field, supplemented by key structured fields (see §4.7). The `narrative_summary` is the single most important source because:

- It is in natural language that embedding models understand best
- It captures project essence in 3–5 connected sentences
- It was stress-test validated: human-written summaries of the 5 test projects produced better retrieval results than structured-field concatenation

---

## 11. Indexing Architecture

### 11.1 v1.1 Index Enhancements

The `project_index.json` gains these additional slices:

```json
{
  "by_completeness_tier": {
    "tier_1_basic": ["PR-PL-005"],
    "tier_2_intermediate": ["PR-PL-002", "PR-UC-004"],
    "tier_3_detailed": ["PR-UC-001", "PR-UC-003"],
    "tier_4_full": []
  },
  "by_project_phase": {
    "pre_fid": ["PR-PL-002", "PR-PL-005"],
    "construction": ["PR-UC-001", "PR-UC-003", "PR-UC-004"]
  },
  "by_developer": {
    "Air Liquide": ["PR-UC-001"],
    "Shell": ["PR-UC-003"]
  },
  "first_of_a_kind": ["PR-UC-001"],
  "stale_entries": []
}
```

### 11.2 Index Rebuild Trigger

Added trigger: `last_data_update` changes → rebuild index for that project (not full rebuild).

---

## 12. Governance & Maintenance

### 12.1 v1.1-Specific Governance Rules

| Rule | Description |
|------|-------------|
| **Schema Freeze** | Schema v1.1 is FROZEN for Gold Dataset v1. No schema changes during Gold Dataset construction. |
| **Tier Progression** | A project at tier_1_basic must be advanced to tier_2_intermediate within 90 days of entry (or flagged as "stale at tier_1") |
| **Freshness Policy** | `last_data_update` > 12 months without change → project flagged as `stale` in indexes |
| **Narrative Review** | `narrative_summary` must be reviewed by a second analyst before `published` status |
| **CAPEX Confidence** | Projects with `capex_confidence = calculated` must not be used as primary CAPEX benchmarks; they are supplementary only |

### 12.2 Update Triggers

| Trigger | Action |
|---------|--------|
| New project announced | Create project reference (status: `planned`, tier: determined by available data) |
| Project reaches FID | Update status, timeline, add CAPEX, recalculate tier |
| Project commissioned | Update status to `operational`, add actuals if available |
| New cost report published | Create/update cost entries, refresh related project CAPEX fields |
| Technology improvement reported | Update technology card (new version) |
| Risk materializes in project | Update risk entry with new evidence |
| **last_data_update > 12 months** | **Flag for review; check for publicly available updates** |
| Annual review cycle | Review all entries, update cost year references, re-assess tier |

### 12.3 Schema Evolution Policy (Post-Freeze)

- Schema v1.1 is **FROZEN** until Gold Dataset v1 (30 projects) is complete
- Change requests are logged but not implemented during freeze
- Post-freeze: Schema v1.2 will be scoped based on: (1) Gold Dataset construction experience, (2) RAG retrieval quality metrics, (3) User feedback from Copilot prototype

---

## 13. Appendix: JSON Templates

| Template File | Schema Version | Purpose |
|---------------|---------------|---------|
| `project_reference_template_v1.1.json` | **v1.1 (CURRENT)** | **Official Gold Dataset entry template** |
| `project_reference_template.json` | v1.0 (archived) | Retained for reference only |
| `technology_card_template.json` | v1.0 | Technology knowledge cards |
| `risk_template.json` | v1.0 | Risk library entries |
| `cost_template.json` | v1.0 | Cost data points |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Knowledge Architect | Initial architecture design |
| 1.1.0 | 2026-06-05 | Senior Knowledge Architect | Schema v1.1: removed 4 unreachable fields, added 10 data-quality fields, demoted power.renewable_type, new Data Management block. Schema FROZEN for Gold Dataset v1. |

---

### Freeze Notice

**This document (database_architecture_v1.1.md) defines the FROZEN Schema for Gold Dataset v1.**

All project reference entries created for the Gold Dataset MUST conform to the v1.1 schema defined in §4 of this document. The authoritative entry template is `templates/project_reference_template_v1.1.json`.

No modifications to the Project Reference Schema are permitted during Gold Dataset construction (next 30 projects). Change requests should be logged for consideration in Schema v1.2.

---

*This document is the knowledge foundation for the Green Hydrogen Project Feasibility Copilot — validated against real-world project data, stress-tested for completeness, and frozen for production use.*
