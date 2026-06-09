# Cost Taxonomy Framework — Green Hydrogen Project CAPEX

**Document:** CAPEX Classification System v1.0
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Industrial Project Controller
**Scope:** PEM and Alkaline electrolysis projects, pre-feasibility through FEED
**Basis:** AACE International Classification 18R-97, adapted for industrial green hydrogen; IEA/IRENA cost reporting structures

---

## 1. Design Principles

| Principle | Implementation |
|-----------|---------------|
| **AACE-aligned** | Follows AACE cost classification (Class 5 → Class 3 → Class 1) recognized by project controllers and lenders |
| **IEA/IRENA-consistent** | Taxonomy aligns with IEA Global Hydrogen Review and IRENA cost reporting — enables direct benchmarking against published data |
| **Technology-differentiated** | Every cost category identifies whether it differs for PEM vs Alkaline |
| **Scale-aware** | Each category identifies scaling behavior (linear, sub-linear, step-change) |
| **Source-traceable** | Every cost category links to benchmark data sources (IEA GHR 2025, IRENA 2024, project data) |
| **Estimation-ready** | Designed to support AACE Class 5 (conceptual, ±30-50%) and Class 4 (feasibility, ±20-30%) estimates |

---

## 2. Taxonomy Overview — 8 Categories, 26 Subcategories

```
GREEN HYDROGEN PROJECT CAPEX TAXONOMY
│
├── CAT-01 ELECTROLYZER SYSTEM (28–45% of total CAPEX)
│   ├── 01.1 Electrolyzer Stack (cells, membranes, electrodes, bipolar plates, assembly)
│   ├── 01.2 Stack Auxiliaries (cooling, monitoring, framing, piping within module)
│   ├── 01.3 Power Electronics (transformer-rectifier, DC distribution, harmonic filtering)
│   └── 01.4 Gas-Liquid Separation (H₂/O₂ separators, demisters, KOH circulation for Alkaline)
│
├── CAT-02 ELECTRICAL INFRASTRUCTURE (10–20% of total CAPEX)
│   ├── 02.1 Grid Connection (substation, transmission line/cable, TSO fees)
│   ├── 02.2 MV/LV Distribution (switchgear, cabling, busbars within plant)
│   └── 02.3 Backup/UPS Systems (diesel generator, battery UPS, black-start capability)
│
├── CAT-03 WATER SYSTEMS (3–6% of total CAPEX)
│   ├── 03.1 Water Treatment (RO, EDI, polishing, storage tanks)
│   └── 03.2 Raw Water Supply (intake, pipeline, pumping, desalination if applicable)
│
├── CAT-04 HYDROGEN PROCESSING (8–15% of total CAPEX)
│   ├── 04.1 Compression (reciprocating/centrifugal/ionic compressors, intercoolers)
│   ├── 04.2 Purification & Drying (PSA, deoxo, TSA dryer, filtration)
│   └── 04.3 Storage & Logistics (compressed gas vessels, tube trailer filling, pipeline injection)
│
├── CAT-05 CIVIL & CONSTRUCTION (8–15% of total CAPEX)
│   ├── 05.1 Site Preparation (earthworks, drainage, roads, fencing, landscaping)
│   ├── 05.2 Buildings & Structures (electrolyzer hall, control room, warehouse, offices)
│   └── 05.3 Foundations & Structural Steel (stack foundations, pipe racks, cable trays)
│
├── CAT-06 THERMAL MANAGEMENT (2–5% of total CAPEX)
│   ├── 06.1 Cooling Systems (cooling towers, dry coolers, heat exchangers, chilled water)
│   └── 06.2 Heat Recovery Integration (district heating connection, heat export piping)
│
├── CAT-07 INSTRUMENTATION & CONTROLS (3–6% of total CAPEX)
│   ├── 07.1 DCS/SIS (Distributed Control System, Safety Instrumented System)
│   ├── 07.2 Instrumentation (sensors, analyzers, flow meters, gas detectors)
│   └── 07.3 Telecommunications & Cybersecurity
│
└── CAT-08 INDIRECT & OWNER'S COSTS (15–25% of total CAPEX)
    ├── 08.1 Engineering & Design (FEED, detailed engineering, 3D modeling)
    ├── 08.2 Procurement & Supply Chain (sourcing, expediting, inspection, logistics)
    ├── 08.3 Construction Management (supervision, commissioning support, contractor overhead)
    ├── 08.4 Owner's Costs (project management, legal, insurance, permitting, land)
    ├── 08.5 Contingency (design allowance, cost escalation, schedule contingency)
    └── 08.6 Financing During Construction (IDC, commitment fees, debt service reserve)
```

