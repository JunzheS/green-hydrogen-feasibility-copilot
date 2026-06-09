# Risk Scoring Methodology — Green Hydrogen Projects

**Document:** FMEA-Based Risk Scoring System
**Date:** 2026-06-05
**Author:** Senior Project Risk Manager & PMO Director
**Methodology Basis:** Failure Mode and Effects Analysis (FMEA) adapted per IEC 60812, integrated with ISO 31000 risk management framework
**Applies To:** All risk records in the Risk Library

---

## 1. Methodology Overview

### 1.1 Why FMEA?

Traditional P×I (Probability × Impact) scoring ignores **detectability** — whether you can see the risk coming. For green hydrogen projects, detectability is crucial:

- An electrolyzer degradation trend can be detected 12-18 months before failure via EIS monitoring (high detectability → manageable even if high probability and impact)
- A sudden diaphragm rupture with gas crossover may have zero warning (low detectability → catastrophic even if low probability)

The FMEA approach (P × I × D) captures this third dimension, producing a more realistic risk priority ranking.

### 1.2 Risk Priority Number (RPN)

```
RPN = Probability × Impact × Detectability

Where:
  Probability:   1–5 (how likely the risk is to occur)
  Impact:        1–5 (how severe the consequences)
  Detectability: 1–5 (how likely you are to detect it before impact)

Range: 1–125
```

---

## 2. Probability Scale

*"What is the likelihood of this risk occurring during the project lifecycle?"*

| Score | Label | Probability Range | Description | Hydrogen Examples |
|-------|-------|------------------|-------------|-------------------|
| **1** | Rare | <5% | Exceptional circumstances; has not occurred in comparable projects | Catastrophic electrolyzer stack failure from manufacturing defect (zero known cases in >100 MW PEM) |
| **2** | Unlikely | 5–15% | Could occur but not expected in normal conditions; isolated incidents in the industry | Iridium supply crisis forcing PEM production halt (has not occurred, but concentration risk exists) |
| **3** | Possible | 15–35% | Might occur under certain conditions; observed in some reference projects | Stack degradation exceeding warranty (observed in ~17% of PEM projects >20 MW with >3 years data) |
| **4** | Likely | 35–65% | Probably will occur at some point; common in similar projects | Grid connection delays (reported in >40% of European renewable energy projects) |
| **5** | Almost Certain | >65% | Expected to occur; has occurred in most comparable projects | Electricity price deviation from financial model (100% of operating projects experience some deviation) |

**Guidance for hydrogen projects:**

- Use Gold Dataset reference projects as evidence: "Observed in X of Y reference projects" → map to probability scale
- For risks with no reference data (FOAK projects), use expert elicitation with explicit uncertainty acknowledgment
- Review probability ratings when new operational data becomes available (e.g., after first stack replacement in a reference project)

---

## 3. Impact Scale

*"If this risk materializes, how severe are the consequences for the project?"*

| Score | Label | Schedule Impact | Cost Impact (100 MW plant) | H₂ Production Impact | Safety Impact | Project Viability |
|-------|-------|----------------|---------------------------|---------------------|---------------|-------------------|
| **1** | Negligible | <2 weeks | <€1M | <2% annual output | No injury | No material effect |
| **2** | Minor | 2 weeks–1 month | €1M–€5M | 2–5% annual output | Minor injury (first aid) | Minor, manageable |
| **3** | Moderate | 1–3 months | €5M–€20M | 5–15% annual output | Major injury (LTI) | Requires management attention; may affect one financial covenant |
| **4** | Major | 3–6 months | €20M–€50M | 15–30% annual output | Single fatality risk | Threatens project economics; may breach loan covenants |
| **5** | Critical | >6 months | >€50M | >30% annual output | Multiple fatality risk | Project viability threatened; potential default |

**Guidance for multi-dimensional impact:**

The overall Impact score is the **maximum** across all five dimensions. If a risk causes a major safety incident (Impact = 4) but only moderate cost (Impact = 3), the overall Impact is 4.

---

## 4. Detectability Scale

*"How likely are we to detect this risk before it causes significant impact?"*

