# Preliminary Feasibility Assessment Report — Template v1.0

**Document:** Standardized Output Format
**Date:** 2026-06-05
**Agent Version:** Preliminary Feasibility Agent v1.0

---

## Report Structure

Every assessment report follows this 8-section structure. Mandatory sections are marked **§**. All factual claims must cite a source.

---

## §1 — Executive Summary

### Project Profile
| Parameter | Value |
|-----------|-------|
| Country | {country} |
| Industry / Offtake | {industry} → mapped to offtake: {offtake_enum} |
| Technology | {technology} |
| Scale | {capacity_mw} MW |
| Target COD | {target_cod} |

### Key Findings

**Technology Readiness:** {1-2 sentence verdict on TRL, maturity, scale proven, application suitability}  
**Reference Projects:** {top 3 similar projects with relevance scores}  
**Key Risks:** {top 3 risks by RPN with categories}  
**Indicative CAPEX:** {range in €M and €/kW with confidence class}  
**Evidence Quality:** {score and category}  
**Critical Gaps:** {1-2 most important knowledge gaps}

### Disclaimer

> *"This is a Preliminary Feasibility Assessment based on the Copilot's current knowledge base (June 2026). It does NOT constitute a feasibility study, investment recommendation, or engineering decision. All CAPEX estimates are AACE Class 4 (±20-30%) or Class 5 (±30-50%). OPEX, LCOH, offtake economics, and regulatory analysis are not yet covered. This report identifies what is KNOWN and what is NOT KNOWN — it does not fill gaps with assumptions."*

---

## §2 — Similar Reference Projects

### Top Matching Projects

| Rank | Project | Country | MW | Tech | Status | Of-take | Score | Why Relevant |
|------|---------|---------|-----|------|--------|--------|-------|-------------|
| #1 | {name} (GA-PR-XXX) | {country} | {MW} | {tech} | {status} | {offtake} | {0.XX} | {1-2 sentence rationale} |
| #2 | ... | | | | | | | |
| ... | | | | | | | | |
| #6 | ... | | | | | | | |

### Key Insights from Reference Projects

- {Insight 1: what similar projects tell us about technology choices, costs, timelines}
- {Insight 2: common challenges or success factors}
- {Insight 3: notable differences between reference projects and the queried project}

### Reference Quality

| Metric | Value |
|--------|-------|
| Projects with same technology | {count}/6 |
| Projects in same country | {count}/6 |
| Projects with same offtake | {count}/6 |
| Operational projects (best evidence) | {count}/6 |
| Average relevance score | {avg_score} |

*Sources: Gold Dataset GA-PR-001 through GA-PR-010*

---

## §3 — Technology Assessment

### Technology Identity
| Parameter | Value |
|-----------|-------|
| Technology | {technology_name} (TC-{TYPE}-001) |
| TRL | {TRL} — {commercial_maturity} |
| Cumulative global capacity | {capacity} MW ({year}) |
| Proven max plant size | {max_mw} MW ({status}) |

### Performance Summary
| Parameter | Value | Relevance |
|-----------|-------|-----------|
| System efficiency | {X} kWh/kg H₂ | {relevance to project} |
| Stack lifetime | {X} hours (~{Y} years) | {relevance} |
| Degradation rate | {X}%/year | {relevance} |
| Output pressure | {X} bar | {relevance to offtake pressure requirements} |
| H₂ purity | {X}% | {relevance to offtake purity requirements} |
| Dynamic response | {X}%/s ramp, {Y}% min load | {relevance to renewable profile} |

### Application Suitability: {industry}

| Assessment | {high / medium / low} |
|-----------|----------------------|
| Rationale | {from Technology Card suitability_per_application} |
| Reference Projects | {Gold Dataset projects demonstrating this application} |

### Scale Assessment

| Assessment | {description} |
|-----------|---------------|
| Project scale | {capacity_mw} MW |
| Proven range | {min}–{max} MW |
| Status | {within / at frontier / beyond} proven deployment range |
| FOAK flag | {true if beyond proven scale or novel application} |

### Key Advantages & Limitations for This Project

**Advantages:**
- {advantage 1 — contextualized for this project}
- {advantage 2}

**Limitations:**
- {limitation 1 — contextualized for this project}
- {limitation 2}

*Sources: TC-{TYPE}-001 §§maturity, performance, scalability, applications, advantages, limitations*

---

## §4 — Key Risks

### Risk Overview

| Category | Risks Identified | Highest RPN | Top Risk |
|----------|-----------------|-------------|----------|
| Technical | {count} | {RPN} | {risk_name} |
| Supply Chain | {count} | {RPN} | {risk_name} |
| Grid & Energy | {count} | {RPN} | {risk_name} |
| Regulatory | {count} | {RPN} | {risk_name} |
| Financial | {count} | {RPN} | {risk_name} |
| Construction | {count} | {RPN} | {risk_name} |
| Operational | {count} | {RPN} | {risk_name} |
| Environmental | {count} | {RPN} | {risk_name} |

### Top 8 Risks (One per Category)

