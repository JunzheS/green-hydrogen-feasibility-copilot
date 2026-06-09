"""Green Hydrogen Project Feasibility Copilot — Streamlit Application.
Professional green-energy theme for project managers.
"""
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
    st.markdown("Green Hydrogen Pre-Feasibility")
    st.divider()

    st.divider()

    if st.session_state.get("report"):
        report = st.session_state["report"]
        pm = report.get("pm_review", {})
        gate = pm.get("gate_outcome", "-")
        conf = pm.get("overall_confidence", {})
        gate_colors = {
            "PROCEED": "#2E7D32", "PROCEED WITH CAUTION": "#F9A825",
            "DO NOT PROCEED": "#C62828", "INSUFFICIENT DATA": "#78909C"
        }
        st.markdown("**Current Assessment**")
        q = st.session_state.get("query", {})
        st.caption(f"{q.get('country','')} | {q.get('capacity_mw','')} MW | {q.get('technology','')}")
        gcolor = gate_colors.get(gate, "#78909C")
        st.markdown(
            f"<span style='background:{gcolor};padding:4px 12px;border-radius:4px;"
            f"color:white;font-weight:600;font-size:0.85em;'>{gate}</span>",
            unsafe_allow_html=True
        )
        st.markdown(f"Confidence: {conf.get('label','-')} ({conf.get('score',0):.2f})")

    st.divider()
    st.caption("KB: 10 projects | 30 risks | 30 cost records")
    st.caption("Engine v1.0 | June 2026")

st.title("Green Hydrogen Project Feasibility Copilot")
st.markdown(
    "<p style='color:#558B2F;font-size:1.05em;'>"
    "Pre-Feasibility Assessment for PEM and Alkaline Electrolysis Projects"
    "</p>", unsafe_allow_html=True
)

if not st.session_state.get("assessment_complete"):
    st.markdown("""
    <div style="background:#F1F8E9;padding:20px;border-radius:8px;border-left:4px solid #2E7D32;margin:20px 0;">
        <strong>Welcome.</strong> Enter your project parameters on the <strong>Project Input</strong> page
        and click <strong>Run Assessment</strong> to generate a complete pre-feasibility report.
        <br><br>
        The Copilot will analyze your project against a knowledge base of
        10 European green hydrogen reference projects, 30 validated risks,
        and industry-standard cost benchmarks.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Reference Projects", "10", "Gold Dataset v1")
    with col2:
        st.metric("Risk Library", "30 risks", "8 categories")
    with col3:
        st.metric("Cost Library", "30 records", "CAPEX + LCOH")

    st.divider()
    st.caption("Navigate using the sidebar links above.")
