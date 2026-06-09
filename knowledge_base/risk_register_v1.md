# Risk Register v1 — Green Hydrogen Project Risk Library

**Document:** Ranked Risk Register
**Date:** 2026-06-05
**Author:** Senior PMO Risk Manager
**Library Scope:** 30 risks across 8 categories
**Evidence Basis:** Gold Dataset (10 projects), Technology Cards (TC-PEM-001, TC-ALK-001), IEA/IRENA/Hydrogen Council industry reports

---

## Risk Distribution Summary

| Risk Class | RPN Range | Count | % |
|-----------|-----------|-------|---|
| 🔴 Critical | 81–125 | 0 | 0% |
| 🟠 High | 46–80 | 0 | 0% |
| 🟡 Medium | 21–45 | 12 | 40% |
| 🟢 Low | 1–20 | 18 | 60% |

**No Critical or High residual risks** — this is correct for a pre-mitigation risk assessment at the technology/project-class level. Individual projects will have Critical/High risks based on their specific circumstances (location, developer experience, offtake status). This register provides the **baseline risk profile** against which project-specific risks are assessed.

---

## Top 10 Medium Risks (RPN 21–45)

### #1 — RK-SCP-001: Electrolyzer Manufacturing Capacity Shortfall (RPN 36)
**P:3 I:4 D:3 | Class: Medium | Category: Supply Chain**

**Why this ranking:** PEM OEM duopoly at >100 MW scale makes this the most impactful supply chain risk. The probability (3) reflects tightening manufacturing capacity through 2028-2030. The impact (4) is major: 12-24 month delivery delay threatens project viability.

**Key evidence:** ITM Power capacity reservation model (REFHYNE II). Siemens Energy Berlin gigafactory supplying 4 of 6 Gold Dataset PEM projects. Normand'Hy's 12-module delivery demonstrating gigafactory capability.

**Mitigation priority:** Capacity reservation at pre-FID. Backup OEM qualification during FEED. BOP stack-agnostic design.

---

### #2 — RK-SCP-005: EPC Contractor Performance Failure (RPN 36)
**P:3 I:4 D:3 | Class: Medium | Category: Supply Chain**

**Why this ranking:** The hydrogen EPC market is immature. No single contractor has delivered a >100 MW green hydrogen plant. The Gold Dataset shows diverse, fragmented EPC approaches (HH1 EPCM, HGHH split scope, HyDeal 4 FEED contractors).

**Key evidence:** HH1: Worley EPCM with Shell owner oversight. HGHH: Split Siemens Energy (electrolyzer) + Kraftanlagen (BOP). HyDeal España: 4 FEED contractors + TSK Owner's Engineer.

**Mitigation priority:** Competitive FEED+EPC procurement. Owner's Engineer with hydrogen experience. Integrated FAT before site commissioning.

---

### #3 — RK-GRD-001: Grid Connection Delay (RPN 32)
**P:4 I:4 D:2 | Class: Medium | Category: Grid & Energy**

**Why this ranking:** Highest probability in the Grid category (4 — >40% of European projects affected). The impact (4) is major: 3-6 month delay, €15M cost at 100 MW. But detectability (2) is good — 6-12 month warning through TSO monitoring.

**Key evidence:** HH1 required new TenneT 380 kV substation. HGHH benefited from existing Moorburg 380 kV connection — brownfield advantage explicitly cited.

**Mitigation priority:** TSO engagement at pre-feasibility. Direct transformer procurement. 6-month hidden schedule buffer. Mobile substation interim solution.

---

### #4 — RK-CST-001: Construction Schedule Overrun (RPN 32)
**P:4 I:4 D:2 | Class: Medium | Category: Construction**

**Why this ranking:** Cumulative overrun is the most likely construction risk (P:4). HH1's 3+ year construction period and Normand'Hy's 5-year development timeline demonstrate realistic durations.