---

## 3. Category Detail

### CAT-01: Electrolyzer System (28–45% of total CAPEX)

**Description:** The core hydrogen production equipment: electrolyzer stacks, module auxiliaries, power conversion, and initial gas handling. This is the most technology-specific category and the primary driver of CAPEX differences between PEM and Alkaline.

| Subcategory | % of Total | Key Cost Drivers | PEM vs Alkaline |
|------------|-----------|-----------------|-----------------|
| **01.1 Stack** | 15–30% | Electrode catalyst material (Ir/Pt for PEM; Ni for Alkaline); membrane/diaphragm material; bipolar plate manufacturing; current density (higher = fewer cells per MW); OEM manufacturing scale | **PEM +70-90% more expensive**: ~€800/kW vs ~€450/kW (installed, 2025). PEM uses precious metals (Ir, Pt) and PFSA membranes; Alkaline uses Ni, steel, Zirfon |
| **01.2 Stack Auxiliaries** | 3–6% | Cooling circuit within module; cell voltage monitoring; module frame and enclosure; internal piping | **Technology-neutral**. Similar cost per MW for both technologies |
| **01.3 Power Electronics** | 6–10% | Rectifier type (IGBT vs thyristor); DC distribution bus; harmonic filtering; transformer integration | **Technology-differentiated**: PEM requires IGBT (higher cost, cleaner power, ~€120-180/kW); Alkaline can use thyristor (lower cost, ~€80-120/kW, more harmonics) |
| **01.4 Gas-Liquid Separation** | 2–4% | H₂/O₂ separator vessels; demister pads; liquid level control; for Alkaline: KOH circulation pumps and electrolyte management | **Alkaline +50% more expensive**: requires separate H₂ and O₂ liquid separation with KOH recirculation; PEM has simpler gas-water separation |

**Technology-specific stack cost drivers (2025 benchmarks):**

| Driver | PEM | Alkaline |
|--------|-----|----------|
| Stack cost (€/kW, installed) | 600–1,100 (central: 800) | 350–600 (central: 450) |
| Learning rate (% per doubling) | 15% | 10% |
| Critical materials | Iridium, platinum, PFSA membrane, titanium | Nickel, Zirfon diaphragm, steel, KOH |
| OEM margin environment | High (limited competition) | Moderate (10+ OEMs + Chinese option) |
| 2030 projected stack cost | €500-600/kW | €350-450/kW |

**Scale sensitivity: HIGH** — stack costs exhibit ~15% (PEM) and ~10% (Alkaline) learning rates. At larger plant scales, stack cost per kW decreases due to manufacturing volume discounts and larger module sizes (fewer modules per MW).

---

### CAT-02: Electrical Infrastructure (10–20% of total CAPEX)

**Description:** All electrical systems from the grid connection point to the electrolyzer rectifier input. This category is strongly location-dependent and influenced by site selection decisions.

