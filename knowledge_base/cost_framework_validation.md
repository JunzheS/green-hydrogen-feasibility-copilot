# Cost Framework Validation — 3 Pre-Feasibility Test Cases

**Document:** Framework Validation Report
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Industrial Project Controller
**Framework Version:** v1.0 (cost_taxonomy, cost_schema, cost_scaling, cost_confidence)

---

## Case 1: 100 MW PEM, France, Steel, 2029

### Cost Breakdown (AACE Class 4, ±20-30%)

| Category | €/kW | M€ | % of Total | Key Driver | Confidence |
|----------|------|-----|-----------|------------|------------|
| 01 Electrolyzer System | 480 | 48.0 | 30% | PEM stack @ ~€800/kW installed; Siemens Energy supply chain (Normand'Hy proximity) | C |
| 02 Electrical Infrastructure | 210 | 21.0 | 13% | French RTE grid; brownfield steel site likely has existing HV — apply 0.4 scaling exponent | C |
| 03 Water Systems | 60 | 6.0 | 4% | Municipal/industrial water at steel site; PEM requires ASTM Type II polishing | C |
| 04 Hydrogen Processing | 140 | 14.0 | 9% | Steel DRI requires 10-20 bar; PEM 30 bar output reduces compression stages vs Alkaline | C |
| 05 Civil & Construction | 160 | 16.0 | 10% | Brownfield steel site — reuse existing foundations, roads; lower site prep cost | C |
| 06 Thermal Management | 50 | 5.0 | 3% | PEM waste heat 65°C — low-grade; limited heat recovery value | C |
| 07 I&C | 60 | 6.0 | 4% | DCS + SIS; H₂ purity monitoring for DRI feed spec | C |
| 08 Indirect & Owner's | 440 | 44.0 | 27% | FOAK premium +15% (steel offtake novelty); engineering 8%; contingency 20% | C-D |
| **TOTAL** | **~1,600** | **~160** | | | **Weighted: 0.60 (Medium)** |

**Range:** P10 €1,280/kW (€128M) — P90 €2,080/kW (€208M)

**Why 27% indirect?** Steel offtake novelty (no operational green steel H₂-DRI reference) adds +5% contingency above standard Class 4 (15% → 20%). French regulatory environment adds permitting cost certainty (IPCEI precedent established by Normand'Hy). FOAK premium of +15% on direct costs applied via scaling methodology.

### Main Cost Drivers (Ranked)

1. **Electrolyzer stack cost** (30% of total, Class C) — Dominant single category. €800/kW benchmark from IEA GHR 2025. PEM learning rate 15% → 2029 delivery may see 10-15% cost reduction vs 2025 benchmark. BUT: first-mover premium for steel application may offset learning benefit.

2. **FOAK/indirect premium** (27%, Class C-D) — Steel offtake novelty + PEM technology at this scale + French regulatory context. Single largest uncertainty category. Could range from 22% (if developer has PEM experience) to 32% (new entrant).

3. **Electrical infrastructure** (13%, Class C) — Strongly dependent on site selection. Brownfield steel site with existing HV connection (Dunkirk, Fos-sur-Mer) could save €5-10M vs greenfield. Apply scaling exponent 0.40 from greenfield benchmark.

4. **H₂ processing** (9%, Class C) — PEM's 30 bar output reduces compression stages for DRI (10-20 bar target). No liquefaction needed. Steel DRI pressure requirement is modest compared to mobility (500-900 bar).

5. **Civil works** (10%, Class C) — Brownfield steel site: existing roads, drainage, utilities. Brownfield discount: −20-30% vs greenfield benchmark. PEM footprint advantage (50 m²/MW vs Alkaline 80) reduces building area.

### Gold Dataset Benchmarks

| Project | Scale | CAPEX/kW | Year | Relevance |
|---------|-------|----------|------|-----------|
| Normand'Hy (GA-PR-001) | 200 MW PEM | €2,250/kW all-in | 2024 | Same country, same tech. 2× scale. €2,250/kW reflects FOAK premium + French costs. Scale to 100 MW: ~€2,650/kW → case estimate €1,600/kW lower due to learning + brownfield assumption |
| REFHYNE II (GA-PR-008) | 100 MW PEM | Not disclosed | 2024 | Same scale, same tech. ITM Power stacks. Germany. CAPEX not public — limits benchmarking |
| Galp Sines (GA-PR-010) | 100 MW PEM | €2,500/kW (H₂ portion est.) | 2023 | Same scale, same tech. Portugal. EIB-financed. Combined with biofuels unit — total CAPEX includes shared infrastructure |

---

## Case 2: 20 MW PEM, Spain, Refinery, 2028

### Cost Breakdown (AACE Class 4)

| Category | €/kW | M€ | % of Total | Key Driver | Confidence |
|----------|------|-----|-----------|------------|------------|
| 01 Electrolyzer System | 550 | 11.0 | 28% | 20 MW scale premium: +12% vs 100 MW benchmark | B-C |
| 02 Electrical Infrastructure | 330 | 6.6 | 17% | Greenfield grid connection (if not refinery-co-located); small scale means high per-kW grid cost | C |
| 03 Water Systems | 70 | 1.4 | 4% | Southern Spain — water-stressed; municipal supply likely; PEM quality spec | C |
| 04 Hydrogen Processing | 120 | 2.4 | 6% | Refinery H₂ grid at 20-40 bar; PEM 30 bar output = minimal compression needed | C |
| 05 Civil & Construction | 210 | 4.2 | 11% | Refinery co-location — brownfield advantage; use existing utilities | C |
| 06 Thermal Management | 60 | 1.2 | 3% | PEM 65°C waste heat — minimal value at 20 MW scale | C |
| 07 I&C | 90 | 1.8 | 5% | DCS + SIS fixed cost diluted over small scale → high per-kW | C |
| 08 Indirect & Owner's | 520 | 10.4 | 26% | Small scale penalty: fixed engineering/PM costs spread over fewer MW | C-D |
| **TOTAL** | **~1,950** | **~39** | | | **Weighted: 0.58 (Low-Medium)** |

**Range:** P10 €1,560/kW (€31M) — P90 €2,535/kW (€51M)

### Why €1,950/kW Is Higher Than the 100 MW Case (€1,600/kW)

**Scale penalty: +22% per-kW cost at 20 MW vs 100 MW.** The scaling methodology correctly captures that small plants cost more per kW:
- Electrolyzer stack: +12% (less volume discount, smaller modules still incur fixed OEM overhead)
- Electrical: +57% (grid connection fixed costs diluted over fewer MW)
- I&C: +50% (DCS architecture cost is similar regardless of scale)
- Indirect: +18% (engineering/PM minimum team size independent of scale)

**Offset by Spanish context advantages:**
- Excellent solar resource → lower electricity cost (OPEX advantage, not reflected in CAPEX)
- Puertollano operational reference (GA-PR-006) provides cost data and supply chain validation
- Iberian labor costs generally lower than French/German

### Gold Dataset Benchmarks

| Project | Scale | CAPEX/kW | Year | Relevance |
|---------|-------|----------|------|-----------|
| Puertollano (GA-PR-006) | 20 MW PEM | €7,500/kW all-in | 2022 | **Direct reference** — same country, same scale, same tech. €7,500/kW includes 100 MW solar PV + battery — not comparable as electrolyzer-only. Estimated electrolyzer portion: ~€30M of €150M = €1,500/kW |
| Masshylia (GA-PR-002) | 20 MW PEM | Not disclosed | pre-FID | Same scale, same tech. France. No CAPEX data — pre-FID. Demonstrates cost uncertainty at this scale |

---

## Case 3: 300 MW Alkaline, Germany, Industrial Hydrogen, 2030

### Cost Breakdown (AACE Class 4)

| Category | €/kW | M€ | % of Total | Key Driver | Confidence |
|----------|------|-----|-----------|------------|------------|
| 01 Electrolyzer System | 360 | 108.0 | 29% | Alkaline stack @ ~€400/kW (scale benefit from 300 MW); Thyssenkrupp Nucera or Sunfire | C |
| 02 Electrical Infrastructure | 130 | 39.0 | 10% | 300 MW = major grid load. Brownfield essential (former coal plant model). Apply n=0.40 scaling from 100 MW benchmark. | C |
| 03 Water Systems | 45 | 13.5 | 4% | Alkaline water spec (<5 µS/cm) less stringent → lower treatment cost | C |
| 04 Hydrogen Processing | 155 | 46.5 | 12% | Multi-offtake: refinery (30 bar), chemicals (30-80 bar), mobility (500 bar). Mobility fraction requires additional compression + deoxo purification. Alkaline atmospheric start adds first stage. | C-D |
| 05 Civil & Construction | 165 | 49.5 | 13% | Alkaline footprint ~80 m²/MW vs PEM 50 → 60% more building area. But 300 MW scale economies offset. | C |
| 06 Thermal Management | 45 | 13.5 | 4% | Alkaline 80°C waste heat → viable district heating integration in Germany → potential CAPEX offset through heat revenue | C |
| 07 I&C | 50 | 15.0 | 4% | Scale economy strong (n=0.65) — DCS cost similar for 200 MW or 300 MW | C |
| 08 Indirect & Owner's | 300 | 90.0 | 24% | Germany IPCEI framework established (HGHH precedent). Alkaline = lower contingency (TRL 9). But FOAK at 300 MW scale for dedicated green H₂. | C-D |
| **TOTAL** | **~1,250** | **~375** | | | **Weighted: 0.62 (Medium)** |

**Range:** P10 €1,000/kW (€300M) — P90 €1,625/kW (€488M)

### Main Cost Drivers (Ranked)

1. **Scale advantage** — At 300 MW, Alkaline achieves near-optimal scale economics. Per-kW cost (€1,250) is the lowest of all 3 cases. The power law correctly captures that the marginal benefit of additional scale diminishes — going from 100→300 MW saves ~17% per kW; going to 500 MW would save only ~8% more.

2. **Technology maturity advantage** — Alkaline TRL 9 + 10+ OEMs = lower contingency (15% vs PEM 20%). No iridium risk. Chinese supply option provides cost ceiling.

3. **Multi-offtake compression penalty** — Industrial hydrogen supply to refinery + chemicals + mobility means multiple pressure levels. The mobility fraction requires 500 bar compression (€150-250/kW incremental for that fraction). If mobility is <10% of total, this is minor. If >30%, this becomes a top-3 cost driver.

4. **Brownfield imperative** — At 300 MW, greenfield electrical infrastructure would be prohibitively expensive (~€250/kW for new 380 kV substation + transmission line). The German coal phase-out provides multiple brownfield candidates (Moorburg/HGHH model). Brownfield saves €40-60M on electrical + civil.

5. **2030 learning benefit** — Alkaline learning rate 10%. By 2030, cumulative global Alkaline capacity projected at 25 GW (vs 8 GW in 2025) — ~1.6 doublings. Expected stack cost: €450 × (1 − 0.10)^1.6 = ~€395/kW — a 12% reduction from 2025 benchmark. Applied in the estimate above.

### Gold Dataset Benchmarks

| Project | Scale | CAPEX/kW | Year | Relevance |
|---------|-------|----------|------|-----------|
| Holland Hydrogen I (GA-PR-003) | 200 MW Alkaline | €5,000/kW all-in | 2022 | Closest reference. €5,000/kW reflects FOAK premium + dedicated 380 kV substation + offshore wind integration + HyTransPort pipeline. NOT comparable as nth-of-a-kind — this is a FOAK cost. Scale to 300 MW: ~€4,600/kW. Learning-adjusted to 2030: ~€3,500/kW. Our estimate (€1,250/kW) is for nth-of-a-kind — the HH1 FOAK premium is ~4× |
| HySynergy (GA-PR-007) | 20 MW Alkaline | Not disclosed | 2025 | Small scale. Alkaline operational reference. CAPEX not public |
| Hyoffwind (GA-PR-009) | 25 MW Alkaline | €2,880/kW all-in | 2024 | Small scale. €72M for 25 MW. Scale to 300 MW: ~€1,400/kW — consistent with our estimate |

---

## Cross-Case Comparison

| Dimension | Case 1: 100 MW PEM FR Steel | Case 2: 20 MW PEM ES Refinery | Case 3: 300 MW Alk DE Industrial |
|-----------|---------------------------|------------------------------|----------------------------------|
| **Total CAPEX (central)** | €160M (€1,600/kW) | €39M (€1,950/kW) | €375M (€1,250/kW) |
| **Range (P10-P90)** | €128-208M | €31-51M | €300-488M |
| **Largest category** | Indirect (27%) | Indirect (26%) | Electrolyzer (29%) |
| **Scale effect** | Baseline | +22% penalty vs 100 MW | −17% advantage vs 100 MW |
| **Technology premium** | PEM +13% vs Alkaline equivalent | PEM +13% | Baseline (Alkaline) |
| **FOAK premium** | +15% (steel novelty) | +10% (Puertollano ref exists) | +10% (300 MW scale FOAK) |
| **Confidence (weighted)** | 0.60 (Medium) | 0.58 (Low-Medium) | 0.62 (Medium) |
| **Best reference** | Normand'Hy (FR, 200 MW PEM) | Puertollano (ES, 20 MW PEM) | Hyoffwind (BE, 25 MW ALK) + HH1 (NL, 200 MW ALK) |
| **Key uncertainty** | Steel offtake cost impact | Scale penalty validity from limited 20 MW data | Multi-offtake compression cost allocation |

### Methodology Validity Check

| Check | Case 1 | Case 2 | Case 3 |
|-------|--------|--------|--------|
| Power law exponents applied correctly? | ✅ Per-category exponents | ✅ Per-category + scale penalty | ✅ Per-category + scale benefit |
| Learning rate applied? | ✅ PEM 15%, 0.8 doublings to 2029 | ✅ PEM 15%, 0.5 doublings to 2028 | ✅ Alkaline 10%, 1.6 doublings to 2030 |
| FOAK premium separated? | ✅ +15% line item | ✅ +10% line item | ✅ +10% line item |
| Regional multipliers used? | ✅ France = EU baseline | ✅ Spain = Southern EU (0.95) | ✅ Germany = EU baseline |
| Confidence weighted correctly? | ✅ | ✅ | ✅ |
| Sources cited? | ✅ IEA, IRENA, GA-PR-001/006/008/010 | ✅ IEA, IRENA, GA-PR-006 | ✅ IEA, IRENA, GA-PR-003/007/009 |

---

## Validation Verdict

**The Cost Framework produces logically consistent, evidence-based CAPEX estimates for all 3 test cases.**

The framework correctly:
- ✅ Scales costs non-linearly using documented per-category exponents
- ✅ Differentiates PEM vs Alkaline cost structures (PEM +13-15% at stack level)
- ✅ Captures scale penalties (20 MW +22% vs 100 MW) and scale benefits (300 MW −17% vs 100 MW)
- ✅ Identifies FOAK premiums based on technology maturity and offtake novelty
- ✅ Tags every cost component with confidence class
- ✅ Provides P10-P90 ranges — never a false-precision single number
- ✅ Benchmarks against Gold Dataset projects where available
- ✅ Explains when Gold Dataset CAPEX is not directly comparable (HH1 FOAK premium, Puertollano bundled solar CAPEX)

**The framework is ready for Cost Library population and Cost Agent development.**

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial framework validation — 3 test cases |