**Key evidence:** HH1: Aug 2022 start → 2025/2026 COD (3-4 years). Normand'Hy: 2021 announcement → 2026 COD (5 years). HGHH: Brownfield advantage enables faster 22-month construction.

**Mitigation priority:** 12-month schedule contingency. Modular construction (HH1 model). Schedule reserves held at PM level.

---

### #5 — RK-FIN-003: Project Financing Failure (RPN 30)
**P:3 I:5 D:2 | Class: Medium | Category: Financial**

**Why this ranking:** Highest impact (5 — Critical) of any Medium risk. Financing failure kills the project. Masshylia's 83% scale-down demonstrates the consequence of unsecured financing.

**Key evidence:** Masshylia: 120 MW → 20 MW due to subsidy dependency. HyDeal: Strong offtake but no FID. Galp Sines: EIB €430M model for public-bank-led financing.

**Mitigation priority:** Secure public funding before approaching commercial lenders. Lender's technical advisor engagement during FEED. Conservative DSCR projections.

---

### #6 — RK-FIN-002: Hydrogen Offtake Default/Revenue Shortfall (RPN 30)
**P:3 I:5 D:2 | Class: Medium | Category: Financial**

**Why this ranking:** Second highest impact (5 — Critical). Offtake is existential. But probability (3) varies significantly by offtaker type.

**Key evidence:** HyDeal: Strongest offtake (20-year, 6.6 Mt, two investment-grade offtakers) but no FID. HySynergy: Operational offtake delivering since Feb 2025. Masshylia: Affiliated offtaker insufficient to support full scale.

**Mitigation priority:** 80%+ under take-or-pay at FID. Diversified offtake portfolio. Investment-grade counterparties.

---

### #7 — RK-REG-003: Subsidy Dependency/Withdrawal (RPN 30)
**P:3 I:5 D:2 | Class: Medium | Category: Regulatory**

**Why this ranking:** Near-universal dependency on public funding. Masshylia's 83% scale-down is the clearest risk evidence in the entire library.

**Key evidence:** Masshylia: 120→20 MW scale-down explicitly attributed to subsidy uncertainty. Normand'Hy: French State + EU IPCEI. HGHH: >€250M confirmed before FID.

**Mitigation priority:** Do NOT take FID before subsidy confirmation. Diversify subsidy sources. Demonstrate pathway to unsubsidized viability by year 10.

---

### #8 — RK-TEC-005: Multi-Vendor Control System Integration (RPN 27)
**P:3 I:3 D:3 | Class: Medium | Category: Technical**

**Why this ranking:** Moderate across all dimensions. Common in FOAK multi-vendor plants.

**Key evidence:** HH1: Yokogawa MAC appointment specifically to manage integration risk. HGHH: Split scope (Siemens + Kraftanlagen + HH-WIN) increases integration challenge.

**Mitigation priority:** Single MAC with contractual integration responsibility. Integrated FAT before site commissioning.

---

### #9 — RK-CST-002: Module Integration/Commissioning Failure (RPN 27)
**P:3 I:3 D:3 | Class: Medium | Category: Construction**

