"""Page 2 — Executive Dashboard with Snapshot, Insights, and Next Actions."""
import streamlit as st
from utils.theme import apply_theme, apply_sidebar; apply_theme(); apply_sidebar()
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

# Decision brief
gc = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}
gt = {"PROCEED":"white","PROCEED WITH CAUTION":"#1B5E20","DO NOT PROCEED":"white","INSUFFICIENT DATA":"white"}
st.markdown(f"""
<div style="background:{gc.get(gate,'#78909C')};border-radius:12px;padding:24px;color:{gt.get(gate,'white')};margin-bottom:16px;">
<div style="display:flex;justify-content:space-between;">
<div><p style="margin:0;opacity:0.7;font-size:0.85rem;">EXECUTIVE DECISION</p>
<h1 style="margin:4px 0;color:inherit;font-size:2rem;">{gate}</h1>
<p style="margin:4px 0;opacity:0.9;">{gate_just.get('rationale','')[:180]}</p></div>
<div style="text-align:right;"><p style="margin:0;font-size:1.1rem;">{q.get('capacity_mw','')} MW {q.get('technology','')}</p>
<p style="margin:2px 0;opacity:0.8;">{q.get('country','')} | {q.get('industry','')} | COD {q.get('target_cod','')}</p>
<p style="margin:2px 0 0;opacity:0.7;">Confidence: {pm.get('overall_confidence',{}).get('label','-')} ({pm.get('overall_confidence',{}).get('score',0):.2f})</p></div></div></div>
""", unsafe_allow_html=True)

# ─── ASSESSMENT SNAPSHOT ───
st.markdown("#### Assessment Snapshot")
col_sp1, col_sp2, col_sp3, col_sp4, col_sp5, col_sp6 = st.columns(6)
with col_sp1: st.metric("Technology", f"{q.get('technology','')} TRL {tech.get('trl','')}")
with col_sp2: st.metric("CAPEX", f"EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M")
with col_sp3: st.metric("LCOH", f"EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg")
with col_sp4: st.metric("Top Risk", risk.get('top_risks',[{}])[0].get('rpn',0) if risk.get('top_risks') else '-', risk.get('top_risks',[{}])[0].get('risk_name','')[:25] if risk.get('top_risks') else '')
with col_sp5: st.metric("Confidence", pm.get('overall_confidence',{}).get('label','-'))
with col_sp6: st.metric("Gate", gate)
st.caption("Scroll down for executive summary, assessment dimensions, and insights.")

st.divider()

# Management summary
st.markdown("#### Executive Summary")
capex_m = capex.get("total",{}).get("central_eur_m",0)
capex_kw = capex.get("total",{}).get("central_eur_per_kw",0)
lcoh_c = lcoh.get("central_eur_per_kg",0)
trl = tech.get("trl","")
suit = tech.get("application_suitability","")
top_risk_name = risk.get("top_risks",[{}])[0].get("risk_name","") if risk.get("top_risks") else "None"
dominant = lcoh.get("dominant_driver","").replace("_"," ").title()
rec = insights[0].get("recommendation","") if insights else ""
st.markdown(f"""
A {q.get('capacity_mw','')} MW {q.get('technology','')} project for {q.get('industry','')} in {q.get('country','')} targeting COD {q.get('target_cod','')}.
Technology readiness is TRL {trl} with **{suit.upper()}** suitability for this application.
Estimated CAPEX: **EUR {capex_m:.0f}M (EUR {capex_kw:.0f}/kW)**. LCOH: **EUR {lcoh_c:.2f}/kg**.
The dominant economic driver is **{dominant}**.
Primary risk: *{top_risk_name}*. {rec}
""")

st.divider()

# Dimensions
st.markdown("#### Assessment Dimensions")
dims = pm.get("dimension_scores", {})
dl = st.columns(4)
for i, (k, lab) in enumerate({"project_references":"References","technology":"Technology","risk":"Risk","economics":"Economics"}.items()):
    d = dims.get(k,{}); qual = d.get("quality","-")
    c = "#2E7D32" if qual=="GOOD" else "#F9A825" if qual=="ADEQUATE" else "#C62828"
    bg = "#E8F5E9" if qual=="GOOD" else "#FFFDE7" if qual=="ADEQUATE" else "#FFEBEE"
    with dl[i]: st.markdown(f"<div style='border:1px solid {c};border-radius:8px;padding:8px;text-align:center;background:{bg};'><p style='color:{c};margin:0;font-weight:600;font-size:1.1rem;'>{qual}</p><p style='margin:2px 0 0;color:#558B2F;'>{lab}</p></div>", unsafe_allow_html=True)

st.divider()

