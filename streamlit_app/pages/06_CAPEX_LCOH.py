"""Page 6 — CAPEX & LCOH with uncertainty-first presentation, system boundary, and dual CAPEX."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme, apply_sidebar; apply_theme(); apply_sidebar()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})

st.title("Cost & Economic Analysis")
st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')} | {q.get('industry','')} | COD {q.get('target_cod','')}")

# ═══════════════════════════════════════════════════════════════
# V1.1: UNCERTAINTY-FIRST PRESENTATION
# Range is PRIMARY; central estimate is SECONDARY
# ═══════════════════════════════════════════════════════════════

st.markdown("#### CAPEX Estimate")
t = capex.get("total", {})
cen, low, high = t.get("central_eur_m",0), t.get("p10_eur_m",0), t.get("p90_eur_m",0)
ckw = t.get("central_eur_per_kw",0)

# ── Primary: Range ──
r1, r2 = st.columns(2)
with r1:
    st.metric("P10 – P90 Range", f"EUR {low:.0f}M – EUR {high:.0f}M",
              delta=f"AACE Class 4 (±20–30%)", delta_color="off")
with r2:
    st.metric("Central Estimate (P50)", f"EUR {cen:.0f}M",
              delta=f"EUR {ckw:.0f}/kW", delta_color="off")

# Range bar — now with correct alignment (V1.1 fix)
pct = ((cen-low)/(high-low))*100 if high>low else 50
st.markdown(f"""
<div style="background:#F1F8E9;border-radius:8px;padding:14px 16px;border:1px solid #C8E6C9;">
<p style="margin:0 0 8px 0;font-weight:600;color:#2E7D32;">Uncertainty Range — AACE Class 4 (Feasibility Study)</p>
<div style="display:flex;justify-content:space-between;font-size:0.9rem;color:#558B2F;margin-bottom:4px;">
<span>P10<br>EUR {low:.0f}M</span>
<span style="position:absolute;left:{pct:.0f}%;transform:translateX(-50%);font-weight:700;">▼<br>EUR {cen:.0f}M</span>
<span>P90<br>EUR {high:.0f}M</span>
</div>
<div style="position:relative;background:#E0E0E0;border-radius:4px;height:16px;margin-top:24px;">
<div style="background:linear-gradient(90deg,#A5D6A7,#2E7D32,#FFCC80,#E65100);width:100%;height:16px;border-radius:4px;"></div>
<div style="position:absolute;left:{pct:.0f}%;top:-10px;width:3px;height:36px;background:#1B5E20;border-radius:2px;"></div>
</div>
<p style="margin:8px 0 0 0;font-size:0.85rem;color:#558B2F;text-align:center;">The P10–P90 range represents the ±20–30% accuracy band typical of pre-feasibility (AACE Class 4) estimates.</p>
</div>
""", unsafe_allow_html=True)

st.caption(f"Confidence: {capex.get('weighted_confidence_label','')} ({capex.get('weighted_confidence',0):.2f}) | AACE Class 4 | Benchmark: {capex.get('benchmark_record','')}")

st.divider()

# ═══════════════════════════════════════════════════════════════
# V1.1: DUAL CAPEX PRESENTATION
# Reference Benchmark vs Industrial Development Budget
# ═══════════════════════════════════════════════════════════════

ind_budget = capex.get("industrial_budget", {})
if ind_budget.get("available", False):
    st.markdown("#### Two Views of CAPEX")
    st.caption("The Reference Benchmark and Industrial Development Budget serve different purposes. Use the right number for the right audience.")

    bc1, bc2 = st.columns(2)

    with bc1:
        ref_m = ind_budget.get("reference_eur_m", cen)
        st.markdown(f"""
<div style="border:2px solid #2E7D32;border-radius:10px;padding:16px;background:#E8F5E9;">
<h4 style="margin:0 0 8px 0;color:#1B5E20;">📋 Reference Benchmark CAPEX</h4>
<p style="font-size:1.4rem;font-weight:700;margin:4px 0;color:#2E7D32;">EUR {ref_m:.0f}M</p>
<p style="font-size:0.85rem;color:#33691E;margin:4px 0;">Nth-of-a-kind | Overnight cost | 2025 EUR</p>
<p style="font-size:0.8rem;color:#558B2F;margin:4px 0;">Use for: technology comparison, cost curve analysis, regulatory filings</p>
</div>
""", unsafe_allow_html=True)

    with bc2:
        ind_m = ind_budget.get("industrial_eur_m", 0)
        delta_pct = ind_budget.get("delta_pct", 0)
        st.markdown(f"""