| Score | Label | Detection Window | Description | Hydrogen Examples |
|-------|-------|-----------------|-------------|-------------------|
| **1** | Almost Certain | >12 months | Clear leading indicators; continuous automated monitoring; predictable trajectory | Stack degradation detected by EIS monitoring 12-18 months before requiring replacement |
| **2** | High | 6–12 months | Regular monitoring provides early warning; some manual interpretation needed | Water quality trending showing gradual RO membrane fouling; quarterly lab analysis confirms |
| **3** | Moderate | 1–6 months | Periodic inspection or analysis may detect; some risk of missing early signals | Grid connection construction progress — monthly TSO meetings detect schedule slippage |
| **4** | Low | Days–weeks | Late detection; symptoms appear close to failure point | Compressor bearing wear — vibration monitoring may only give 2-4 weeks warning before failure |
| **5** | Very Low | Hours or no warning | Sudden failure with no precursor; or monitoring not in place | Diaphragm rupture with H₂-O₂ mixing; requires redundant gas purity monitoring with automatic trip |

**Guidance:**

- A risk with probability 5 and impact 5 but detectability 1 (RPN=25) may be manageable through monitoring
- A risk with probability 1 and impact 5 but detectability 5 (RPN=25) is equally dangerous but harder to manage
- This is the key insight of FMEA: equal RPNs may require different treatment strategies

---

## 5. Risk Class Thresholds

| Risk Class | RPN Range | Color | PMO Response |
|-----------|-----------|-------|-------------|
| **Low** | 1–20 | 🟢 Green | Accept; monitor at standard review cadence (6-monthly) |
| **Medium** | 21–45 | 🟡 Yellow | Manage; active monitoring with defined indicators; quarterly review |
| **High** | 46–80 | 🟠 Orange | Mitigate; dedicated risk owner; specific mitigation actions with deadlines; monthly review |
| **Critical** | 81–125 | 🔴 Red | Escalate to Steering Committee; immediate action required; weekly review; contingency plan must be funded and ready |

### 5.1 Class Distribution Target

For a well-managed pre-feasibility project portfolio, the target risk distribution is:

| Risk Class | Target % of Total Risks | Comment |
|-----------|------------------------|---------|
| Low | 30–40% | Most operational risks should be here after mitigation |
| Medium | 35–45% | Typical for pre-mitigation project risks |
| High | 10–20% | Focus of active risk management effort |
| Critical | 0–5% | Should be zero after mitigation; residual criticals require board attention |

### 5.2 Residual Risk Acceptance Criteria

After mitigation:
- No risks should remain in the **Critical** class (RPN ≥ 81)
- **High** residual risks must be approved by the Project Director with documented acceptance rationale
- Risk reduction effectiveness = 1 − (Residual RPN / Initial RPN). Target ≥ 40% reduction for High/Critical risks.

---

## 6. Risk Heat Map (P × I)

The heat map below shows Probability × Impact only (for visualization; actual RPN includes Detectability):

```
Impact →
  5  |  5  |  10  |  15  |  20  |  25  |
  4  |  4  |   8  |  12  |  16  |  20  |
  3  |  3  |   6  |   9  |  12  |  15  |
  2  |  2  |   4  |   6  |   8  |  10  |
  1  |  1  |   2  |   3  |   4  |   5  |
     └──────────────────────────────────┘
       1      2      3      4      5    Probability →
```

| Color | P×I Range | Interpretation |
|-------|-----------|---------------|
| 🟢 Green | 1–4 | Low priority |
| 🟡 Yellow | 5–9 | Medium priority |
| 🟠 Orange | 10–15 | High priority |
| 🔴 Red | 16–25 | Critical priority |

**Note:** The P×I heat map is provided for visual communication with stakeholders. The full RPN (P×I×D) is the authoritative risk priority metric used for ranking and resource allocation.

---

## 7. Scoring Workflow

### 7.1 Initial Assessment

```
1. IDENTIFY the risk (name + category + subcategory per taxonomy)
2. DESCRIBE: summary, detailed description, root cause, trigger events
3. SCORE: Probability (1-5), Impact (1-5), Detectability (1-5)
4. COMPUTE: RPN = P × I × D
5. CLASSIFY: Low / Medium / High / Critical
6. DOCUMENT: Rationale for each score, citing evidence
```

### 7.2 Mitigation Planning

```
7. DEFINE strategy: Avoid / Reduce / Transfer / Accept / Contingency
8. PLAN preventive actions (reduce probability)
9. PLAN corrective actions (reduce impact)
10. PLAN monitoring indicators (improve detectability)
11. RE-SCORE residual risk: P', I', D' → RPN'
12. VERIFY reduction: Is RPN' acceptable? If not, iterate on mitigation.
```

### 7.3 Ongoing Monitoring

```
13. ASSIGN risk owner + review cadence
14. TRACK monitoring indicators
15. RE-ASSESS at each review gate or when a trigger event is detected
16. UPDATE risk record with new scores, evidence, and lessons learned
```

---

## 8. Scoring Examples (From Validation Cases)

