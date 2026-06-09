"""Page 6 — CAPEX & LCOH with charts and visual analysis."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})

st.title("Cost & Economic Analysis")
st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")

# ─── CAPEX ───
st.markdown("#### Capital Expenditure")
t = capex.get("total", {})
central, low, high = t.get("central_eur_m",0), t.get("p10_eur_m",0), t.get("p90_eur_m",0)
ckw = t.get("central_eur_per_kw",0)

m1, m2, m3 = st.columns(3)
with m1: st.metric("Central", f"EUR {central:.0f}M", f"EUR {ckw:.0f}/kW")
with m2: st.metric("P10 (Optimistic)", f"EUR {low:.0f}M")
with m3: st.metric("P90 (Pessimistic)", f"EUR {high:.0f}M")

pct_mid = ((central-low)/(high-low))*100 if high>low else 50
st.markdown(f"""
<div style="background:#F1F8E9;border-radius:8px;padding:10px 16px;border:1px solid #C8E6C9;">
<div style="display:flex;justify-content:space-between;color:#558B2F;font-size:0.9rem;">
<span>P10: EUR {low:.0f}M</span><span style="font-weight:700;">Central: EUR {central:.0f}M</span><span>P90: EUR {high:.0f}M</span></div>
<div style="background:#E0E0E0;border-radius:4px;height:12px;margin-top:6px;">
<div style="background:linear-gradient(90deg,#A5D6A7,#2E7D32);width:{pct_mid:.0f}%;height:12px;border-radius:4px;"></div></div></div>
""", unsafe_allow_html=True)

st.caption(f"Confidence: {capex.get('weighted_confidence_label','')} ({capex.get('weighted_confidence',0):.2f}) | AACE Class 4")

st.divider()

# ─── COST BREAKDOWN BAR + TABLE ───
st.markdown("#### Cost Breakdown")
bd = capex.get("breakdown", [])
if bd:
    rows = [{"Category": b["category"][:30], "EUR M": b["eur_m"], "%": b["pct_of_total"], "Conf.": b.get("confidence","C")} for b in bd]
    df = pd.DataFrame(rows)
    c1, c2 = st.columns([3, 2])
    with c1:
        st.bar_chart(df.set_index("Category")["EUR M"], use_container_width=True, height=300)
    with c2:
        st.dataframe(df[["Category","EUR M","%","Conf."]], use_container_width=True, hide_index=True,
                     column_config={
                         "EUR M": st.column_config.NumberColumn(format="%.1f"),
                         "%": st.column_config.NumberColumn(format="%.1f%%")})

    # Cost drivers text
    st.markdown("**Cost Drivers**")
    st.markdown("""
| Driver | Share | Lever |
|--------|-------|-------|
| Electrolyser Stack | ~30% | Technology choice (PEM vs Alkaline) |
| Indirect & Contingency | ~24% | FOAK premium, EPC strategy, developer experience |
| Grid Connection | ~12% | Brownfield vs greenfield site selection |
| Hydrogen Processing | ~9% | Offtake pressure requirement (PEM has advantage) |
""")
st.divider()

# ─── LCOH ───
st.markdown("#### Levelized Cost of Hydrogen")
lc = lcoh.get("central_eur_per_kg",0)
lp10 = lcoh.get("p10_eur_per_kg",0)
lp90 = lcoh.get("p90_eur_per_kg",0)

cl1, cl2, cl3 = st.columns(3)
with cl1: st.metric("Central LCOH", f"EUR {lc:.2f}/kg")
with cl2: st.metric("P10", f"EUR {lp10:.2f}/kg")
with cl3: st.metric("P90", f"EUR {lp90:.2f}/kg")

st.caption(f"Assumptions: {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)} EUR/MWh, {lcoh.get('assumptions',{}).get('full_load_hours',4500)} hrs/yr")

# LCOH decomposition chart + table
st.markdown("#### LCOH Waterfall")
decomp = lcoh.get("decomposition",[])
if decomp:
    dc = [{"Component": d["component"], "EUR/kg": d["eur_per_kg"], "%": d["pct"]} for d in decomp]
    df_lcoh = pd.DataFrame(dc)
    dc1, dc2 = st.columns([1, 1])
    with dc1:
        st.dataframe(df_lcoh, use_container_width=True, hide_index=True,
                     column_config={"EUR/kg": st.column_config.NumberColumn(format="%.2f")})
    with dc2:
        st.bar_chart(df_lcoh.set_index("Component")["EUR/kg"], use_container_width=True, height=250)

# Tornado
st.markdown("#### Sensitivity Tornado")
for t_item in lcoh.get("tornado",[]):
    st.markdown(f"- **{t_item['driver']}**: {t_item['impact']}")

if lcoh.get("data_quality_note"):
    st.warning(lcoh["data_quality_note"][:200])

st.caption("LCOH is CLASS D (preliminary); OPEX Library not yet populated.")