| Subcategory | % of Total | Key Cost Drivers | Location Sensitivity |
|------------|-----------|-----------------|---------------------|
| **02.1 Grid Connection** | 5–12% | Distance to existing HV infrastructure; TSO/DSO connection charges; new substation vs. reuse; transformer lead times; grid reinforcement costs | **VERY HIGH**: Brownfield sites with existing HV connection (HGHH/Moorburg) save €10-30M vs greenfield sites requiring new substation |
| **02.2 MV/LV Distribution** | 3–5% | Plant layout; cable trenching distance; switchgear rating; arc-flash protection | LOW: Determined by plant layout, not location |
| **02.3 Backup/UPS Systems** | 1–3% | Black-start requirements; grid reliability at site; safety system UPS autonomy requirements | MEDIUM: Sites with unstable grid (developing countries, remote areas) require larger backup systems |

**Technology differentiation:** PEM's IGBT rectifier requires cleaner input power (may need active harmonic filtering on weak grids). Alkaline's thyristor rectifier generates more harmonics (may need filtering to meet grid code). Net cost impact: PEM +5-10% on power electronics; Alkaline +3-5% on harmonic filtering. Largely offsets.

---

### CAT-03: Water Systems (3–6% of total CAPEX)

**Description:** Water treatment and supply systems from raw water source to electrolyzer feed point. PEM requires significantly higher water quality than Alkaline.

| Subcategory | % of Total | Key Cost Drivers | PEM vs Alkaline |
|------------|-----------|-----------------|-----------------|
| **03.1 Water Treatment** | 2–4% | Required water quality (conductivity spec); raw water quality (fresh vs. seawater vs. recycled); treatment train complexity; redundancy requirements | **PEM +30-50% more expensive**: ASTM Type II (<1 µS/cm) requires RO+EDI+polishing vs Alkaline (<5 µS/cm) requiring RO+mixed-bed only |
| **03.2 Raw Water Supply** | 1–2% | Source type (municipal, surface water, groundwater, seawater); pipeline distance; pumping head; desalination if seawater | TECHNOLOGY-NEUTRAL. Desalination (RO) adds €200-400K per 1,000 m³/day capacity — relevant for coastal MENA projects |

**Scale sensitivity: LOW** — water treatment capacity scales near-linearly with plant capacity. Unit cost (€/kW) is roughly constant across scales. Water demand: ~10-11 L/kg H₂ for both technologies.

---

### CAT-04: Hydrogen Processing (8–15% of total CAPEX)

**Description:** Downstream hydrogen compression, purification, drying, storage, and offtake interface. This is the category where Alkaline's atmospheric output creates a significant cost penalty vs PEM's pressurized output.

| Subcategory | % of Total | Key Cost Drivers | PEM vs Alkaline |
|------------|-----------|-----------------|-----------------|
| **04.1 Compression** | 3–8% | Inlet pressure (PEM 30 bar vs Alkaline 1 bar); outlet pressure requirement (pipeline 30-80 bar, storage 200-500 bar, mobility 500-900 bar); compressor type; number of stages | **Alkaline +100-200% more expensive**: Atmospheric output requires full compression train; PEM's 30 bar eliminates first 1-2 compression stages, saving 30-50% on compression CAPEX |
| **04.2 Purification & Drying** | 2–4% | Required H₂ purity (refinery 99.9% vs mobility 99.97%+); inlet purity (PEM 99.99% vs Alkaline 99.9%); deoxo vs PSA vs TSA | **Alkaline +50-100% more expensive** for mobility applications (requires deoxo catalytic purifier); for industrial applications both technologies generally sufficient |
| **04.3 Storage & Logistics** | 2–4% | Storage type (compressed gas vessels, tube trailers, pipeline injection); required buffer capacity (hours/days of production); offtake interface (pipeline, trailer filling, liquefaction) | TECHNOLOGY-NEUTRAL. Determined by offtake logistics, not electrolyzer technology |

**Scale sensitivity: MODERATE** — compression cost scales sub-linearly (larger compressors are more efficient per unit throughput). Storage cost scales near-linearly (vessel volume proportional to H₂ mass).

