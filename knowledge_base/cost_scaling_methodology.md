# Cost Scaling Methodology — Green Hydrogen Project CAPEX

**Document:** Scale Adjustment Methodology
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Industrial Project Controller
**Scope:** PEM and Alkaline electrolysis, 5 MW to 1+ GW

---

## 1. Why Costs Scale Non-Linearly

Green hydrogen plants exhibit **economies of scale** — the cost per kW decreases as plant capacity increases. This is driven by three mechanisms:

| Mechanism | Description | Example |
|-----------|------------|---------|
| **Equipment scale efficiency** | Larger equipment units cost less per unit capacity | A 50 MW transformer costs less per MW than five 10 MW transformers |
| **Fixed-cost dilution** | Engineering, permitting, site mobilization are largely fixed regardless of scale | A FEED study costs ~€3-5M whether the plant is 20 MW or 200 MW |
| **Learning-curve effects** | Cumulative global deployment reduces manufacturing cost over time | PEM stack costs decline ~15% per doubling of global installed capacity |

---

## 2. The Power Law Scaling Model

### 2.1 Core Formula

```
Cost_at_Scale_B = Cost_at_Scale_A × (Scale_B / Scale_A)^n

Where:
  n = scaling exponent (cost-capacity factor)
```

| Exponent (n) | Behavior | Example Categories |
|-------------|----------|-------------------|
| 1.0 | **Linear** — cost per kW constant | Water treatment, instrumentation (some components) |
| 0.6–0.8 | **Economies of scale** — typical for process equipment | Electrolyzer stack, compression, heat exchangers, tanks/vessels |
| 0.3–0.5 | **Strong economies of scale** — large equipment or fixed-cost-dominated | Grid connection (fixed TSO study + single transformer), engineering, project management |
| ~0.0 | **Near-fixed** — cost independent of scale | Permitting, land (within reason), owner's minimum team |

### 2.2 Category-Specific Scaling Exponents

| Category | Exponent (n) | Rationale |
|----------|-------------|-----------|
| 01.1 Electrolyzer Stack | 0.85–0.95 | Near-linear: more MW = more cells. Scale savings from larger module sizes and volume pricing. PEM closer to 0.90 (more material-cost-dominated); Alkaline closer to 0.85 (more manufacturing-labor-dominated). |
| 01.3 Power Electronics | 0.75–0.85 | Moderate scale economies: larger rectifier units are more efficient per MW. |
| 02.1 Grid Connection | 0.30–0.50 | Strong scale economies: TSO study cost is fixed; one 200 MVA transformer costs less than two 100 MVA units. |
| 03 Water Systems | 0.80–0.90 | Near-linear: water treatment trains scale proportionally to flow. |
| 04.1 Compression | 0.70–0.80 | Moderate scale economies: larger compressors have better specific power and cost less per unit throughput. |
| 05 Civil & Construction | 0.70–0.85 | Moderate scale economies: building area scales roughly with capacity but with efficiency at larger scales. |
| 07 I&C | 0.60–0.75 | Fixed-cost-dominated: DCS architecture is similar for 20 MW or 200 MW; additional I/O points add marginal cost. |
| 08 Indirect & Owner's | 0.50–0.65 | Strong scale economies: engineering, PM, and owner's team size grow sub-linearly with capacity. |

### 2.3 Worked Examples

**Example 1: PEM Electrolyzer Stack from 20 MW to 100 MW**

```
Reference: 20 MW PEM stack = €900/kW installed (Class 4, 2025)
Target: 100 MW PEM stack cost

Cost₁₀₀ = 900 × (100/20)^0.90
       = 900 × (5.0)^0.90
       = 900 × 4.26
       = €3,834/kW for full 100 MW stack
Per-kW: €3,834/kW / 5.0 = €767/kW

→ Scale savings: 900 → 767 €/kW (15% reduction)
```

**Example 2: Grid Connection from 100 MW to 300 MW**

```
Reference: 100 MW greenfield grid connection = €180/kW (Class 4, 2025)
Target: 300 MW grid connection

Cost₃₀₀ = 180 × (300/100)^0.40
       = 180 × (3.0)^0.40
       = 180 × 1.55
       = €279/kW for full 300 MW connection
Per-kW: €279/kW / 3.0 = €93/kW

→ Scale savings: 180 → 93 €/kW (48% reduction)
```

**Example 3: Full Plant — 20 MW vs 100 MW vs 300 MW PEM**

| Category | n | 20 MW (€/kW) | 100 MW (€/kW) | 300 MW (€/kW) |
|----------|---|-------------|--------------|--------------|
| 01 Electrolyzer System | 0.90 | 550 | 480 | 430 |
| 02 Electrical Infrastructure | 0.45 | 330 | 210 | 155 |
| 03 Water Systems | 0.85 | 70 | 60 | 53 |
| 04 Hydrogen Processing | 0.75 | 175 | 135 | 110 |
| 05 Civil & Construction | 0.80 | 200 | 150 | 125 |
| 06 Thermal Management | 0.80 | 58 | 45 | 38 |
| 07 I&C | 0.65 | 90 | 60 | 47 |
| 08 Indirect & Owner's | 0.55 | 520 | 360 | 280 |
| **TOTAL (€/kW)** | | **~1,993** | **~1,500** | **~1,238** |
| **TOTAL (M€)** | | **~40** | **~150** | **~371** |

