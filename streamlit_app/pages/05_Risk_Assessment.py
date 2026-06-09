"""Page 5 -- Risk Assessment with heatmap and category breakdown."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
risk = report.get("risk_assessment", {})

st.title("Risk Assessment")
st.caption(f"{risk.get('total_filtered',0)} risks filtered from library of 30")

counts = risk.get("risk_count_by_class", {})
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Critical", counts.get("critical", 0))
with col2: st.metric("High", counts.get("high", 0))
with col3: st.metric("Medium", counts.get("medium", 0))
with col4: st.metric("Low", counts.get("low", 0))

st.divider()

st.subheader("Top Risks by RPN")
top = risk.get("top_risks", [])
if top:
    rows = []
    for r in top[:16]:
        rows.append({
            "Risk": r["risk_name"][:80], "ID": r["risk_id"],
            "Category": r["category"].replace("_", " ").title(),
            "P": r["probability"], "I": r["impact"], "D": r["detectability"],
            "RPN": r["rpn"], "Class": r["risk_class"].upper(),
        })
    df = pd.DataFrame(rows)
    def color_class(v):
        cs = {"CRITICAL": "background:#C62828;color:white;font-weight:600",
              "HIGH": "background:#EF6C00;color:white;font-weight:600",
              "MEDIUM": "background:#F9A825;color:#1B5E20;font-weight:600",
              "LOW": "background:#2E7D32;color:white;font-weight:600"}
        return cs.get(v, "")
    st.dataframe(df.style.applymap(color_class, subset=["Class"]), use_container_width=True, hide_index=True)

st.divider()

st.subheader("Risks by Category")
by_cat = risk.get("risks_by_category", {})
if by_cat:
    cat_names, rpns = [], []
    for cn, rl in by_cat.items():
        if rl:
            cat_names.append(cn.replace("_", " ").title())
            rpns.append(max(r["rpn"] for r in rl))
    if cat_names:
        st.bar_chart(pd.DataFrame({"Category": cat_names, "Max RPN": rpns}).set_index("Category"))

st.subheader("Risk Details")
for r in top[:12]:
    with st.expander(f"[{r['risk_class'].upper()}] {r['risk_id']} -- {r['risk_name'][:90]} (RPN: {r['rpn']})"):
        st.markdown(f"**Category:** {r.get('category','').replace('_',' ').title()} > {r.get('subcategory','')}")
        st.markdown(f"**P:** {r.get('probability','')}/5 | **I:** {r.get('impact','')}/5 | **D:** {r.get('detectability','')}/5")
        st.markdown(f"**Description:** {r.get('description','')[:300]}")
        if r.get("mitigation"):
            st.markdown(f"**Mitigation:** {r['mitigation'][:250]}")