---

### CAT-05: Civil & Construction (8–15% of total CAPEX)

**Description:** Site preparation, buildings, foundations, and structural works. Alkaline's larger footprint (80 m²/MW vs PEM 50 m²/MW) drives higher civil costs.

| Subcategory | % of Total | Key Cost Drivers | PEM vs Alkaline |
|------------|-----------|-----------------|-----------------|
| **05.1 Site Preparation** | 3–6% | Greenfield vs brownfield; soil conditions; contamination remediation; flood risk; seismic zone; site accessibility | **Alkaline +30-60% more expensive**: 60% larger footprint means more earthworks, drainage, paving |
| **05.2 Buildings & Structures** | 3–5% | Electrolyzer hall (enclosed vs open-air); control room blast protection; warehouse; office; local building codes; climate (snow/wind loads) | **Alkaline +40-60% more expensive**: Larger electrolyzer hall; additional KOH electrolyte storage building |
| **05.3 Foundations** | 2–4% | Soil bearing capacity; dynamic loading (compressors); stack module weight; pipe rack foundations | **Alkaline +30-50% more expensive**: More equipment to support (larger footprint, heavier components) |

**Scale sensitivity: MODERATE** — site preparation costs have a high fixed component (mobilization, access roads). Building area scales with plant capacity but with economies of scale (a 200 MW hall is not 10× the cost of a 20 MW hall).

---

### CAT-06: Thermal Management (2–5% of total CAPEX)

| Subcategory | Description | Key Cost Drivers |
|------------|------------|-----------------|
| **06.1 Cooling Systems** | Heat rejection for electrolyzer (15-25% of electrical input) and compression intercoolers | Cooling type (wet vs dry); ambient temperature; water availability; local environmental regulations on thermal discharge |
| **06.2 Heat Recovery** | District heating or industrial heat export integration | Proximity to heat offtaker; temperature match (Alkaline 80°C > PEM 65°C); heat exchanger and piping |

**Technology differentiation:** Alkaline generates higher-grade waste heat (80°C vs PEM 65°C) — more viable for district heating, which can offset CAPEX through heat revenue. Heat recovery adds €50-100/kW for the heat export system but can generate €5-15/MWh heat revenue.

---

### CAT-07: Instrumentation & Controls (3–6% of total CAPEX)

| Subcategory | % of Total | Description |
|------------|-----------|------------|
| **07.1 DCS/SIS** | 2–3% | Distributed Control System + Safety Instrumented System to IEC 61511. Single MAC vs multi-vendor integration affects cost. |
| **07.2 Instrumentation** | 1–2% | H₂ purity analyzers, dew point meters, flow meters (custody transfer), gas detectors, flame detectors, temperature/pressure transmitters |
| **07.3 Telecom/Cybersecurity** | 0.5–1% | Plant network, remote operations connectivity, OT cybersecurity per IEC 62443 |

**Technology differentiation: MINIMAL.** Both technologies require similar automation scope. PEM may have slightly more instrumentation (individual cell voltage monitoring) but the difference is <5% of this category.

---

### CAT-08: Indirect & Owner's Costs (15–25% of total CAPEX)

**Description:** Non-equipment costs covering engineering, management, contingency, and financing. This category is more dependent on project delivery model and developer experience than on technology choice.

| Subcategory | % of Direct Costs | Key Drivers |
|------------|-------------------|------------|
| **08.1 Engineering & Design** | 5–10% | FEED vs detailed engineering split; in-house vs outsourced engineering; project complexity (FOAK vs nth-of-a-kind) |
| **08.2 Procurement & Supply Chain** | 2–4% | Global vs local sourcing; logistics complexity; inspection requirements; import duties |
| **08.3 Construction Management** | 3–6% | EPCM vs LSTK vs multi-contract; construction duration; site location (remote = higher mobilization) |
| **08.4 Owner's Costs** | 3–5% | Project management team; legal and permitting; insurance (construction all-risk); land cost; development costs |
| **08.5 Contingency** | 10–30% of subtotal | Estimate maturity: Class 5 (±30-50%) → 25-30% contingency; Class 4 (±20-30%) → 15-20%; Class 3 (±10-20%) → 10-15%. FOAK projects: +5-10% additional |
| **08.6 Financing During Construction** | Varies | Construction duration; interest rate environment; debt/equity ratio; commitment fees |

