# Source Governance Framework — Green Hydrogen Project Feasibility Copilot

**Document Version:** 1.0.0
**Date:** 2026-06-05
**Author:** Lead Knowledge Engineer & Data Governance Manager
**Applies To:** All Gold Dataset project records, technology cards, risk entries, and cost data points
**Status:** ACTIVE

---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Source Quality Levels](#2-source-quality-levels)
3. [Source Reliability Scoring](#3-source-reliability-scoring)
4. [Source Type Classification](#4-source-type-classification)
5. [Source Selection Heuristics](#5-source-selection-heuristics)
6. [Source Validation Rules](#6-source-validation-rules)
7. [Source Conflict Resolution](#7-source-conflict-resolution)
8. [Source Decay Policy](#8-source-decay-policy)
9. [Source Attribution Standards](#9-source-attribution-standards)
10. [Appendix: Pre-Qualified Source List](#10-appendix-pre-qualified-source-list)

---

## 1. Purpose & Scope

### 1.1 Purpose

This framework defines how sources are classified, scored, selected, and validated for the Green Hydrogen Project Feasibility Copilot knowledge base. Every data point in the system — whether a project fact, technology specification, risk assessment, or cost figure — must be traceable to a source classified under this framework.

### 1.2 Scope

- **Applies to:** All Gold Dataset records, Technology Knowledge Cards, Risk Library entries, and Cost Library entries
- **Applies to:** Both structured data fields and narrative content
- **Does NOT apply to:** Pipeline-generated metadata (embedding vectors, index entries, derived calculations) — these inherit source quality from their upstream data

### 1.3 Core Principles

| Principle | Description |
|-----------|-------------|
| **Every fact has a source** | No field is populated without at least one traceable source reference |
| **Source quality is explicit** | Every source carries a quality level (A/B/C/D) and reliability score (1–5) |
| **Primary over secondary** | Primary sources (developer, government) are preferred over secondary (media, analyst) |
| **Recency over legacy** | Within the same quality tier, more recent sources take precedence |
| **Consensus over single-source** | When two independent sources agree, confidence increases |
| **Transparency over completeness** | A gap with a note is better than a guess without a source |

---

## 2. Source Quality Levels

### 2.1 Level A — Official Primary Sources (Highest Trust)

Sources directly controlled by the project developer, technology provider, or regulatory authority. These represent the authoritative record of fact.

| Sub-type | Examples | Typical Use |
|----------|----------|-------------|
| Developer press releases | Air Liquide press release announcing Normand'Hy FID | Capacity, timeline, offtaker, developer |
| Official project websites | normandhy.airliquide.com, hghh.eu | All project facts |
| Investor presentations | Shell Capital Markets Day, TotalEnergies Strategy Presentation | CAPEX, capacity, timeline |
| Regulatory filings | EU IPCEI documentation, environmental impact assessments | Technology, environmental data |
| Government announcements | BMWK (German ministry) funding announcements | Funding, policy support, timeline |
| Company annual reports | Air Liquide 2024 Annual Report, Shell 2024 Annual Report | Operational status, CAPEX spent |
| OEM datasheets | Siemens Energy Silyzer product sheet, Thyssenkrupp Nucera Scalum datasheet | Technology specifications |
| EPC contract awards | Worley EPCM award announcement for HH1 | EPC contractor, scope |

**Characteristics:**
- Directly from the entity being described
- Legally or reputationally accountable for accuracy
- Typically date-stamped
- Revision-controlled (supersedes previous versions)

**Default reliability score range: 4–5**

### 2.2 Level B — Authoritative Industry Sources (High Trust)

Publications from recognized international organizations, government agencies, and industry bodies with established research methodologies and peer/internal review processes.

| Sub-type | Examples | Typical Use |
|----------|----------|-------------|
| IEA reports | IEA Global Hydrogen Review 2025 | Technology trends, cost benchmarks, capacity data |
| IRENA reports | IRENA Green Hydrogen Cost Reduction 2024 | Cost data, learning rates, technology comparison |
| EU official publications | EU Innovation Fund project summaries, JRC reports | Project descriptions, funding amounts |
| Hydrogen Council reports | Hydrogen Insights 2024 | Industry trends, project pipeline |
| National laboratory reports | NREL, Fraunhofer, CEA publications | Technology performance, cost modeling |
| BloombergNEF (BNEF) | BNEF Hydrogen Market Outlook | Market data, project tracking |
| Wood Mackenzie reports | WoodMac Hydrogen Market Service | Project database, cost analysis |
| ISO/IEC standards | ISO 22734, IEC 62282 | Technology specifications, safety requirements |
| National statistics agencies | Destatis, INSEE, CBS | Macro-economic context, energy prices |

**Characteristics:**
- Institutional authorship with named analysts or committees
- Published methodology
- Peer-reviewed or internally reviewed
- Regular publication cycle

**Default reliability score range: 3–5**

### 2.3 Level C — Professional Media & Industry Sources (Medium Trust)

Publications from established industry media outlets, trade journals, and professional news organizations with dedicated energy/hydrogen coverage.

| Sub-type | Examples | Typical Use |
|----------|----------|-------------|
| Industry news outlets | H2 View, Hydrogen Insight, Recharge News, FuelCellChina | Breaking project news, capacity announcements, contract awards |
| Trade journals | Chemical Engineering, Power Engineering, H2 Tech | Technical details, project descriptions |
| Conference presentations | World Hydrogen Summit, European Hydrogen Week | Project updates, technology developments |
| Professional analyst reports | Aurora Energy Research, Rystad Energy, Guidehouse | Cost estimates, market projections (when based on cited data) |
| Industry association publications | Hydrogen Europe, CHBC, Hydrogen UK | Policy context, industry statistics |
| Port authority publications | Port of Rotterdam, Port of Hamburg | Infrastructure details, project locations |

**Characteristics:**
- Journalistic or professional editorial standards
- Named authors or editorial team
- Typically cites primary sources
- May have commercial interest but editorial independence

**Default reliability score range: 2–4**

### 2.4 Level D — Unverified Secondary Sources (Low Trust)

Sources that lack institutional accountability, editorial review, or direct access to project information. Used only as supplementary confirmation or when higher-tier sources are unavailable.

| Sub-type | Examples | Typical Use |
|----------|----------|-------------|
| Industry blogs | Personal blogs, company marketing blogs | Supplementary context only |
| Unverified databases | Community-maintained project trackers | Cross-reference only; do not use as sole source |
| Social media | LinkedIn posts, Twitter/X announcements | Early signals only; must be confirmed by Level A–C source |
| Wikipedia & Wikimedia | Wikipedia articles | Background context only; never as primary source |
| Aggregated news sites | General news aggregation platforms | Redirect to original source |
| AI-generated content | LLM outputs, automated summaries | NEVER use as a source |

**Characteristics:**
- No institutional accountability
- No editorial review process
- May be anonymous or pseudonymous
- May be AI-generated or aggregated

**Default reliability score range: 1–2**

**Restriction:** Level D sources cannot be the sole source for any mandatory field. They may only be used as supplementary confirmation alongside a Level A, B, or C source.

---

## 3. Source Reliability Scoring

### 3.1 Scoring Scale

| Score | Label | Definition | Example |
|-------|-------|------------|---------|
| 5 | **Definitive** | Official, audited, legally binding | Audited annual report CAPEX figure for an operational project |
| 4 | **Authoritative** | Official but unaudited; institutional with methodology | IEA Global Hydrogen Review; developer press release with named executive quote |
| 3 | **Reliable** | Institutional or professional with editorial standards | H2 View article citing named sources; conference presentation |
| 2 | **Plausible** | Professional but unverified; secondary without primary citation | Analyst estimate without methodology; news article without named source |
| 1 | **Uncertain** | Unverified, anonymous, or clearly speculative | Blog post; community database; social media rumor |

### 3.2 Scoring Algorithm

For each source, the reliability score is determined by combining:

```
Reliability Score = Institutional Weight × Content Weight

Institutional Weight (1.0–5.0):
  5.0 = Developer/owner official publication, regulatory filing, audited report
  4.0 = Government agency, IEA/IRENA, OEM official datasheet
  3.0 = Major industry research (BNEF, WoodMac), industry association
  2.5 = Professional media with dedicated energy coverage
  2.0 = General business media, trade publications
  1.0 = Blog, social media, unverified database

Content Weight (0.2–1.0 multiplier):
  1.0 = Named author/analyst, cites primary sources, recent, detailed
  0.8 = Named author, secondary analysis, recent
  0.6 = Editorial/unsigned, cites sources, recent
  0.4 = Unsigned, no sources cited, generic
  0.2 = Anonymous, speculative, outdated

Final Score = round(Institutional Weight × Content Weight)
Clamped to range [1, 5]
```

### 3.3 Minimum Source Requirements by Field Importance

| Field Category | Minimum Source Level | Minimum Reliability Score | Minimum Source Count |
|---------------|---------------------|--------------------------|---------------------|
| Mandatory fields | B or higher | ≥ 3 | 1 |
| Tier A essential fields | B or higher | ≥ 3 | 1 |
| CAPEX / financial data | B or higher | ≥ 4 | 2 (independent) or 1 (Level A) |
| Technology specifications | C or higher | ≥ 3 | 1 |
| Timeline dates | B or higher | ≥ 3 | 1 |
| Stakeholder names | B or higher | ≥ 3 | 1 |
| Narrative summary | — (synthesized by analyst) | — | ≥ 2 sources, at least 1 Level A or B |

---

## 4. Source Type Classification

### 4.1 Source Type Taxonomy

| `source_type` Enum Value | Definition | Typical Quality Level | Examples |
|--------------------------|------------|----------------------|----------|
| `press_release` | Official developer/company press release | A | Air Liquide Normand'Hy FID announcement |
| `investor_presentation` | Company investor day/earnings presentation | A | Shell Capital Markets Day 2024 |
| `company_filing` | Annual report, SEC filing, regulatory filing | A | Air Liquide 2024 Annual Report |
| `government_announcement` | Government ministry/press release | A–B | BMWK IPCEI funding announcement |
| `industry_report` | Published report from recognized institution | B | IEA Global Hydrogen Review 2025 |
| `academic_paper` | Peer-reviewed journal or conference paper | B | Journal of Power Sources, EES |
| `project_website` | Official project-dedicated website | A–B | normandhy.airliquide.com |
| `oem_datasheet` | Official electrolyzer manufacturer datasheet | A–B | Siemens Energy Silyzer 300 datasheet |
| `news_article` | Professional industry media article | C | H2 View, Hydrogen Insight |
| `conference_presentation` | Slides/talk from industry conference | B–C | World Hydrogen Summit presentation |
| `database` | Third-party project database | C–D | IEA H₂ Projects Database, BNEF database |
| `expert_interview` | Direct communication with project stakeholder | B | Interview with project director (cited) |
| `blog` | Personal/company blog post | D | LinkedIn article, company blog |
| `social_media` | Social media post (Twitter/X, LinkedIn) | D | Developer's LinkedIn announcement (use as signal only) |
| `other` | Catch-all for unclassified sources | D | Default; reclassify when type determined |

### 4.2 Source Type to Quality Level Mapping

```
press_release        → Level A (developer), Level B (government)
investor_presentation → Level A
company_filing       → Level A
government_announcement → Level A (national), Level B (municipal)
industry_report      → Level B (IEA/IRENA/H₂ Council), Level C (commercial)
academic_paper       → Level B (peer-reviewed), Level C (preprint)
project_website      → Level A (developer-owned), Level B (third-party)
oem_datasheet        → Level A (official product sheet), Level B (third-party summary)
news_article         → Level C (industry media), Level D (general media)
conference_presentation → Level B (named speaker + organization), Level C (unnamed)
database             → Level C (paid/professional), Level D (community)
expert_interview     → Level B (cited + attributable), Level C (anonymous)
blog                 → Level D
social_media         → Level D
```

---

## 5. Source Selection Heuristics

### 5.1 Selection Priority

When multiple sources exist for a single fact, select using this priority cascade:

1. **Level A + recency:** Official developer source, most recent
2. **Level A + historic:** Official developer source, older (for timeline evolution)
3. **Level B + recency:** Authoritative industry source, most recent
4. **Level B + specific:** Authoritative source that specifically addresses this project (not generic)
5. **Level C + corroborated:** Media source confirmed by another independent Level C source
6. **Level C + single:** Single media source (flag as "single-sourced")
7. **Level D:** NEVER as sole source. Use only in `sources[]` array as supplementary.

### 5.2 The "Two-Source Rule" for Financial Data

CAPEX figures, per-kW costs, and LCOH values require stricter sourcing than other fields:

- **If Level A source available:** 1 source sufficient (e.g., developer-stated total CAPEX in press release)
- **If only Level B source available:** 2 independent sources required (e.g., IEA report + BNEF report agreeing within 20%)
- **If only Level C source available:** Flag as `capex_confidence: "media_report"` — do NOT use as primary CAPEX benchmark
- **Never use Level D source for financial data**

### 5.3 Recency Preference

| Data Type | Maximum Source Age (Preferred) | Maximum Source Age (Acceptable) |
|-----------|-------------------------------|-------------------------------|
| Project status | 6 months | 12 months |
| Capacity data | 12 months | 24 months |
| CAPEX data | 24 months | 36 months (with inflation note) |
| Technology specifications | 36 months | 60 months |
| Timeline dates | 12 months | 24 months |
| Stakeholder information | 12 months | 36 months |

---

## 6. Source Validation Rules

### 6.1 Mandatory Source Validation

Before a project record reaches `published` status, all sources must pass:

1. **Existence check:** URL resolves (200 OK) or local file exists
2. **Date check:** Publication date and retrieval date are present
3. **Relevance check:** Source actually mentions the project by name
4. **Consistency check:** Source does not contradict other Level A/B sources on the same fact
5. **Attribution check:** Source has identifiable author or publishing organization

### 6.2 Source Confidence Assignment

| Source Quality Level | Reliability Score | → | `sources[].confidence` |
|---------------------|-------------------|---|----------------------|
| A | 4–5 | → | `high` |
| B | 3–5 | → | `high` (score 4–5) or `medium` (score 3) |
| C | 2–4 | → | `medium` (score 3–4) or `low` (score 2) |
| D | 1–2 | → | `low` |

### 6.3 URL Accessibility

- All `sources[].url` values must be tested before `published` status
- 301/302 redirects: follow and store the final URL
- 404/410/503: store `local_file_ref` to archived PDF copy; flag URL as `broken`
- Paywalled content: note `"requires_subscription": true` in source metadata

---

## 7. Source Conflict Resolution

### 7.1 Conflict Detection

Source conflicts are identified when two sources disagree on a factual field (not opinion/estimate) by a material margin:

| Field Type | Material Conflict Threshold |
|-----------|----------------------------|
| Capacity (MW) | > 5% difference |
| CAPEX (EUR) | > 15% difference |
| Timeline dates | > 6 months difference |
| Technology type | Qualitative difference (PEM vs Alkaline) |
| Stakeholder names | Qualitative difference |

### 7.2 Conflict Resolution Procedure

```
1. IDENTIFY the conflict (which field, which sources)
2. CLASSIFY the sources by quality level
3. PRIORITIZE higher-quality-level source
4. VERIFY priority source against a third source if possible
5. DOCUMENT the conflict in status_detail or a note field
6. FLAG the field with an appropriate confidence level
```

### 7.3 Conflict Documentation Pattern

When a conflict cannot be resolved, document using this pattern in `status_detail`:

```
"Source conflict: [Field] reported as [Value A] by [Source A, Level A, Score 5] 
and as [Value B] by [Source B, Level C, Score 3]. Using [Value A] with 
medium confidence pending third-source verification."
```

---

## 8. Source Decay Policy

### 8.1 Decay Timeline

Sources age and lose reliability. The following decay schedule applies:

| Source Type | Full Trust Period | Decay Period | After Decay |
|-------------|------------------|--------------|-------------|
| Level A — Project website | 12 months | 12–24 months | Flag for review; check for updates |
| Level A — Press release (event) | 6 months | 6–12 months | Event may be superseded; seek updated source |
| Level B — Industry report | 12 months | 12–36 months | Newer edition likely available |
| Level C — News article | 6 months | 6–18 months | Check for follow-up articles |
| Level D — Any | 3 months | 3–6 months | Treat as deprecated |

### 8.2 Decay Actions

When a source enters the decay period:
1. The project record's `last_data_update` is compared against the source date
2. If `last_data_update` < source_date + decay_period, no action
3. If `last_data_update` > source_date + decay_period, the project is flagged for review
4. Stale projects appear in `indexes/project_index.json` under `stale_entries`

---

## 9. Source Attribution Standards

### 9.1 Source Citation Format

Every source in the `sources[]` array must follow this standard:

```json
{
  "source_id": "SRC-YYYY-NNN",
  "source_type": "<<from controlled vocabulary>>",
  "source_quality_level": "<<A | B | C | D>>",
  "source_reliability_score": "<<1-5>>",
  "title": "<<Exact document title>>",
  "author": "<<Organization or person>>",
  "url": "<<URL or null if not public>>",
  "local_file_ref": "<<path relative to knowledge_base/>>",
  "publication_date": "<<YYYY-MM-DD>>",
  "retrieval_date": "<<YYYY-MM-DD>>",
  "confidence": "<<high | medium | low>>",
  "notes": "<<Optional: page number, specific quote, access restrictions>>"
}
```

### 9.2 Source ID Convention

```
SRC-{YEAR}-{SEQUENTIAL 3-DIGIT}
Example: SRC-2026-001, SRC-2026-002, ...

Allocated sequentially per year. Year = publication year of the source.
```

---

## 10. Appendix: Pre-Qualified Source List

### 10.1 Pre-Qualified Level A Sources

| Source | Type | Default Reliability | Notes |
|--------|------|--------------------|-------|
| Air Liquide Press Room | press_release | 5 | https://www.airliquide.com/group/press-releases-news |
| Shell Media Centre | press_release | 5 | https://www.shell.com/media.html |
| TotalEnergies Press Releases | press_release | 5 | https://totalenergies.com/media |
| Siemens Energy Press | press_release | 5 | https://press.siemens-energy.com/ |
| ENGIE Newsroom | press_release | 5 | https://en.newsroom.engie.com/ |
| Thyssenkrupp Nucera News | press_release | 4 | https://thyssenkrupp-nucera.com/news/ |
| EU IPCEI Registry | government_announcement | 5 | https://ec.europa.eu/competition/ipcei/ |
| BMWK Press (Germany) | government_announcement | 5 | https://www.bmwk.de/ |
| European Commission Press | government_announcement | 5 | https://ec.europa.eu/commission/presscorner/ |
| HyDeal Official | press_release | 4 | https://www.hydeal.com/ |

### 10.2 Pre-Qualified Level B Sources

| Source | Type | Default Reliability | Notes |
|--------|------|--------------------|-------|
| IEA Hydrogen Publications | industry_report | 5 | https://www.iea.org/topics/hydrogen |
| IRENA Hydrogen Reports | industry_report | 5 | https://www.irena.org/ |
| Hydrogen Council Reports | industry_report | 4 | https://hydrogencouncil.com/ |
| EU Innovation Fund Project Portal | database | 4 | https://ec.europa.eu/innovation-fund/ |
| BloombergNEF (BNEF) | industry_report | 4 | Paywalled; store local copies |
| Wood Mackenzie H2 Service | industry_report | 4 | Paywalled |
| NREL H2 Analysis | industry_report | 4 | https://www.nrel.gov/hydrogen/ |
| Fraunhofer ISE H2 | industry_report | 4 | https://www.ise.fraunhofer.de/ |

### 10.3 Pre-Qualified Level C Sources

| Source | Type | Default Reliability | Notes |
|--------|------|--------------------|-------|
| H2 View | news_article | 3 | https://www.h2-view.com/ |
| Hydrogen Insight | news_article | 3 | https://www.hydrogeninsight.com/ |
| Recharge News | news_article | 3 | https://www.rechargenews.com/ |
| FuelCellChina | news_article | 2 | Aggregator; verify against primary |
| H2 Bulletin | news_article | 3 | https://www.h2bulletin.com/ |
| S&P Global Commodity Insights | news_article | 3 | https://www.spglobal.com/commodityinsights/ |
| Blackridge Research (project database) | database | 2 | https://www.blackridgeresearch.com/ |
| Energy News (energynews.biz) | news_article | 2 | Aggregator |

### 10.4 Explicitly Excluded Sources

The following are NEVER acceptable as sources for Gold Dataset records:

- Wikipedia or any Wikimedia project
- AI-generated content (ChatGPT, Claude, Gemini, etc.)
- Personal blogs without named author + verifiable credentials
- Social media posts (may be used as discovery signals only)
- Preprints without peer review (may be used as supplementary, flagged as `preprint`)
- Company marketing materials without specific project data
- Sources behind paywalls without a local archived copy

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Lead Knowledge Engineer & Data Governance Manager | Initial Source Governance Framework |

---

*This framework governs all source selection, classification, and validation for the Green Hydrogen Project Feasibility Copilot Gold Dataset. Every project record must comply.*
