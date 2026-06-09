# Risk Library Validation Report — 3 Feasibility Test Cases

**Document:** Validation Against Hypothetical Pre-Feasibility Projects
**Date:** 2026-06-05
**Author:** Senior PMO Risk Manager
**Library Version:** Sprint 1 (30 risks)

---

## Case A: France, 100 MW PEM, Steel, 2029

### Project Profile
- **Scale:** 100 MW (medium-to-large commercial)
- **Technology:** PEM (TRL 8, early commercial)
- **Offtake:** Steel (H₂-DRI, industrial process)
- **Country:** France (EU, IPCEI-eligible, nuclear-heavy grid)
- **Maturity:** Pre-feasibility, target COD 2029

### Top 5 Risks for This Project

| Rank | Risk ID | Risk Name | RPN | Class | Why Selected |
|------|---------|-----------|-----|-------|-------------|
| 1 | **RK-FIN-002** | Hydrogen Offtake Default/Revenue Shortfall | 30 | Medium | Steel offtake is the single largest uncertainty. No operational green steel H₂-DRI plant exists globally. The offtaker (steel company) faces its own decarbonization economics, technology risk (DRI shaft furnace), and cyclical industry exposure. Unlike refinery offtakers (proven), steel offtakers are unproven. HyDeal España (GA-PR-005) has the strongest steel offtake in the dataset but no FID — cautionary evidence. |
| 2 | **RK-REG-003** | Subsidy Dependency/Withdrawal | 30 | Medium | French State support (€190M for Normand'Hy) demonstrates France's commitment, but the 2029 COD means the project is exposed to the 2027 French presidential election cycle. Masshylia (GA-PR-002) demonstrates that French hydrogen projects are NOT immune to subsidy risk — 83% scale-down despite being in the same country. |
| 3 | **RK-SCP-003** | OEM Single-Source Dependency (PEM) | 12 (Low) | PEM OEM duopoly at >100 MW. A French steel project would likely select Siemens Energy (Normand'Hy supply chain, 150 km proximity) — but this means single-source dependency. RPN is Low (12) because OEM concentration is a chronic structural risk, not an acute threat. However, for a 20-year steel offtake, the project needs confidence that Siemens Energy (or ITM Power) will still support the stack design through multiple replacement cycles. |
| 4 | **RK-GRD-001** | Grid Connection Delay | 32 | Medium | France's nuclear-heavy grid (70% nuclear) provides stable, low-carbon baseload — good for electrolysis. But the French grid (RTE) faces the same transformer lead time constraints as all of Europe. Normand'Hy (GA-PR-001) is connected to the RTE grid at Port-Jérôme — demonstrating feasibility. A steel site (Dunkirk or Fos-sur-Mer) would need to verify grid capacity at the specific location. |
| 5 | **RK-TEC-001** | PEM Stack Degradation | 24 | Medium | For a steel offtake (baseload 24/7 operation), dynamic operation degradation is less likely than for a solar-coupled project. However, steel H₂-DRI requires consistent, reliable H₂ supply — any unplanned stack replacement outage directly impacts the steel plant's production. The N+1 redundancy mitigation is essential. Puertollano (GA-PR-006, operational PEM) provides degradation data from Spanish solar climate — partially transferable to French conditions. |

### Supporting Evidence

**From Gold Dataset:**
- Normand'Hy (GA-PR-001): Same country, same technology, similar scale (200 MW). Demonstrates PEM deployment in France with Air Liquide/Siemens Energy supply chain. The existence of this project 150 km from likely steel sites provides strong local ecosystem evidence.
- REFHYNE II (GA-PR-008): Same technology, same scale (100 MW), refinery offtake (industrial process — transferable to steel). ITM Power capacity reservation model applicable.
- Masshylia (GA-PR-002): Cautionary evidence on subsidy dependency in France. The scale-down demonstrates that even well-backed projects face financing risk.

**From Technology Cards:**
- TC-PEM-001: PEM suitability for steel rated HIGH. "Pressurized output (30 bar) reduces compression energy for DRI shaft furnace (~10-20 bar requirement). PEM modularity enables phased capacity build-out."
- TC-PEM-001 TCR-PEM-001: Stack degradation risk — relevant for steel baseload operation.

**Risk Gaps:** No risk in the library specifically addresses steel offtake risk (unproven technology application). This is a Sprint 2 addition candidate: "RK-FIN-005: Green Steel Offtake Market Development Risk."

### Suggested Mitigations

1. Structure offtake agreement with steelmaker to include minimum take-or-pay and H₂ price indexed to carbon price (EU ETS) — aligning incentives
2. Engage with French government (France 2030 program) and EU Innovation Fund early — Normand'Hy's €190M French State support is a precedent
3. Select Siemens Energy as OEM (Normand'Hy supply chain proximity) but negotiate fixed-price stack replacement and technology refresh provisions
4. Conduct grid capacity study at target steel site (Dunkirk or Fos-sur-Mer) during pre-feasibility — do not assume RTE capacity
5. Design N+1 stack redundancy — essential for baseload steel offtake where production continuity is critical

---

## Case B: Germany, 300 MW Alkaline, Industrial Hydrogen, 2030

### Project Profile
- **Scale:** 300 MW (large commercial, largest Alkaline green H₂ plant would be FOAK at this scale)
- **Technology:** Alkaline (TRL 9, mature)
- **Offtake:** Industrial hydrogen (multi-offtake: refinery, chemicals, mobility — broad mapping)
- **Country:** Germany (EU, IPCEI, strong industrial base)
- **Maturity:** Pre-feasibility, target COD 2030

### Top 5 Risks for This Project

| Rank | Risk ID | Risk Name | RPN | Class | Why Selected |
|------|---------|-----------|-----|-------|-------------|
| 1 | **RK-FIN-003** | Project Financing Failure | 30 | Medium | 300 MW Alkaline plant estimated CAPEX: ~€360-400M total installed. This is in the "large project finance" category requiring a lending syndicate. No 300 MW dedicated green H₂ Alkaline plant has reached financial close. Lenders will benchmark against HH1 (200 MW, €1B FOAK cost) — but HH1's €5,000/kW all-in cost is not financeable without EU Innovation Fund support. The project must demonstrate a path to €1,200-1,500/kW total installed cost to be bankable. |
| 2 | **RK-FIN-002** | Hydrogen Offtake — Multi-Offtake Complexity | 30 | Medium | Industrial hydrogen supply means MULTIPLE offtakers across refinery, chemicals, and mobility. Each offtaker has different: purity requirements (mobility >99.97%, refinery >99.9%), pressure requirements (pipeline vs. tube trailer), and contract durations. Alkaline's 99.9% purity requires additional purification (deoxo + dryer) for mobility offtake — adding €50-100/kW to that fraction of production. Managing offtake portfolio complexity adds commercial risk. |
| 3 | **RK-SCP-001** | Electrolyzer Manufacturing Capacity (Alkaline-adjusted) | 24 (Medium, Alkaline variant) | For Alkaline, probability is lower (more OEMs) but at 300 MW scale, only 2-3 OEMs can supply (Thyssenkrupp Nucera, Sunfire, potentially John Cockerill). Thyssenkrupp Nucera has a 2.5 GW/year gigafactory and HH1 (200 MW) reference. Sunfire has a 100 MW Alkaline module under development for RWE GET H2 Nukleus. The capacity exists but must be reserved. |
| 4 | **RK-GRD-001** | Grid Connection Delay | 32 | Medium | 300 MW is equivalent to a medium-sized gas turbine — a significant grid load. German industrial zones (Ruhr, Rheinland) have grid congestion. HGHH (GA-PR-004) demonstrates the brownfield advantage (existing 380 kV connection). A greenfield 300 MW project would need new or upgraded grid infrastructure — 3-5 year lead time in congested German grid zones. |
| 5 | **RK-CST-001** | Construction Schedule Overrun | 32 | Medium | At 300 MW, this would be the LARGEST dedicated green hydrogen Alkaline plant in the world (HH1 is 200 MW). FOAK at this scale. HH1's 3-4 year construction for 200 MW suggests 4-5 years for 300 MW. The 2030 COD target requires FID by 2026-2027 — aggressive but achievable if the project leverages Thyssenkrupp Nucera's HH1 experience. |

### Key Technology Differentiation

This case demonstrates Alkaline's risk advantage at large scale:
- **No iridium risk** (RK-SCP-002) — Alkaline uses nickel and steel
- **Lower OEM concentration risk** (RK-SCP-003) — 10+ Alkaline OEMs vs 4 PEM
- **BUT higher grid/renewable integration risk** — Alkaline's slower dynamics mean the project should pair with steady renewable sources (offshore wind, hydro) rather than solar
- **RWE GET H2 Nukleus** (300 MW, Germany, Alkaline portion = 100 MW Sunfire) would be a direct reference if added to the Gold Dataset. This gap is noted.

### Supporting Evidence

**From Gold Dataset:**
- Holland Hydrogen I (GA-PR-003): Same technology, 200 MW (closest scale reference), neighboring country (Netherlands). Thyssenkrupp Nucera Scalum stacks. The single most relevant reference project.
- Hamburg Green Hydrogen Hub (GA-PR-004): Germany, 100 MW — but PEM, not Alkaline. Demonstrates German regulatory/IPCEI funding pathway.
- HySynergy (GA-PR-007): 20 MW Alkaline, operational — small scale but provides operational data and RFNBO certification precedent.

**From Technology Cards:**
- TC-ALK-001: TRL 9, mature. Industrial hydrogen applications all rated HIGH suitability. Cost: €400/kW stack at 200+ MW scale.

### Suggested Mitigations

1. Secure offtake portfolio with minimum 3 offtakers (refinery anchor + chemical + mobility) — no single offtaker >50% of production
2. Reserve Thyssenkrupp Nucera manufacturing capacity during pre-feasibility (HH1 model)
3. Target brownfield site with existing grid connection (HGHH/Moorburg model) — German coal phaseout provides multiple candidates
4. Pair with offshore wind PPA (North Sea) — steadier than solar, better suited to Alkaline's baseload profile
5. Engage KfW/IPCEI/BMBF for German federal funding early — HGHH's >€250M confirmed before FID is the model

---

## Case C: Spain, 20 MW PEM, Refinery, 2028

### Project Profile
- **Scale:** 20 MW (small commercial/demonstration)
- **Technology:** PEM (TRL 8)
- **Offtake:** Refinery (proven application)
- **Country:** Spain (EU, excellent solar resource)
- **Maturity:** Pre-feasibility, target COD 2028

### Top 5 Risks for This Project

| Rank | Risk ID | Risk Name | RPN | Class | Why Selected |
|------|---------|-----------|-----|-------|-------------|
| 1 | **RK-REG-003** | Subsidy Dependency | 30 | Medium | Spain's hydrogen subsidies flow through PERTE ERHA (Proyectos Estratégicos para la Recuperación y Transformación Económica — Energías Renovables, Hidrógeno y Almacenamiento). The program is competitive, with multiple rounds. A 20 MW refinery project competes against larger projects (HyDeal 7,400 MW, Puertollano expansion to 800 MW) for the same funding pool. Small projects may be deprioritized vs. giga-scale strategic projects. |
| 2 | **RK-GRD-003** | Renewable Intermittency (Solar) | 24 | Medium | Spain's solar resource is excellent but variable. A 20 MW PEM + ~50 MW solar PV configuration (similar to Puertollano's 20+100 MW design) must manage daily solar cycling. PEM is the correct technology choice (fast ramp, low min load) but the renewable profile MUST be modeled with hourly resolution during feasibility — annual average capacity factors are insufficient. The 2028 COD is tight — the project must start permitting immediately. |
| 3 | **RK-TEC-001** | PEM Stack Degradation Under Solar Cycling | 24 | Medium | 20 MW + solar PV = high daily cycling. Puertollano (GA-PR-006) is the DIRECT reference — same country, same technology, same scale, same solar profile, operational since 2022. The project should request operational degradation data from Iberdrola/Puertollano (if publicly available) or negotiate warranty terms based on Puertollano's operational profile. |
| 4 | **RK-REG-001** | Environmental Permitting — Water in Southern Spain | 24 | Medium | Southern Spain (Andalusia, Murcia) is water-stressed. Even though 20 MW electrolysis consumes only ~200 m³/day, the water permit will face scrutiny. Puertollano (Ciudad Real, Castilla-La Mancha — also water-stressed) successfully permitted water use — demonstrating feasibility but also the regulatory burden. |
| 5 | **RK-FIN-001** | CAPEX Overrun at Small Scale | 24 | Medium | At 20 MW, CAPEX per kW is higher than at 100 MW (scale premium: ~€900/kW stack vs €800/kW at 100 MW; ~€1,800/kW total vs ~€1,500/kW). A small project has less room for cost overrun — a €5M overrun is 25% of a €20M stack budget vs 6% of an €80M budget at 100 MW. The project financial model is less robust to CAPEX escalation. |

### Why This Case Has the Lowest Overall Risk

Compared to Cases A and B:
- **Proven technology + proven application:** 20 MW PEM for refinery is demonstrated (Puertollano chemical plant, Masshylia biorefinery)
- **Excellent reference project:** Puertollano (GA-PR-006) is operational since 2022 — near-identical profile
- **Small scale reduces absolute risk exposure:** €30-40M total project vs €150M (Case A) or €400M (Case B)
- **Fast deployment:** 20 MW can be built in 18-24 months vs 3-5 years for larger plants
- **Spanish solar resource is among Europe's best** — renewable integration risk is lower, not higher

The primary risk is **permitting timeline** (3 years from now to 2028 COD) and **subsidy competition** (small projects vs. giga-scale). These are manageable with early action.

### Supporting Evidence

**From Gold Dataset:**
- Puertollano (GA-PR-006): THE reference — Spain, PEM, 20 MW, solar PV, operational 2022. Near-perfect match. Provides operational data, regulatory precedent, and supply chain validation.
- Masshylia (GA-PR-002): 20 MW PEM, refinery offtake (biorefinery), France. Similar scale and application but pre-FID. Demonstrates subsidy dependency risk even for well-backed projects.

**From Technology Cards:**
- TC-PEM-001: Refinery application rated HIGH. PEM's pressurized output valuable for refinery H₂ grid (20-40 bar). Dynamic response suits solar profile.

### Suggested Mitigations

1. Apply for PERTE ERHA funding in the next round — do not delay. Small projects need early submission to compete with giga-scale strategic projects.
2. Request operational data from Iberdrola/Puertollano (if accessible) to inform degradation warranty negotiations with OEM
3. Engage water authority during pre-feasibility — Puertollano's successful water permit in water-stressed Ciudad Real provides precedent
4. Select OEM with Spanish/European manufacturing (Nel Hydrogen has European presence; Plug Power is US-based — logistics risk)
5. Budget 25% CAPEX contingency at feasibility — small projects are less robust to overruns

---

## Cross-Case Analysis

| Dimension | Case A (FR Steel PEM 100MW) | Case B (DE Industrial Alk 300MW) | Case C (ES Refinery PEM 20MW) |
|-----------|---------------------------|--------------------------------|------------------------------|
| **Dominant risk category** | Financial (offtake) | Financial (financing) | Regulatory (subsidy competition) |
| **Top RPN** | 30 | 30 | 30 |
| **Total Medium risks activated** | 8 | 10 | 6 |
| **Technology risk level** | Medium (PEM, limited steel refs) | Low-Medium (Alkaline, FOAK at 300MW) | Low (PEM, Puertollano ref exists) |
| **Best reference project** | Normand'Hy (GA-PR-001) | Holland Hydrogen I (GA-PR-003) | Puertollano (GA-PR-006) |
| **Reference quality** | Good (same country, 2× scale) | Good (neighbor country, 1.5× scale) | **Excellent (same country, same scale)** |
| **Key evidence gap** | No steel offtake PEM project | No German 300MW Alkaline project | No refinery-specific 20MW PEM in Spain |
| **Overall risk assessment** | **Moderate** — financing + unproven steel offtake | **Moderate-High** — FOAK scale + multi-offtake complexity | **Low-Moderate** — proven configuration, excellent reference |

---

## Validation Verdict

**The Risk Library supports meaningful, differentiated risk assessments for all 3 hypothetical pre-feasibility cases.**

The library correctly:
- ✅ Identifies different dominant risks for each case (offtake for steel, financing for 300MW, subsidy for small Spain)
- ✅ Differentiates technology risk (PEM OEM concentration for Case A, Alkaline dynamics for Case B, PEM proven for Case C)
- ✅ References appropriate Gold Dataset projects for evidence
- ✅ Provides specific, actionable mitigations (not generic advice)
- ✅ Identifies evidence gaps honestly (no steel offtake PEM project; no German 300MW Alkaline project)

The library is **ready for Risk Agent integration**. The primary gap is the 9 uncovered subcategories (to be addressed in Sprint 2) and the need for more project-specific risk evidence from additional Gold Dataset projects.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior PMO Risk Manager | Initial validation report — 3 test cases |