**Key insight:** Moving from 20 MW to 100 MW yields a 25% per-kW cost reduction. Moving from 100 MW to 300 MW yields an additional 17% reduction. The largest marginal benefit is in the first scale step.

---

## 3. Learning Curve Effects

### 3.1 Technology Learning Rate

Beyond plant-level scale economies, the electrolyzer industry experiences **manufacturing learning** — stack costs decline as cumulative global manufacturing capacity doubles.

```
Cost_at_Time_B = Cost_at_Time_A × (Cumulative_Capacity_B / Cumulative_Capacity_A)^log₂(1 − LR)

Where LR = learning rate
```

| Technology | Learning Rate | Source | Implication |
|-----------|--------------|--------|------------|
| **PEM** | 15% | IEA GHR 2025, IRENA 2024, Technology Card TC-PEM-001 | Costs decline 15% per doubling of global PEM capacity |
| **Alkaline** | 10% | IEA GHR 2025, IRENA 2024, TC-ALK-001 | Slower decline — technology is already mature |

**Projected stack cost evolution:**

| Year | Global PEM (GW) | PEM Stack (€/kW) | Global Alk (GW) | Alk Stack (€/kW) |
|------|----------------|-----------------|-----------------|-----------------|
| 2025 | 4.5 | 800 | 8.0 | 450 |
| 2028 | 9 | 720 | 14 | 420 |
| 2030 | 18 | 620 | 25 | 395 |
| 2035 | 50 | 480 | 70 | 355 |

### 3.2 Distinguishing Scale Effects from Learning Effects

A common error is double-counting: a 2030 plant at 300 MW benefits from BOTH the scale effect (larger plant) AND the learning effect (cheaper stacks). The methodology calculates them sequentially:

```
Step 1: Adjust reference cost to target scale using power law
Step 2: Adjust scale-adjusted cost to target year using learning curve
```

---

## 4. Step-Change Costs (Discontinuities)

Some costs do not scale smoothly — they have step changes:

| Trigger | Step Change | Example |
|---------|------------|---------|
| **Grid voltage level change** | Moving from 110 kV → 380 kV connection: +€5-10M for higher-voltage substation | ~150 MW threshold in many European grids |
| **Seveso threshold (5 t H₂)** | Additional safety systems, blast protection, safety report | ~10 MW with on-site compressed gas storage |
| **Seveso upper tier (50 t H₂)** | Full safety case, emergency planning zone, public consultation | ~80 MW with on-site compressed gas storage |
| **Compression stage addition** | Each additional compression stage (e.g., 30→100→300→500 bar) | Determined by offtake pressure requirement |
| **Modular vs stick-built** | Modular construction viable below ~50 MW (transportable modules); above requires site assembly | ~50 MW per single module |

---

## 5. Scaling Limitations

### 5.1 When NOT to Use Power Law

- **Cross-technology:** Do not scale a PEM cost to Alkaline, or vice versa. The technologies have different cost structures.
- **Cross-region:** Do not scale a European cost to China or MENA without applying regional multipliers first.
- **Extreme extrapolation:** Do not scale a 5 MW pilot cost to 1 GW (>200×). Maximum recommended extrapolation: 10×.
- **First-of-a-kind projects:** FOAK projects carry a 10-30% premium not captured by standard scaling. Apply FOAK premium separately.

### 5.2 FOAK Premium Guidelines

| Project Type | FOAK Premium (% added to scaled cost) | Rationale |
|-------------|--------------------------------------|-----------|
| First PEM plant >100 MW by developer | +15-25% | Limited internal reference data; learning-by-doing |
| First Alkaline plant >200 MW by developer | +5-15% | Alkaline technology is mature; premium is for integration scale |
| First hydrogen project by developer (any technology) | +20-30% | No internal project delivery capability; full learning curve |
| nth-of-a-kind (same developer, same technology, similar scale) | 0% | Reference class forecasting applies |

---

## 6. Discounting for Procurement Strategy

| Strategy | Cost Impact vs. Benchmark | Rationale |
|----------|--------------------------|-----------|
| **LSTK (Lump-Sum Turnkey)** | +10-20% | Contractor assumes construction risk; prices contingency into lump sum |
| **EPCM (Engineering, Procurement, Construction Management)** | Baseline (0%) | Owner manages interfaces; benchmark costs typically reflect EPCM model |
| **Multi-contract (split scope)** | −5-10% on equipment; +5-10% on integration | Competitive tension on each package, but higher owner's engineering cost |
| **Chinese OEM (Alkaline only)** | −40-60% vs Western OEM | Lower labor and material costs; lower performance guarantees; EU regulatory risk |
| **Framework agreement with OEM** | −5-15% | Volume discount; preferred pricing for multi-project developers |

---

## 7. Usage Guidelines for the Cost Agent

1. **Always document the reference scale and target scale** — do not apply scaling as a black box
2. **Apply scaling sequentially by category** — do not scale total CAPEX; scale each cost category with its own exponent
3. **Flag extrapolations beyond 10×** — require explicit justification
4. **Separate scale effects from learning effects** — use the two-step method
5. **Add FOAK premium as a separate line item** — do not embed in scaling exponents
6. **Document all assumptions** — scaling exponent, learning rate, reference source

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial scaling methodology |
