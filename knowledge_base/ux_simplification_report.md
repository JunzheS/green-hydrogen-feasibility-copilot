# UX Simplification & User-Centric Navigation — Audit Report

**Date:** 2026-06-09
**Current state:** 16 pages at the same navigation level
**Goal:** Reorganize from a project manager's perspective, not a developer's

---

## Phase 1 — User Persona Analysis

### Persona 1: Project Manager

| Need | Essential Pages | Optional | Cognitive Load |
|------|----------------|----------|---------------|
| See my project status | Assessment Report | — | Low |
| Understand what to do next | Dashboard, Project Input | — | Low |
| Review risks quickly | Risk Assessment | — | Low |
| Understand CAPEX | CAPEX & LCOH | — | Low |
| Share results with team | PDF Export, Assessment History | — | Low |
| **OEM/developer data** | — | OEM Intelligence, Developer Intel | **HIGH — not relevant to PM** |

**Verdict:** PM needs 5 pages. 11 other pages create noise.

### Persona 2: PMO

| Need | Essential Pages | Optional | Cognitive Load |
|------|----------------|----------|---------------|
| Gate review | Assessment Report, Agent Trace | — | Low |
| Compare past assessments | Assessment History | — | Low |
| Validate methodology | Source Transparency, Contradiction Detection | — | Medium |
| Audit decision quality | Agent Trace | — | Medium |
| **OEM/developer market intel** | — | OEM Intel, Developer Intel | **HIGH — not PMO scope** |

**Verdict:** PMO needs 6 pages. Market intelligence pages are secondary.

### Persona 3: Engineering Manager

| Need | Essential Pages | Optional | Cognitive Load |
|------|----------------|----------|---------------|
| Technology assessment | Technology Assessment | — | Low |
| Compare technologies | Technology Comparison | — | Low |
| Reference projects | Reference Projects | — | Low |
| Technical risks | Risk Assessment | — | Low |
| CAPEX details | CAPEX & LCOH | — | Low |
| OEM supply chain | OEM Intelligence | — | Medium |
| **Developer analysis** | — | Developer Intel | **Not needed** |

**Verdict:** Engineering Manager needs 6-7 pages. Flows logically from tech → comparison → references.

### Persona 4: Recruiter

| Need | Essential Pages | Optional | Cognitive Load |
|------|----------------|----------|---------------|
| Understand what this is | Home, Why This Matters | — | Low |
| See it working | Project Input, Assessment Report | — | Low |
| Understand tech depth | CAPEX & LCOH, Agent Trace | — | Medium |
| Market intelligence | — | OEM Intel, Developer Intel | **Not needed** |

**Verdict:** Recruiter needs 5-6 pages. Follows a demo narrative.

### Persona 5: Technical Expert / Hydrogen Specialist

| Need | Essential Pages | Optional | Cognitive Load |
|------|----------------|----------|---------------|
| Browse reference database | Reference Projects | — | Low |
| OEM market analysis | OEM Intelligence | — | Low |
| Developer landscape | Developer Intelligence | — | Low |
| Source quality | Source Transparency | — | Low |
| All assessment details | All pages | — | Medium |

**Verdict:** Technical expert uses the most pages. The current flat navigation serves this persona best.

---

## Phase 2 — Navigation Hierarchy Recommendation

```
CORE ASSESSMENT (5 pages — Primary workflow)
├── Project Input
├── Assessment Report
├── Risk Dashboard
├── CAPEX & LCOH
└── Assessment History

ADVANCED ANALYSIS (5 pages — Secondary drill-down)
├── Reference Projects (score breakdown)
├── Technology Assessment (technical details)
├── Technology Comparison (PEM vs Alkaline)
├── Agent Trace (decision traceability)
└── Contradiction Detection (agent alignment)

MARKET INTELLIGENCE (2 pages — Expert user)
├── OEM Intelligence
└── Developer Intelligence

ABOUT THE PLATFORM (3 pages — Onboarding + trust)
├── Home / Landing
├── Source Quality
└── Why This Matters
```

### Benefits of This Structure

1. **CORE ASSESSMENT** — The 5 pages a PM needs every time, immediately accessible
2. **ADVANCED ANALYSIS** — One click away, available when deeper analysis is needed
3. **MARKET INTELLIGENCE** — Separate section for OEM/developer analysis
4. **ABOUT THE PLATFORM** — Transparency and trust signals, separate from workflow

---

## Phase 3 — Landing Experience Review

### Current Home Page Assessment

