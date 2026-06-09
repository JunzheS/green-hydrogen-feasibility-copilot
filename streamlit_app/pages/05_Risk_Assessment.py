"""Page 5 -- Risk Assessment with consequences and intelligence."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
risk = report.get("risk_assessment", {})
consequences = report.get("risk_consequences", [])
top = risk.get("top_risks", [])

st.title("Risk Assessment")
st.caption(f"{risk.get('total_filtered',0)} risks filtered from library of 30 | {len(consequences)} with consequence analysis")

# Class distribution
counts = risk.get("risk_count_by_class", {})
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Critical", counts.get("critical", 0))
with col2: st.metric("High", counts.get("high", 0))
with col3: st.metric("Medium", counts.get("medium", 0))
with col4: st.metric("Low", counts.get("low", 0))

st.divider()

# Consequence-enhanced risk table
st.subheader("Risk Register with Consequence Analysis")
if consequences:
    rows = []
    for r in consequences:
        refs = r.get("reference_projects", [])
        rows.append({
            "Risk ID": r.get("risk_id", ""),
            "Risk": r.get("risk_name", "")[:65],
            "Class": r.get("risk_class", "").upper(),
            "RPN": r.get("rpn", 0),
            "Category": r.get("category", "").replace("_", " ").title(),
            "Mitigation": r.get("mitigation", "")[:80],
            "Reference Projects": ", ".join(refs[:3]) if refs else "-",
        })
    df = pd.DataFrame(rows)
    def color_class(v):
        cs = {"CRITICAL": "background:#C62828;color:white;font-weight:600",
              "HIGH": "background:#EF6C00;color:white;font-weight:600",
              "MEDIUM": "background:#F9A825;color:#1B5E20;font-weight:600",
              "LOW": "background:#2E7D32;color:white;font-weight:600"}
        return cs.get(v, "")
    st.dataframe(df.style.applymap(color_class, subset=["Class"]), use_container_width=True, hide_index=True)
else:
    st.dataframe(pd.DataFrame(top[:16]), use_container_width=True, hide_index=True)

st.divider()

# Detailed risk cards with consequence intelligence
st.subheader("Risk Deep Dive")
for r in (consequences if consequences else top[:8]):
    with st.expander(f"[{r.get('risk_class','').upper()}] {r.get('risk_id','')} -- {r.get('risk_name','')[:90]} (RPN: {r.get('rpn',0)})"):
        cat = r.get('category','').replace('_',' ').title()
        st.markdown(f"**Category:** {cat}")
        st.markdown(f"**P:** {r.get('probability',3)}/5 | **I:** {r.get('impact',3)}/5 | **D:** {r.get('detectability',3)}/5")
        st.markdown(f"**Description:** {r.get('description','')[:300]}")
        if r.get("mitigation"):
            st.markdown(f"**Mitigation:** {r['mitigation'][:250]}")
        refs = r.get("reference_projects", [])
        if refs:
            st.markdown(f"**Reference Projects:** {', '.join(refs[:4])}")
