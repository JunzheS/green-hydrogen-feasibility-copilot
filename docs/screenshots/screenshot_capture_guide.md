# Screenshot Capture Guide

This guide explains exactly what screenshots to capture for the README. Each screenshot should be a full browser window capture (1920x1080 recommended) saved as PNG.

---

## Prerequisites

1. Run the application:
   ```bash
   cd hydrogen-copilot
   streamlit run streamlit_app/app.py
   ```
2. Open http://localhost:8501 in your browser
3. Navigate to **Project Input** and enter:
   - Country: France
   - Industry: Steel
   - Technology: PEM
   - Capacity: 100 MW
   - Target COD: 2029
4. Click **Run Assessment**
5. Navigate through each page below and capture

---

## Screenshot 1: Executive Dashboard

**File:** `docs/screenshots/dashboard.png`

**Target page:** Assessment Report (after running the France 100 MW PEM Steel assessment)

**What to capture:**
- The full gate banner at top (should show "PROCEED WITH CAUTION" in amber/gold)
- Five KPI metrics below: Technology, TRL, CAPEX, LCOH, Top Risks
- Four dimension quality cards: Reference Projects, Technology, Risk, Economics
- Key Findings list text below
- The green sidebar navigation should be visible on the left
- **Do NOT scroll** — capture the viewport showing the gate banner, KPIs, and dimension cards

**Alternative crop:** If the full page is too long, crop to show:
- Gate banner
- KPI row
- At least 2 of the 4 dimension cards

---

## Screenshot 2: Agent Trace Page (Flagship)

**File:** `docs/screenshots/agent_trace.png`

**Target page:** Agent Trace

**What to capture:**
- The complete 6-step flow diagram at the top (User Input > Agent 1 > Agent 2 > Agent 3 > Agent 4 > Decision)
- Step 0 (User Input) with the JSON query visible
- Step 1 (Agent 1 - Retrieval) showing:
  - Decision: Top match Normand'Hy (score 0.81)
  - Method: 5-dimension weighted similarity scoring
  - Evidence sources listed
- The green gradient chain from left (lighter) to right (darker) should be visible

**Important:** This is the flagship page. Capture a clean, information-rich view that shows the flow AND the first two steps expanded.

---

## Screenshot 3: CAPEX & LCOH Page

**File:** `docs/screenshots/capex_lcoh.png`

**Target page:** CAPEX & LCOH

**What to capture:**
- CAPEX metrics row (Central Estimate, P10, P90)
- The P10-P90 range bar with central marker
- Cost breakdown table with 8 categories
- The bar chart showing cost by category
- If the viewport allows, also show LCOH metrics and decomposition at the bottom

**Alternative:** Two crops if the full page is too long:
1. Top section: CAPEX estimate + breakdown table + bar chart
2. Bottom section: LCOH waterfall + decomposition + sensitivity tornado

---

## Image Processing Requirements

| Requirement | Specification |
|------------|---------------|
| Format | PNG |
| Resolution | 1920x1080 recommended (minimum 1280x720) |
| File size | Under 500 KB each |
| Browser | Chrome or Edge (best CSS rendering) |
| Background | White (the application theme) |
| Sidebar | Visible (shows the application context) |

---

## Verification Checklist

- [ ] `dashboard.png` shows the PROCEED WITH CAUTION gate with green theme
- [ ] `agent_trace.png` shows the complete agent flow with Normand'Hy as top match
- [ ] `capex_lcoh.png` shows the CAPEX breakdown with cost categories table
- [ ] All files are under 500 KB
- [ ] All files are PNG format
- [ ] No personal information visible in the screenshots
- [ ] The green energy theme is clearly visible
- [ ] README placeholder paths match the actual file paths
