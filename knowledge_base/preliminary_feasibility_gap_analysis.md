# Preliminary Feasibility Agent — Gap Analysis

**Document:** Knowledge & Capability Gaps for Full Feasibility Agent
**Date:** 2026-06-05
**Author:** Senior Hydrogen Project Consultant, PMO Lead & AI Solution Architect
**Basis:** 5-case validation (preliminary_feasibility_validation_report.md)

---

## 1. What the Preliminary Agent CAN Do

| Capability | Status | Quality |
|-----------|--------|---------|
| Retrieve similar reference projects | ✅ | 0.77 avg relevance (GOOD) |
| Assess technology readiness and suitability | ✅ | TRL + application mapping from Technology Cards |
| Identify key risks with RPN and evidence | ✅ | 8 categories × top 2 = 16 risks contextualized |
| Estimate indicative CAPEX ranges | ✅ | Class C (±25-30%) with category breakdown |
| Assess evidence quality | ✅ | Weighted score with level breakdown |
| Identify knowledge gaps | ✅ | Case-specific gap detection |
| Recommend next studies | ✅ | Prioritized by gap impact |

---

## 2. What Is Missing — Required for Full Feasibility Agent (M10+)

### 2.1 CRITICAL: OPEX & LCOH Module

**Current state:** Cost Library covers CAPEX only. Technology Cards contain OPEX breakdowns (electricity 70-75%, maintenance 8-10%, stack replacement 10-15%) but these are descriptive, not computational.

**Gap:** A true feasibility assessment requires LCOH (Levelized Cost of Hydrogen). The agent cannot answer: "Will this project produce hydrogen at a competitive cost?" Without LCOH, feasibility assessment is incomplete — the project may be technically sound and CAPEX-reasonable but economically unviable.

**Required:**
- OPEX methodology (electricity price scenarios, maintenance cost models, stack replacement scheduling)
- LCOH calculation model (CAPEX amortization + OPEX / annual H₂ production)
- Electricity price data per country/region
- Water cost data per country/region
- Carbon price scenarios (EU ETS)

**Dependency:** M7C milestone (OPEX integration)

---

### 2.2 CRITICAL: Regulatory & Permitting Module

**Current state:** Risk Library covers regulatory risks (5 risks in RK-REG-001 through 005) at a general level. The agent identifies permitting delay risk but cannot provide country-specific permitting timelines, costs, or requirements.

**Gap:** Permitting is the most common cause of project delay (Masshylia, HGHH evidence). A full Feasibility Agent must provide:
- Country-specific permitting pathway (which permits, in what sequence, how long)
- Estimated permitting cost and duration
- Key regulatory milestones (IPCEI eligibility, RFNBO compliance pathway)
- Country-specific subsidy programs and application timelines

**Required:**
- Country-specific regulatory knowledge base (France ICPE, German BImSchG, Spanish PERTE, etc.)
- RFNBO compliance assessment module
- Subsidy program database (IPCEI, EU Innovation Fund, national programs)

**Dependency:** Regulatory Knowledge Base milestone (future)

---

### 2.3 CRITICAL: Offtake & Market Module

**Current state:** Gold Dataset projects have offtake fields (primary_application, offtaker_name). Technology Cards have application suitability ratings. The agent identifies offtake risk (RK-FIN-002) but cannot assess offtake market economics.

**Gap:** The agent cannot answer:
- What is the market price for green hydrogen in this region?
- Is there sufficient offtake demand for this project's production?
- What offtake agreement structures are standard in this market?
- How does the carbon price (EU ETS) affect the offtaker's willingness to pay?

**Required:**
- Regional H₂ price benchmarks (grey, blue, green premium)
- Offtake agreement structure database (take-or-pay, indexation, duration)
- Carbon price scenarios and impact on offtake economics

---

### 2.4 IMPORTANT: Feasibility Scoring Methodology

**Current state:** The Preliminary Agent deliberately does NOT score feasibility.

**Gap:** For a full Feasibility Agent, a structured scoring methodology is needed that combines technology, risk, cost, and market dimensions into a holistic feasibility assessment. This must be:
- Transparent (not a black box)
- Weighted by evidence quality (low-confidence dimensions contribute less to the score)
- Calibrated against reference projects

**Required:**
- Multi-dimensional scoring framework
- Weight calibration methodology
- Score interpretation guidelines
- Reference class validation

---

### 2.5 IMPORTANT: Quantitative Risk Integration

**Current state:** Risks are presented with RPN and qualitative assessment. The agent contextualizes risks but does not quantify their financial impact on the specific project.

**Gap:** The agent says "Grid connection delay could cost €15M" (from Risk Library) but does not adjust this to the project's specific CAPEX and schedule. A full Feasibility Agent should:
- Scale risk cost impact to project size (not all risks are the same € amount at 20 MW vs. 300 MW)
- Compute aggregate risk exposure (sum of risk-adjusted costs)
- Perform sensitivity analysis (which risk has the largest impact on project economics?)