<div style="border:2px solid #E65100;border-radius:10px;padding:16px;background:#FFF3E0;">
<h4 style="margin:0 0 8px 0;color:#BF360C;">🏗️ Industrial Development Budget</h4>
<p style="font-size:1.4rem;font-weight:700;margin:4px 0;color:#E65100;">EUR {ind_m:.0f}M <span style="font-size:0.9rem;font-weight:400;">(+{delta_pct:.0f}% vs benchmark)</span></p>
<p style="font-size:0.85rem;color:#BF360C;margin:4px 0;">First project | Total investment | Year-of-expenditure EUR</p>
<p style="font-size:0.8rem;color:#E65100;margin:4px 0;">Use for: budget planning, funding applications, board presentations</p>
</div>
""", unsafe_allow_html=True)

    # Factor breakdown
    factors = ind_budget.get("factors", {})
    with st.expander("Industrial Budget — Factor Breakdown"):
        fcols = st.columns(4)
        with fcols[0]:
            st.metric("FOAK Multiplier", f"{factors.get('foak_multiplier',1.0):.2f}×")
            st.caption(f"Scale FOAK: {factors.get('foak_scale',False)} | App FOAK: {factors.get('foak_application',False)}")
        with fcols[1]:
            st.metric("IDC Factor", f"{factors.get('idc_factor',1.0):.2f}×")
            st.caption(factors.get("idc_assumption",""))
        with fcols[2]:
            st.metric("Scope Factor", f"{factors.get('scope_factor',1.0):.2f}×")
            st.caption(f"{len(factors.get('scope_items',[]))} scope items")
        with fcols[3]:
            st.metric("Escalation", f"{factors.get('escalation_factor',1.0):.3f}×")
            st.caption(f"{factors.get('escalation_rate_pct',3):.0f}%/yr × {factors.get('escalation_years',0)}yr ({factors.get('cost_year','')}→{factors.get('target_cod','')})")

        st.markdown(f"**Total Multiplier:** {factors.get('total_multiplier',1.0):.3f}×")
        st.caption(ind_budget.get("note",""))

        if factors.get("scope_items"):
            st.markdown("**Scope Items Included (beyond Reference Benchmark):**")
            for item in factors["scope_items"]:
                st.markdown(f"- {item}")

    st.caption(f"Industrial Budget calibration: {ind_budget.get('technology_calibration','PEM-calibrated')}. See industrial_budget_methodology.md for factor sources and limitations.")

elif ind_budget.get("available") is False:
    st.info(f"ℹ️ Industrial Development Budget not available: {ind_budget.get('reason','')}")

st.divider()

# ═══════════════════════════════════════════════════════════════
# Cost Breakdown
# ═══════════════════════════════════════════════════════════════

st.markdown("#### Cost Breakdown by Category")
bd = capex.get("breakdown", [])
if bd:
    rows = [{"Category": b["category"], "EUR M": b["eur_m"], "%": b["pct_of_total"], "EUR/kW": b["eur_per_kw"], "Conf.": b.get("confidence","C")} for b in bd]
    df = pd.DataFrame(rows)
    ca, cb = st.columns([3,2])
    with ca: st.bar_chart(df.set_index("Category")["EUR M"], height=300)
    with cb: st.dataframe(df[["Category","EUR M","%","Conf."]], use_container_width=True, hide_index=True,
                          column_config={"EUR M": st.column_config.NumberColumn(format="%.1f"),
                                         "%": st.column_config.NumberColumn(format="%.1f%%")})

st.divider()

# ═══════════════════════════════════════════════════════════════
# V1.1: SYSTEM BOUNDARY TRANSPARENCY
# ═══════════════════════════════════════════════════════════════

with st.expander("📐 System Boundary — What's Included / Excluded", expanded=False):
    st.markdown("""
The CAPEX estimate covers the electrolysis plant from **grid connection point** to **offtake battery limit**.
It does **not** include dedicated renewable generation, downstream customer infrastructure, or financing costs.
    """)

    sb1, sb2 = st.columns(2)

    with sb1:
        st.markdown("""
##### ✅ Included in CAPEX
| System | Category | Description |
|--------|----------|-------------|
| Electrolyzer stacks + power electronics | 01 (32%) | PEM stacks, IGBT rectifiers, gas-liquid separation, module auxiliaries |
| Grid connection + plant electrical | 02 (14%) | HV substation 110–380 kV, MV/LV distribution, backup UPS |
| Ultra-pure water treatment | 03 (4%) | RO + EDI + polishing loop, ASTM Type II |
| H₂ compression + purification | 04 (9%) | Compression to offtake pressure, TSA drying, metering |
| Civil + construction | 05 (10%) | Site prep, buildings, foundations, roads, drainage, fencing |
| Thermal management | 06 (3%) | Cooling towers, heat exchangers, closed-loop cooling |
| Instrumentation + controls | 07 (4%) | DCS, SIS (IEC 61511), gas detection, fire protection |
| Engineering + owner's costs | 08 (24%) | FEED + detailed eng., procurement, PM, permitting, land, contingency |

##### ⚠️ Partially Included
| Item | Coverage |
|------|----------|
| H₂ buffer storage | Process buffer only (minutes–hours). Bulk storage (cavern, tube trailer) excluded. |
| ATEX / safety systems | Embedded in civil (05) and I&C (07). Not a separate line item. |
| Commissioning | Embedded in Indirect & Owner's (08). |
""")

    with sb2:
        st.markdown("""
