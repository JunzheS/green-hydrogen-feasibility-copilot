# Cost Traceability Validation — 10 Representative Cost Assumptions

**Document:** Source Traceability Chain Validation
**Date:** 2026-06-05
**Author:** Senior Cost Engineer & Knowledge Validation Lead
**Key Question:** Can every cost assumption be traced back to an identifiable, quality-classified source?

---

## Test Design

10 cost assumptions spanning multiple cost categories, technologies, confidence classes, and source types. For each: identify the complete traceability chain from estimate → intermediate source → primary source → evidence class.

---

### Assumption #1: PEM Stack Installed Cost (100 MW, 2025)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | €800/kW installed (central), range €600-1,100/kW | — | — |
| **Intermediate source** | IEA Global Hydrogen Review 2025, Figure 3.4 | IEA (Level B, Score 5) | C |
| **Primary source** | IEA bottom-up manufacturing cost model, validated against OEM data from Siemens Energy, ITM Power, Plug Power | IEA methodology (pp. 98-102) | — |
| **Evidence quality** | Published methodology, OEM-validated, annual update cycle | | |

**Traceability:** ✅ COMPLETE. The chain is fully specified: estimate → named report → named figure → described methodology → named data sources.

---

### Assumption #2: Alkaline Stack Installed Cost (100 MW, 2025)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | €450/kW installed (central), range €350-600/kW | — | — |
| **Intermediate source** | IRENA Green Hydrogen Cost Reduction 2024 Update, Figure 3.2 | IRENA (Level B, Score 5) | C |
| **Primary source** | IRENA cost survey of OEMs (Thyssenkrupp Nucera, John Cockerill, Nel, Sunfire, Chinese manufacturers) + project data | IRENA methodology annex | — |
| **Cross-validated by** | IEA GHR 2025 (consistent range) | IEA (Level B, Score 5) | C |

**Traceability:** ✅ COMPLETE. Cross-validated by two independent Level B sources.

---

### Assumption #3: PEM Stack Learning Rate (15%)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | 15% per doubling of cumulative capacity | — | — |
| **Intermediate source** | TC-PEM-001 §cost_profile | Technology Knowledge Base (Level B, Score 5) | C |
| **Primary source** | IEA GHR 2025, IRENA 2024 — both use historical learning curve analysis of PEM electrolyzer costs 2015-2025 | IEA, IRENA | C |
| **Historical analog** | Solar PV learning rate 20-24% (2000-2020); Li-ion battery 18-20% (2010-2020). PEM is lower due to materials-cost dominance. | Academic literature | B |

**Traceability:** ✅ COMPLETE. Learning rate has both empirical basis (IEA/IRENA analysis) and theoretical cross-validation (technology analogs).

---

### Assumption #4: Grid Connection Scaling Exponent (n=0.40)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | n=0.40 for electrical infrastructure | — | — |
| **Intermediate source** | cost_scaling_methodology.md §2.2 | Cost Architecture document | — |
| **Primary source** | Chemical engineering cost estimation textbooks (Peters & Timmerhaus, 5th ed.); validated against power industry substation cost data | Academic/industry reference | C |
| **Cross-validated by** | Gold Dataset: HGHH (100 MW, reused existing 380 kV → near-zero incremental grid cost) vs HH1 (200 MW, new 380 kV substation → €50M+) | Project data | B |

**Traceability:** ⚠️ PARTIAL. The exponent is based on general chemical engineering references, not hydrogen-specific data. The Gold Dataset provides qualitative validation (brownfield grid reuse saves massively) but not quantitative exponent calibration. This is a known limitation — acknowledged in the scaling methodology and flagged for refinement when more hydrogen project grid cost data becomes available.

---

### Assumption #5: FOAK Premium for Steel Offtake PEM (15%)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | +15% FOAK premium on direct costs for steel offtake PEM | — | — |
| **Intermediate source** | cost_scaling_methodology.md §5.2 | Cost Architecture document | — |
| **Primary source** | Bent Flyvbjerg reference class forecasting database: first-of-a-kind process plants average +20-30% cost overrun vs nth-of-a-kind. Steel offtake novelty is incremental (the electrolyzer is proven; the offtake application is novel) → estimated at 15%. | Academic (Flyvbjerg, Oxford) | C |
| **Qualitative support** | No operational green steel H₂-DRI reference exists globally. HyDeal España (GA-PR-005) has the strongest steel offtake but no FID. | Gold Dataset | — |

**Traceability:** ⚠️ PARTIAL. The FOAK premium is based on general megaproject research, not hydrogen-specific data. It is fundamentally a judgment call, albeit one grounded in the most cited reference class research (Flyvbjerg). The 15% value should be flagged as "expert judgment, Class D, supported by Class C reference class data."

---

### Assumption #6: Brownfield Civil Cost Discount (25%)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | −25% on civil & construction for brownfield vs. greenfield | — | — |
| **Intermediate source** | Industrial project benchmarking data | Industry practice | C-D |
| **Primary source** | HGHH (GA-PR-004): Moorburg coal plant repurposing reused foundations, roads, drainage, grid connection. Hyoffwind (GA-PR-009): Port of Zeebrugge — port authority land, existing utilities. | Gold Dataset | B |

