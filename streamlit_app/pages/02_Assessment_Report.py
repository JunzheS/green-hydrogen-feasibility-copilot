"""Page 2 — Executive Decision Brief with management summary and pros/cons."""
import streamlit as st
from utils.theme import apply_theme; apply_theme()
from components.pdf_export import generate_html_report

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
pm = report.get("pm_review", {})
tech = report.get("technology_assessment", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})
risk = report.get("risk_assessment", {})
insights = report.get("executive_insights", [])
gate_just = report.get("gate_justification", {})
gate = gate_just.get("decision", pm.get("gate_outcome", "-"))

# ─── HEADER ───
gc = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}
gtc = {"PROCEED":"white","PROCEED WITH CAUTION":"#1B5E20","DO NOT PROCEED":"white","INSUFFICIENT DATA":"white"}
st.markdown(f"""
<div style="background:{gc.get(gate,'#78909C')};border-radius:12px;padding:28px;color:{gtc.get(gate,'white')};">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div><p style="margin:0;font-size:0.85rem;opacity:0.8;">DECISION BRIEF</p>
<h1 style="margin:4px 0 0 0;color:inherit;font-size:2rem;">{gate}</h1>
<p style="margin:6px 0 0 0;font-size:1rem;opacity:0.9;">{gate_just.get('rationale','')[:160]}</p></div>
<div style="text-align:right;">
<p style="margin:0;font-size:1.1rem;">{q.get('capacity_mw','')} MW {q.get('technology','')}</p>
<p style="margin:2px 0;opacity:0.8;">{q.get('country','')} | {q.get('industry','')} | COD {q.get('target_cod','')}</p>
<p style="margin:2px 0 0;opacity:0.7;">Confidence: {pm.get('overall_confidence',{}).get('label','-')} ({pm.get('overall_confidence',{}).get('score',0):.2f})</p>
</div></div></div>
""", unsafe_allow_html=True)

# ─── MANAGEMENT SUMMARY ───
st.markdown("#### Executive Summary")
capex_m = capex.get("total",{}).get("central_eur_m",0)
capex_kw = capex.get("total",{}).get("central_eur_per_kw",0)
lcoh_c = lcoh.get("central_eur_per_kg",0)
trl = tech.get("trl","")
suit = tech.get("application_suitability","")
top_risk = risk.get("top_risks",[{}])[0].get("risk_name","") if risk.get("top_risks") else "None"
dominant = lcoh.get("dominant_driver","").replace("_"," ").title()
if insights:
    rec_text = insights[0].get("recommendation","")
else:
    rec_text = "See Key Findings below for detailed recommendations."
st.markdown(f"""
A {q.get('capacity_mw','')} MW {q.get('technology','')} project for {q.get('industry','')} in {q.get('country','')} targeting COD {q.get('target_cod','')}. Technology readiness is TRL {trl} with **{suit.upper()}** suitability for this application. The estimated CAPEX is **EUR {capex_m:.0f}M (EUR {capex_kw:.0f}/kW)** with LCOH of **EUR {lcoh_c:.2f}/kg**. The dominant economic driver is **{dominant}**. The primary risk identified is *{top_risk}*. {rec_text}
""")

# ─── PROS / CONS ───
st.markdown("#### Why This Decision?")
pc1, pc2 = st.columns(2)
with pc1:
    st.markdown("**Pros**")
    pros = []
    if trl >= 8: pros.append(f"**Proven technology** — TRL {trl}, commercially deployed at scale")
    suit_ok = "high" in suit or suit == "high"
    if suit_ok: pros.append("**Application suitability** — rated HIGH for this offtake")
    dims = pm.get("dimension_scores", {})
    ref_ok = dims.get("project_references",{}).get("quality") in ("GOOD","ADEQUATE")
    if ref_ok: pros.append("**Comparable references exist** — validated against real project data")
    if not pros: pros.append("Technology is commercially viable")
    for p in pros: st.markdown(f"- {p}")
with pc2:
    st.markdown("**Cons / Risks**")
    cons = []
    if dims.get("economics",{}).get("quality") == "ADEQUATE":
        cons.append("**Economic uncertainty** — CAPEX confidence is ADEQUATE; OEM quotation recommended")
    if dims.get("risk",{}).get("quality") != "GOOD":
        cons.append("**Risk data gaps** — some risks lack project-evidenced mitigation")
    if pm.get("critical_gaps"):
        cons.append("**Knowledge gaps** — critical information missing for complete assessment")
    if not cons: cons.append("No significant risks identified at pre-feasibility level")
    for c in cons: st.markdown(f"- {c}")

st.divider()

# ─── INSIGHTS ───
if insights:
    st.markdown("#### Key Findings")
    for ins in insights:
        bg = {"COST":"#E8F5E9","TECH":"#E8F5E9","BENCH":"#E8F5E9","RISK":"#FFF3E0","CAPEX":"#E8F5E9"}.get(ins.get("label",""),"#F9FBE7")
        st.markdown(f"""
        <div style="border:1px solid #C8E6C9;border-radius:8px;padding:14px;margin:8px 0;background:{bg};">
        <div style="display:flex;justify-content:space-between;"><strong>{ins.get('icon','')} {ins['title']}</strong><span style="color:#558B2F;font-size:0.82rem;">{ins.get('label','')}</span></div>
        <p style="margin:6px 0 0;font-size:0.92rem;">{ins.get('observation','')[:200]}</p>
        <p style="margin:4px 0 0;font-size:0.92rem;"><strong>Recommendation:</strong> {ins.get('recommendation','')[:250]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.divider()

# ─── CONDITIONS ───
if gate_just.get("conditions"):
    st.markdown("#### Conditions for Advancement")
    for i, c in enumerate(gate_just["conditions"], 1):
        st.markdown(f"- **{i}.** {c}")
    st.divider()

# ─── GAPS ───
if pm.get("critical_gaps") or pm.get("important_gaps"):
    st.markdown("#### Knowledge Gaps")
    for g in pm.get("critical_gaps",[]): st.error(g)
    for g in pm.get("important_gaps",[]): st.warning(g)
    st.divider()

# ─── EXPORT ───
col_e, _ = st.columns([1,3])
with col_e:
    html = generate_html_report(q, report)
    st.download_button("Export PDF Report", html, file_name=f"h2_assessment_{st.session_state.get('current_assessment_id','report')}.html", mime="text/html", type="primary")
    st.caption("Open in browser, Ctrl+P / Cmd+P to print to PDF.")
st.caption(f"Assessment {st.session_state.get('current_assessment_id','-')} | Copilot v1.0")