**Why this ranking:** Moderate probability and impact for FOAK plants. Sequential module delivery (Normand'Hy) vs parallel (HH1) affects risk profile.

**Key evidence:** Normand'Hy: 12 staggered modules requiring sequential commissioning. HH1: 10 parallel rows enabling simultaneous commissioning.

**Mitigation priority:** First-module learning optimization. Integrated FAT. Single MAC for integration.

---

### #10 — RK-TEC-003: H₂ Processing Equipment Failure (RPN 27)
**P:3 I:3 D:3 | Class: Medium | Category: Technical**

**Why this ranking:** Routine industrial risk — compressors and PSA systems have well-known failure modes. Affects both technologies but Alkaline more severely (atmospheric output requires full compression train).

**Key evidence:** Industrial gas plant reliability benchmarks. N+1 compressor configuration is standard best practice.

**Mitigation priority:** N+1 compressor configuration. Online condition monitoring. Spare parts inventory for long-lead items.

---

## Top 10 Low Risks (RPN 1–20)

### #11 — RK-TEC-001: PEM Stack Degradation (RPN 24)
**P:3 I:4 D:2 | Class: Medium | Category: Technical**

Despite RPN 24 (Medium), this is among the most **important** risks for PEM projects — high impact, good detectability through EIS monitoring. 17% frequency in reference projects.

**Key evidence:** TC-PEM-001 TCR-PEM-001. Puertollano operational data. REFHYNE I degradation informing REFHYNE II warranty.

---

### #12 — RK-SCP-004: Long-Lead Electrical Equipment (RPN 24)
**P:4 I:3 D:2 | Class: Medium | Category: Supply Chain**

Transformer lead times of 18-36 months are the industry norm. Managed through early procurement.

**Key evidence:** HH1 165t transformer transport. HGHB brownfield advantage (no new transformer).

---

### #13 — RK-REG-001: Environmental Permitting Delays (RPN 24)
**P:4 I:3 D:2 | Class: Medium | Category: Regulatory**

Affects >50% of large European industrial projects. Schedule impact only (no equipment damage).

**Key evidence:** Masshylia Concertation process. HGHH 3-year permitting phase.

---

### #14 — RK-GRD-003: Renewable Intermittency (RPN 24)
**P:3 I:4 D:2 | Class: Medium | Category: Grid & Energy**

Technology-differentiated: PEM captures 8-12% more solar energy than Alkaline. The most financially significant operational risk over 20 years.

**Key evidence:** Puertollano solar+PEM+battery model. HH1 offshore wind+Alkaline matching.

---

### #15 — RK-GRD-002: Grid Capacity Congestion (RPN 24)
**P:3 I:4 D:2 | Class: Medium | Category: Grid & Energy**

Growing barrier in European industrial clusters. Site selection is the primary mitigation.

**Key evidence:** HH1 required new 380 kV substation. HGHb reused existing 380 kV.

---

### #16 — RK-FIN-001: CAPEX Overrun (RPN 24)
**P:3 I:4 D:2 | Class: Medium | Category: Financial**

FOAK projects average 20-30% overrun across all sectors. Budget 25% contingency at feasibility.

**Key evidence:** Masshylia scale-down as pre-FID CAPEX discovery. HH1 €5,000/kW FOAK cost.

---

### #17 — RK-REG-002: RFNBO Certification (RPN 20)
**P:2 I:5 D:2 | Class: Low | Category: Regulatory**

Impact is critical (loss of green premium) but probability is low for well-designed projects. HySynergy achieved certification in 2025.

**Key evidence:** HySynergy RFNBO certified. HH1 designed for certification from inception.

---

### #18 — RK-TEC-002: Alkaline Carbonate Formation (RPN 20)
**P:5 I:2 D:2 | Class: Low | Category: Technical**

Almost certain to occur (inherent chemistry) but minor impact (managed through routine maintenance). A textbook example of FMEA advantage — high probability does not mean high risk.

**Key evidence:** TC-ALK-001 TCR-ALK-001. 100+ years of chlor-alkali management experience.

---

### #19 — RK-OPS-001: Workforce Shortage (RPN 18)
**P:3 I:3 D:2 | Class: Low | Category: Operational**

Technology-differentiated: PEM talent pool scarcer than Alkaline (chlor-alkali transfer).

**Key evidence:** Air Liquide internal workforce advantage. Iberdrola+Fertiberia partnership model.

---

### #20 — RK-FIN-004: OPEX Escalation (RPN 18)
**P:3 I:3 D:2 | Class: Low | Category: Financial**

Limited operational data for large-scale plants. OEM maintenance estimates may be optimistic.

**Key evidence:** Puertollano (3+ years operational data). HySynergy (grid balancing revenue offsets OPEX).

---

## Remaining Low Risks (RPN <18)

| Rank | ID | Risk | RPN | Note |
|------|----|----|-----|------|
| 21 | RK-CST-003 | Site Conditions | 18 | Brownfield remediation risk; HGHH Moorburg coal ash case study |
| 22 | RK-REG-005 | Safety Regulatory (ATEX/Seveso) | 16 | Experienced developers mitigate; new entrants face higher probability |
| 23 | RK-ENV-001 | Water Scarcity/Community Opposition | 16 | Location-dependent; Galp Sines recycled water model mitigates |
| 24 | RK-GRD-004 | Electricity Price Volatility | 15 | Perfect detectability makes this Low despite P:5 — the FMEA advantage case study |
| 25 | RK-TEC-004 | Technology Obsolescence | 12 | 15% PEM learning rate documented; BOP stack-agnostic design mitigates |
| 26 | RK-SCP-003 | OEM Single-Source Dependency | 12 | Perfect visibility (publicly traded OEMs); managed through procurement |
| 27 | RK-SCP-002 | Iridium Supply Constraint | 8 | Medium-term (2030+) risk; loading reduction technology progressing |
| 28 | RK-GRD-005 | Power Quality Issues | 12 | Well-characterized during FEED; filtering/ride-through solutions available |
| 29 | RK-REG-004 | Land Acquisition | 12 | Most projects target industrial zones/brownfield; HGHH Moorburg model |
| 30 | RK-OPS-002 | Water Supply Interruption | 6 | Lowest RPN in library; dedicated water contracts (HH1/Evides model) effectively mitigate |

---

## Risk Prioritization by Project Phase

### Pre-Feasibility Phase (Focus: Deal-breakers)

1. RK-REG-003 Subsidy Dependency (RPN 30)
2. RK-FIN-003 Financing Failure (RPN 30)
3. RK-FIN-002 Offtake Risk (RPN 30)
4. RK-GRD-002 Grid Congestion (RPN 24)
5. RK-REG-001 Permitting Delays (RPN 24)

### FEED & Construction Phase (Focus: Execution)

1. RK-SCP-001 OEM Capacity (RPN 36)
2. RK-SCP-005 EPC Performance (RPN 36)
3. RK-GRD-001 Grid Connection (RPN 32)
4. RK-CST-001 Schedule Overrun (RPN 32)
5. RK-FIN-001 CAPEX Overrun (RPN 24)

### Operations Phase (Focus: Sustained Performance)

1. RK-TEC-001 PEM Degradation (RPN 24)
2. RK-GRD-003 Renewable Intermittency (RPN 24)
3. RK-GRD-004 Electricity Price (RPN 15)
4. RK-OPS-001 Workforce (RPN 18)
5. RK-FIN-004 OPEX Escalation (RPN 18)

---

## Technology-Differentiated Risk Rankings

### PEM-Specific Top Risks
1. RK-TEC-001 Stack Degradation (RPN 24)
2. RK-SCP-002 Iridium Supply (RPN 8)
3. RK-SCP-003 OEM Dependency (RPN 12)
4. RK-TEC-004 Technology Obsolescence (RPN 12)

### Alkaline-Specific Top Risks
1. RK-TEC-002 Carbonate Formation (RPN 20)
2. RK-GRD-003 Renewable Intermittency (amplified for Alkaline — slower dynamics)

### Technology-Neutral (Both affected equally)
All 25 remaining risks apply to both technologies.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior PMO Risk Manager | Initial risk register — 30 risks ranked |

---

*This register provides the baseline risk profile for green hydrogen projects. No risks achieved Critical (RPN≥81) or High (RPN≥46) status at the technology-class level — this is correct. Project-specific risks (location, developer, offtake) will add Critical and High risks in project-level assessments. The register is designed to be filtered by technology, phase, and category for targeted risk reviews.*
