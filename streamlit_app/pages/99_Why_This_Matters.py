"""Page 99 — Recruiter Mode / Why This Project Is Different."""
import streamlit as st

st.title("Why This Project Is Different")
st.caption("A structured decision-support platform — not a machine learning model, not a chat bot, not a database.")

st.divider()

# 1: Multi-Agent Architecture
st.markdown("#### Multi-Agent Reasoning Architecture")
st.markdown("""
This platform uses **four deterministic agents** that process structured knowledge in sequence:

| Agent | Role | Method |
|-------|------|--------|
| **Agent 1 — Knowledge Retrieval** | Find comparable reference projects | 5-dimension weighted similarity scoring |
| **Agent 2 — Technical Assessment** | Evaluate technology readiness | TRL, application suitability, FOAK risk |
| **Agent 3 — Risk & Economic Assessment** | Quantify risks and costs | FMEA scoring + AACE Class 4 cost estimation |
| **Agent 4 — PM Review** | Quality-gate the assessment | Evidence audit, confidence calibration, gate decision |

Each agent uses documented, deterministic formulas. The same input always produces the same output.
""")

st.divider()

# 2: Not a Black Box
st.markdown("#### Full Decision Traceability")
st.markdown("""
Every conclusion in the assessment report can be traced back to:

1. **A specific knowledge record** — which project, risk, or cost benchmark was used
2. **A specific methodology** — how the calculation was performed
3. **A specific source** — IEA report, IRENA benchmark, developer press release

The **Agent Trace** page visualises this as a complete reasoning chain from user input to gate decision.
""")

st.divider()

# 3: Deterministic by Design
st.markdown("#### Deterministic, Audit-Ready, Reproducible")
st.markdown("""
Unlike machine learning systems, this platform:

* **Has no training data** — all knowledge is structured JSON records
* **Has no model weights** — every calculation is a documented formula
* **Cannot hallucinate** — outputs are constrained to structured reasoning paths
* **Is fully testable** — 35/35 regression tests validate every validation scenario
* **Is auditable** — every decision cites its evidence and methodology

This makes it suitable for **project governance, lender presentations, and regulatory review** — contexts where black-box AI is not acceptable.
""")

st.divider()

# 4: Industrial-Grade Methodologies
st.markdown("#### Engineering Methodologies Applied")
st.markdown("""
| Methodology | Application |
|-------------|-------------|
| **AACE International 18R-97** | Cost estimate classification (Class 5 through Class 1) |
| **ISO 31000:2018** | Risk management framework |
| **IEC 60812** | Failure Mode and Effects Analysis (FMEA) for risk scoring |
| **PMBOK 7th Edition** | Phase-gate project governance |
| **ISO 16290** | Technology Readiness Level (TRL) definitions |
| **Source Governance Framework** | 4-level (A/B/C/D) source quality taxonomy |
""")

st.divider()

# 5: Knowledge Engineering
st.markdown("#### Structured Knowledge Base")
st.markdown("""
| Asset | Records | Source Quality |
|-------|---------|---------------|
| **Gold Dataset (project references)** | 82 projects | 52% Level A (official sources) |
| **Risk Library** | 30 risks (8 categories) | FMEA-scored with mitigation actions |
| **Cost Library** | 30 CAPEX records | AACE Class 4 with confidence weighting |
| **Technology Knowledge Cards** | PEM + Alkaline | IEA/IRENA validated |
| **Architecture documents** | 69 design documents | Complete system specification |

Every data point follows a published **Source Governance Framework** with A/B/C/D quality levels. Zero unverified (Level D) sources are used.
""")

st.divider()

# 6: What a Recruiter Should Know
st.markdown("#### Key Differentiators")
st.markdown("""
1. **Not a machine learning project.** This is a knowledge engineering and decision-support platform built with standard industrial methodologies.

2. **Not a chat bot.** Users enter structured project parameters and receive a structured assessment report — not open-ended conversation.

3. **Not a database.** The knowledge base is curated, validated, and governed by a published quality framework.

4. **Designed by domain experts, for domain experts.** The platform speaks the language of project management — AACE cost classes, ISO risk management, PMBOK phase-gate reviews.

5. **Built for traceability.** Every decision is sourced, every calculation is documented, every conclusion is auditable.
""")

st.divider()

st.caption("Built with Python 3.10+ (stdlib only for the engine), Streamlit, and structured JSON knowledge. 35/35 regression tests passing across 5 validation scenarios. On GitHub: github.com/JunzheS/green-hydrogen-feasibility-copilot")
