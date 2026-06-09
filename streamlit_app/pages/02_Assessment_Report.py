"""Page 2 -- Executive Dashboard & Assessment Report."""
import streamlit as st
from utils.theme import apply_theme; apply_theme()
from components.pdf_export import generate_html_report

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})
pm = report.get("pm_review", {})
tech = report.get("technology_assessment", {})
capex = report.get("capex_assessment", {})
lcoh = report.get("lcoh_assessment", {})
risk = report.get("risk_assessment", {})

st.title("Assessment Report")
st.caption(f"{query.get('capacity_mw','')} MW {query.get('technology','')} | {query.get('country','')} | {query.get('industry','')} | COD {query.get('target_cod','')}")

# Gate banner
gate = pm.get("gate_outcome", "-")
conf = pm.get("overall_confidence", {})
gate_colors = {"PROCEED": "#2E7D32", "PROCEED WITH CAUTION": "#F9A825", "DO NOT PROCEED": "#C62828", "INSUFFICIENT DATA": "#78909C"}
gate_texts = {"PROCEED": "white", "PROCEED WITH CAUTION": "#1B5E20", "DO NOT PROCEED": "white", "INSUFFICIENT DATA": "white"}

st.markdown(f"""
<div style="background:{gate_colors.get(gate,'#78909C')};padding:20px;border-radius:8px;color:{gate_texts.get(gate,'white')};margin-bottom:20px;">
<p style="margin:0;font-size:0.85em;opacity:0.9;">Project Status</p>
<h2 style="margin:2px 0 0 0;color:inherit;font-size:1.6em;">{gate}</h2>
<p style="margin:4px 0 0 0;opacity:0.9;">Confidence: {conf.get('label','-')} ({conf.get('score',0):.2f})</p>
</div>
""", unsafe_allow_html=True)

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("Technology", query.get("technology", "-"))
with col2: st.metric("TRL", tech.get("trl", "-"))
with col3: st.metric("CAPEX", f"EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M")
with col4: st.metric("LCOH", f"EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg")
with col5: st.metric("Top Risks", len(risk.get("top_risks", [])))

st.divider()

# Dimension scores
st.subheader("Dimension Assessment")
dims = pm.get("dimension_scores", {})
cols = st.columns(4)
labels = {"project_references": "Reference Projects", "technology": "Technology", "risk": "Risk", "economics": "Economics"}
for i, (key, label) in enumerate(labels.items()):
    d = dims.get(key, {})
    with cols[i]:
        color = "#2E7D32" if d.get("quality") == "GOOD" else "#F9A825" if d.get("quality") == "ADEQUATE" else "#C62828"
        bg = "#F1F8E9" if d.get("quality") == "GOOD" else "#FFFDE7" if d.get("quality") == "ADEQUATE" else "#FFEBEE"
        st.markdown(f"""
        <div style="border:1px solid {color};border-radius:8px;padding:12px;text-align:center;background:{bg};">
        <p style="color:{color};margin:0;font-weight:600;font-size:1.2em;">{d.get('quality','-')}</p>
        <p style="margin:4px 0 0 0;font-size:0.85em;color:#558B2F;">{label}</p>
        <p style="color:#78909C;font-size:0.8em;margin:2px 0 0;">conf: {d.get('confidence',0):.2f}</p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Key findings
st.subheader("Key Findings")
findings = []
tech_name = tech.get('technology_name','')
findings.append(f"**Technology:** {tech_name} is at TRL {tech.get('trl','')} ({tech.get('commercial_maturity','')}). "
    f"Application suitability for {query.get('industry','')}: **{tech.get('application_suitability','').upper()}**.")
findings.append(f"**Scale:** {query.get('capacity_mw','')} MW is {tech.get('scale_status','').replace('_',' ')} "
    f"(max proven: {tech.get('max_proven_mw','')} MW). "
    f"{'First-of-a-kind for application.' if tech.get('is_foak_for_application') else 'Not first-of-a-kind.'}")
findings.append(f"**CAPEX:** EUR {capex.get('total',{}).get('central_eur_m',0):.0f}M "
    f"(range EUR {capex.get('total',{}).get('p10_eur_m',0):.0f}M -- EUR {capex.get('total',{}).get('p90_eur_m',0):.0f}M). "
    f"Confidence: {capex.get('weighted_confidence_label','')}.")
findings.append(f"**LCOH:** EUR {lcoh.get('central_eur_per_kg',0):.2f}/kg "
    f"(P10-P90: EUR {lcoh.get('p10_eur_per_kg',0):.2f}--{lcoh.get('p90_eur_per_kg',0):.2f}/kg). "
    f"Dominant driver: **{lcoh.get('dominant_driver','').replace('_',' ')}**.")
for f in findings:
    st.markdown(f"-  {f}")

st.divider()

# Knowledge gaps
st.subheader("Knowledge Gaps")
for g in pm.get("critical_gaps", []):
    st.error(f"CRITICAL: {g}")
for g in pm.get("important_gaps", []):
    st.warning(f"IMPORTANT: {g}")
if not pm.get("critical_gaps") and not pm.get("important_gaps"):
    st.success("No significant knowledge gaps identified.")

st.divider()

# Conditions
if pm.get("conditions"):
    st.subheader("Conditions for Advancement")
    for i, c in enumerate(pm.get("conditions", []), 1):
        st.markdown(f"{i}.  {c}")

st.divider()

# Export
col_exp, _ = st.columns([1, 3])
with col_exp:
    html_report = generate_html_report(
        st.session_state.get("query", {}),
        st.session_state["report"]
    )
    st.download_button(
        label="Export PDF Report",
        data=html_report,
        file_name=f"h2_feasibility_report_{st.session_state.get('current_assessment_id','')}.html",
        mime="text/html",
        type="primary",
    )
    st.caption("Open in browser and print to PDF (Ctrl+P / Cmd+P)")

st.divider()
st.caption(f"Assessment ID: {st.session_state.get('current_assessment_id','-')} | Copilot Engine v1.0 | "
    f"Generated {st.session_state.get('current_assessment_id','')[:14] if st.session_state.get('current_assessment_id') else '-'}")