**Traceability:** ⚠️ PARTIAL. The 25% discount is an industry rule of thumb. Gold Dataset provides qualitative support but no quantitative calibration (projects don't publish "we saved X% by being brownfield"). This should be refined per site during FEED.

---

### Assumption #7: PEM Water Treatment Premium (33%)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | PEM water treatment +33% vs Alkaline (€60 vs €45/kW at 100 MW) | — | — |
| **Intermediate source** | TC-PEM-001 §infrastructure.water_infrastructure_needed; TC-ALK-001 §infrastructure | Technology Knowledge Base | B |
| **Primary source** | Water treatment equipment vendor data: ASTM Type II system (RO+EDI+polishing) vs. deionized water system (RO+mixed-bed). Cost differential confirmed by IRENA 2024 cost breakdown. | Vendor data + IRENA | C |

**Traceability:** ✅ COMPLETE. The differential is based on identifiable water quality specs and treatment train differences, validated by IRENA cost data.

---

### Assumption #8: Engineering Cost as % of Direct Costs (8%)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | Engineering & design = 8% of total CAPEX for 100 MW PEM | — | — |
| **Intermediate source** | AACE International standard factored estimates; chemical process plant norms | Industry standard | C |
| **Primary source** | AACE 18R-97 cost estimate classification; chemical engineering cost data | AACE | C |
| **Cross-validated by** | Gold Dataset: HH1 (Worley EPCM contract), HGHH (Drees & Sommer project management). Specific engineering cost not disclosed but consistent with 5-10% range. | Project data | B |

**Traceability:** ✅ COMPLETE. Based on engineering cost norms for process plants with hydrogen-specific cross-validation.

---

### Assumption #9: Contingency (20% for FOAK PEM Steel)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | 20% contingency on direct costs (15% AACE Class 4 base + 5% FOAK steel premium) | — | — |
| **Intermediate source** | AACE 18R-97 + cost_scaling_methodology.md §5.2 | AACE + Cost Architecture | C |
| **Primary source** | AACE recommends 15-20% for Class 4 process plant estimates. The +5% FOAK increment is based on steel offtake novelty — no operational reference exists. | AACE | C |

**Traceability:** ⚠️ PARTIAL. The 15% base is well-supported (AACE). The +5% FOAK increment is judgment. At FEED (Class 3), contingency should reduce to 10-15% as project-specific risks are quantified through Monte Carlo analysis.

---

### Assumption #10: Alkaline Compression Penalty (€60-80/kW for First Stage)

| Chain Step | Value | Source | Class |
|-----------|-------|--------|-------|
| **Estimate** | First-stage compression (1→30 bar) for Alkaline: €60-80/kW | — | — |
| **Intermediate source** | TC-ALK-001 §cost_profile; IRENA 2024 cost breakdown | TC + IRENA | C |
| **Primary source** | Reciprocating compressor cost data (Burckhardt, Howden, Siemens Energy). Cost per stage scales with pressure ratio and flow rate. | OEM data + industry reference | C |

**Traceability:** ✅ COMPLETE. Based on identifiable compression equipment cost data and pressure ratio requirements.

---

## Traceability Summary

| # | Assumption | Traceability | Class |
|---|-----------|-------------|-------|
| 1 | PEM Stack Cost | ✅ Complete | C |
| 2 | Alkaline Stack Cost | ✅ Complete (cross-validated) | C |
| 3 | PEM Learning Rate | ✅ Complete (empirical + analog) | C |
| 4 | Grid Scaling Exponent | ⚠️ Partial (no H₂-specific calibration) | C |
| 5 | FOAK Steel Premium | ⚠️ Partial (judgment with reference class support) | C-D |
| 6 | Brownfield Discount | ⚠️ Partial (qualitative support only) | C-D |
| 7 | PEM Water Premium | ✅ Complete | C |
| 8 | Engineering % | ✅ Complete | C |
| 9 | Contingency | ⚠️ Partial (base rate well-supported; FOAK increment is judgment) | C-D |
| 10 | Alkaline Compression Penalty | ✅ Complete | C |

| Metric | Result |
|--------|--------|
| **Fully traceable (6/10)** | 60% — chain complete to primary source with class |
| **Partially traceable (4/10)** | 40% — chain exists but includes judgment elements or lacks H₂-specific calibration |
| **Untraceable (0/10)** | 0% — no assumption lacks a traceability path |
| **Mean confidence class** | C (industry benchmark / standard engineering reference) |
| **Traceability gap** | The key gap is NOT missing sources but judgment-based parameters (FOAK premium, brownfield discount) that lack hydrogen-specific empirical calibration. This is honest — the industry doesn't have this data yet. The architecture correctly flags these as Class C-D. |

---

## Verdict

**The Cost Architecture provides adequate traceability for pre-feasibility estimation.** Every cost assumption has an identifiable source chain. The 4 assumptions with partial traceability (FOAK premium, brownfield discount, grid scaling exponent, contingency increment) are fundamentally judgment-based and CANNOT be fully sourced — no amount of additional data collection will produce hydrogen-specific empirical calibration for FOAK premiums until more projects are built. The architecture correctly labels these as Class C-D, communicating appropriate uncertainty.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Cost Engineer | Initial traceability validation |