##### ❌ Excluded from CAPEX
| Item | Reason |
|------|--------|
| Dedicated renewable generation | Separate project scope (solar farm, wind farm) |
| Bulk H₂ storage (>24 hr) | Offtake-side infrastructure |
| H₂ dispensing / refuelling stations | Customer-side infrastructure |
| Pipeline injection station | Offtake-side; grid operator responsibility |
| Interest During Construction (IDC) | Financing cost, not CAPEX |
| Initial stack replacement inventory | OPEX reserve (sinking fund in LCOH) |
| Grid reinforcement beyond connection point | TSO responsibility |
| Owner's pre-FID development costs | Sunk cost |
| Decommissioning provision | End-of-life liability |

##### ✅ Included in LCOH (OPEX)
| Component | Value | Basis |
|-----------|-------|-------|
| Electricity | 55 kWh/kg × €/MWh | System efficiency + user price |
| Stack replacement | €350/kW sinking fund | Technology Card |
| Maintenance | €0.30/kg (PEM) | Technology Card proxy |
| Labor | €0.18/kg (PEM) | Technology Card proxy |
| Other (water, insurance, land) | €0.25/kg | Technology Card proxy |

##### ❌ Excluded from LCOH
| Item | Reason |
|------|--------|
| Grid connection tariff (TURPE/Netzentgelt) | Site-specific; not in proxy |
| CO₂ emission costs | Jurisdiction-dependent |
| H₂ transport to offtaker | Customer-side cost |
| Compression energy beyond offtake pressure | Included in 55 kWh/kg system efficiency |
""")

    st.caption("System boundary traceable to: CS-IND-006 (all-in benchmark), CS-ELC-001, CS-ELI-001, CS-HPR-001, CS-CIV-001, CS-IND-001/002/003/004, and cost_scaling_methodology.md.")

st.divider()

# ═══════════════════════════════════════════════════════════════
# LCOH — Uncertainty-First
# ═══════════════════════════════════════════════════════════════

st.markdown("#### Levelized Cost of Hydrogen (LCOH)")

lc = lcoh.get("central_eur_per_kg",0); lp10 = lcoh.get("p10_eur_per_kg",0); lp90 = lcoh.get("p90_eur_per_kg",0)

lr1, lr2 = st.columns(2)
with lr1:
    st.metric("P10 – P90 Range", f"EUR {lp10:.2f} – {lp90:.2f} /kg",
              delta=f"Dominant driver: {lcoh.get('dominant_driver','').replace('_',' ').title()}", delta_color="off")
with lr2:
    st.metric("Central Estimate (P50)", f"EUR {lc:.2f} /kg")

st.caption(f"Assumptions: {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)} EUR/MWh, {lcoh.get('assumptions',{}).get('full_load_hours',4500)} hrs/yr, {lcoh.get('assumptions',{}).get('wacc_pct',7):.0f}% WACC, {lcoh.get('assumptions',{}).get('project_life_years',20)} yr life")

# LCOH waterfall
st.markdown("#### LCOH Decomposition")
decomp = lcoh.get("decomposition",[])
if decomp:
    dc = [{"Component": d["component"], "EUR/kg": d["eur_per_kg"], "%": d["pct"]} for d in decomp]
    df_l = pd.DataFrame(dc)
    da, db = st.columns([1,1])
    with da: st.dataframe(df_l, use_container_width=True, hide_index=True,
                          column_config={"EUR/kg": st.column_config.NumberColumn(format="%.2f")})
    with db: st.bar_chart(df_l.set_index("Component")["EUR/kg"], height=250)

st.divider()

# Sensitivity Tornado
st.markdown("#### Sensitivity Tornado")
tornado = lcoh.get("tornado", [])
if tornado:
    import re
    tdata = []
    for item in tornado:
        txt = item.get("impact", "")
        m = re.findall(r'[\d.]+', txt)
        v = float(m[0]) if m else 0
        tdata.append({"Driver": item["driver"], "Impact +/-EUR/kg": v})
    td = pd.DataFrame(tdata).sort_values("Impact +/-EUR/kg", ascending=False)
    st.bar_chart(td.set_index("Driver")["Impact +/-EUR/kg"], height=280)

# Data quality note — prominent V1.1
if lcoh.get("data_quality_note"):
    st.warning(f"⚠️ **Data Quality:** {lcoh['data_quality_note']}")

st.divider()

# Navigation
st.markdown("""<div style="display:flex;gap:16px;font-size:0.9rem;">
""", unsafe_allow_html=True)
st.page_link("pages/02_Assessment_Report.py", label="← Assessment Report")
st.markdown("""<span style="color:#558B2F;">|</span>
""", unsafe_allow_html=True)
st.page_link("pages/03_Reference_Projects.py", label="Reference Projects →")
st.markdown("""</div>""", unsafe_allow_html=True)
