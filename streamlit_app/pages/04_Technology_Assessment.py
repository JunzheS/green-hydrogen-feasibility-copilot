"""Page 4 -- Technology Assessment."""
import streamlit as st
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})
tech = report.get("technology_assessment", {})

st.title("Technology Assessment")
st.caption(f"{query.get('technology','')} Electrolysis for {query.get('industry','')} at {query.get('capacity_mw','')} MW")

st.subheader("Technology Readiness")
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("TRL", f"{tech.get('trl','')}/9")
with col2: st.metric("Maturity", tech.get("commercial_maturity", "").replace("_", " ").title())
with col3: st.metric("Max Proven Scale", f"{tech.get('max_proven_mw','')} MW")
with col4: st.metric("Suitability", tech.get("application_suitability", "").upper())

st.info(tech.get("trl_rationale", ""))

st.subheader("Scale Assessment")
s = tech.get("scale_status", "unknown")
st.markdown(f"**Scale Status:** {'within proven range' if 'within' in s else 'at frontier' if 'frontier' in s else 'beyond proven range'}")
st.markdown(f"**FOAK for Application:** {'Yes' if tech.get('is_foak_for_application') else 'No'}")
st.caption(tech.get("scale_detail", ""))

st.subheader(f"Application: {query.get('industry','')}")
suit = tech.get("application_suitability", "medium")
su_color = {"high": "#2E7D32", "medium": "#F9A825", "low": "#C62828", "not_recommended": "#C62828"}
st.markdown(f"<span style='background:{su_color.get(suit,'#78909C')};padding:2px 10px;border-radius:4px;color:white;font-weight:600;'>{suit.upper()}</span>", unsafe_allow_html=True)
st.markdown(tech.get("application_rationale", ""))

st.subheader("Performance Characteristics")
for note in tech.get("performance_notes", []):
    st.markdown(f"-  {note}")

c1, c2 = st.columns(2)
with c1:
    st.subheader("Key Advantages")
    for a in tech.get("key_advantages", [])[:6]:
        st.markdown(f"-  {a}")
with c2:
    st.subheader("Key Limitations")
    for l in tech.get("key_limitations", [])[:6]:
        st.markdown(f"-  {l}")

st.divider()
st.caption(f"Source: {tech.get('technology_id','')} | Confidence: {tech.get('confidence','')}")