| # | Risk ID | Risk Name | Cat. | P | I | D | RPN | Class | Key Mitigation |
|---|---------|-----------|------|---|---|---|-----|-------|---------------|
| 1 | RK-XXX-XXX | {name} | {cat} | {P} | {I} | {D} | {RPN} | {class} | {top mitigation} |
| ... | | | | | | | | | |

### Risk Evidence Quality

| Metric | Value |
|--------|-------|
| Risks with Gold Dataset project evidence | {count}/{total} |
| Risks with Technology Card evidence | {count}/{total} |
| Risks relying solely on industry reports | {count}/{total} |

*Sources: Risk Library RK-XXX-001 through RK-XXX-030; Technology Cards TC-PEM-001, TC-ALK-001*

---

## §5 — Indicative CAPEX Assessment

### Disclaimer

> *"This is an AACE Class {4/5} estimate (±{range}%). It is based on industry benchmarks and scaled reference data — NOT on project-specific FEED engineering or OEM quotations. Actual costs will vary based on site conditions, procurement strategy, and market conditions at time of order."*

### CAPEX Breakdown

| Category | €/kW | M€ | % of Total | Confidence | Key Driver |
|----------|------|-----|-----------|------------|------------|
| 01 Electrolyzer System | {X} | {Y} | {Z}% | {class} | {driver} |
| 02 Electrical Infrastructure | | | | | |
| 03 Water Systems | | | | | |
| 04 Hydrogen Processing | | | | | |
| 05 Civil & Construction | | | | | |
| 06 Thermal Management | | | | | |
| 07 I&C | | | | | |
| 08 Indirect & Owner's | | | | | |
| **TOTAL (central)** | **{X}** | **{Y}** | **100%** | **{class}** | |
| **RANGE (P10–P90)** | **{low}–{high}** | **{low}–{high}** | | | |

### Cost Driver Analysis

| Rank | Driver | Impact | Why |
|------|--------|--------|-----|
| 1 | {driver} | ±{X}M€ | {explanation} |
| 2 | {driver} | ±{X}M€ | {explanation} |
| 3 | {driver} | ±{X}M€ | {explanation} |

### Benchmark Comparison

| Reference Project | Scale | CAPEX/kW | Year | Adjusted to Query Scale | Notes |
|------------------|-------|----------|------|------------------------|-------|
| {project} (GA-PR-XXX) | {MW} MW | €{X}/kW | {year} | €{Y}/kW | {comparability notes} |

*Sources: Cost Library CS-XXX-001 through CS-XXX-030; cost_scaling_methodology.md; Gold Dataset project financial fields*

---

## §6 — Evidence Quality Assessment

### Source Distribution

| Level | Count | % | Example Sources |
|-------|-------|---|-----------------|
| A — Official Primary | {count} | {X}% | {examples} |
| B — Authoritative Industry | {count} | {X}% | {examples} |
| C — Professional Media | {count} | {X}% | {examples} |
| D — Unverified | 0 | 0% | — |
| **Total unique sources** | **{count}** | | |

### Evidence Quality Score: {X.XX} → {CATEGORY}

### Confidence by Assessment Dimension

| Dimension | Confidence | Weakest Area |
|-----------|-----------|-------------|
| Project References | {HIGH/MEDIUM/LOW} | {gap} |
| Technology Assessment | {HIGH/MEDIUM/LOW} | {gap} |
| Risk Assessment | {HIGH/MEDIUM/LOW} | {gap} |
| Cost Assessment | {HIGH/MEDIUM/LOW} | {gap} |

---

## §7 — Knowledge Gaps

### Critical Gaps (High Priority)

| # | Gap | Impact | Recommended Action |
|---|-----|--------|-------------------|
| 1 | {description} | {why it matters} | {what to do} |
| 2 | ... | | |

### Important Gaps (Medium Priority)

| # | Gap | Impact | Recommended Action |
|---|-----|--------|-------------------|
| 3 | {description} | {why it matters} | {what to do} |

### Inherent Limitations (Cannot Be Resolved with Current Data)

| # | Limitation | Why |
|---|-----------|-----|
| 1 | No operational >100 MW PEM plant exists to provide Class A cost data | Industry maturity — all large PEM plants are under construction |
| 2 | {limitation} | {reason} |

---

## §8 — Recommended Next Studies

### Priority 1 — Pre-Feasibility Advancement

- □ {Action 1} — {rationale and expected outcome}
- □ {Action 2}
- □ {Action 3}

### Priority 2 — Knowledge Base Enhancement

- □ {Action 4}
- □ {Action 5}

### Priority 3 — Long-Lead Activities

- □ {Action 6}

---

## Report Metadata

| Field | Value |
|-------|-------|
| Report ID | PFA-{YYYY}-{NNN} |
| Agent Version | Preliminary Feasibility Agent v1.0 |
| Generation Date | {ISO 8601 datetime} |
| Knowledge Base Version | Gold Dataset v1 (10 projects), Risk Library Sprint 1 (30 risks), Cost Library Sprint 1 (30 records) |
| Input Query | {JSON} |

---

*End of Preliminary Feasibility Assessment Report*