### Example 1: Grid Connection Delay

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Probability | 4 (Likely) | Grid delays reported in >40% of European renewable projects; TSO resource constraints well-documented |
| Impact | 4 (Major) | 3-6 months schedule slip; €20-50M revenue loss; CO₂ compliance risk if grey H₂ used as interim |
| Detectability | 2 (High) | Monthly TSO meetings; construction progress reports; regulatory milestone tracking — 6-12 month detection window |
| **RPN** | **32** | **Class: Medium** — active management required |

### Example 2: Electrolyzer Supplier Delay

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Probability | 3 (Possible) | PEM OEMs have delivery track record but are scaling rapidly; slot reservation system partially mitigates |
| Impact | 4 (Major) | 3-6 month delay; delayed revenue; potential offtake agreement default |
| Detectability | 3 (Moderate) | Manufacturing progress tracked via milestone payments; 3-6 month detection window if transparent reporting |
| **RPN** | **36** | **Class: Medium** — active management required |

### Example 3: Electricity Price Volatility

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Probability | 5 (Almost Certain) | Electricity prices ALWAYS deviate from financial model; 100% of operating projects experience this |
| Impact | 3 (Moderate) | Electricity is 70% of OPEX; €5-20M OPEX impact over project life at 100 MW scale |
| Detectability | 1 (Almost Certain) | Wholesale electricity prices are publicly available daily; forward curves provide 12-24 month visibility |
| **RPN** | **15** | **Class: Low** — accept; monitor and use hedging |

**Key insight from Example 3:** Despite being "Almost Certain" (P=5), the combination of moderate impact (I=3) and near-perfect detectability (D=1) makes this a Low-class risk. This demonstrates why the FMEA approach is superior to P×I alone (which would give 15, a misleadingly high score).

---

## 9. Scoring Guidelines for Hydrogen-Specific Factors

### 9.1 Technology Maturity Adjustments

| Factor | PEM Adjustment | Alkaline Adjustment |
|--------|---------------|-------------------|
| Technology maturity | +1 to probability for FOAK risks (limited >100 MW references) | No adjustment (TRL 9, mature) |
| OEM availability | +1 to probability for supply chain risks (only 4 major OEMs) | −1 to probability (10+ OEMs, Chinese option) |
| Dynamic operation | −1 to probability for renewable intermittency risks (better ramp capability) | +1 to probability for renewable intermittency risks (slower response) |

### 9.2 Scale Adjustments

| Scale | Adjustment |
|-------|-----------|
| <10 MW (pilot/demo) | −1 to impact (smaller absolute financial exposure) |
| 10–100 MW (commercial entry) | No adjustment |
| 100–500 MW (large commercial) | +1 to impact (larger absolute financial exposure) |
| >500 MW (giga-scale) | +1 to impact AND +1 to detectability (more complex, harder to detect all risks early) |

### 9.3 First-of-a-Kind Premium

FOAK projects carry an inherent risk premium across all categories:
- +1 to probability for technical, supply chain, and construction risks
- +1 to impact for financial risks (lenders price FOAK conservatively)
- −1 to detectability for technical risks (less operational data = harder to detect degradation trends)

---

## 10. RPN Allocation Example: Risk Budget per Category

For a 100 MW PEM greenfield project at pre-feasibility stage, a target RPN budget might be:

| Category | Target Total RPN | Max RPN per Risk | Typical Risk Count |
|----------|-----------------|------------------|--------------------|
| Technical | ≤ 120 | 60 | 3-5 risks |
| Supply Chain | ≤ 80 | 45 | 2-3 risks |
| Grid & Energy | ≤ 100 | 50 | 3-4 risks |
| Regulatory | ≤ 60 | 36 | 2-3 risks |
| Financial | ≤ 80 | 45 | 2-4 risks |
| Construction | ≤ 60 | 36 | 2-3 risks |
| Operational | ≤ 50 | 30 | 2-3 risks |
| Environmental | ≤ 50 | 30 | 2-3 risks |
| **TOTAL** | **≤ 600** | | **18-28 risks** |

**Note:** This is a HEURISTIC, not a formula. Risk budgets are management tools for proportionality, not hard constraints. A project with a genuinely unique risk should include it regardless of budget.

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-05 | Senior Project Risk Manager & PMO Director | Initial PMO risk scoring methodology |

---

*This methodology adapts IEC 60812 FMEA principles to the specific context of industrial green hydrogen projects. The three-dimensional scoring (P×I×D) provides a more realistic risk prioritization than traditional P×I matrices, especially for risks where detectability is a differentiating factor (e.g., slow degradation vs. sudden failure).*
