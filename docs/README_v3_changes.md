# README v3 — Changes from v2

**Date:** 2026-06-09
**Focus:** Credibility, recruiter perception, product positioning
**Guarding principle:** No technical content was changed.

---

## Change 1: Removed Overclaiming

**v2 (before):**
> "Built by a Chemical Engineering PhD specialised in Green Hydrogen and Industrial Decarbonisation, with senior expertise in project management, industrial cost engineering, and AI system architecture."

**v3 (after):**
> *(Entire statement removed from hero section.)*

**Reasoning:** "Senior expertise in [...] AI system architecture" is difficult to verify from a GitHub profile. Rather than include a claim that could be questioned during a technical interview, the v3 README lets the project speak for itself. The quality of the architecture, methodology references, and validation results provide sufficient credibility.

---

## Change 2: Reframed AI Positioning

**v2 used repeatedly across multiple sections:**
- "No machine learning, no black boxes"
- "No ML frameworks, no cloud APIs, no databases"
- "The system is transparent by design. There are no hidden weights, no training data dependencies"
- "No black-box AI"
- "Zero external dependencies for the engine"

**v3 replacement language:**
- "Explainable reasoning system built on documented industrial methodologies"
- "Deterministic by design — all calculations use documented formulas"
- Only ONE mention: `"This is not a machine learning model. It is an explainable reasoning system."`

**Reasoning:** The repeated "no AI / no ML / no black box" language was defensive and over-emphasised what the project is NOT rather than what it IS. Engineering managers and recruiters recognise the value of deterministic, explainable systems without needing to be told repeatedly that it is not ML. The more professional framing is to describe what the system does (structured engineering decision-support, traceable reasoning, documented methodologies) rather than what it does not do.

**Texts removed (7 occurrences):**
- "Zero external dependencies for the engine. The src/ package uses only Python standard library. No ML frameworks, no cloud APIs, no databases." → replaced with "The core reasoning module uses only Python standard library."
- "No black-box AI" section → replaced with "Structured Engineering Decision-Support" section
- "The system is transparent by design. There are no hidden weights, no training data dependencies, and no model degradation over time." → removed entirely
- "No machine learning, no black boxes" → replaced with "deterministic by design"
- All remaining "no ML/black box" variants across the document → replaced with positive framing

---

## Change 3: Added Executive Showcase Section

**v2:** The first substantive section was "Why This Project Matters" — text describing the problem.

**v3:** A new "How It Works in 20 Seconds" section appears immediately after the hero, showing:

```
Input                         Output
────────────────────────────────────────────────────────────
Country:    France            Gate Decision:      PROCEED WITH CAUTION
Industry:   Steel             Technology:         PEM — TRL 8/9
Technology: PEM               Suitability:        HIGH for H2-DRI
Capacity:   100 MW            CAPEX:              EUR 150M (EUR 1,500/kW)
COD:        2029              LCOH:               EUR 4.96/kg
                              Top Reference:      Normand'Hy (Score: 0.81)
                              Top Risk:           Manufacturing Capacity (RPN 36)
                              Critical Gap:       No steel-offtake PEM reference
```

Plus the line: "Every number is traceable to its evidence source — industry reports, project data, or engineering standards."

**Reasoning:** A recruiter scanning the README should understand the product in 20 seconds. The previous version required scrolling past problem statements and architecture diagrams before seeing any output. The showcase section lets a reader instantly see: input format, output format, and the type of results produced.

---

## Change 4: Reduced Emphasis on Record Counts

**v2 used these phrases across the document:**
- "72 validated knowledge records"
- "72 records across 4 asset classes"
- "Knowledge Base: 141 files (72 structured records)"
- "10 European projects" (mentioned 3+ times)
- "30 risk records" / "30 CAPEX records" (repeated)

**v3 replacement language:**
- "Curated European hydrogen project dataset"
- "Structured knowledge base"
- "Validated risk library"
- "Industry cost benchmarks"

**Reasoning:** Highlighting "72 records" or "10 projects" can sound small to someone unfamiliar with hydrogen project data (where 10 well-documented projects is actually substantial). Emphasising quality over quantity ("curated", "validated", "structured") is more credible. The specific numbers are still available in the Knowledge Base section for those who need them.

**Specific replacements:**
- Table of Contents description: "Knowledge Base: 141 files (72 data + 69 docs)" → removed from directory tree (kept minimal)
- "72 validated knowledge records across 4 asset classes" → "Structured project references, validated risk library, industry cost benchmarks"
- Repeated "10 projects" mentions → consolidated to one mention in the Knowledge Base table

---

## Change 5: Screenshots Moved Below Hero

**v2 order:**
Hero > Table of Contents > Why This Matters > Architecture > Screenshots > Key Features > ...

**v3 order:**
Hero > **How It Works in 20 Seconds** > **Screenshots** > Table of Contents > Why This Matters > Architecture > ...

**Reasoning:** Visual proof (screenshots) should appear before architecture diagrams. A recruiter scanning the page sees: (1) what the product does, (2) what it looks like, (3) then the details of how it works. This follows the standard product README pattern: value proposition → visual proof → architecture → details.

---

## Change 6: Recruiter-First Experience Optimization

**v2 assumed the reader would read top to bottom.** Problem statements and target audience sections appeared before any example output.

**v3 is optimised for the 30-second scan:**

| Seconds | What reader sees | Section |
|---------|-----------------|---------|
| 0-5 | Project name, value proposition, badges | Hero |
| 5-15 | Example input and output (CAPEX, LCOH, gate decision, top risk) | How It Works in 20 Seconds |
| 15-25 | Three screenshots showing the actual application | Screenshots |
| 25-30 | Quick decision: "Do I want to learn more?" → scrolls to details or leaves | — |

After the 30-second hook, the remaining sections provide depth for those who need it: Architecture, Features, Differentiators, Validation, Quick Start.

### Supporting Changes for Recruiter Optimization

| Change | v2 | v3 |
|--------|-----|-----|
| "Why This Project Matters" audience table | Used technical role descriptions | Simplified to "Who Uses It" with 4 clear roles |
| "Key Features" section | 7 subsections with detailed methodology | Same 7 features, shorter descriptions focused on WHAT not HOW |
| "Technology Stack" | Table with 6 rows including rationale column | Table with 6 rows, no rationale column (rationale is implicit) |
| "Project Structure" | Full directory tree (50+ lines) | Simplified 6-line overview |
| Evidence of credibility | Distributed across sections | Consolidated in "What Makes This Different" + "Validation Results" |
| First 5 badges | Included "Live Demo" badge | Kept all badges, added context |

---

## Files Changed

| File | Status |
|------|--------|
| `README_v3.md` | Created (v3 of the README) |
| `docs/README_v3_changes.md` | Created (this document) |
| All other files | Unchanged |

---

## Summary

| Metric | v2 | v3 | Delta |
|--------|-----|-----|-------|
| Lines | 377 | 264 | -113 (30% shorter) |
| Screenshots before architecture? | No | Yes | Improved visual flow |
| "No AI/ML/black box" mentions | 7 | 0 | Removed defensive language |
| "72 records" / "10 projects" mentions | 5+ | 2 (in knowledge base section only) | Reduced counting emphasis |
| Time to first output example | ~3 scrolls | ~1 scroll | Faster understanding |
| Overclaiming statements | 1 (author expertise) | 0 | More conservative |
| Technical content changed? | No | No | Zero changes to methodology |