---

### 2.6 IMPORTANT: Knowledge Base Expansion (All Dimensions)

| Dimension | Current | Needed for Full Agent | Sprint |
|-----------|---------|----------------------|--------|
| **Gold Dataset projects** | 10 | 30 (balanced technology, offtake, geography) | Sprint 2-3 |
| **Risk Library entries** | 30 | 50-60 (fill 9 uncovered subcategories) | Sprint 2 |
| **Cost Library entries** | 30 (CAPEX only) | 50 (CAPEX + OPEX) | Sprint 2 + M7C |
| **Technology Cards** | 2 (PEM + ALK) | 2 (sufficient, needs annual update) | — |
| **Regulatory database** | 0 | Country-specific permitting pathways for EU + key markets | Future |
| **Offtake market data** | 0 | Regional H₂ price benchmarks | Future |

---

### 2.7 OPTIONAL: Advanced Reasoning Capabilities

| Capability | Description | Priority |
|-----------|------------|----------|
| **Technology recommendation** | Agent could recommend PEM vs. Alkaline based on project profile | LOW — decision belongs to project team; agent should present comparison data only |
| **Multi-phase assessment** | Assess feasibility at pre-feasibility, feasibility, and FEED gates with different confidence levels | MEDIUM — valuable for project governance |
| **Portfolio risk assessment** | Assess correlated risks across a developer's project portfolio (e.g., multiple PEM projects all dependent on iridium supply) | LOW — enterprise feature |
| **Monte Carlo simulation** | Probabilistic cost and schedule modeling | MEDIUM — adds rigor but requires significant data |
| **Automatic report generation** | Full narrative report from structured data | MEDIUM — template exists; LLM-based narrative generation should be validated for accuracy |

---

## 3. Gap Priority Matrix

| # | Gap | Severity | Effort | Dependency | Timeline |
|---|-----|---------|--------|-----------|----------|
| 1 | OPEX/LCOH Module | CRITICAL | HIGH (new milestone) | M7C | Before M10 |
| 2 | Regulatory Module | CRITICAL | HIGH (new milestone) | Country data collection | Before M10 |
| 3 | Offtake/Market Module | CRITICAL | HIGH (new milestone) | Market data collection | Before M10 |
| 4 | Scoring Methodology | IMPORTANT | MEDIUM | All critical gaps resolved | M10 |
| 5 | Quantitative Risk Integration | IMPORTANT | MEDIUM | Risk Library expansion | M10 |
| 6 | Knowledge Base Expansion | IMPORTANT | MEDIUM-HIGH | Sprint 2-3 | Ongoing |
| 7 | Advanced Capabilities | OPTIONAL | VARIES | Core agent complete | Post-M10 |

---

## 4. Roadmap to Full Feasibility Agent (M10)

```
M9 (CURRENT): Preliminary Feasibility Agent
  ✅ Project matching
  ✅ Technology assessment
  ✅ Risk identification
  ✅ CAPEX range estimation
  ✅ Evidence quality assessment
  ✅ Gap identification

M7C: OPEX & LCOH Integration
  ⬜ OPEX taxonomy and methodology
  ⬜ LCOH calculation model
  ⬜ Electricity price database
  ⬜ OPEX Cost Library entries

M9B: Regulatory Knowledge Base
  ⬜ EU country permitting pathways
  ⬜ RFNBO compliance assessment
  ⬜ Subsidy program database

M9C: Offtake & Market Module
  ⬜ Regional H₂ price benchmarks
  ⬜ Offtake agreement structures
  ⬜ Carbon price scenarios

M10: Full Feasibility Agent
  ⬜ Multi-dimensional scoring
  ⬜ Quantitative risk integration
  ⬜ LCOH estimation
  ⬜ Regulatory pathway assessment
  ⬜ Market/offtake assessment
  ⬜ Integrated feasibility report
```

---

## 5. Verdict

**The Preliminary Feasibility Agent (M9) is a solid foundation for the Full Feasibility Agent (M10).**

It successfully integrates four knowledge domains (projects, technology, risks, costs) into a coherent assessment workflow. The agent is appropriately scoped — it identifies what is known and what is not known without pretending to have capabilities that require modules not yet built.

The three critical gaps (OPEX/LCOH, regulatory, offtake/market) are each substantial new workstreams. They should be addressed in dedicated milestones (M7C, M9B, M9C) before integration into M10. **The Preliminary Agent is production-ready for its current scope. The Full Feasibility Agent requires completion of these three modules plus a scoring methodology.**

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Hydrogen Project Consultant, PMO Lead & AI Solution Architect | Initial gap analysis |