# Pros/Cons
st.markdown("#### Why This Decision?")
pc1, pc2 = st.columns(2)
with pc1:
    st.markdown("**Pros**")
    pros = []
    if trl >= 8: pros.append(f"Proven technology — TRL {trl}, commercially deployed")
    if "high" in suit: pros.append("Rated HIGH suitability for this offtake")
    if dims.get("project_references",{}).get("quality") in ("GOOD","ADEQUATE"): pros.append("Comparable references exist in the dataset")
    for p in pros or ["Technology is commercially viable"]: st.markdown(f"- {p}")
with pc2:
    st.markdown("**Cons / Risks**")
    cons = []
    if dims.get("economics",{}).get("quality")!="GOOD": cons.append("Economic confidence is ADEQUATE — OEM quotation recommended")
    if dims.get("risk",{}).get("quality")!="GOOD": cons.append("Some risks lack project-evidenced mitigation")
    if pm.get("critical_gaps"): cons.append("Critical knowledge gaps exist — see gaps section")
    for c in cons or ["No significant risks identified at this stage"]: st.markdown(f"- {c}")

st.divider()

# Insights
if insights:
    st.markdown("#### Key Findings")
    for ins in insights:
        bg_c = "#E8F5E9" if ins.get("label") in ("TECH","BENCH","COST","CAPEX") else "#FFF3E0"
        st.markdown(f"""
<div style="border:1px solid #C8E6C9;border-radius:8px;padding:14px;margin:8px 0;background:{bg_c};">
<div style="display:flex;justify-content:space-between;"><strong>{ins.get('icon','')} {ins['title']}</strong><span style="color:#558B2F;font-size:0.85rem;">{ins.get('label','')}</span></div>
<p style="margin:6px 0 0;font-size:0.95rem;">{ins.get('observation','')[:200]}</p>
<p style="margin:4px 0 0;font-size:0.95rem;"><strong>Recommendation:</strong> {ins.get('recommendation','')[:250]}</p>
</div>""", unsafe_allow_html=True)
    st.divider()

# ─── NEXT ACTIONS ───
st.markdown("#### What Should Happen Next?")
next_actions = []
capex_conf = capex.get('weighted_confidence_label','')
if capex_conf != "GOOD":
    next_actions.append("**1. Obtain an OEM budget quotation** for the electrolyser stack to upgrade CAPEX confidence from Class C to Class B, narrowing the estimate range by 10-15%.")
next_actions.append(f"**{len(next_actions)+1}. Secure renewable electricity pricing.** Electricity is the dominant LCOH driver. Target a fixed-price PPA at or below EUR {lcoh.get('assumptions',{}).get('electricity_price_eur_per_mwh',40)}/MWh before FEED completion.")
if tech.get("is_foak_for_application") or tech.get("is_foak_for_scale"):
    next_actions.append(f"**{len(next_actions)+1}. Commission a technology qualification study** to resolve first-of-a-kind risk for {q.get('industry','')} application. Engage OEM and EPC contractor.")
next_actions.append(f"**{len(next_actions)+1}. Launch FEED study** with a qualified engineering contractor to move from AACE Class 4 to Class 3 estimate accuracy.")
for na in next_actions[:4]:
    st.markdown(f"- {na}")

st.divider()

# Conditions
if gate_just.get("conditions"):
    st.markdown("#### Conditions for Advancement")
    for i, c in enumerate(gate_just["conditions"], 1): st.markdown(f"- **{i}.** {c}")
    st.divider()

# Gaps
if pm.get("critical_gaps") or pm.get("important_gaps"):
    st.markdown("#### Knowledge Gaps")
    for g in pm.get("critical_gaps",[]): st.error(g)
    for g in pm.get("important_gaps",[]): st.warning(g)
    st.divider()

# Export
col_e, _ = st.columns([1,3])
with col_e:
    html = generate_html_report(q, report)
    st.download_button("Export PDF Report", html, file_name=f"h2_assessment_{st.session_state.get('current_assessment_id','report')}.html", mime="text/html", type="primary")
    st.caption("Open in browser, Ctrl+P / Cmd+P to print to PDF.")
# ─── EXPERT DRILL-DOWN ───
with st.expander("Expert Analysis Tools"):
    c1, c2 = st.columns(2)
    with c1:
        st.page_link("pages/03_Reference_Projects.py", label="Reference Projects")
        st.page_link("pages/04_Technology_Assessment.py", label="Technology Assessment")
        st.page_link("pages/09_Technology_Comparison.py", label="Technology Comparison")
        st.page_link("pages/07_Agent_Trace.py", label="Agent Trace")
    with c2:
        st.page_link("pages/30_OEM_Intelligence.py", label="OEM Intelligence")
        st.page_link("pages/31_Developer_Intelligence.py", label="Developer Intelligence")
        st.page_link("pages/33_Source_Transparency.py", label="Source Transparency")
        st.page_link("pages/32_Contradiction_Detection.py", label="Agent Collaboration")
    st.caption("Expert analysis tools for deeper investigation. Also available in the sidebar under Expert Results.")

st.caption(f"Assessment {st.session_state.get('current_assessment_id','-')} | Copilot v1.0")
