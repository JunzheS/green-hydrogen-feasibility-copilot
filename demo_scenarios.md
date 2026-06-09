# Demonstration Scenarios — Live Demo Walkthrough

**Document:** 3 pre-configured scenarios for live demos
**Date:** 2026-06-05

---

## Scenario 1: France, Steel, PEM, 100 MW, 2029

### Why This Scenario

This is the **most technically interesting** case. French PEM ecosystem is strong (Normand'Hy 200 MW), steel offtake is novel (no operational reference), and the gate is "Proceed with Caution" — perfect for demonstrating how the Copilot identifies knowledge gaps.

### Inputs

| Field | Value |
|-------|-------|
| Country | France |
| Industry | Steel |
| Technology | PEM |
| Capacity | 100 MW |
| Target COD | 2029 |

### Expected Outputs (Talking Points)

**Executive Dashboard:** Gate = PROCEED WITH CAUTION, confidence GOOD (0.65)

*"Notice the gate is 'proceed with caution' — not because the technology is risky, but because NO PEM plant has ever supplied a steel DRI furnace. The Copilot correctly identifies this as a knowledge gap."*

**Reference Projects:**
- #1 Normand'Hy (FR, 200 MW PEM, score 0.81) — same country, same tech
- #2 REFHYNE II (DE, 100 MW PEM, score 0.81) — exact scale match
- *"Look at why Normand'Hy is ranked #1 — same country, Air Liquide supply chain just 150 km from French steel sites."*

**Technology Assessment:** TRL 8, HIGH suitability for steel
- *"PEM's pressurized output at 30 bar means the hydrogen is already at DRI furnace pressure — no first-stage compression needed. That saves EUR 8-10M vs Alkaline."*

**CAPEX:** EUR 150M (EUR 1,500/kW)
- *"Electrolyzer system is 32% of total. Notice the indirect costs at 24% — that's where the steel FOAK premium sits."*

**LCOH:** EUR 4.96/kg
- *"Electricity is 44% of LCOH. That's the single most important assumption — a EUR 10/MWh change swings LCOH by EUR 0.55/kg."*

**Key Talking Point:** *"The Copilot doesn't just give you numbers — it tells you which numbers matter most and why."*

---

## Scenario 2: Germany, Alkaline, 300 MW, Industrial Hydrogen, 2030

### Why This Scenario

Demonstrates **Alkaline's cost advantage at large scale** and the **FOAK risk at 300 MW**. Best for showing technology comparison.

### Inputs

| Field | Value |
|-------|-------|
| Country | Germany |
| Industry | Industrial Hydrogen |
| Technology | Alkaline |
| Capacity | 300 MW |
| Target COD | 2030 |

### Expected Outputs (Talking Points)

**Executive Dashboard:** Gate = PROCEED, confidence GOOD (0.65)

*"Alkaline at 300 MW in Germany — the gate is PROCEED. Alkaline is TRL 9, fully mature, and Germany has the strongest hydrogen ecosystem in Europe."*

**Reference Projects:**
- #1 Holland Hydrogen I (NL, 200 MW ALK, score 0.93) — near-perfect match
- *"HH1 is Shell's 200 MW Alkaline plant. Same technology, Thyssenkrupp Nucera stacks — a German company. The supply chain is directly transferable."*

**CAPEX:** EUR 346M (EUR 1,154/kW)
- *"Compare this to Scenario 1 — EUR 1,154/kW vs EUR 1,500/kW for PEM. That's Alkaline's cost advantage at scale. But notice the compression cost is higher — atmospheric output means you pay for the first stage."*

**LCOH:** EUR 4.17/kg (lowest of all 3 scenarios)
- *"Lowest LCOH because: (a) Alkaline efficiency advantage, (b) scale economies at 300 MW, (c) German offshore wind provides high capacity factor."*

**Key Talking Point:** *"The Copilot shows you WHY Alkaline wins at large scale — and where it doesn't. At 20 MW, the difference largely disappears. The answer depends on YOUR project."*

---

## Scenario 3: Spain, Refinery, 20 MW PEM, 2028

### Why This Scenario

Demonstrates **small-scale penalty** and **near-identical reference project matching**. Best for showing the traceability feature.

### Inputs

| Field | Value |
|-------|-------|
| Country | Spain |
| Industry | Refinery |
| Technology | PEM |
| Capacity | 20 MW |
| Target COD | 2028 |

### Expected Outputs (Talking Points)

**Executive Dashboard:** Gate = PROCEED, confidence GOOD (0.65)

*"This is the strongest reference match in the entire knowledge base — Puertollano is a 20 MW PEM plant in Spain, operational since 2022. Near-identical profile."*

**Reference Projects:**
- #1 Masshylia (FR, 20 MW PEM, score 0.93) — same scale + industry
- #3 Puertollano (ES, 20 MW PEM, score 0.84) — same country + scale + tech
- *"Puertollano is only #3 because its offtake is ammonia, not refinery. But it's the most valuable reference — it's OPERATIONAL at exactly this scale in Spain with solar coupling."*

**CAPEX:** EUR 41M (EUR 2,050/kW)
- *"Notice the per-kW cost is higher than Scenario 1 — EUR 2,050/kW vs EUR 1,500/kW. That's the small-scale penalty. Fixed costs like engineering, permitting, and grid connection are spread over fewer MW."*

**Agent Trace Page (FLAGSHIP):**
- *"Now let me show you the Agent Trace page — this is the differentiator. Every decision the Copilot made, you can trace back to the evidence source. Agent 2 says TRL 8 and HIGH suitability — click to see it references TC-PEM-001 section maturity and applications. Agent 3 says CAPEX EUR 41M — click to see it used CS-ELC-003 from the Cost Library, scaled from 100 MW to 20 MW."*

**Key Talking Point:** *"This isn't a black box. Every number has a story. Every story has a source."*

---

## Cross-Scenario Comparison

| Metric | Scenario 1 (FR PEM 100MW) | Scenario 2 (DE ALK 300MW) | Scenario 3 (ES PEM 20MW) |
|--------|--------------------------|--------------------------|--------------------------|
| Gate | PROCEED WITH CAUTION | PROCEED | PROCEED |
| CAPEX (EUR/kW) | 1,500 | 1,154 | 2,050 |
| LCOH (EUR/kg) | 4.96 | 4.17 | 5.59 |
| Top risk | Supply Chain (RPN 36) | Financing (RPN 30) | Subsidy (RPN 30) |
| Best reference | Normand'Hy | Holland Hydrogen I | Puertollano (operational!) |
| Key insight | Steel offtake is novel | Alkaline scale advantage | Small-scale penalty is real |

---

## Demo Tips

1. **Start with Scenario 1** — most technically interesting, shows gap detection
2. **Use Scenario 2 to compare** — "Now let me show you why Alkaline wins at large scale"
3. **Use Scenario 3 for traceability** — "Now let me show you where the numbers come from"
4. **Always show the Agent Trace page** — it's the differentiator
5. **Emphasize the knowledge base** — "10 real projects, 30 validated risks, every data point traceable to IEA/IRENA"
6. **Be honest about limitations** — "LCOH is Class D because the OPEX Library isn't populated yet. The Copilot tells you this — it doesn't hide its limitations."
