# Recruiter Demo Script — 5-Minute Walkthrough

**Document:** Recruiter-facing demonstration guide
**Date:** 2026-06-05
**Target Audience:** Technical recruiters, engineering managers, PMO directors
**Demo Length:** 5 minutes

---

## Minute 1: The Problem (30 seconds)

*"Project managers evaluating green hydrogen feasibility spend weeks searching for reference projects, technology benchmarks, and cost data. There's no centralized tool for this — until now."*

**What to show:** Streamlit home page with KPIs (10 projects, 30 risks, 30 cost records)

---

## Minute 2: Run an Assessment (60 seconds)

*"Let me enter a project — France, 100 MW PEM for a steel plant, targeting 2029."*

**What to click:**
1. Navigate to **Project Input** page
2. Select: Country = France, Industry = Steel, Technology = PEM
3. Slide: Capacity = 100 MW, Target COD = 2029
4. Click **Run Assessment**

**What to say while it runs:**
*"The engine is loading 72 knowledge records — 10 real European projects, 30 validated risks, 30 cost benchmarks — and running a 4-agent reasoning pipeline. Everything is deterministic, source-traced, and validated with 35/35 regression tests."*

---

## Minute 3: The Results (90 seconds)

*"The assessment is complete. Let me show you what it produced."*

**What to show (Executive Dashboard):**
- Gate banner: **PROCEED WITH CAUTION** (orange)
- *"The Copilot says proceed with caution — not because the technology is risky, but because no PEM plant has ever supplied a steel furnace. It found a knowledge gap and flagged it."*
- KPIs: TRL 8, CAPEX EUR 150M, LCOH EUR 4.96/kg

**What to show (Reference Projects):**
- *"It found 6 similar projects. Normand'Hy in France is the top match — same country, same technology. Look, it explains WHY: same country, refinery offtake shares industrial gas handling with steel."*

**What to show (Agent Trace — the key differentiator):**
- Navigate to **Agent Trace** page
- *"This is what makes this project unique. Every decision the Copilot made — you can trace back to the evidence. Agent 2 says TRL 8. Click — it references the PEM Technology Card, validated against IEA Global Hydrogen Review 2025. Agent 3 says CAPEX EUR 150M. Click — it used the Cost Library, scaled from the IEA benchmark, adjusted for 2029 delivery with the PEM learning curve. Nothing is a black box."*

---

## Minute 4: What Makes This Unique (90 seconds)

*"Three things distinguish this from any other hydrogen tool."*

**1. Knowledge base, not just code.**
*"There are 72 validated JSON records behind this app — 10 real European hydrogen projects, each with 66 structured fields. 30 risks scored with PMO-grade FMEA methodology. 30 cost records sourced from IEA, IRENA, and actual project data. Every data point has a source."*

**2. Deterministic, explainable AI.**
*"There's no machine learning, no black box. Every calculation — project similarity, risk scoring, CAPEX scaling, LCOH decomposition — is a documented, auditable formula. The Agent Trace page proves it."*

**3. Designed for engineers, not data scientists.**
*"This was built by a senior hydrogen project manager, an industrial cost engineer, and an AI architect working together. The output speaks the language of project governance — AACE cost classes, ISO 31000 risk management, PMBOK phase-gate methodology."*

---

## Minute 5: Closing (30 seconds)

*"The Copilot is currently a validated MVP — 35/35 regression tests passing, all 72 knowledge records verified. The Streamlit app is a demonstration of what's possible. The architecture is designed to scale to a true multi-agent system with OPEX modeling, regulatory assessment, and enterprise deployment."*

*"I can send you the GitHub repository — it runs with two commands and has zero external API dependencies. Everything is local, deterministic, and auditable."*

---

## Frequently Asked Questions (Anticipated)

**Q: Is this a real product or a prototype?**
A: It's a validated prototype with production-grade knowledge engineering. The 72 knowledge records are real project data. The algorithms are documented and tested. It's ready for a pilot deployment with a hydrogen consulting team.

**Q: Where does the data come from?**
A: The Gold Dataset was built from public sources — Air Liquide press releases, Shell investor presentations, EU Innovation Fund documents, IEA Global Hydrogen Review 2025, IRENA cost reports. Every data point is traceable to a source with a quality level (A/B/C) and retrieval date.

**Q: How accurate are the CAPEX estimates?**
A: The Copilot is honest about this — all estimates are AACE Class 4 (±20-30%) based on industry benchmarks. It does NOT produce false precision. The Cost Confidence Framework prevents Class D data from masquerading as Class C.

**Q: What's the technology stack?**
A: Python 3.10+ standard library for the engine (zero external dependencies for reasoning), Streamlit for the UI, JSON files for the knowledge base. No databases, no APIs, no cloud dependencies.

**Q: Can you add more projects / risks / cost data?**
A: Yes. The knowledge base is file-based — adding a new project is a single JSON file. The schemas are documented and validated. A junior analyst can populate records following the templates.
