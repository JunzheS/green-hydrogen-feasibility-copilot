# Risk Taxonomy Framework — Green Hydrogen Projects

**Document:** Risk Classification System v1.0
**Date:** 2026-06-05
**Author:** Senior Project Risk Manager & PMO Director
**Scope:** PEM and Alkaline electrolysis projects, pre-feasibility through early operations
**Standard Basis:** ISO 31000:2018 Risk Management, PMI PMBOK 7th Edition, adapted for industrial green hydrogen

---

## Table of Contents

1. [Design Principles](#1-design-principles)
2. [Taxonomy Overview — 8 Categories, 36 Subcategories](#2-taxonomy-overview)
3. [Category 1: Technical & Technology Risks](#3-category-1-technical--technology-risks)
4. [Category 2: Supply Chain & Procurement Risks](#4-category-2-supply-chain--procurement-risks)
5. [Category 3: Grid & Energy Risks](#5-category-3-grid--energy-risks)
6. [Category 4: Regulatory, Permitting & Policy Risks](#6-category-4-regulatory-permitting--policy-risks)
7. [Category 5: Financial & Commercial Risks](#7-category-5-financial--commercial-risks)
8. [Category 6: Construction & Execution Risks](#8-category-6-construction--execution-risks)
9. [Category 7: Operational & Maintenance Risks](#9-category-7-operational--maintenance-risks)
10. [Category 8: Environmental & Social Risks](#10-category-8-environmental--social-risks)
11. [Project Phase Mapping](#11-project-phase-mapping)
12. [Technology-Specific Risk Profiles](#12-technology-specific-risk-profiles)

---

## 1. Design Principles

| Principle | Implementation |
|-----------|---------------|
| **PMO-grade** | Follows ISO 31000 structure recognizable by project managers and lenders |
| **Hydrogen-specific** | Every category and subcategory is defined through a green hydrogen lens, not generic infrastructure |
| **Technology-differentiated** | Risks are tagged PEM/Alkaline where technology choice changes the risk profile |
| **Phase-mapped** | Every subcategory identifies which project phases it applies to |
| **RAG-compatible** | Hierarchical category→subcategory enables precise metadata filtering for the Retrieval Agent |
| **Agent-ready** | Each subcategory includes trigger events, not just descriptions — enabling future automated risk detection |
| **Extensible** | New subcategories can be added without restructuring the top-level taxonomy |
| **Traceable** | Every risk links to evidence sources in the Project Database and Technology Cards |

---

## 2. Taxonomy Overview — 8 Categories, 36 Subcategories

```
RISK TAXONOMY FOR GREEN HYDROGEN PROJECTS
│
├── CAT-01 TECHNICAL & TECHNOLOGY RISKS
│   ├── 01.1 Electrolyzer Performance & Degradation
│   ├── 01.2 Hydrogen Processing (Compression, Purification, Drying)
│   ├── 01.3 Balance of Plant Reliability
│   ├── 01.4 Technology Obsolescence
│   └── 01.5 Control & Safety Systems
│
├── CAT-02 SUPPLY CHAIN & PROCUREMENT RISKS
│   ├── 02.1 Electrolyzer Manufacturing Capacity & Lead Times
│   ├── 02.2 Critical Materials Availability (Ir, PFSA, Ti, Ni)
│   ├── 02.3 OEM/Single-Source Dependency
│   ├── 02.4 Logistics & Import/Export Delays
│   └── 02.5 Contractor & Subcontractor Performance
│
├── CAT-03 GRID & ENERGY RISKS
│   ├── 03.1 Grid Connection Delays
│   ├── 03.2 Grid Capacity & Congestion
│   ├── 03.3 Renewable Energy Availability & Intermittency
│   ├── 03.4 Electricity Price Volatility
│   └── 03.5 Power Quality & Harmonic Issues
│
├── CAT-04 REGULATORY, PERMITTING & POLICY RISKS
│   ├── 04.1 Environmental Permitting Delays
│   ├── 04.2 Green H₂ Certification (RFNBO Compliance)
│   ├── 04.3 Subsidy & Policy Instability
│   ├── 04.4 Land Acquisition & Rights
│   └── 04.5 Safety Regulatory Compliance (ATEX, PED, Seveso)
│
├── CAT-05 FINANCIAL & COMMERCIAL RISKS
│   ├── 05.1 CAPEX Overrun
│   ├── 05.2 OPEX Escalation
│   ├── 05.3 Financing & Interest Rate Risk
│   ├── 05.4 Hydrogen Offtake & Revenue Risk
│   └── 05.5 Currency & Inflation Risk
│
├── CAT-06 CONSTRUCTION & EXECUTION RISKS
│   ├── 06.1 Site Preparation & Civil Works
│   ├── 06.2 Module Integration & Commissioning
│   ├── 06.3 Schedule Overrun
│   └── 06.4 Construction Quality & Defects
│
├── CAT-07 OPERATIONAL & MAINTENANCE RISKS
│   ├── 07.1 Workforce Availability & Skills
│   ├── 07.2 Water Supply & Quality
│   ├── 07.3 Hydrogen Storage & Logistics
│   └── 07.4 Planned & Unplanned Outages
│
└── CAT-08 ENVIRONMENTAL & SOCIAL RISKS
    ├── 08.1 Water Scarcity & Competing Uses
    ├── 08.2 Carbon Footprint & Lifecycle Emissions
    └── 08.3 Community Opposition & Social License
```

---

## 3. Category 1: Technical & Technology Risks

**Definition:** Risks originating from the electrolysis technology itself, the balance of plant equipment, or the integration of new/emerging technologies in an industrial setting. These are the most hydrogen-specific risks in the taxonomy.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **01.1** | Electrolyzer Performance & Degradation | The electrolyzer stack fails to meet warranted efficiency, lifetime, or degradation rate specifications | PEM stack degradation exceeding 1.0%/year under dynamic operation; Alkaline diaphragm fouling from carbonate build-up; lower-than-expected system efficiency (kWh/kg H₂) | PEM: higher degradation rate, dynamic operation accelerates it. Alkaline: slower degradation but carbonate fouling specific to liquid electrolyte. | FEED, Construction, Operations |
| **01.2** | Hydrogen Processing | Downstream H₂ compression, purification, drying, or metering equipment underperforms or fails | Reciprocating compressor premature wear; PSA/TSA purification efficiency loss; H₂ dryer dew point excursions; metering inaccuracies affecting offtake billing | PEM: less purification required (99.99% purity native). Alkaline: requires deoxo + dryer for fuel cell-grade; atmospheric output requires full compression train. | Construction, Commissioning, Operations |
| **01.3** | Balance of Plant Reliability | Non-electrolyzer plant systems experience failures affecting production | Pump failures; heat exchanger fouling; transformer/rectifier faults; instrumentation drift; pipe/valve leaks | Technology-agnostic, but PEM's higher water purity requirements increase water treatment BOP complexity | Operations |
| **01.4** | Technology Obsolescence | The chosen electrolyzer technology is superseded by a significantly cheaper or more efficient technology within the project life | Rapid PEM cost reduction (15% learning rate) making early projects uncompetitive; breakthrough Alkaline designs (zero-gap, pressurized) obsoleting atmospheric legacy plants | PEM: fast innovation cycle, 15% learning rate. Alkaline: slower innovation, mature. FOAK PEM projects face higher obsolescence risk. | Pre-Feasibility, Feasibility, Operations |
| **01.5** | Control & Safety Systems | DCS, SIS, or safety instrumented functions fail to perform as specified | H₂-in-O₂ analyzer false trips causing unnecessary shutdowns; DCS integration issues with multi-OEM equipment; cybersecurity vulnerabilities in connected plant systems | Technology-agnostic | FEED, Commissioning, Operations |

---

## 4. Category 2: Supply Chain & Procurement Risks

**Definition:** Risks related to the availability, delivery, quality, and cost of equipment, materials, and services required to build and maintain the hydrogen plant.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **02.1** | Electrolyzer Manufacturing Capacity & Lead Times | Global electrolyzer manufacturing capacity cannot meet demand, causing delivery delays and price increases | 18-24 month lead times for 20 MW PEM stack modules during industry boom; gigafactory ramp-up delays; slot reservation competition among developers | PEM: 4 major OEMs, Siemens Energy + ITM Power dominant >20 MW. Alkaline: 10+ OEMs, but Chinese supply carries quality/performance risk. | Pre-Feasibility, Feasibility, FEED |
| **02.2** | Critical Materials Availability | Raw materials required for electrolyzer manufacturing experience supply constraints, price spikes, or geopolitical disruption | Iridium price spike (PEM); titanium supply concentration (Russia/China); PFSA membrane production capacity; nickel price volatility (Alkaline); Zirfon diaphragm supply | PEM: iridium (critical, South Africa >80%), titanium, PFSA membrane, platinum. Alkaline: nickel, Zirfon, steel, KOH — all abundant. | Pre-Feasibility, Construction |
| **02.3** | OEM/Single-Source Dependency | Reliance on a single electrolyzer manufacturer creates schedule, pricing, and warranty risk | Only 2 OEMs can supply >20 MW PEM modules; proprietary stack interfaces prevent multi-sourcing; OEM financial distress or insolvency | PEM: HIGH concentration risk. Alkaline: LOW — 10+ suppliers + Chinese option. | Feasibility, FEED, Construction |
| **02.4** | Logistics & Import/Export Delays | Transportation, customs, or trade barriers delay equipment delivery | Oversized electrolyzer modules requiring special transport permits; port congestion delaying shipment; customs clearance delays for imported stacks; trade sanctions affecting OEM country of origin | Affects projects importing from non-local OEMs (e.g., European project using US-manufactured Plug Power stacks) | Construction |
| **02.5** | Contractor & Subcontractor Performance | EPC, EPCM, or subcontractors fail to meet quality, schedule, or safety standards | EPC contractor with limited hydrogen experience; subcontractor quality issues on H₂ piping welding (requiring specialized certifications); labour disputes; contractor insolvency | Technology-agnostic | FEED, Construction, Commissioning |

---

## 5. Category 3: Grid & Energy Risks

**Definition:** Risks related to the electricity supply that powers the electrolyzer. Electricity represents 70-75% of OPEX and is the single largest cost and operational dependency.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **03.1** | Grid Connection Delays | The electrical grid connection for the plant is not completed on time | TSO/DSO transformer delivery delayed; substation construction behind schedule; grid connection agreement negotiation prolongs beyond plan; IPCEI-funded grid upgrades not completed | Technology-agnostic. PEM (IGBT rectifier, tighter power quality) vs Alkaline (thyristor rectifier, more tolerant) affects grid connection specification but not delay risk. | Feasibility, FEED, Construction |
| **03.2** | Grid Capacity & Congestion | The local grid cannot deliver the contracted capacity or connection is denied due to congestion | Grid congestion in industrial clusters (Rotterdam, Antwerp, Ruhr); connection queue priority given to other users; network reinforcement costs allocated to project | Technology-agnostic | Pre-Feasibility, Feasibility |
| **03.3** | Renewable Energy Availability & Intermittency | The dedicated or contracted renewable power source produces less energy than forecast | Lower-than-expected wind resource (offshore wind capacity factor 45% forecast vs 38% actual); solar PV degradation faster than projected; PPA counterparty under-delivers renewable electrons | PEM: dynamic operation partially compensates for intermittency. Alkaline: slower response means more renewable energy is lost during ramping periods. | Pre-Feasibility, Feasibility, Operations |
| **03.4** | Electricity Price Volatility | The price of electricity deviates significantly from the project's financial model assumptions | Wholesale electricity price spike during low renewable production; PPA price renegotiation; carbon price changes affecting grid electricity cost; merit order effect reducing captured price for renewable generators | Technology-agnostic, but PEM's higher efficiency (55 vs 53 kWh/kg) means it is marginally less exposed to price volatility per kg H₂ produced | Operations |
| **03.5** | Power Quality & Harmonic Issues | Grid power quality problems cause electrolyzer trips, rectifier damage, or efficiency loss | Voltage sags from nearby industrial loads; harmonic distortion from thyristor rectifiers feeding back to grid; frequency deviations causing DCS trips; reactive power penalties | Alkaline (thyristor rectifier): higher harmonic generation, may require active filtering. PEM (IGBT rectifier): lower harmonics, better power quality, but more sensitive to voltage sags. | FEED, Commissioning, Operations |

---

## 6. Category 4: Regulatory, Permitting & Policy Risks

**Definition:** Risks arising from government regulation, permitting requirements, policy frameworks, and certification standards specific to green hydrogen production.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **04.1** | Environmental Permitting Delays | Required environmental permits are delayed, denied, or challenged | EIA (Environmental Impact Assessment) taking 18+ months; water abstraction permit contested; Natura 2000 / biodiversity impact assessment extending timeline; public inquiry triggered by local opposition | Technology-agnostic | Pre-Feasibility, Feasibility |
| **04.2** | Green H₂ Certification (RFNBO Compliance) | The project fails to achieve or maintain certification as producing renewable hydrogen under EU RFNBO rules | Additionality requirements not met (renewable asset commissioning timing); temporal correlation rules (hourly matching from 2030); geographical correlation (bidding zone constraints); certification body delays or rejection | Technology-agnostic for certification eligibility, but PEM's dynamic operation better supports hourly matching requirements | Pre-Feasibility, Feasibility, Operations |
| **04.3** | Subsidy & Policy Instability | Government subsidies, tax incentives, or policy support are reduced, delayed, or withdrawn | IPCEI funding not disbursed on schedule; election-driven policy reversal; carbon price trajectory divergence from assumptions; EU ETS free allowance phaseout affecting industrial offtake competitiveness | Technology-agnostic | Pre-Feasibility, Feasibility, Operations |
| **04.4** | Land Acquisition & Rights | Land required for the plant or renewable generation cannot be secured on acceptable terms | Land price inflation in industrial zones; competing land uses (agriculture, residential); mineral rights complications; land contamination from previous industrial use requiring remediation | Technology-agnostic, but PEM's smaller footprint (50 m²/MW vs 80 m²/MW) reduces land acquisition exposure | Pre-Feasibility, Feasibility |
| **04.5** | Safety Regulatory Compliance | The plant design or operation fails to meet safety regulations for hydrogen production and handling | ATEX zoning non-compliance; Pressure Equipment Directive (PED) certification delays; Seveso III Directive classification triggering additional requirements; fire protection system approval delays | Technology-agnostic; Alkaline has additional KOH handling safety regulations | FEED, Construction, Commissioning |

---

## 7. Category 5: Financial & Commercial Risks

**Definition:** Risks affecting the project's capital cost, operating cost, revenue, financing, and overall financial viability.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **05.1** | CAPEX Overrun | Total project capital expenditure exceeds the budgeted amount | Scope creep during FEED; EPC contract change orders; unexpected civil works costs (ground conditions); electrolyzer price increase between bid and order; contingency drawdown exceeding planned reserve | PEM: higher stack cost, more exposed to precious metal price volatility. Alkaline: lower stack cost, but larger civil works (bigger footprint) partially offsets. | Feasibility, FEED, Construction |
| **05.2** | OPEX Escalation | Operating costs exceed projections, eroding project margins | Electricity cost higher than PPA assumption (see 03.4); maintenance costs higher than benchmark (limited operational data for large PEM/Alkaline); water costs exceeding forecast; insurance premium escalation after industry incidents | PEM: higher maintenance cost (specialized Ti/PFSA expertise, more frequent stack replacement). Alkaline: KOH electrolyte management, carbonate removal consumables. | Operations |
| **05.3** | Financing & Interest Rate Risk | Project financing cannot be secured, or financing costs exceed assumptions | Debt market conditions tighten; interest rate increases during construction (floating rate exposure); lender technical due diligence requirements not met; equity partner withdrawal | Technology-agnostic. Lenders may prefer Alkaline (lower technology risk, TRL 9 vs PEM TRL 8) for conservative project finance. | Pre-Feasibility, Feasibility |
| **05.4** | Hydrogen Offtake & Revenue Risk | The hydrogen produced cannot be sold at the assumed volume or price | Offtaker financial distress or bankruptcy; H₂ market price below project LCOH; offtake agreement renegotiation; slower-than-expected H₂ market development; competing grey/blue H₂ undercutting green H₂ price | Technology-agnostic for volume risk. PEM's higher purity may command a premium for mobility/electronics applications. | Pre-Feasibility, Feasibility, Operations |
| **05.5** | Currency & Inflation Risk | Exchange rate movements or general inflation erode project economics | EUR/USD exchange rate affecting US-manufactured equipment cost; local currency inflation in construction labour; construction material cost escalation (steel, concrete, copper) | Technology-agnostic | Feasibility, Construction |

---

## 8. Category 6: Construction & Execution Risks

**Definition:** Risks arising during the physical construction, installation, integration, and commissioning of the hydrogen plant.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **06.1** | Site Preparation & Civil Works | Ground conditions, site access, or civil engineering challenges cause delays or cost increases | Unexpected ground contamination at brownfield site; piling difficulties; archaeological discovery; flood risk requiring elevated platform construction | Technology-agnostic. Alkaline's larger footprint increases civil works exposure. | Construction |
| **06.2** | Module Integration & Commissioning | Integration of electrolyzer modules with BOP systems fails or takes longer than planned | Multi-OEM interface problems (electrolyzer from OEM A, rectifier from OEM B, DCS from OEM C); commissioning sequence delays; performance test failures; H₂ purity not achieved during commissioning | Technology-agnostic, but PEM (more complex BOP, stricter water quality) may have longer commissioning than Alkaline | Commissioning |
| **06.3** | Schedule Overrun | The overall project schedule slips, delaying first hydrogen production and revenue | Cumulative delays from permitting (04.1), grid connection (03.1), equipment delivery (02.1), and commissioning (06.2); force majeure events (pandemic, extreme weather, conflict); contractor resource constraints | Technology-agnostic | Construction, Commissioning |
| **06.4** | Construction Quality & Defects | Workmanship or material defects result in rework, warranty claims, or operational problems | H₂ piping weld defects discovered during pressure testing; concrete foundation cracking; electrical installation non-compliance; instrumentation calibration errors | Technology-agnostic | Construction, Commissioning |

---

## 9. Category 7: Operational & Maintenance Risks

**Definition:** Risks affecting the plant's ability to operate reliably, safely, and cost-effectively after commissioning.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **07.1** | Workforce Availability & Skills | Qualified personnel cannot be recruited, trained, or retained | Shortage of PEM electrolyzer technicians in new H₂ hubs; competition for chemical engineers from oil & gas; specialized training lead time (6-12 months); key person dependency (only 1-2 people understand the full system) | PEM: smaller workforce pool (newer technology). Alkaline: larger talent pool (chlor-alkali industry transfer). | Pre-Feasibility, Operations |
| **07.2** | Water Supply & Quality | Water supply is insufficient, interrupted, or fails to meet quality specifications | Raw water source curtailment during drought; RO membrane fouling from variable raw water quality; EDI system failure causing water quality excursion; water supply contract dispute | PEM: stricter water quality (ASTM Type II, <1 µS/cm) — higher treatment complexity, more sensitive to excursions. Alkaline: less stringent (<5 µS/cm) but additional KOH electrolyte quality management. | Feasibility, Operations |
| **07.3** | Hydrogen Storage & Logistics | On-site H₂ storage or offtake logistics experience capacity constraints or failures | Compressed gas storage vessel inspection outage; tube trailer loading system downtime; pipeline injection pressure mismatch; H₂ inventory imbalance (production > offtake capacity) | Technology-agnostic. PEM's pressurized output (30 bar) simplifies storage vs Alkaline's atmospheric output. | Operations |
| **07.4** | Planned & Unplanned Outages | Production is interrupted for scheduled or unscheduled maintenance | Stack replacement outage (4-6 weeks per module); BOP equipment failure causing forced outage; grid outage causing full plant trip; cold restart delay (PEM 15 min, Alkaline 60 min) affecting production recovery | PEM: faster restart (15 min) minimizes production loss from short outages. Alkaline: 60 minute restart means a 30-minute grid blip causes 90+ minutes of lost production. | Operations |

---

## 10. Category 8: Environmental & Social Risks

**Definition:** Risks related to the project's environmental impact, community relations, and social license to operate.

### Subcategories

| ID | Subcategory | Definition | Typical Examples | Technology Specificity | Primary Phases |
|----|------------|------------|------------------|----------------------|---------------|
| **08.1** | Water Scarcity & Competing Uses | The project's water consumption creates or exacerbates local water stress | Water abstraction permit contested by agricultural users; drought conditions reducing raw water availability; desalination brine disposal environmental impact; public perception of "water-for-hydrogen" in water-stressed regions | Technology-agnostic (~10-11 L water per kg H₂ for both technologies). Location-dependent: critical in Spain, Portugal, MENA; less critical in Netherlands, Denmark. | Pre-Feasibility, Feasibility, Operations |
| **08.2** | Carbon Footprint & Lifecycle Emissions | The project's lifecycle GHG emissions exceed regulatory thresholds or stakeholder expectations | Electrolyzer manufacturing carbon footprint; renewable energy lifecycle emissions (solar panel manufacturing, wind turbine concrete); H₂ compression and transport emissions; RFNBO 70% GHG reduction threshold not met on lifecycle basis | Technology-agnostic for operating emissions. PEM's iridium and titanium have higher embodied carbon than Alkaline's nickel and steel. | Pre-Feasibility, Feasibility |
| **08.3** | Community Opposition & Social License | Local community opposition delays or blocks the project | NIMBY opposition to industrial development; concerns about H₂ safety (explosion risk perception); noise complaints (compressor station); visual impact of renewable generation; lack of local employment benefits perceived by community | Technology-agnostic | Pre-Feasibility, Feasibility, Construction |

---

## 11. Project Phase Mapping

This matrix shows which risk subcategories are active in each project phase. Risks peak in FEED/Construction (execution phase) and Operations (revenue phase).

```
Subcategory              Pre-Feas  Feasibility  FEED  Construction  Commissioning  Operations
─────────────────────────────────────────────────────────────────────────────────────────
01.1 Electrolyzer Perf       ○           ●         ●         ○             ●            ●
01.2 H₂ Processing           —           —         ○         ●             ●            ●
01.3 BOP Reliability         —           —         —         —             ○            ●
01.4 Technology Obsc         ●           ●         ○         —             —            ●
01.5 Control & Safety        —           —         ●         ○             ●            ●

02.1 Mfg Capacity            ●           ●         ●         ○             —            —
02.2 Critical Materials      ●           ○         —         ●             —            —
02.3 OEM Dependency          —           ●         ●         ●             —            —
02.4 Logistics               —           —         —         ●             ●            —
02.5 Contractor Perf         —           —         ●         ●             ●            —

03.1 Grid Connection         —           ●         ●         ●             ●            —
03.2 Grid Congestion         ●           ●         —         —             —            —
03.3 Renewable Avail         ●           ●         —         —             —            ●
03.4 Electricity Price       —           —         —         —             —            ●
03.5 Power Quality           —           —         ●         —             ●            ●

04.1 Env Permitting          ●           ●         —         —             —            —
04.2 RFNBO Certification     ●           ●         —         —             ○            ●
04.3 Subsidy Instability     ●           ●         —         —             —            ●
04.4 Land Acquisition        ●           ●         —         —             —            —
04.5 Safety Regulatory       —           —         ●         ●             ●            —

05.1 CAPEX Overrun           —           ●         ●         ●             —            —
05.2 OPEX Escalation         —           ○         —         —             —            ●
05.3 Financing Risk          ●           ●         —         —             —            —
05.4 Offtake/Revenue         ●           ●         —         —             —            ●
05.5 Currency/Inflation      —           ●         —         ●             —            —

06.1 Site/Civil Works        —           —         —         ●             —            —
06.2 Module Integration      —           —         —         —             ●            —
06.3 Schedule Overrun        —           —         —         ●             ●            —
06.4 Construction Quality    —           —         —         ●             ●            —

07.1 Workforce               ●           ○         —         —             —            ●
07.2 Water Supply            —           ●         —         —             ○            ●
07.3 H₂ Storage/Logistics    —           —         —         —             ●            ●
07.4 Outages                 —           —         —         —             —            ●

08.1 Water Scarcity          ●           ●         —         —             —            ●
08.2 Carbon Footprint        ●           ●         —         —             —            —
08.3 Community Opposition    ●           ●         ○         ●             —            —
─────────────────────────────────────────────────────────────────────────────────────────
● = Primary phase  ○ = Secondary phase  — = Not applicable
```

---

## 12. Technology-Specific Risk Profiles

### 12.1 PEM-Specific Risk Accentuation

PEM projects face elevated risk in these subcategories:

| Subcategory | Why PEM Risk is Higher |
|------------|----------------------|
| **01.1** Electrolyzer Performance | Degradation rate 1.0%/year (vs Alkaline 0.5%); limited >100 MW reference data; dynamic operation impact still being characterized |
| **01.4** Technology Obsolescence | 15% learning rate means 2025-vintage PEM stacks may be cost-uncompetitive by 2030 vs next-generation stacks |
| **02.2** Critical Materials | Iridium (rare, supply-concentrated), PFSA membrane (limited manufacturers), titanium pricing |
| **02.3** OEM Dependency | Only 4 OEMs for >10 MW PEM modules; Siemens Energy/ITM Power duopoly at 100+ MW |
| **03.5** Power Quality (opposite) | PEM's IGBT rectifier produces cleaner power but is more sensitive to grid voltage sags |
| **05.1** CAPEX Overrun | Higher stack cost (€800/kW vs €450/kW) means PEM projects have more capital at risk per MW |
| **07.2** Water Quality | ASTM Type II water (<1 µS/cm) requires more complex treatment; membrane contamination risk from water excursions |

### 12.2 Alkaline-Specific Risk Accentuation

Alkaline projects face elevated risk in these subcategories:

| Subcategory | Why Alkaline Risk is Higher |
|------------|---------------------------|
| **01.1** (aspect) | Carbonate formation from CO₂ absorption requires ongoing electrolyte management; not a failure mode for PEM's sealed system |
| **03.3** Renewable Intermittency | Slower dynamic response (2%/s vs 10%/s ramp, 15% vs 5% minimum load) loses 5-10% more renewable energy during variable conditions |
| **06.1** Civil Works | Larger footprint (80 m²/MW vs 50 m²/MW) increases site preparation costs and schedule |
| **07.4** Outages | 60-minute cold start vs 15-minute PEM means unplanned outages cause longer production gaps |
| **04.5** Safety (aspect) | KOH liquid electrolyte handling adds chemical safety regulatory burden not present for PEM |

---

## 13. Taxonomy Usage Guidelines

### 13.1 For Risk Library Construction

1. Every risk entry MUST be assigned to exactly one category and one subcategory
2. If a risk spans two categories, assign to the PRIMARY category and reference the secondary in `cascading_risks`
3. Use the subcategory numbers as the risk ID prefix: `RK-TEC-001` = Technical risk #1, `RK-GRD-003` = Grid risk #3
4. Always tag applicable technologies and project phases

### 13.2 For the Retrieval Agent

1. Query by `risk_category` for broad filtering (e.g., "show all grid & energy risks")
2. Query by `risk_subcategory` for precise retrieval (e.g., "show only electricity price volatility risks")
3. Filter by `applicability.technology_types` to show only PEM or Alkaline risks
4. Filter by `applicability.project_phase` to show risks active in the user's current phase

### 13.3 For the Future Risk Agent

1. Scan trigger events against project data to auto-detect emerging risks
2. Weight acute risks (categories 03, 04, 06) higher for projects approaching construction
3. Weight chronic risks (categories 01, 05, 07) higher for operational projects
4. Cross-reference with Gold Dataset to find projects where similar risks materialized

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Project Risk Manager & PMO Director | Initial risk taxonomy for green hydrogen projects |

---

*This taxonomy is the foundation for all risk-related knowledge in the Copilot. It is aligned with ISO 31000, differentiated by technology (PEM/Alkaline), mapped to project phases, and designed for RAG retrieval and future agent reasoning.*
