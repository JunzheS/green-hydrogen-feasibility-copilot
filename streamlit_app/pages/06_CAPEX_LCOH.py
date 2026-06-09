"""Page 6 — CAPEX & LCOH with real tornado chart and cost breakdown."""
import streamlit as st
import pandas as pd

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})

st.title("Cost & Economic Analysis")
st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')}")

# CAPEX
st.markdown("#### Capital Expenditure")
t = capex.get("total", {})
cen, low, high = t.get("central_eur_m",0), t.get("p10_eur_m",0), t.get("p90_eur_m",0)
ckw = t.get("central_eur_per_kw",0)
m1, m2, m3 = st.columns(3)
with m1: st.metric("Central", f"EUR {cen:.0f}M", f"EUR {ckw:.0f}/kW")
with m2: st.metric("P10 (Optimistic)", f"EUR {low:.0f}M")
with m3: st.metric("P90 (Pessimistic)", f"EUR {high:.0f}M")
pct = ((cen-low)/(high-low))*100 if high>low else 50
st.markdown(f"""
<div style="background:#F1F8E9;border-radius:8px;padding:10px 16px;border:1px solid #C8E6C9;">
<div style="display:flex;justify-content:space-between;color:#558B2F;"><span>P10: EUR {low:.0f}M</span>
<span style="font-weight:700;">Central: EUR {cen:.0f}M</span><span>P90: EUR {high:.0f}M</span></div>
<div style="background:#E0E0E0;border-radius:4px;height:12px;margin-top:6px;">
<div style="background:linear-gradient(90deg,#A5D6A7,#2E7D32);width:{pct:.0f}%;height:12px;border-radius:4px;"></div></div></div>
""", unsafe_allow_html=True)
st.caption(f"Confidence: {capex.get('weighted_confidence_label','')} ({capex.get('weighted_confidence',0):.2f}) | AACE Class 4")

st.divider()

# Cost breakdown bar
st.markdown("#### Cost Breakdown")
bd = capex.get("breakdown", [])
if bd:
    rows = [{"Category": b["category"][:30], "EUR M": b["eur_m"], "%": b["pct_of_total"], "Conf.": b.get("confidence","C")} for b in bd]
    df = pd.DataFrame(rows)
    ca, cb = st.columns([3,2])
    with ca: st.bar_chart(df.set_index("Category")["EUR M"], height=300)
    with cb: st.dataframe(df[["Category","EUR M","%","Conf."]], use_container_width=True, hide_index=True,
                          column_config={"EUR M": st.column_config.NumberColumn(format="%.1f"),
                                         "%": st.column_config.NumberColumn(format="%.1f%%")})

st.divider()

# LCOH
st.markdown("#### Levelized Cost of Hydrogen")
lc = lcoh.get("central_eur_per_kg",0); lp10 = lcoh.get("p10_eur_per_kg",0); lp90 = lcoh.get("p90_eur_per_kg",0)
l1, l2, l3 = st.columns(3)
with l1: st.metric("Central", f"EUR {lc:.2f}/kg")
with l2: st.metric("P10", f"EUR {lp10:.2f}/kg")
with l3: st.metric("P90", f"EUR {lp90:.2f}/kg")
st.caption(f"{lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)} EUR/MWh, {lcoh.get('assumptions',{}).get('full_load_hours',4500)} hrs/yr")

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

# ─── REAL TORNADO CHART ───
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

if lcoh.get("data_quality_note"):
    st.warning(lcoh["data_quality_note"][:200])
st.caption("LCOH is CLASS D (preliminary); OPEX Library not yet populated.")

st.divider()
st.markdown("""<div style="display:flex;gap:16px;font-size:0.9rem;">
<a href='/Assessment_Report' target='_self' style="color:#2E7D32;">← Assessment Report</a>
<a href='/Reference_Projects' target='_self' style="color:#2E7D32;">Reference Projects →</a>
</div>""", unsafe_allow_html=True)
