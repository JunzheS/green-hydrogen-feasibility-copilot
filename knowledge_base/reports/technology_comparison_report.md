# Technology Comparison Report — PEM vs Alkaline Electrolysis

**Document:** Comparative Technology Assessment for Pre-Feasibility Decision Support
**Date:** 2026-06-05
**Author:** Senior Hydrogen Technology Expert
**Source Cards:** TC-PEM-001 (v1.0), TC-ALK-001 (v1.0)
**Purpose:** Support Project Managers and Engineering Consultants in technology selection during pre-feasibility assessment

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Side-by-Side Comparison](#2-side-by-side-comparison)
3. [Dimension-by-Dimension Analysis](#3-dimension-by-dimension-analysis)
4. [Technology Selection Decision Matrix](#4-technology-selection-decision-matrix)
5. [Hybrid PEM+Alkaline Configurations](#5-hybrid-pemalkaline-configurations)
6. [Cost-of-Hydrogen Impact Analysis](#6-cost-of-hydrogen-impact-analysis)
7. [Recommendations by Project Profile](#7-recommendations-by-project-profile)

---

## 1. Executive Summary

PEM and Alkaline electrolysis are both commercially viable technologies for industrial green hydrogen production. The choice between them is not a question of "which is better" but "which is better for this specific project." The decision is primarily driven by:

1. **Project scale** — Alkaline dominates economics at >500 MW; PEM competitive at <200 MW
2. **Renewable profile** — PEM excels with variable solar/wind; Alkaline suits baseload renewables
3. **Application purity needs** — PEM's inherent 99.99% purity eliminates purification cost for mobility and some chemical applications
4. **Risk appetite** — PEM offers better dynamic performance but higher technology risk (iridium, fewer OEMs); Alkaline offers lower technology risk but less operational flexibility
5. **Total cost of ownership** — Alkaline's lower CAPEX is partially offset by higher compression cost (atmospheric output) and purification cost for purity-sensitive applications

| Dimension | PEM | Alkaline | Winner for Typical Projects |
|-----------|-----|----------|---------------------------|
| CAPEX (stack, €/kW) | 600–1,100 (central: 800) | 350–600 (central: 450) | **Alkaline** (40-50% lower) |
| Stack lifetime (hours) | 60,000–80,000 | 80,000–100,000 | **Alkaline** (30-40% longer) |
| Efficiency (kWh/kg H₂) | 55 | 53 | **Alkaline** (4% more efficient) |
| Dynamic response (ramp %/s) | 10 | 2 | **PEM** (5× faster) |
| H₂ purity (%) | 99.99 | 99.9 | **PEM** (no purification needed for mobility) |
| Minimum load (%) | 5 | 15 | **PEM** (better turndown) |
| Cold start (minutes) | 15 | 60 | **PEM** (4× faster) |
| Output pressure (bar) | 30 | 1 (atmospheric) | **PEM** (reduces compression cost) |
| Footprint (m²/MW) | 50 | 80 | **PEM** (40% smaller) |
| Precious metal risk | Yes (Ir, Pt) | No | **Alkaline** (no supply constraint) |
| Technology maturity (TRL) | 8 | 9 | **Alkaline** (fully mature) |
| OEM count (>10 MW) | 4 | 10+ | **Alkaline** (better supply security) |
| Chinese supply option | No | Yes (40-60% cheaper) | **Alkaline** (cost ceiling option) |
| Waste heat quality (°C) | 65 | 80 | **Alkaline** (better for district heating) |

---

## 2. Side-by-Side Comparison

### 2.1 Technical Performance

| Parameter | PEM | Alkaline | Source | Assessment |
|-----------|-----|----------|--------|------------|
| System efficiency | 55 kWh/kg H₂ (LHV 60%) | 53 kWh/kg H₂ (LHV 62%) | IEA GHR 2025; IRENA 2024 | Alkaline is 4% more efficient — significant for OPEX (>70% of LCOH is electricity) |
| Current density | 2.0 A/cm² | 0.4 A/cm² | Academic review papers; OEM datasheets | PEM is 5× more power-dense; requires fewer cells per MW |
| Stack lifetime | 60,000–80,000 hours | 80,000–100,000 hours | OEM warranty data; IEA 2025 | Alkaline stacks last 30-40% longer — lower replacement frequency |
| Degradation rate | ~1.0%/year | ~0.5%/year | IEA Electrolyser Durability 2025 | Alkaline degrades at half the rate — more predictable long-term OPEX |
| H₂ purity | >99.99% | >99.9% | OEM datasheets | PEM purity is "fuel-cell grade" without treatment; Alkaline requires deoxo for mobility |
| Output pressure | 15–50 bar (nominal 30) | 1–30 bar (typical 1) | IEA GHR 2025 | PEM pressurized output saves 30-50% on compression energy |
| Operating temperature | 50–80°C | 60–90°C | Technology cards TC-PEM-001, TC-ALK-001 | Alkaline delivers higher-grade waste heat |

### 2.2 Dynamic Performance

| Parameter | PEM | Alkaline | Pre-Feasibility Impact |
|-----------|-----|----------|----------------------|
| Ramp rate | 10%/second | 2%/second | Solar-only projects: PEM captures more morning/evening generation |
| Minimum load | 5% | 15% | During low renewable periods, PEM can stay online at lower power |
| Cold start | 15 minutes | 60 minutes | After overnight shutdown, PEM restarts 4× faster — critical for solar |
| Warm start | 1 minute | 10 minutes | PEM advantages compound for projects with >100 start-stop cycles/year |
| Load range | 5–100% | 15–100% | PEM offers 90% turndown range vs Alkaline 85% |

**Net dynamic advantage: PEM.** For projects with solar PV (daily cycling), PEM captures an estimated 5-10% more renewable energy over a year due to faster ramp, lower minimum load, and faster cold start. This advantage diminishes for offshore wind (more consistent output) or projects with significant battery storage.

### 2.3 CAPEX

| Cost Component | PEM (€/kW) | Alkaline (€/kW) | Delta | Source |
|---------------|------------|-----------------|-------|--------|
| Electrolyzer stack (installed) | 600–1,100 | 350–600 | PEM +75% | IEA GHR 2025; IRENA 2024; project data |
| Balance of plant | 200–400 | 250–450 | Similar | Industry norms |
| Power supply (rectifier) | 100–200 | 80–180 | Similar | IGBT vs thyristor trade-offs |
| Water treatment | 50–100 | 30–60 | PEM +50% | Stricter water quality for PEM |
| Compression (to 30 bar) | 50–100 | 150–250 | Alkaline +150% | PEM output is already at 30 bar |
| Civil/construction | 100–200 | 150–300 | Alkaline +50% | Larger Alkaline footprint |
| **Total installed (range)** | **1,100–2,100** | **1,010–1,840** | **PEM +5-15%** | IRENA 2024 total system cost |
| **Total installed (central 100 MW)** | **~1,500** | **~1,300** | **PEM +15%** | Author estimate from project data |

**Key insight:** Alkaline's stack cost advantage (~75% cheaper) is partially offset by higher compression cost (atmospheric output), larger civil works, and (for mobility applications) purification cost. At total installed plant cost, the gap narrows to approximately 15% in favor of Alkaline. This is why both technologies compete effectively at 50-200 MW scale.

### 2.4 OPEX

| OPEX Component | PEM | Alkaline | Delta Driver |
|---------------|-----|----------|-------------|
| Electricity | 70% of total OPEX | 75% of total OPEX | PEM saves ~5% via better dynamic integration with renewables |
| Stack replacement | 15% | 10% | Alkaline stacks last 30-40% longer |
| Maintenance | 10% | 8% | PEM has more frequent turnaround + specialized Ti/PFSA expertise |
| Water/consumables | 2% | 2% | Similar |
| Other (insurance, overhead) | 3% | 5% | Alkaline has KOH handling, electrolyte management overhead |

**Net OPEX: Roughly equivalent over 20-year project life.** Alkaline's lower maintenance and stack replacement costs are offset by PEM's electricity savings (higher effective capacity factor from better dynamic operation). The choice of renewable profile has a larger impact on OPEX than the technology choice.

---

## 3. Dimension-by-Dimension Analysis

### 3.1 TRL and Maturity

| | PEM | Alkaline |
|---|-----|----------|
| TRL | 8 (system complete, first commercial plants at >100 MW) | 9 (fully proven in operational environment at scale) |
| Years of industrial operation | ~10 years at >1 MW; ~3 years at >100 MW | >100 years at all scales |
| Cumulative global capacity | ~4.5 GW | ~8 GW |
| Risk profile | Technology risk: moderate (early commercial, limited >100 MW reference data) | Technology risk: low (fully proven across all scales and applications) |
| Warranty confidence | Limited long-term warranty data at >100 MW scale | Established warranty framework from chlor-alkali transfer |

**For pre-feasibility:** Alkaline has lower technology risk. If the project's primary constraint is technology risk (lender requirements, first-time developer), Alkaline is the safer choice. If the project's primary constraint is operational flexibility (variable renewable integration), PEM's higher technology risk may be acceptable.

### 3.2 Dynamic Operation

This is PEM's strongest differentiator and the primary reason to select PEM despite higher CAPEX.

| Scenario | PEM Advantage | Quantitative Impact |
|----------|--------------|--------------------|
| Solar PV only (Spain, MENA, Chile) | **High** | PEM captures 8-12% more solar energy per year due to faster morning ramp, lower minimum load at dawn/dusk |
| Offshore wind (North Sea) | **Low** | Wind is steadier; Alkaline's 15% minimum load rarely binding; capacity factors comparable |
| Onshore wind (Germany, Denmark) | **Medium** | PEM advantage 3-5% better effective capacity factor |
| Solar + battery hybrid | **Low-Medium** | Battery buffers intermittency, reducing PEM's dynamic advantage |
| Grid-connected baseload | **None** | Both technologies operate at steady full load; Alkaline's lower CAPEX dominates |

### 3.3 Industrial Suitability by Application

| Application | PEM Suitability | Alkaline Suitability | Recommended |
|------------|----------------|---------------------|-------------|
| **Ammonia (giga-scale)** | Medium-High | **High** | **Alkaline** — lower CAPEX dominates at >500 MW scale; purity sufficient |
| **Ammonia (small-medium)** | **High** | High | **Tie** — PEM's flexibility valuable for solar-coupled ammonia |
| **Refinery** | **High** | High | **Technology-agnostic** — both proven; choice depends on renewable profile |
| **Steel (DRI)** | High | **High** | **Technology-agnostic** — both viable; Alkaline favored at giga-scale |
| **Methanol** | **High** | High | **PEM** — high purity beneficial for methanol synthesis catalyst |
| **Mobility (distributed)** | **High** | Medium | **PEM** — inherent purity + pressurized output + fast dynamics |
| **Mobility (central hub)** | **High** | High | **Slight PEM advantage** — Alkaline with purification is viable |
| **Industrial heat** | Medium | **High** | **Alkaline** — lower CAPEX + higher-grade waste heat |
| **Grid injection** | **High** | Medium | **PEM** — dynamic response for grid balancing revenue |

### 3.4 Risk Profile Comparison

| Risk Category | PEM Risk Level | Alkaline Risk Level | Notes |
|---------------|---------------|---------------------|-------|
| **Technology risk** | Moderate | Low | PEM has fewer >100 MW references; Alkaline is industrially mature |
| **Supply chain risk** | Moderate-High | Low | PEM depends on iridium (~80% from South Africa); Alkaline materials are abundant |
| **Performance risk** | Moderate | Low | PEM stack degradation under dynamic operation is still being characterized |
| **OEM concentration risk** | High | Low | PEM: 4 major OEMs vs Alkaline: 10+ OEMs + Chinese supply option |
| **Cost overrun risk** | Moderate | Low | PEM costs are less predictable due to precious metal exposure and fewer reference projects |
| **Operational risk** | Low | Low-Moderate | PEM: simpler operation (no liquid electrolyte); Alkaline: KOH handling adds complexity |
| **Regulatory risk** | Low | Low | Both technologies qualify as "green hydrogen" under EU RFNBO rules |

**Overall risk profile: Alkaline is lower-risk across nearly all dimensions.** For first-time hydrogen developers or projects with conservative financing, Alkaline's lower risk profile is a significant advantage. For experienced industrial gas developers (Air Liquide, Linde), PEM's higher technology risk is manageable.

### 3.5 Typical Project Size

| Project Size | Typical Technology Choice | Rationale |
|-------------|--------------------------|-----------|
| <5 MW (pilot/demo) | Either; often PEM | Small scale favors fast deployment; PEM modularity + dynamic capability valued |
| 5–50 MW (industrial demo) | Either; balanced | This is the competitive zone where both technologies are viable; project-specific factors dominate |
| 50–200 MW (commercial) | Either; PEM slightly favored | PEM dominant in recent FIDs at this scale (Normand'Hy, REFHYNE II, HGHH); HH1 (Alkaline) is a notable exception |
| 200–500 MW (large commercial) | Balanced; Alkaline gaining | Larger scale favors Alkaline economics; PEM viable with multiple stack modules |
| >500 MW (giga-scale) | Alkaline dominant | Economics dominate; Alkaline's CAPEX advantage becomes material; NEOM (2 GW), MadoquaPower2X (500 MW) both Alkaline |
| >1 GW (mega-scale) | Alkaline dominant; possible hybrid | DNV projects Alkaline to be 60-70% of 2050 electrolyzer capacity; PEM provides flexibility in hybrid configurations |

---

## 4. Technology Selection Decision Matrix

Use this matrix during pre-feasibility to determine the recommended technology for a project.

### Scoring Instructions

Score each factor 1-5 for the project:
- 1 = Strongly favors Alkaline
- 3 = Technology-neutral
- 5 = Strongly favors PEM

| # | Factor | Weight | Score 1 (Alkaline) | Score 3 (Neutral) | Score 5 (PEM) |
|---|--------|--------|-------------------|-------------------|---------------|
| 1 | Project scale (MW) | 20% | >500 MW | 50–200 MW | <50 MW |
| 2 | Renewable profile | 25% | Baseload/offshore wind/hydro | Onshore wind or solar+battery | Pure solar PV |
| 3 | Application purity need | 15% | Combustion/heat | Ammonia/refinery/steel | Mobility/electronics |
| 4 | Dynamic operation need | 15% | Baseload 24/7 | Moderate cycling (weekly) | Daily cycling (solar) |
| 5 | Technology risk appetite | 10% | Conservative (first-time developer) | Balanced | Experienced developer |
| 6 | Space constraints | 5% | Abundant land | Standard industrial site | Constrained brownfield site |
| 7 | Waste heat offtake value | 5% | District heating nearby | Low-value heat recovery | No heat offtake |
| 8 | Supply chain security priority | 5% | Must avoid critical materials | Balanced | Accepts material risk |

**Weighted Score Interpretation:**
- **>3.5:** PEM recommended
- **2.5–3.5:** Technology-agnostic; project-specific factors or hybrid configuration recommended
- **<2.5:** Alkaline recommended

### Example: Normand'Hy (GA-PR-001) — 200 MW, grid-connected, refinery, France

| Factor | Score | Weight | Weighted |
|--------|-------|--------|----------|
| Scale (200 MW) | 3 | 20% | 0.60 |
| Renewable (grid-mix) | 3 | 25% | 0.75 |
| Purity (refinery + mobility) | 4 | 15% | 0.60 |
| Dynamics (moderate) | 3 | 15% | 0.45 |
| Risk (Air Liquide) | 4 | 10% | 0.40 |
| Space (brownfield) | 4 | 5% | 0.20 |
| Heat (no offtake) | 3 | 5% | 0.15 |
| Supply chain (acceptable) | 3 | 5% | 0.15 |
| **Total** | | | **3.30** |

**Result: Technology-agnostic (scores in balanced zone).** Air Liquide selected PEM — consistent with their technology strategy and the mobility offtake requiring high purity. An Alkaline alternative would also be viable for the refinery offtake portion.

---

## 5. Hybrid PEM+Alkaline Configurations

For projects >200 MW, a hybrid configuration combining both technologies is increasingly considered.

### 5.1 Hybrid Rationale

| PEM Role | Alkaline Role | Optimal Ratio |
|----------|---------------|---------------|
| Flexible "peaking" capacity (solar following, grid services) | Baseload "bulk" production | 20-30% PEM, 70-80% Alkaline |
| High-purity stream for mobility/chemical offtake | Standard-purity stream for combustion/heat offtake | Determined by offtake split |
| Phase 1 fast deployment (modular PEM) | Phase 2-3 bulk expansion (Alkaline) | Phased: 100% PEM Phase 1, transition to hybrid Phase 2+ |

### 5.2 Hybrid Economics

A 500 MW hybrid plant (100 MW PEM + 400 MW Alkaline):
- **Blended CAPEX:** ~€530/kW stack (vs €800/kW all-PEM or €450/kW all-Alkaline)
- **Operational flexibility:** PEM provides renewable balancing; Alkaline provides baseload
- **Risk diversification:** Not dependent on single technology or OEM
- **Complexity penalty:** Two different BOP systems, control integration, maintenance capabilities

**Recommendation:** Hybrid should be evaluated for projects >300 MW with diverse offtake profiles or >500 MW at any application.

---

## 6. Cost-of-Hydrogen Impact Analysis

The technology choice influences LCOH through CAPEX amortization, electricity consumption, stack replacement, and compression/purification costs.

| LCOH Component | PEM (€/kg H₂) | Alkaline (€/kg H₂) | Delta Driver |
|---------------|---------------|---------------------|-------------|
| CAPEX amortization | 0.45 | 0.35 | Alkaline lower stack cost |
| Electricity (at €40/MWh) | 2.20 | 2.12 | Alkaline 4% more efficient |
| Stack replacement | 0.12 | 0.08 | Alkaline longer life |
| O&M | 0.10 | 0.08 | PEM more frequent maintenance |
| Compression (to 30 bar) | 0.05 | 0.12 | PEM already at pressure |
| Water | 0.02 | 0.02 | Similar |
| **Total LCOH (€/kg)** | **2.94** | **2.77** | **Alkaline ~6% lower** |

Note: Assumes 100 MW scale, 4,500 full-load hours/year, 7% WACC, €40/MWh electricity, 20-year project life. Actual LCOH is highly project-specific.

**Key insight:** The LCOH difference of ~€0.17/kg (6%) is within the uncertainty range of pre-feasibility estimates. At €40/MWh electricity, the 4% efficiency difference (€0.08/kg) is the single largest driver after CAPEX. At higher electricity prices (>€60/MWh), the efficiency advantage of Alkaline becomes dominant. At lower electricity prices (<€25/MWh, e.g., MENA solar), CAPEX matters more and Alkaline's advantage widens.

---

## 7. Recommendations by Project Profile

### Profile A: "Large-Scale Baseload" (>500 MW, ammonia/steel, baseload renewable)

**Recommendation: Alkaline**

Rationale: At this scale, CAPEX dominates economics. Alkaline's €350-450/kW vs PEM's €600-800/kW translates to €125-175M CAPEX savings per 500 MW. Baseload operation means dynamic capability has near-zero value. Alkaline's longer stack life and lower degradation rate reduce lifecycle cost. Reference: NEOM (2 GW Alkaline), MadoquaPower2X (500 MW Alkaline).

### Profile B: "Solar-Coupled Mid-Scale" (50-200 MW, solar PV, refinery/mobility)

**Recommendation: PEM**

Rationale: Solar PV daily cycling requires dynamic capability. PEM's 10%/second ramp, 5% minimum load, and 15-minute cold start capture 8-12% more solar energy annually. Refinery/mobility applications value PEM's inherent high purity and pressurized output. The higher CAPEX is offset by higher effective capacity factor and reduced compression/purification cost. Reference: Normand'Hy (200 MW PEM), Puertollano (20 MW PEM).

### Profile C: "First-Time Developer" (20-100 MW, any application)

**Recommendation: Alkaline**

Rationale: Lower technology risk, more OEM choices, lower CAPEX. First-time developers value bankability and proven track record over dynamic performance. Alkaline's >100-year industrial history provides comfort to lenders. No exposure to iridium price volatility. Reference: HySynergy (20 MW Alkaline, Everfuel).

### Profile D: "Constrained Brownfield" (<200 MW, limited space, repurposing existing infrastructure)

**Recommendation: PEM**

Rationale: PEM's 40% smaller footprint per MW is valuable at space-constrained industrial sites. Faster modular deployment minimizes site disruption. Pressurized output simplifies integration with existing hydrogen infrastructure (refineries typically have H₂ distribution at 20-40 bar). Reference: HGHH (100 MW PEM at former Moorburg coal plant), Shell REFHYNE II (100 MW PEM at Wesseling refinery).

### Profile E: "Industrial Heat with District Heating" (>50 MW, baseload, heat offtake)

**Recommendation: Alkaline**

Rationale: Alkaline's higher-grade waste heat (80°C vs 65°C) enables viable district heating integration. Lower CAPEX. Dynamic capability not needed for baseload heat. KOH handling complexity is manageable at industrial sites. Reference: HGHH includes district heating integration.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Hydrogen Technology Expert | Initial technology comparison report |

---

*This comparison report is designed for pre-feasibility technology selection. For detailed FEED-level engineering, project-specific OEM quotations and integrated plant modeling are required. The recommendations are based on technology-level benchmarks and should be validated against project-specific conditions.*
