"""Page 2 — Executive Dashboard. Consulting-style decision brief."""
import streamlit as st
from utils.theme import apply_theme; apply_theme()
from components.pdf_export import generate_html_report
import pandas as pd

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

# ─── HEADER CARD ───
gc = {"PROCEED":"#2E7D32","PROCEED WITH CAUTION":"#F9A825","DO NOT PROCEED":"#C62828","INSUFFICIENT DATA":"#78909C"}
gt = {"PROCEED":"white","PROCEED WITH CAUTION":"#1B5E20","DO NOT PROCEED":"white","INSUFFICIENT DATA":"white"}
st.markdown(f"""
<div style="background:{gc.get(gate,'#78909C')};border-radius:12px;padding:28px;color:{gt.get(gate,'white')};margin-bottom:20px;">
<div style="display:flex;justify-content:space-between;align-items:center;">
<div>
<p style="margin:0;font-size:0.85rem;opacity:0.8;">DECISION BRIEF</p>
<h1 style="margin:4px 0 0 0;color:inherit;font-size:2rem;">{gate}</h1>
<p style="margin:6px 0 0 0;font-size:1rem;opacity:0.9;">{gate_just.get('rationale','')[:120]}</p>
</div>
<div style="text-align:right;">
<p style="margin:0;font-size:1.1rem;">{q.get('capacity_mw','')} MW {q.get('technology','')}</p>
<p style="margin:2px 0;opacity:0.8;">{q.get('country','')} | {q.get('industry','')} | COD {q.get('target_cod','')}</p>
<p style="margin:2px 0;opacity:0.7;font-size:0.9rem;">Confidence: {pm.get('overall_confidence',{}).get('label','-')} ({pm.get('overall_confidence',{}).get('score',0):.2f})</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ─── QUICK METRICS ───
m1, m2, m3, m4 = st.columns(4)
with m1: st.metric("CAPEX", f"EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M", f"EUR {capex.get('total',{}).get('central_eur_per_kw',0):.0f}/kW")
with m2: st.metric("LCOH", f"EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg", f"P10-P90: EUR {lcoh.get('p10_eur_per_kg',0):.2f}-{lcoh.get('p90_eur_per_kg',0):.2f}")
with m3: st.metric("Technology", f"{tech.get('trl','')}/9", f"{q.get('technology','')} | {tech.get('application_suitability','').upper()}")
with m4: st.metric("Risk", f"{risk.get('total_filtered',0)} identified", f"Top: {risk.get('top_risks',[{}])[0].get('rpn',0) if risk.get('top_risks') else 0} RPN")

# ─── DIMENSION SCORES ───
st.markdown("#### Assessment Dimensions")
dims = pm.get("dimension_scores", {})
dl = st.columns(4)
dlabels = {"project_references":"References","technology":"Technology","risk":"Risk","economics":"Economics"}
for i, (k, lab) in enumerate(dlabels.items()):
    d = dims.get(k, {})
    qual = d.get("quality", "-")
    c = "#2E7D32" if qual == "GOOD" else "#F9A825" if qual == "ADEQUATE" else "#C62828"
    bg = "#E8F5E9" if qual == "GOOD" else "#FFFDE7" if qual == "ADEQUATE" else "#FFEBEE"
    with dl[i]:
        st.markdown(f"<div style='border:1px solid {c};border-radius:8px;padding:8px;text-align:center;background:{bg};'><p style='color:{c};margin:0;font-weight:600;'>{qual}</p><p style='margin:2px 0 0;color:#558B2F;font-size:0.82rem;'>{lab}</p></div>", unsafe_allow_html=True)

st.divider()

# ─── EXECUTIVE INSIGHTS ───
if insights:
    st.markdown("#### Key Findings")
    for ins in insights:
        ico = ins.get("icon", "•")
        bg_color = "#E8F5E9" if ins["label"] in ("TECH","BENCH") else "#FFF3E0" if ins["label"] == "RISK" else "#F1F8E9"
        st.markdown(f"""
        <div style="border:1px solid #C8E6C9;border-radius:8px;padding:14px;margin:8px 0;background:{bg_color};">
        <div style="display:flex;justify-content:space-between;"><strong>{ico} {ins['title']}</strong><span style="color:#558B2F;font-size:0.8rem;">{ins['label']}</span></div>
        <p style="margin:6px 0 0;font-size:0.92rem;">{ins['observation'][:180]}</p>
        <p style="margin:4px 0 0;font-size:0.92rem;"><strong>Recommendation:</strong> {ins['recommendation'][:200]}</p>
        </div>
        """, unsafe_allow_html=True)
    st.divider()

# ─── CONDITIONS FOR ADVANCEMENT ───
if gate_just.get("conditions"):
    st.markdown("#### Conditions for Advancement")
    for i, c in enumerate(gate_just["conditions"], 1):
        st.markdown(f"- **{i}.** {c}")

# ─── GAPS ───
if pm.get("critical_gaps") or pm.get("important_gaps"):
    st.markdown("#### Information Gaps")
    for g in pm.get("critical_gaps", []):
        st.error(g)
    for g in pm.get("important_gaps", []):
        st.warning(g)

st.divider()

# ─── EXPORT ───
col_e, _ = st.columns([1, 3])
with col_e:
    html = generate_html_report(q, report)
    st.download_button("Export PDF Report", html, file_name=f"h2_assessment_{st.session_state.get('current_assessment_id','report')}.html", mime="text/html", type="primary")
    st.caption("Open HTML in browser, then Ctrl+P / Cmd+P to print to PDF.")

st.caption(f"Assessment {st.session_state.get('current_assessment_id','-')} | Copilot v1.0")