| Criterion | Rating | Observation |
|-----------|--------|-------------|
| First-time understanding in 30s | ⚠️ 6/10 | Value proposition in title and tagline, but agent architecture diagram is complex for first view |
| Main value proposition visible | ✅ 8/10 | "Multi-Agent Decision-Support" is clear. KPIs show capability breadth. |
| Guided toward assessment | ⚠️ 6/10 | "Navigate to Project Input in the sidebar" at very bottom. User must scroll past agent architecture first. |
| Trust signals visible | ⚠️ 5/10 | KPIs visible but knowledge base depth not communicated |
| Recruiter appeal | ✅ 7/10 | Agent architecture diagram is the differentiator but too much text around it |

### Recommended Home Page Changes

1. **Move the "How It Works" 3-step flow above the agent architecture diagram** — a first-time visitor needs the simple version first, the details second
2. **Add a prominent "Start Assessment" button** linking directly to Project Input
3. **De-emphasize the agent architecture diagram** (foldable or secondary) — it's impressive but adds cognitive load for first visit
4. **Move KPIs to sidebar** or make them less dominant — the landing page should guide toward action, not display database statistics

---

## Phase 4 — Recruiter Demo Flow (3 Minutes)

| Step | Page | Time | What to Show |
|------|------|------|-------------|
| **1** | Home | 15s | Title, tagline, 3-step How It Works flow |
| **2** | Project Input | 20s | Enter France, Steel, PEM, 100 MW, 2029. Click Run. |
| **3** | Assessment Report | 60s | Gate banner, CAPEX, LCOH, management summary, next actions |
| **4** | CAPEX & LCOH | 30s | Cost breakdown bar chart, LCOH waterfall |
| **5** | Agent Trace | 30s | Timeline showing all 4 agents with decision and evidence |
| **6** | Why This Matters | 25s | Architecture, determinism, traceability summary |
| **Total** | | **3 min** | |

### Recruiter pages to hide from main flow:
- OEM Intelligence, Developer Intelligence — purely technical, not demo-relevant
- Source Transparency — too granular for first impression
- Contradiction Detection — assumes pre-existing understanding of agents
- Technology Comparison — good but not needed in 3-minute demo

---

## Phase 5 — Concrete Recommendations

### KEEP (Core workflow — always visible)

| Page | Reason |
|------|--------|
| Home | Landing page, never hide |
| Project Input | Entry point for all assessments |
| Assessment Report | Primary output for all personas |
| Risk Dashboard | Core deliverable for PMs and PMOs |
| CAPEX & LCOH | Core deliverable for all personas |

### MERGE (Combine related content)

| Pages to Merge | Into | Rationale |
|---------------|------|-----------|
| Reference Projects + Technology Assessment + Technology Comparison | A single "Technical Analysis" section, or 2 sub-pages under one header | These 3 pages are all technical analysis — a PM rarely needs all 3 |

### MOVE (Secondary navigation — collapsed by default)

| Page | Destination | Rationale |
|------|-------------|-----------|
| Agent Trace | Advanced Analysis section | Critical for audit, secondary for initial workflow |
| Contradiction Detection | Advanced Analysis section | Interesting but advanced |
| OEM Intelligence | Market Intelligence section | Niche, expert-only |
| Developer Intelligence | Market Intelligence section | Niche, expert-only |
| Source Transparency | About the Platform section | Trust signal, not workflow |
| Assessment History | Core Assessment (keep) | Usable by all personas |

### HIDE (From sidebar — accessible via links or footer)

| Page | Rationale |
|------|-----------|
| 99 Why This Matters | Hide from sidebar (add a "?" icon linking to it). External recruiters need it but returning users don't. |

---

## Summary: 16 → 4 Categories

| Category | Pages | Primary Persona |
|----------|-------|----------------|
| **Core Assessment** | Input, Report, Risks, CAPEX, History | Project Manager, PMO |
| **Advanced Analysis** | References, Technology, Comparison, Trace, Contradictions | Engineering Manager, Technical Expert |
| **Market Intelligence** | OEM, Developer | Technical Expert |
| **About Platform** | Home, Source, Why This Matters | Recruiter, New users |

### Implementation Notes

1. No code changes required beyond sidebar link grouping
2. Category headers in the sidebar replace flat link list
3. Market Intelligence pages remain accessible but visually separated
4. Recruiter flow requires zero clicks through the flat list — they navigate directly

### Navigation Example

```
Home
─ Core Assessment ─
Project Input
Assessment Report
Risk Dashboard
CAPEX & LCOH
Assessment History
─ Advanced Analysis ─
Reference Projects
Technology Assessment
Technology Comparison
Agent Trace
Agent Collaboration
─ Market Intelligence ─
OEM Intelligence
Developer Intelligence
─ About ─
Source Quality
Why This Matters
```
