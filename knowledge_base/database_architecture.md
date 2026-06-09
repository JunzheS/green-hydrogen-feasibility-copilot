# Green Hydrogen Project Feasibility Copilot — Knowledge Architecture v1

**Document Version:** 1.0.0
**Date:** 2026-06-05
**Status:** Draft — Architecture Design Phase
**Author:** Senior Knowledge Architect
**Target System:** Local RAG-based Multi-Agent Copilot

---

## Table of Contents

1. [Overview & Design Principles](#1-overview--design-principles)
2. [System Architecture Overview](#2-system-architecture-overview)
3. [Folder Structure](#3-folder-structure)
4. [Schema 1: Project Reference Database](#4-schema-1-project-reference-database)
5. [Schema 2: Technology Knowledge Card](#5-schema-2-technology-knowledge-card)
6. [Schema 3: Risk Database](#6-schema-3-risk-database)
7. [Schema 4: Cost Database](#7-schema-4-cost-database)
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
| **Cross-Referencing** | Entities link bidirectionally (project → risks → costs → technology) | UUID-based references with relationship tables |
| **Cost-Aware** | CAPEX estimation is a core downstream task | Granular cost decomposition with confidence scoring |
| **Risk-Aware** | Risk analysis is a core downstream task | Structured risk taxonomy linked to real project evidence |
| **Scalable** | Schema must accommodate 1000+ projects, 200+ risks, 100+ cost entries | Normalized structure, index-ready fields |
| **Human-Readable** | JSON artifacts must be editable by domain experts without tooling | Flat structures where possible, clear field naming |
| **Technology-Scoped** | PEM and Alkaline only — no SOEC, AEM, or other technologies | Enum-constrained technology fields |

### 1.3 Target Use Cases (RAG Queries)

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
│                     RAG QUERY ORCHESTRATOR                          │
│  (Agent Router: Query Classification → Schema Routing → Synthesis) │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │   PROJECT    │ │  TECHNOLOGY  │ │     RISK     │ │    COST    │ │
│  │  REFERENCES  │ │    CARDS     │ │   LIBRARY    │ │  LIBRARY   │ │
│  │   (JSON)     │ │   (JSON)     │ │   (JSON)     │ │  (JSON)    │ │
│  └──────┬───────┘ └──────┬───────┘ └──────┬───────┘ └──────┬─────┘ │
│         │                │                │                │       │
│  ┌──────┴────────────────┴────────────────┴────────────────┴─────┐ │
│  │                    HYBRID SEARCH INDEX                         │ │
│  │  ┌──────────────────┐  ┌──────────────────┐                   │ │
│  │  │ Vector Index     │  │ Keyword/Metadata │                   │ │
│  │  │ (embeddings/)    │  │ Index (indexes/) │                   │ │
│  │  └──────────────────┘  └──────────────────┘                   │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                   SOURCE DOCUMENTS                             │ │
│  │  (PDFs, spreadsheets, reports, papers — raw ingested files)   │ │
│  └───────────────────────────────────────────────────────────────┘ │
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
├── project_references/                # Structured project reference entries
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
│   │   └── {risk_id}.json             # e.g., RK-TEC-001.json
│   ├── financial/                     # CAPEX, OPEX, funding risks
│   │   └── {risk_id}.json             # e.g., RK-FIN-001.json
│   ├── regulatory/                    # Permitting, policy, certification risks
│   │   └── {risk_id}.json             # e.g., RK-REG-001.json
│   ├── operational/                   # O&M, supply chain, workforce risks
│   │   └── {risk_id}.json             # e.g., RK-OPS-001.json
│   ├── market/                        # Hydrogen demand, offtake, pricing risks
│   │   └── {risk_id}.json             # e.g., RK-MKT-001.json
│   └── environmental/                 # Water, land, emissions, social license risks
│       └── {risk_id}.json             # e.g., RK-ENV-001.json
│
├── cost_library/                      # Structured CAPEX cost entries
│   ├── electrolyzer_stack/            # Stack-specific costs
│   │   └── {cost_id}.json             # e.g., CS-STK-001.json
│   ├── balance_of_plant/              # BOP: piping, instrumentation, controls
│   │   └── {cost_id}.json             # e.g., CS-BOP-001.json
│   ├── civil_works/                   # Site preparation, buildings, foundations
│   │   └── {cost_id}.json             # e.g., CS-CIV-001.json
│   ├── power_supply/                  # Transformer, rectifier, grid connection
│   │   └── {cost_id}.json             # e.g., CS-PWR-001.json
│   ├── water_treatment/               # Water purification, desalination if needed
│   │   └── {cost_id}.json             # e.g., CS-WTR-001.json
│   ├── hydrogen_processing/           # Compression, purification, drying
│   │   └── {cost_id}.json             # e.g., CS-HPR-001.json
│   ├── storage/                       # H₂ storage (tanks, caverns, pipelines)
│   │   └── {cost_id}.json             # e.g., CS-STO-001.json
│   └── indirect_costs/                # EPC, owner's costs, contingency, commissioning
│       └── {cost_id}.json             # e.g., CS-IND-001.json
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
    ├── project_reference_template.json
    ├── technology_card_template.json
    ├── risk_template.json
    └── cost_template.json
```

---

## 4. Schema 1: Project Reference Database

### 4.1 Purpose

Store structured references to real-world industrial green hydrogen projects. This schema is the **backbone** of the Copilot — it feeds similar-project lookup, CAPEX benchmarking, risk identification, and feasibility scoring.

### 4.2 Schema Definition

#### 4.2.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 1 | `project_id` | `string` | Unique identifier, format: `PR-{STATUS}-{NNN}` (e.g., `PR-OP-001`) | **Yes** |
| 2 | `project_name` | `string` | Official project name | **Yes** |
| 3 | `alias_names` | `string[]` | Alternative names, former names, local names | No |
| 4 | `status` | `enum` | `operational` \| `under_construction` \| `planned` \| `decommissioned` \| `cancelled` | **Yes** |
| 5 | `status_detail` | `string` | Free-text status nuance (e.g., "Partially commissioned — Phase 1 online, Phase 2 under construction") | No |

#### 4.2.2 Location Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 6 | `location.country` | `string` | Country (ISO 3166-1) | **Yes** |
| 7 | `location.region` | `string` | Sub-national region / state / province | No |
| 8 | `location.city` | `string` | Nearest city or industrial zone | No |
| 9 | `location.coordinates.lat` | `number` | Latitude (decimal degrees) | No |
| 10 | `location.coordinates.lon` | `number` | Longitude (decimal degrees) | No |
| 11 | `location.region_classification` | `enum` | `europe` \| `north_america` \| `latin_america` \| `mena` \| `sub_saharan_africa` \| `asia_pacific` \| `china` \| `india` \| `australia` \| `other` | **Yes** |

#### 4.2.3 Technology Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 12 | `technology.type` | `enum` | `PEM` \| `Alkaline` \| `PEM+Alkaline` (hybrid) | **Yes** |
| 13 | `technology.electrolyzer_manufacturer` | `string` | Electrolyzer OEM name | No |
| 14 | `technology.electrolyzer_model` | `string` | Specific stack/module model if known | No |
| 15 | `technology.stack_pressure_type` | `enum` | `atmospheric` \| `pressurized` \| `differential` | No |
| 16 | `technology.technology_card_ref` | `string` | Foreign key → `technology_cards/{technology_id}.json` | No |

#### 4.2.4 Capacity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 17 | `capacity.electrolyzer_capacity_mw` | `number` | Total electrolyzer nameplate capacity (MWₑ) | **Yes** |
| 18 | `capacity.electrolyzer_capacity_mw_source` | `enum` | `stated` \| `estimated` \| `calculated` | No |
| 19 | `capacity.hydrogen_output_kg_per_day` | `number` | Design H₂ output (kg/day) | No |
| 20 | `capacity.hydrogen_output_tons_per_year` | `number` | Design H₂ output (tons/year) | No |
| 21 | `capacity.number_of_stacks` | `integer` | Number of electrolyzer stacks | No |
| 22 | `capacity.stack_capacity_mw` | `number` | Individual stack rating (MWₑ) | No |

#### 4.2.5 Power Supply Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 23 | `power.renewable_type` | `enum` | `solar_pv` \| `onshore_wind` \| `offshore_wind` \| `solar_pv_wind_hybrid` \| `hydro` \| `grid_mix` \| `other` | **Yes** |
| 24 | `power.renewable_capacity_mw` | `number` | Dedicated renewable capacity (MW) | No |
| 25 | `power.grid_connection` | `boolean` | Is the project grid-connected? | No |
| 26 | `power.grid_connection_detail` | `string` | Description of grid connection arrangement | No |
| 27 | `power.ppa_structure` | `string` | Power purchase agreement structure (if known) | No |
| 28 | `power.expected_capacity_factor_percent` | `number` | Expected/actual capacity factor (%) | No |

#### 4.2.6 Water Supply Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 29 | `water.source_type` | `enum` | `freshwater` \| `seawater_desalination` \| `brackish_desalination` \| `wastewater_recycled` \| `municipal` \| `other` | No |
| 30 | `water.consumption_cubic_m_per_hour` | `number` | Water consumption (m³/h) | No |
| 31 | `water.water_treatment_provider` | `string` | Water treatment EPC/OEM | No |

#### 4.2.7 Hydrogen Offtake Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 32 | `offtake.primary_application` | `enum` | `ammonia` \| `methanol` \| `refinery` \| `steel` \| `mobility` \| `grid_injection` \| `industrial_heat` \| `export` \| `other` | **Yes** |
| 33 | `offtake.secondary_applications` | `enum[]` | Secondary offtake uses | No |
| 34 | `offtake.offtaker_name` | `string` | Name of offtaker if known | No |
| 35 | `offtake.offtake_agreement_type` | `string` | Type of offtake agreement (e.g., "10-year fixed-price") | No |
| 36 | `offtake.h2_storage_type` | `enum` | `compressed_gas` \| `liquid` \| `ammonia` \| `LOHC` \| `pipeline` \| `salt_cavern` \| `none` \| `other` | No |
| 37 | `offtake.h2_storage_capacity_kg` | `number` | H₂ storage capacity (kg) | No |

#### 4.2.8 Project Stakeholders Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 38 | `stakeholders.developer` | `string` | Lead project developer | **Yes** |
| 39 | `stakeholders.developer_type` | `enum` | `utility` \| `oil_and_gas` \| `industrial_gas` \| `renewable_developer` \| `chemical_company` \| `consortium` \| `startup` \| `state_owned` \| `other` | No |
| 40 | `stakeholders.co_developers` | `string[]` | Co-developers / JV partners | No |
| 41 | `stakeholders.epc_contractor` | `string` | EPC contractor | No |
| 42 | `stakeholders.operations_operator` | `string` | O&M operator | No |
| 43 | `stakeholders.financial_advisors` | `string[]` | Financial advisors | No |
| 44 | `stakeholders.lenders` | `string[]` | Debt providers / lenders | No |

#### 4.2.9 Financial Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 45 | `financial.total_capex_eur` | `number` | Total project CAPEX (EUR) | No |
| 46 | `financial.capex_per_kw_eur` | `number` | CAPEX per kW installed (EUR/kW) | No |
| 47 | `financial.capex_breakdown_available` | `boolean` | Is detailed CAPEX breakdown available? | No |
| 48 | `financial.capex_year_reference` | `integer` | Year of CAPEX data (for inflation adjustment) | No |
| 49 | `financial.funding_sources` | `string[]` | e.g., `["equity", "project_finance_debt", "eu_grant", "government_subsidy"]` | No |
| 50 | `financial.total_investment_decision_date` | `string` | FID date (ISO 8601 date or year) | No |
| 51 | `financial.expected_irr_percent` | `number` | Expected/projected IRR (%) | No |
| 52 | `financial.lcoh_eur_per_kg` | `number` | Levelized cost of hydrogen (EUR/kg) if known | No |

#### 4.2.10 Timeline Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 53 | `timeline.announcement_date` | `string` | Project announcement date (ISO 8601) | No |
| 54 | `timeline.fid_date` | `string` | Final investment decision date | No |
| 55 | `timeline.construction_start_date` | `string` | Construction start date | No |
| 56 | `timeline.commissioning_date` | `string` | Commissioning / COD date | No |
| 57 | `timeline.construction_duration_months` | `integer` | Construction duration (months) | No |
| 58 | `timeline.current_operational_year` | `integer` | Current year of operation (if operational) | No |

#### 4.2.11 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 59 | `sources` | `object[]` | Array of source references (see sub-schema below) | **Yes** |
| 59a | `sources[].source_id` | `string` | Unique source identifier | **Yes** |
| 59b | `sources[].source_type` | `enum` | `press_release` \| `investor_presentation` \| `industry_report` \| `academic_paper` \| `news_article` \| `government_announcement` \| `company_filing` \| `conference_presentation` \| `expert_interview` \| `database` | **Yes** |
| 59c | `sources[].title` | `string` | Source document title | **Yes** |
| 59d | `sources[].url` | `string` | URL (if publicly available) | No |
| 59e | `sources[].local_file_ref` | `string` | Relative path to local copy in `source_documents/` | No |
| 59f | `sources[].publication_date` | `string` | Date of source publication (ISO 8601) | No |
| 59g | `sources[].retrieval_date` | `string` | Date source was retrieved | **Yes** |
| 59h | `sources[].confidence` | `enum` | `high` \| `medium` \| `low` — reliability of this source | **Yes** |

#### 4.2.12 RAG Metadata Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 60 | `rag_metadata.chunk_id` | `string` | Identifier for the chunked portion of this record | No |
| 61 | `rag_metadata.embedding_model` | `string` | Embedding model used (e.g., `text-embedding-3-large`) | No |
| 62 | `rag_metadata.embedding_version` | `string` | Version of embedding | No |
| 63 | `rag_metadata.last_indexed` | `string` | ISO 8601 timestamp of last indexing | No |
| 64 | `rag_metadata.text_for_embedding` | `string` | Pre-computed concatenation of key text fields for embedding | **Yes** |
| 65 | `rag_metadata.keywords` | `string[]` | Controlled-vocabulary keywords for hybrid search | **Yes** |
| 66 | `rag_metadata.tags` | `string[]` | User-defined tags for flexible categorization | No |

### 4.3 Controlled Vocabularies

#### Status Values
```
operational | under_construction | planned | decommissioned | cancelled
```

#### Technology Types
```
PEM | Alkaline | PEM+Alkaline
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

#### Source Confidence
```
high | medium | low
```

### 4.4 RAG Chunking Strategy

Each project reference is stored as a **single JSON file** but is chunked for embedding as follows:

- **Chunk 1 (Identity + Location):** Fields 1–11 — project identity and where
- **Chunk 2 (Technology + Capacity):** Fields 12–22 — what technology and how big
- **Chunk 3 (Power + Water + Offtake):** Fields 23–37 — inputs and outputs
- **Chunk 4 (Stakeholders + Financial):** Fields 38–52 — who and how much
- **Chunk 5 (Timeline + Narrative Summary):** Fields 53–58 — when

Each chunk is embedded separately and linked via `project_id` + `chunk_id`. This enables fine-grained retrieval: a query about "PEM stack manufacturers" retrieves Chunk 2 only, not the entire record.

---

## 5. Schema 2: Technology Knowledge Card

### 5.1 Purpose

Capture structured technical knowledge about PEM and Alkaline electrolysis technologies. This schema feeds technology comparison, maturity assessment, and technology risk evaluation. Each card represents a **technology variant** (not a specific product) — e.g., "PEM Electrolysis — Pressurized — Large Scale (> 100 MW)" is one card.

### 5.2 Schema Definition

#### 5.2.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 1 | `technology_id` | `string` | Unique identifier, format: `TC-{TYPE}-{NNN}` (e.g., `TC-PEM-001`) | **Yes** |
| 2 | `technology_name` | `string` | Human-readable technology name | **Yes** |
| 3 | `technology_type` | `enum` | `PEM` \| `Alkaline` | **Yes** |
| 4 | `technology_subtype` | `string` | Variant (e.g., "Pressurized PEM", "Atmospheric Alkaline", "Zero-gap Alkaline") | No |
| 5 | `card_version` | `string` | Semantic version of this card (e.g., `1.2.0`) | **Yes** |
| 6 | `card_status` | `enum` | `draft` \| `reviewed` \| `published` \| `superseded` | **Yes** |
| 7 | `supersedes` | `string` | Reference to previous version `technology_id` | No |
| 8 | `superseded_by` | `string` | Reference to newer version `technology_id` | No |

#### 5.2.2 Technology Maturity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 9 | `maturity.trl_level` | `integer` | Technology Readiness Level (1–9, per EU H2020 / NASA scale) | **Yes** |
| 10 | `maturity.trl_rationale` | `string` | Justification for TRL assignment | **Yes** |
| 11 | `maturity.trl_assessment_date` | `string` | Date of TRL assessment (ISO 8601) | No |
| 12 | `maturity.trl_assessed_by` | `string` | Organization/person who assessed TRL | No |
| 13 | `maturity.commercial_maturity` | `enum` | `r_and_d` \| `pilot` \| `demonstration` \| `early_commercial` \| `commercial` \| `mature` | **Yes** |
| 14 | `maturity.mrl_level` | `integer` | Manufacturing Readiness Level (1–10) | No |
| 15 | `maturity.technology_learning_rate_percent` | `number` | Observed learning rate (% cost reduction per doubling of cumulative capacity) | No |
| 16 | `maturity.cumulative_global_capacity_mw` | `number` | Estimated cumulative installed global capacity (MW) | No |
| 17 | `maturity.cumulative_capacity_year` | `integer` | Year of cumulative capacity estimate | No |

#### 5.2.3 Technical Performance Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 18 | `performance.nominal_current_density_a_per_cm2` | `number` | Nominal current density (A/cm²) | No |
| 19 | `performance.current_density_range_a_per_cm2` | `object` | `{min, max, typical}` current density range | No |
| 20 | `performance.system_efficiency_kwh_per_kg_h2` | `number` | System-level electrical consumption (kWhₑ/kg H₂) | **Yes** |
| 21 | `performance.system_efficiency_lhv_percent` | `number` | System efficiency based on H₂ LHV (%) | No |
| 22 | `performance.stack_lifetime_hours` | `number` | Expected stack lifetime (operating hours) | **Yes** |
| 23 | `performance.stack_lifetime_years` | `number` | Expected stack lifetime (calendar years at nominal operation) | No |
| 24 | `performance.stack_degradation_rate_percent_per_year` | `number` | Expected degradation rate (% efficiency loss per year) | No |
| 25 | `performance.operating_temperature_range_c` | `object` | `{min, max, nominal}` operating temperature (°C) | **Yes** |
| 26 | `performance.operating_pressure_range_bar` | `object` | `{min, max, nominal}` operating pressure (bar) | No |
| 27 | `performance.hydrogen_output_purity_percent` | `number` | H₂ output purity (%) | No |
| 28 | `performance.hydrogen_output_pressure_bar` | `number` | H₂ output delivery pressure (bar) | No |
| 29 | `performance.cold_start_time_minutes` | `number` | Cold start time to full load (minutes) | No |
| 30 | `performance.warm_start_time_minutes` | `number` | Warm start time to full load (minutes) | No |
| 31 | `performance.min_load_percent` | `number` | Minimum stable load (% of nominal) | No |
| 32 | `performance.load_ramp_rate_percent_per_second` | `number` | Load ramp rate (%/s) | No |
| 33 | `performance.water_consumption_liters_per_kg_h2` | `number` | Water consumption (L/kg H₂ produced) | No |
| 34 | `performance.water_quality_required` | `string` | Required water quality (e.g., "ASTM Type II, <1 µS/cm") | No |

#### 5.2.4 Scalability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 35 | `scalability.typical_stack_size_mw` | `number` | Typical single-stack rating (MW) | No |
| 36 | `scalability.max_stack_size_mw` | `number` | Largest commercially available single stack (MW) | No |
| 37 | `scalability.typical_plant_size_range_mw` | `object` | `{min, max, typical}` plant size range proven at scale | **Yes** |
| 38 | `scalability.modularity` | `enum` | `highly_modular` \| `modular` \| `limited_modularity` | No |
| 39 | `scalability.footprint_sqm_per_mw` | `number` | Approximate footprint (m²/MW) | No |
| 40 | `scalability.max_plant_size_known_mw` | `number` | Largest known single plant using this technology (MW) | No |
| 41 | `scalability.scaling_constraints` | `string[]` | Known constraints to scaling (e.g., `["iridium_supply", "membrane_manufacturing"]`) | No |

#### 5.2.5 Infrastructure Requirements Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 42 | `infrastructure.power_supply_requirements` | `string` | Description of power quality/infrastructure needs | **Yes** |
| 43 | `infrastructure.water_infrastructure_needed` | `string` | Water supply & treatment infrastructure description | **Yes** |
| 44 | `infrastructure.cooling_requirements` | `string` | Cooling system requirements | No |
| 45 | `infrastructure.hydrogen_compression_needed` | `boolean` | Is downstream compression typically required? | No |
| 46 | `infrastructure.footprint_requirements` | `string` | Qualitative description of land/footprint needs | No |
| 47 | `infrastructure.control_system_requirements` | `string` | Control system & automation requirements | No |
| 48 | `infrastructure.workforce_skill_requirements` | `string` | Required workforce skills & certifications | No |
| 49 | `infrastructure.supply_chain_critical_materials` | `string[]` | Critical materials (e.g., `["iridium", "PFSA_membrane", "titanium"]`) | **Yes** |
| 50 | `infrastructure.maintenance_requirements` | `string` | Description of O&M regime | No |

#### 5.2.6 Industrial Applications Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 51 | `applications.primary_applications` | `enum[]` | Best-suited primary applications | **Yes** |
| 52 | `applications.unsuitable_applications` | `enum[]` | Applications where this technology is NOT recommended | No |
| 53 | `applications.application_notes` | `string` | Qualitative notes on application fit | No |
| 54 | `applications.reference_project_ids` | `string[]` | Foreign keys → `project_references/` entries demonstrating this application | No |

#### 5.2.7 Advantages & Limitations Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 55 | `advantages` | `string[]` | Key advantages of this technology | **Yes** |
| 56 | `limitations` | `string[]` | Key limitations / challenges | **Yes** |
| 57 | `technology_differentiators` | `string[]` | What makes this technology different from the other type | No |
| 58 | `improvement_trajectory` | `string` | Expected near-term improvements (next 5 years) | No |

#### 5.2.8 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 59 | `sources` | `object[]` | Array of source references (same sub-schema as Project Reference §4.2.11) | **Yes** |

#### 5.2.9 RAG Metadata Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 60 | `rag_metadata.chunk_id` | `string` | Chunk identifier | No |
| 61 | `rag_metadata.embedding_model` | `string` | Embedding model used | No |
| 62 | `rag_metadata.embedding_version` | `string` | Version of embedding | No |
| 63 | `rag_metadata.last_indexed` | `string` | ISO 8601 timestamp of last indexing | No |
| 64 | `rag_metadata.text_for_embedding` | `string` | Pre-computed concatenation of key text fields | **Yes** |
| 65 | `rag_metadata.keywords` | `string[]` | Controlled keywords for hybrid search | **Yes** |
| 66 | `rag_metadata.tags` | `string[]` | User-defined tags | No |

### 5.3 Controlled Vocabularies

#### Commercial Maturity
```
r_and_d | pilot | demonstration | early_commercial | commercial | mature
```

#### Modularity
```
highly_modular | modular | limited_modularity
```

### 5.4 TRL Scale Reference (EU H2020)

| TRL | Description | Relevant to H₂ Electrolysis |
|-----|-------------|---------------------------|
| 1 | Basic principles observed | Fundamental electrochemistry |
| 2 | Technology concept formulated | Cell design concept |
| 3 | Experimental proof of concept | Lab-scale single cell (< 100 W) |
| 4 | Technology validated in lab | Lab-scale short stack (< 1 kW) |
| 5 | Technology validated in relevant environment | Pilot stack (~10–100 kW) |
| 6 | Technology demonstrated in relevant environment | Field demo (~100 kW–1 MW) |
| 7 | System prototype demonstrated in operational environment | Pre-commercial demo (~1–10 MW) |
| 8 | System complete and qualified | First commercial plants (~10–100 MW) |
| 9 | Actual system proven in operational environment | Mature commercial deployment (> 100 MW) |

**Current Assessment (2026):**
- **PEM Electrolysis:** TRL 8–9 (commercially deployed at >100 MW scale)
- **Alkaline Electrolysis:** TRL 9 (mature, deployed for decades at scale)

---

## 6. Schema 3: Risk Database

### 6.1 Purpose

Store structured risk entries linked to hydrogen project references. Each risk entry captures a specific risk scenario, its characteristics, consequences, mitigation strategies, and evidence from real projects.

### 6.2 Risk Taxonomy

```
Technical Risks
├── Electrolyzer Performance (degradation, efficiency shortfall)
├── Stack Manufacturing (quality, supply chain, defects)
├── Balance of Plant (piping, instrumentation failures)
├── Power Supply Integration (intermittency, power quality)
├── Water Treatment (quality deviations, membrane fouling)
├── Hydrogen Processing (compressor failures, purification issues)
├── Storage & Logistics (leaks, embrittlement, boil-off)
└── Control Systems (cybersecurity, automation failures)

Financial Risks
├── CAPEX Overrun (cost escalation, scope creep)
├── OPEX Overrun (maintenance costs, electricity price)
├── Financing Risk (interest rate, currency, refinancing)
├── Revenue Risk (H₂ price volatility, offtake default)
└── Subsidy Risk (policy change, grant clawback)

Regulatory Risks
├── Permitting Delays (environmental, construction, operating)
├── Certification Risk (RFNBO, green H₂ standards)
├── Policy Instability (subsidy regime changes)
├── Land Acquisition (land rights, community opposition)
└── Cross-Border Regulation (import/export rules)

Operational Risks
├── Supply Chain Disruption (critical materials, spare parts)
├── Workforce Availability (skilled labor shortage)
├── Technology Obsolescence (rapid tech evolution)
├── Integration Risk (multi-vendor, first-of-a-kind)
└── Force Majeure (natural disasters, pandemics, conflict)

Market Risks
├── Hydrogen Demand (slower-than-expected market growth)
├── Competing Technologies (battery-electric, direct electrification)
├── Carbon Pricing (uncertainty in CO₂ price trajectory)
└── Import Competition (cheaper H₂ from other regions)

Environmental Risks
├── Water Scarcity (competing uses, drought)
├── Biodiversity Impact (land use, habitat disruption)
├── Social License (community acceptance, NIMBY)
├── Carbon Footprint (lifecycle emissions compliance)
└── Climate Physical Risk (flooding, extreme weather at site)
```

### 6.3 Schema Definition

#### 6.3.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 1 | `risk_id` | `string` | Unique identifier, format: `RK-{CATEGORY}-{NNN}` (e.g., `RK-TEC-001`) | **Yes** |
| 2 | `risk_name` | `string` | Short, descriptive risk name | **Yes** |
| 3 | `risk_description` | `string` | Detailed description of the risk scenario (2–5 sentences) | **Yes** |
| 4 | `risk_category` | `enum` | `technical` \| `financial` \| `regulatory` \| `operational` \| `market` \| `environmental` | **Yes** |
| 5 | `risk_subcategory` | `string` | Finer-grained category (see taxonomy above) | **Yes** |
| 6 | `risk_version` | `string` | Semantic version (e.g., `1.0.0`) | **Yes** |
| 7 | `risk_status` | `enum` | `draft` \| `reviewed` \| `published` | **Yes** |

#### 6.3.2 Risk Assessment Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 8 | `assessment.probability_qualitative` | `enum` | `very_low` \| `low` \| `moderate` \| `high` \| `very_high` | **Yes** |
| 9 | `assessment.probability_quantitative_percent` | `number` | Quantitative probability estimate (% over project lifetime) | No |
| 10 | `assessment.impact_qualitative` | `enum` | `negligible` \| `minor` \| `moderate` \| `major` \| `critical` | **Yes** |
| 11 | `assessment.impact_cost_eur` | `number` | Estimated financial impact (EUR) if risk materializes | No |
| 12 | `assessment.impact_schedule_months` | `number` | Estimated schedule delay (months) if risk materializes | No |
| 13 | `assessment.risk_score` | `number` | Calculated risk score (Probability × Impact, 1–25 scale) | No |
| 14 | `assessment.risk_level` | `enum` | `low` \| `medium` \| `high` \| `critical` — derived from risk_score | **Yes** |
| 15 | `assessment.assessment_method` | `string` | How was this assessed? (e.g., "Expert elicitation, 5 SMEs") | No |
| 16 | `assessment.assessment_date` | `string` | ISO 8601 date of assessment | No |
| 17 | `assessment.assessed_by` | `string` | Person/organization who performed the assessment | No |

#### 6.3.3 Applicability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 18 | `applicability.technology_types` | `enum[]` | Applicable technologies: `PEM`, `Alkaline`, or both | **Yes** |
| 19 | `applicability.project_scale` | `enum` | `any` \| `small_less_than_10mw` \| `medium_10_to_100mw` \| `large_100_to_500mw` \| `very_large_greater_than_500mw` | **Yes** |
| 20 | `applicability.project_phase` | `enum[]` | Phases where this risk is relevant | **Yes** |
| 21 | `applicability.region_relevance` | `enum[]` | Regions where this risk is particularly relevant | No |
| 22 | `applicability.first_of_a_kind_only` | `boolean` | Is risk specific to first-of-a-kind projects? | No |

#### 6.3.4 Project Phase Enum
```
development | feasibility | permitting | financing | engineering | procurement |
construction | commissioning | operations | decommissioning | all_phases
```

#### 6.3.5 Consequences Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 23 | `consequences.description` | `string` | Narrative description of consequences if risk materializes | **Yes** |
| 24 | `consequences.worst_case_scenario` | `string` | Worst-case outcome description | No |
| 25 | `consequences.cascading_risks` | `string[]` | `risk_id` references to risks that may cascade from this one | No |

#### 6.3.6 Mitigation Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 26 | `mitigation.strategy` | `enum` | `avoid` \| `reduce` \| `transfer` \| `accept` \| `contingency` | **Yes** |
| 27 | `mitigation.actions` | `object[]` | Array of specific mitigation actions | **Yes** |
| 27a | `mitigation.actions[].action_id` | `string` | Action identifier | **Yes** |
| 27b | `mitigation.actions[].description` | `string` | Description of the mitigation action | **Yes** |
| 27c | `mitigation.actions[].responsible_party` | `string` | Who is responsible? (e.g., "EPC Contractor", "Developer") | No |
| 27d | `mitigation.actions[].timing` | `enum` | `pre_fid` \| `pre_construction` \| `during_construction` \| `during_operations` \| `ongoing` | No |
| 27e | `mitigation.actions[].effectiveness` | `enum` | `high` \| `medium` \| `low` — estimated effectiveness | No |
| 27f | `mitigation.actions[].cost_eur` | `number` | Estimated cost of mitigation | No |

#### 6.3.7 Evidence & Reference Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 28 | `evidence.reference_project_ids` | `string[]` | Foreign keys → real projects where this risk materialized | No |
| 29 | `evidence.incident_descriptions` | `string[]` | Brief descriptions of real incidents | No |
| 30 | `evidence.lessons_learned` | `string` | Key lessons from real projects | No |
| 31 | `evidence.frequency_in_reference_projects` | `string` | Qualitative frequency (e.g., "Occurred in 3 of 50 reference projects") | No |
| 32 | `evidence.industry_standards_reference` | `string[]` | Relevant standards (e.g., `["ISO 31000", "IEC 62282"]`) | No |

#### 6.3.8 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 33 | `sources` | `object[]` | Array of source references (same sub-schema as §4.2.11) | **Yes** |

#### 6.3.9 RAG Metadata Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 34 | `rag_metadata.text_for_embedding` | `string` | Pre-computed text concatenation for embedding | **Yes** |
| 35 | `rag_metadata.keywords` | `string[]` | Controlled keywords for hybrid search | **Yes** |
| 36 | `rag_metadata.last_indexed` | `string` | ISO 8601 timestamp of last indexing | No |

---

## 7. Schema 4: Cost Database

### 7.1 Purpose

Store structured CAPEX cost data points for green hydrogen projects. This schema supports CAPEX range estimation, cost benchmarking, and learning-curve projections. Each entry represents a specific cost data point from a real project or authoritative industry report.

### 7.2 Cost Taxonomy

```
Electrolyzer Stack
├── PEM Stack (membrane, electrodes, bipolar plates, assembly)
├── Alkaline Stack (electrodes, diaphragms, bipolar plates, assembly)
└── Stack Auxiliaries (cooling, monitoring, frame)

Balance of Plant (BOP)
├── Power Electronics (transformer, rectifier, switchgear)
├── Gas-Liquid Separation (separators, demisters, piping)
├── Gas Conditioning (deoxo, drying, purification)
├── Thermal Management (heat exchangers, cooling towers, chillers)
├── Instrumentation & Control (sensors, DCS, SCADA, analyzers)
└── Piping & Valves (H₂ piping, water piping, nitrogen purge)

Civil Works
├── Site Preparation (earthworks, roads, drainage, fencing)
├── Buildings (electrolyzer hall, control room, warehouse, offices)
├── Foundations (stack foundations, tank pads, pipe racks)
└── Structural Steel (pipe racks, cable trays, access platforms)

Power Supply
├── Grid Connection (substation, transmission line, switchgear)
├── Renewable Dedicated (if co-located: solar farm, wind farm)
└── Backup Power (diesel generator, UPS, battery)

Water Treatment
├── Water Source Development (wells, intake, pipelines)
├── Desalination (RO plant if seawater)
├── Demineralization (EDI, ion exchange, polishing)
└── Wastewater Treatment (brine disposal, neutralization)

Hydrogen Processing
├── Compression (reciprocating, centrifugal, ionic)
├── Purification (PSA, membrane, deoxo)
├── Drying & Cooling
└── Metering & Quality Control

Storage
├── Compressed Gas Storage (tubes, bottles, vessels)
├── Liquid H₂ Storage (liquefaction + cryogenic tanks)
├── Pipeline Injection Station
├── Ammonia Conversion (if applicable)
└── Tube Trailer Filling Station

Indirect Costs
├── EPC / EPCM Costs (engineering, procurement, construction management)
├── Owner's Costs (project management, legal, insurance, permitting)
├── Commissioning & Start-up
├── Contingency (design, cost, schedule contingency)
├── Financing Costs (during construction — IDC)
└── Development Costs (feasibility studies, due diligence)
```

### 7.3 Schema Definition

#### 7.3.1 Core Identity Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 1 | `cost_id` | `string` | Unique identifier, format: `CS-{CATEGORY}-{NNN}` (e.g., `CS-STK-001`) | **Yes** |
| 2 | `cost_name` | `string` | Descriptive name for this cost data point | **Yes** |
| 3 | `cost_category` | `enum` | Top-level category (see taxonomy) | **Yes** |
| 4 | `cost_subcategory` | `string` | Sub-category (see taxonomy) | **Yes** |
| 5 | `cost_version` | `string` | Semantic version (e.g., `1.0.0`) | **Yes** |
| 6 | `cost_status` | `enum` | `draft` \| `reviewed` \| `published` | **Yes** |

#### 7.3.2 Cost Data Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 7 | `cost_data.eur_per_kw` | `number` | Point-estimate or central value (EUR/kW installed) | **Yes** |
| 8 | `cost_data.eur_per_kw_low` | `number` | Low-end estimate (P10 or minimum) | No |
| 9 | `cost_data.eur_per_kw_high` | `number` | High-end estimate (P90 or maximum) | No |
| 10 | `cost_data.eur_per_kg_per_day` | `number` | Alternate metric: EUR per kg/day of H₂ production capacity | No |
| 11 | `cost_data.cost_basis` | `enum` | `installed_cost` \| `equipment_only` \| `epc_total` \| `all_in` | **Yes** |
| 12 | `cost_data.currency_original` | `string` | Original currency if not EUR | No |
| 13 | `cost_data.exchange_rate_used` | `number` | Exchange rate applied to convert to EUR | No |
| 14 | `cost_data.exchange_rate_date` | `string` | Date of exchange rate used (ISO 8601) | No |
| 15 | `cost_data.is_inflation_adjusted` | `boolean` | Has this cost been adjusted for inflation? | No |
| 16 | `cost_data.cost_year` | `integer` | Year of the original cost data (for inflation context) | **Yes** |
| 17 | `cost_data.inflation_base_year` | `integer` | Base year for inflation adjustment (e.g., 2024) | No |
| 18 | `cost_data.escalation_rate_applied_percent` | `number` | Annual escalation/inflation rate applied | No |

#### 7.3.3 Project Context Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 19 | `context.technology_type` | `enum` | `PEM` \| `Alkaline` \| `PEM+Alkaline` \| `technology_agnostic` | **Yes** |
| 20 | `context.project_scale_mw` | `number` | Project scale this cost applies to (MW) | **Yes** |
| 21 | `context.project_scale_category` | `enum` | `small_less_than_10mw` \| `medium_10_to_100mw` \| `large_100_to_500mw` \| `very_large_greater_than_500mw` | No |
| 22 | `context.scale_is_extrapolated` | `boolean` | Is this cost extrapolated from a different scale? | No |
| 23 | `context.extrapolation_method` | `string` | If extrapolated, method used (e.g., "0.7 power scaling law") | No |
| 24 | `context.project_reference_id` | `string` | Foreign key → `project_references/{project_id}.json` | No |
| 25 | `context.project_location_region` | `enum` | Region classification (same as Project Reference §4.2.2) | No |
| 26 | `context.greenfield_or_brownfield` | `enum` | `greenfield` \| `brownfield` \| `expansion` | No |
| 27 | `context.epc_contract_type` | `enum` | `lump_sum_turnkey` \| `epcm` \| `cost_plus` \| `hybrid` \| `unknown` | No |
| 28 | `context.local_content_percent` | `number` | Estimated local content (%) | No |

#### 7.3.4 Cost Confidence Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 29 | `confidence.level` | `enum` | `a_actual_cost` \| `b_budget_quote` \| `c_industry_benchmark` \| `d_analyst_estimate` \| `e_expert_judgment` | **Yes** |
| 30 | `confidence.rationale` | `string` | Justification for confidence level | **Yes** |
| 31 | `confidence.range_confidence_percent` | `number` | Confidence interval for low–high range (e.g., 80 for P10–P90) | No |
| 32 | `confidence.data_points_contributing` | `integer` | Number of data points behind this estimate | No |
| 33 | `confidence.verified_by_second_source` | `boolean` | Has a second independent source confirmed this? | No |

#### 7.3.5 Cost Drivers Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 34 | `cost_drivers.primary_drivers` | `string[]` | Main factors driving this cost | No |
| 35 | `cost_drivers.sensitivity_to_scale` | `enum` | `high` \| `medium` \| `low` — how scale-dependent is this cost? | No |
| 36 | `cost_drivers.learning_rate_assumption_percent` | `number` | Assumed learning rate for future projection (% per doubling) | No |
| 37 | `cost_drivers.regional_multiplier_notes` | `string` | Regional cost variation notes (e.g., "MENA +15%, Asia −10%") | No |
| 38 | `cost_drivers.exclusions` | `string[]` | What is explicitly NOT included in this cost? | No |

#### 7.3.6 Source Traceability Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 39 | `sources` | `object[]` | Array of source references (same sub-schema as §4.2.11) | **Yes** |

#### 7.3.7 RAG Metadata Block

| # | Field Name | Data Type | Description | Mandatory |
|---|-----------|-----------|-------------|-----------|
| 40 | `rag_metadata.text_for_embedding` | `string` | Pre-computed text concatenation for embedding | **Yes** |
| 41 | `rag_metadata.keywords` | `string[]` | Controlled keywords for hybrid search | **Yes** |
| 42 | `rag_metadata.last_indexed` | `string` | ISO 8601 timestamp of last indexing | No |

### 7.4 Cost Confidence Levels

| Level | Code | Description | Example |
|-------|------|-------------|---------|
| A | `a_actual_cost` | Actual contracted/spent cost from a real project | Audited CAPEX from NEOM phase 1 |
| B | `b_budget_quote` | Budgetary quotation from OEM/EPC | PEM stack quote from manufacturer |
| C | `c_industry_benchmark` | Published benchmark from authoritative source | IEA / IRENA / BNEF cost report |
| D | `d_analyst_estimate` | Analyst estimate (moderate confidence) | Consultant report estimate |
| E | `e_expert_judgment` | Expert judgment / rule of thumb (low confidence) | SME rough estimate based on analogous industry |

### 7.5 Cost Basis Definitions

| Cost Basis | Scope |
|------------|-------|
| `equipment_only` | Ex-works equipment price, no installation, no BOP |
| `installed_cost` | Equipment + direct installation (labor, materials, subcontractors) |
| `epc_total` | Full EPC scope: engineering, procurement, construction, commissioning |
| `all_in` | EPC total + owner's costs + contingency + financing during construction |

---

## 8. Cross-Reference Strategy

### 8.1 Relationship Map

```
┌──────────────────┐         ┌──────────────────┐
│    TECHNOLOGY    │◄────────│     PROJECT      │
│      CARDS      │  FK     │   REFERENCES     │
│                  │         │                  │
│ technology_id ───┼─────────┤ technology_card_ref
│                  │         │                  │
└──────────────────┘         └───┬──────┬───────┘
                                 │      │
                                 │ FK   │ FK
                                 ▼      ▼
                        ┌──────────────────┐
                        │      RISK        │
                        │     LIBRARY      │
                        │                  │
                        │ reference_project_ids[]
                        │                  │
                        └──────────────────┘
                                 │
                                 │ cross-reference
                                 ▼
                        ┌──────────────────┐
                        │      COST        │
                        │     LIBRARY      │
                        │                  │
                        │ project_reference_id
                        │                  │
                        └──────────────────┘

┌──────────────────────────────────────────────────────────┐
│              CROSS-REFERENCE INDEX                       │
│  (indexes/cross_reference_index.json)                   │
│                                                          │
│  Maps: project_id → [risk_ids, cost_ids, technology_id]  │
│  Maps: risk_id    → [project_ids, technology_ids]        │
│  Maps: cost_id    → [project_ids, technology_ids]        │
└──────────────────────────────────────────────────────────┘
```

### 8.2 Referential Integrity Rules

1. Every `technology_card_ref` in Project Reference must resolve to an existing `technology_id`
2. Every `reference_project_ids[]` in Risk Library should resolve to existing `project_id` entries
3. Every `project_reference_id` in Cost Library should resolve to an existing `project_id`
4. Cross-reference index is rebuilt on every write operation
5. Deletion of a referenced entity triggers a warning and requires explicit cascade or nullification

---

## 9. RAG Integration Guidelines

### 9.1 Retrieval Strategy

| Query Type | Retrieval Mode | Schema(s) Targeted | Top-K |
|------------|---------------|-------------------|-------|
| "Find similar projects" | Hybrid (semantic + metadata filter) | Project Reference | 10–20 |
| "Compare technologies" | Semantic | Technology Knowledge Card | 2–5 |
| "Identify risks for X" | Metadata-filtered semantic | Risk Database | 5–15 |
| "Estimate CAPEX for X" | Metadata-filtered semantic + aggregation | Cost Database | 10–30 |
| "Generate feasibility report" | Multi-hop (project → risks → costs → technology) | All schemas | Variable |
| "Answer specific question" | Semantic search across all schemas | All schemas | 5–10 |

### 9.2 Hybrid Search Design

Each schema supports **hybrid search** combining:

1. **Vector Similarity:** Cosine similarity on `text_for_embedding` field
2. **Metadata Filtering:** Exact match / range / enum filters on structured fields
3. **Keyword Boost:** BM25-style keyword matching on `keywords` and `tags` fields
4. **Cross-Reference Expansion:** Following FK links to pull related entities

#### Example Hybrid Query (Pseudo-SQL):

```
SELECT project_id, project_name, capacity_electrolyzer_mw, total_capex_eur
FROM project_references
WHERE technology_type = 'PEM'
  AND status IN ('operational', 'under_construction')
  AND capacity_electrolyzer_mw BETWEEN 50 AND 200
  AND region_classification = 'europe'
ORDER BY vector_similarity(query_embedding, embedding) DESC
LIMIT 15;
```

### 9.3 Agent Routing Logic

```
Query → Classifier Agent
  ├─ "project lookup"        → ProjectReferenceAgent
  ├─ "technology question"   → TechnologyCardAgent
  ├─ "risk assessment"       → RiskAnalysisAgent
  ├─ "cost estimation"       → CostEstimationAgent
  ├─ "feasibility scoring"   → MultiAgentOrchestrator
  │    ├─ ProjectReferenceAgent (find comparables)
  │    ├─ TechnologyCardAgent (technology fit)
  │    ├─ RiskAnalysisAgent (identify risks)
  │    ├─ CostEstimationAgent (CAPEX range)
  │    └─ SynthesisAgent (score + report)
  └─ "report generation"     → ReportGenerationAgent
```

---

## 10. Embedding & Chunking Strategy

### 10.1 Chunking Approach

| Schema | Chunking Strategy | Chunks per Entity | Rationale |
|--------|------------------|-------------------|-----------|
| Project Reference | Block-based (5 chunks) | 5 | Enables targeted retrieval (e.g., only financial block) |
| Technology Card | Block-based (6 chunks) | 6 | Blocks align with query types (performance vs. scalability) |
| Risk Database | Single-chunk (whole record) | 1 | Risks are compact enough for single-chunk embedding |
| Cost Database | Single-chunk (whole record) | 1 | Costs are compact enough for single-chunk embedding |

### 10.2 `text_for_embedding` Construction

The `text_for_embedding` field is a pre-computed concatenation of the most semantically rich fields for each schema:

#### Project Reference
```
{project_name}. {status}. Located in {location.country}, {location.region_classification}.
{technology.type} electrolysis, {capacity.electrolyzer_capacity_mw} MW.
Powered by {power.renewable_type}. Primary offtake: {offtake.primary_application}.
Developed by {stakeholders.developer}. CAPEX: {financial.capex_per_kw_eur} EUR/kW.
Keywords: {keywords}. Tags: {tags}.
```

#### Technology Card
```
{technology_name}. Type: {technology_type} ({technology_subtype}).
TRL {maturity.trl_level} — {maturity.commercial_maturity}.
Efficiency: {performance.system_efficiency_kwh_per_kg_h2} kWh/kg H₂.
Stack lifetime: {performance.stack_lifetime_hours} hours.
Operating at {performance.operating_temperature_range_c.nominal}°C.
Typical plant scale: {scalability.typical_plant_size_range_mw.min}–{scalability.typical_plant_size_range_mw.max} MW.
Advantages: {advantages}. Limitations: {limitations}.
Critical materials: {infrastructure.supply_chain_critical_materials}.
Keywords: {keywords}.
```

#### Risk Database
```
{risk_name}. Category: {risk_category} > {risk_subcategory}.
Probability: {assessment.probability_qualitative}, Impact: {assessment.impact_qualitative}.
Applies to: {applicability.technology_types} at {applicability.project_scale}.
Consequences: {consequences.description}.
Mitigation strategy: {mitigation.strategy}.
Evidence: {evidence.lessons_learned}.
Keywords: {keywords}.
```

#### Cost Database
```
{cost_name}. Category: {cost_category} > {cost_subcategory}.
EUR/kW: {cost_data.eur_per_kw} (range {cost_data.eur_per_kw_low}–{cost_data.eur_per_kw_high}).
Basis: {cost_data.cost_basis}. Year: {cost_data.cost_year}.
Technology: {context.technology_type}. Scale: {context.project_scale_mw} MW.
Confidence: {confidence.level}.
Cost drivers: {cost_drivers.primary_drivers}.
Keywords: {keywords}.
```

### 10.3 Embedding Model Recommendations

| Model | Dimensions | Use Case | Notes |
|-------|-----------|----------|-------|
| `text-embedding-3-large` | 3072 | Primary embedding | Best multilingual support |
| `text-embedding-3-small` | 1536 | Lightweight alternative | 5× cheaper, marginally lower quality |
| `bge-m3` | 1024 | Local/offline embedding | Open-source, good multilingual |
| `stella_en_1.5B` | 8192 | Maximum retrieval quality | Open-source, SOTA on MTEB |

### 10.4 Vector Database Selection

| Database | Type | Recommendation |
|----------|------|----------------|
| **ChromaDB** | Embedded vector DB | **Recommended** — local-first, no server, Python-native |
| FAISS | In-memory index | Good for static datasets, fast search |
| LanceDB | Columnar + vector | Good for mixed structured/unstructured queries |
| Qdrant | Standalone server | Better for production deployment with API |

**Initial recommendation:** ChromaDB for prototype → Qdrant or LanceDB for production.

---

## 11. Indexing Architecture

### 11.1 Index Files

Each index is a JSON file mapping searchable terms/metadata values to entity IDs.

#### `project_index.json`
```json
{
  "by_technology": {
    "PEM": ["PR-OP-001", "PR-OP-003", "PR-UC-002"],
    "Alkaline": ["PR-OP-002", "PR-PL-005"]
  },
  "by_region": {
    "europe": ["PR-OP-001", "PR-UC-001"],
    "mena": ["PR-OP-003", "PR-PL-002"]
  },
  "by_status": {
    "operational": ["PR-OP-001", "PR-OP-002"],
    "under_construction": ["PR-UC-001"]
  },
  "by_capacity_range": {
    "0-10mw": ["PR-PL-001"],
    "10-50mw": ["PR-OP-002", "PR-UC-003"],
    "50-200mw": ["PR-OP-001", "PR-UC-001"],
    "200-500mw": ["PR-UC-002"],
    "500mw-plus": ["PR-OP-003", "PR-PL-005"]
  }
}
```

#### `cross_reference_index.json`
```json
{
  "project_to_risks": {
    "PR-OP-001": ["RK-TEC-001", "RK-FIN-003", "RK-REG-002"]
  },
  "project_to_costs": {
    "PR-OP-001": ["CS-STK-001", "CS-BOP-001", "CS-PWR-002"]
  },
  "risk_to_projects": {
    "RK-TEC-001": ["PR-OP-001", "PR-UC-003", "PR-PL-007"]
  },
  "technology_to_projects": {
    "TC-PEM-001": ["PR-OP-001", "PR-UC-002", "PR-PL-003"]
  }
}
```

---

## 12. Governance & Maintenance

### 12.1 Version Control

- All JSON entities use semantic versioning (`major.minor.patch`)
- `major`: Schema-breaking changes
- `minor`: New fields added (backward-compatible)
- `patch`: Corrections, clarifications, source updates

### 12.2 Review Workflow

```
Draft → SME Review → Published → (Periodic Review) → Updated/Superseded
```

### 12.3 Update Triggers

| Trigger | Action |
|---------|--------|
| New project announced | Create project reference (status: `planned`) |
| Project reaches FID | Update status to `under_construction` |
| Project commissioned | Update status to `operational`, add actual CAPEX |
| New cost report published (IEA, IRENA, BNEF) | Create/update cost entries |
| Technology improvement reported | Update technology card (new version) |
| Risk materializes in project | Update risk entry with new evidence |
| Annual review cycle | Review all entries, update cost year references |

### 12.4 Data Quality Rules

1. Every entity MUST have at least one source with `confidence: "high"` before `published` status
2. Cost entries MUST specify `cost_year` and `cost_basis`
3. Risk entries MUST link to at least one reference project or industry standard
4. Technology cards MUST be reviewed annually against latest publications
5. Project references MUST be updated within 30 days of publicly announced status changes

### 12.5 Schema Evolution Policy

- Schema changes are proposed via **Architecture Change Request (ACR)**
- ACR must include: rationale, impact assessment, migration plan
- Backward-compatible changes (new optional fields): fast-track, 48h review
- Breaking changes: require migration script, full regression test of retrieval quality

---

## 13. Appendix: JSON Templates

The following template files are maintained in `/knowledge_base/templates/`:

| Template File | Schema Reference | Purpose |
|---------------|-----------------|---------|
| `project_reference_template.json` | §4 | Template for new project reference entries |
| `technology_card_template.json` | §5 | Template for new technology knowledge cards |
| `risk_template.json` | §6 | Template for new risk entries |
| `cost_template.json` | §7 | Template for new cost data points |

Each template is a **fully annotated example** with placeholder data, designed to be copied and filled in by domain experts.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Knowledge Architect | Initial architecture design |

---

**Next Steps:**
1. ✅ Architecture design complete
2. ⬜ Populate technology cards (PEM-001, ALK-001) with real data
3. ⬜ Ingest first 20 reference projects
4. ⬜ Populate risk library with top 50 risks
5. ⬜ Populate cost library with IEA/IRENA benchmark data
6. ⬜ Build embedding pipeline and indexes
7. ⬜ Implement RAG retrieval router
8. ⬜ Prototype feasibility scoring agent

---

*This document is the knowledge foundation for the Green Hydrogen Project Feasibility Copilot. All downstream AI agents, retrieval systems, and user-facing features depend on the integrity and consistency of this architecture.*
