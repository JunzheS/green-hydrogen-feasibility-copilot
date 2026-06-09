"""Green Hydrogen Project Feasibility Copilot — Streamlit Application."""
import streamlit as st

st.set_page_config(
    page_title="H2 Feasibility Copilot",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.session import init_session
from utils.theme import apply_theme

init_session()
apply_theme()

with st.sidebar:
    st.markdown("## H2 Feasibility Copilot")
    st.markdown("Green Hydrogen Pre-Feasibility Assessment")
    st.divider()

    if st.session_state.get("report"):
        report = st.session_state["report"]
        pm = report.get("pm_review", {})
        gate = pm.get("gate_outcome", "-")
        conf = pm.get("overall_confidence", {})
        gate_colors = {"PROCEED": "#2E7D32", "PROCEED WITH CAUTION": "#F9A825",
                       "DO NOT PROCEED": "#C62828", "INSUFFICIENT DATA": "#78909C"}
        st.markdown("**Current Assessment**")
        q = st.session_state.get("query", {})
        st.caption(f"{q.get('country','')} | {q.get('capacity_mw','')} MW | {q.get('technology','')}")
        gcolor = gate_colors.get(gate, "#78909C")
        st.markdown(f"<span style='background:{gcolor};padding:4px 12px;border-radius:4px;color:white;font-weight:600;font-size:0.85em;'>{gate}</span>", unsafe_allow_html=True)
        st.markdown(f"Confidence: {conf.get('label','-')} ({conf.get('score',0):.2f})")

    st.divider()
    st.caption("KB: 10 projects | 30 risks | 30 cost records")
    st.caption("Engine v1.0 | June 2026")

# ─── MAIN CONTENT ───
st.title("Green Hydrogen Project Feasibility Copilot")
st.markdown("<p style='color:#558B2F;font-size:1.05em;'>Pre-Feasibility Assessment for PEM and Alkaline Electrolysis Projects</p>", unsafe_allow_html=True)

if not st.session_state.get("assessment_complete"):
    # ─── Knowledge Base KPIs ───
    col_k1, col_k2, col_k3, col_k4, col_k5 = st.columns(5)
    with col_k1: st.metric("Projects", "10", "European references")
    with col_k2: st.metric("Risks", "30", "8 categories")
    with col_k3: st.metric("Cost Records", "30", "CAPEX benchmarks")
    with col_k4: st.metric("Technology Cards", "2", "PEM + Alkaline")
    with col_k5: st.metric("Tests", "35/35", "all passing")

    # ─── Welcome ───
    st.markdown("""
    <div style="background:#F1F8E9;padding:20px;border-radius:8px;border-left:4px solid #2E7D32;margin:16px 0;">
        <strong>Welcome.</strong> Enter your project parameters on the <strong>Project Input</strong> page
        and click <strong>Run Assessment</strong> to generate a complete pre-feasibility report.
    </div>
    """, unsafe_allow_html=True)

    # ─── About ───
    st.subheader("Why This Tool")
    st.markdown("""
    Pre-feasibility assessments for green hydrogen projects require weeks of manual research.
    This Copilot answers in seconds: What is a realistic CAPEX range? What are the top risks?
    How mature is this technology for my application? What reference projects exist?
    """)

    # ─── Workflow ───
    st.subheader("Assessment Workflow")
    wf_cols = st.columns(4)
    steps = [
        ("1. Input", "Enter 5 project parameters: country, industry, technology, capacity, COD"),
        ("2. Retrieve", "Matching against 10 European reference projects"),
        ("3. Assess", "Technology readiness, risks, CAPEX and LCOH"),
        ("4. Decide", "Gate decision with evidence traceability"),
    ]
    for i, (title, desc) in enumerate(steps):
        with wf_cols[i]:
            st.markdown(f"**{title}**")
            st.caption(desc)

    # ─── Example Output ───
    st.subheader("Example Output")
    st.code(
        "Gate: PROCEED WITH CAUTION\n"
        "CAPEX: EUR 150M (EUR 1,500/kW)\n"
        "LCOH: EUR 4.96/kg\n"
        "Top Reference: Normand'Hy (Score 0.81)\n"
        "Top Risk: Manufacturing Capacity (RPN 36)"
    )

    st.divider()
    st.caption("Navigate to **Project Input** in the sidebar to begin.")
