# Future Product Roadmap — Green Hydrogen Project Feasibility Copilot

**Document:** Product Vision & Development Roadmap
**Date:** 2026-06-05
**Current Version:** V1.0 — Streamlit MVP (shipped)

---

## V1.0 — Streamlit MVP (CURRENT)

**Status:** ✅ SHIPPED

### What It Does
- Single-user local Streamlit application
- 4-agent reasoning pipeline (matching → technology → risk/cost → PM review)
- 8-page UI: Input, Dashboard, Projects, Technology, Risks, CAPEX/LCOH, Agent Trace, History
- Knowledge base: 10 projects, 30 risks, 30 cost records, 2 technology cards
- All reasoning deterministic and source-traced
- 35/35 regression tests passing

### Limitations
- Single user, local only
- OPEX/LCOH uses proxy data (Class D) — OPEX Library not populated
- No regulatory country-specific database
- No offtake market analysis
- Knowledge base limited to 10 European projects
- Single-agent architecture (not true multi-agent runtime)

---

## V1.5 — Streamlit Cloud (NEXT)

**Status:** 🔜 Next (2-4 weeks)

### What's New
- Deploy to Streamlit Cloud (share.streamlit.io)
- Public URL — no installation required
- Improved error handling for cloud environment
- Session persistence improvements
- Mobile-responsive layout

### Key Deliverables
- Streamlit Cloud deployment
- CI/CD pipeline (GitHub Actions for regression tests)
- Public demo link

---

## V2.0 — Cloud Application (3-6 months)

**Status:** 📋 Planned

### What's New

#### Knowledge Base Expansion
- Gold Dataset: 10 → 30 projects (balanced PEM/Alkaline, all EU countries, + MENA)
- Risk Library: 30 → 50 risks (fill 9 uncovered subcategories)
- Cost Library: 30 → 50 records (add Chinese Alkaline benchmarks)
- **OPEX Library: 30 records (NEW)**

#### LCOH Production-Grade
- Populated OPEX Library enables Class C LCOH estimates
- Country-specific electricity price data
- Carbon price scenarios (EU ETS)
- Breakeven analysis vs grey/blue hydrogen

#### Multi-User Support
- User accounts (basic auth)
- Saved assessments per user
- Assessment sharing

#### Enhanced Technology Assessment
- Technology recommendation logic (PEM vs Alkaline trade-off analysis)
- Hourly renewable matching assessment for RFNBO compliance

---

## V3.0 — Multi-Agent Runtime (6-12 months)

**Status:** 📋 Future

### What's New

#### True Multi-Agent Architecture
- 4 independent agents with message passing
- Agent 1 (Retrieval) — promoted to peer from sub-component
- Agent 2 (Technical) — extracted from P2 pipeline
- Agent 3 (Risk & Economic) — extracted from P3+P4, enhanced with LCOH
- Agent 4 (PM Review) — cross-dimension QA
- Agent 5 (Regulatory Assessor) — country-specific permitting pathways (NEW)
- Agent 6 (Offtake/Market) — regional H2 pricing, carbon pricing (NEW)

#### Agent Communication Protocol
- JSON message envelopes with schema versioning
- Contradiction detection and resolution
- Confidence calibration per agent
- Escalation rules for cross-agent disagreements

#### Decision Traceability Layer
- Immutable session memory (one per agent per session)
- Complete audit trail from query to gate decision
- Contradiction registry with resolution tracking
- Future learning readiness (structured data for eventual ML training)

---

## V4.0 — Enterprise Deployment (12-24 months)

**Status:** 📋 Vision

### What's New

#### Enterprise Features
- SSO / OAuth authentication
- Role-based access (analyst, PM, director)
- Multi-project portfolio management
- Audit logging and compliance reporting
- SLA-backed availability

#### Knowledge Base as a Service
- Automated knowledge base updates from IEA/IRENA/Hydrogen Council
- Real-time project pipeline tracking
- Commodity price integration (iridium, nickel, electricity)
- Regulatory change monitoring

#### Advanced Analytics
- Monte Carlo simulation for probabilistic CAPEX/LCOH
- Portfolio risk assessment (correlated risks across projects)
- Scenario comparison (PEM vs Alkaline, greenfield vs brownfield)
- Benchmarking against industry peers

#### Integration
- REST API for enterprise system integration
- Webhook notifications for risk trigger events
- Export to Power BI / Tableau
- Integration with project management tools (MS Project, Primavera)

---

## Feature Comparison Matrix

| Feature | V1.0 | V1.5 | V2.0 | V3.0 | V4.0 |
|---------|------|------|------|------|------|
| Project matching | ✅ | ✅ | ✅ | ✅ | ✅ |
| Technology assessment | ✅ | ✅ | ✅ | ✅ | ✅ |
| Risk assessment | ✅ | ✅ | ✅ | ✅ | ✅ |
| CAPEX estimation | ✅ | ✅ | ✅ | ✅ | ✅ |
| LCOH estimation | ⚠️ Class D | ⚠️ Class D | ✅ Class C | ✅ Class B | ✅ Class A |
| Agent traceability | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cloud deployment | ❌ | ✅ | ✅ | ✅ | ✅ |
| Multi-user | ❌ | ❌ | ✅ | ✅ | ✅ |
| OPEX Library | ❌ | ❌ | ✅ | ✅ | ✅ |
| Regulatory database | ❌ | ❌ | ❌ | ✅ | ✅ |
| Offtake/market analysis | ❌ | ❌ | ❌ | ✅ | ✅ |
| Multi-agent runtime | ❌ | ❌ | ❌ | ✅ | ✅ |
| Monte Carlo simulation | ❌ | ❌ | ❌ | ❌ | ✅ |
| Enterprise SSO | ❌ | ❌ | ❌ | ❌ | ✅ |
| REST API | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Knowledge Base Growth Projection

| Asset | V1.0 | V2.0 | V3.0 | V4.0 |
|-------|------|------|------|------|
| Gold Dataset projects | 10 | 30 | 50 | 100+ |
| Risk Library entries | 30 | 50 | 70 | 100+ |
| Cost Library entries | 30 | 50 | 80 | 120+ |
| OPEX Library entries | 0 | 30 | 60 | 100+ |
| Technology Cards | 2 | 2 | 4 | 6 |
| Country regulatory profiles | 0 | 0 | 10 | 25+ |
| Regional H2 price benchmarks | 0 | 0 | 5 | 15+ |

---

## Investment / Resourcing Estimates

| Version | Timeline | Team Size | Key Skills |
|---------|----------|-----------|-----------|
| V1.5 — Cloud | 2-4 weeks | 1 dev | Streamlit Cloud, CI/CD |
| V2.0 — Cloud App | 3-6 months | 2-3 devs + 1 PM | Full-stack, DB, auth |
| V3.0 — Multi-Agent | 6-12 months | 3-4 devs + 1 architect | Distributed systems, agent frameworks |
| V4.0 — Enterprise | 12-24 months | 5-8 devs + PM + architect | Enterprise SaaS, compliance, scale |

---

## Document Control

| Version | Date | Author |
|---------|------|--------|
| 1.0.0 | 2026-06-05 | Lead AI Solution Architect |