**Technology differentiation: MINIMAL** for engineering/management. PEM may have slightly higher contingency (less reference data, higher technology uncertainty). FOAK PEM projects: contingency +5-10% vs standard.

---

## 4. Cost Breakdown Template (AACE Class 4 — Feasibility Estimate)

| Category | PEM (100 MW) % | Alkaline (100 MW) % | PEM (100 MW) €/kW | Alkaline (100 MW) €/kW |
|----------|---------------|---------------------|-------------------|----------------------|
| 01. Electrolyzer System | 32% | 28% | 480 | 360 |
| 02. Electrical Infrastructure | 14% | 15% | 210 | 195 |
| 03. Water Systems | 4% | 3% | 60 | 45 |
| 04. Hydrogen Processing | 9% | 12% | 135 | 156 |
| 05. Civil & Construction | 10% | 13% | 150 | 169 |
| 06. Thermal Management | 3% | 3% | 45 | 45 |
| 07. Instrumentation & Controls | 4% | 4% | 60 | 52 |
| 08. Indirect & Owner's Costs | 24% | 22% | 360 | 286 |
| **TOTAL (€/kW)** | | | **~1,500** | **~1,308** |
| **TOTAL (M€, 100 MW)** | | | **~150** | **~131** |

*Note: These are AACE Class 4 indicative values (±20-30%) based on IRENA 2024, IEA GHR 2025, and Technology Card cost profiles. Project-specific values will vary based on location, offtake, site conditions, and procurement strategy.*

---

## 5. Cost Driver Sensitivity Matrix

| Cost Driver | Impact on Total CAPEX | Affected Categories | Technology-Specific? |
|------------|----------------------|---------------------|---------------------|
| **Technology choice (PEM vs Alkaline)** | ±10-20% | 01, 04, 05 | YES — primary driver |
| **Plant scale (MW)** | −10-25% per doubling | 01 (strong), 05 (moderate), 08 (strong) | YES — PEM learning rate 15%, Alkaline 10% |
| **Site selection (greenfield vs brownfield)** | ±5-15% | 02, 05, 08 | NO |
| **Offtake pressure requirement** | ±3-8% | 04.1 | YES — Alkaline more sensitive (atmospheric start) |
| **Water source (fresh vs seawater vs recycled)** | ±1-3% | 03 | NO |
| **EPC contract strategy (LSTK vs EPCM vs multi-contract)** | ±5-10% | 08 | NO |
| **Regional labor and material costs** | ±10-20% | 02, 05, 08 | NO |
| **FOAK premium** | +10-20% | ALL | Technology-dependent: PEM FOAK premium higher than Alkaline |

---

## 6. Taxonomy Usage Guidelines

### For Cost Library Construction
1. Every cost entry MUST be assigned to one category and one subcategory
2. If a cost source provides data for multiple categories, create separate entries per category
3. Tag each entry with applicable technology, scale range, and region
4. Cross-reference with Gold Dataset project when the cost is project-specific
5. Cross-reference with Technology Card when the cost is a technology-level benchmark

### For the Future Cost Agent
1. Query by `cost_category` + `technology_type` + `scale_range` for targeted benchmarking
2. Use `cost_scaling_methodology.md` for scale adjustments
3. Weight cost estimates by `cost_confidence_framework.md` class
4. Aggregate categories bottom-up for total CAPEX range estimates

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer & Industrial Project Controller | Initial cost taxonomy framework |
