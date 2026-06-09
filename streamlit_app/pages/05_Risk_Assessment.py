"""Page 5 -- Risk Dashboard with consequence analysis and heatmap."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Run one from **Project Input**.")
    st.stop()

report = st.session_state["report"]
q = st.session_state.get("query", {})
risk = report.get("risk_assessment", {})
consequences = report.get("risk_consequences", [])
top = risk.get("top_risks", [])

st.title("Risk Dashboard")
st.caption(f"{q.get('capacity_mw','')} MW {q.get('technology','')} | {q.get('country','')} | {q.get('industry','')}")

# Risk class metrics
st.markdown("#### Risk Profile")
counts = risk.get("risk_count_by_class", {})
rc1, rc2, rc3, rc4 = st.columns(4)
with rc1: st.metric("Critical", counts.get("critical", 0), "requires executive attention")
with rc2: st.metric("High", counts.get("high", 0), "dedicated risk owner needed")
with rc3: st.metric("Medium", counts.get("medium", 0), "monthly monitoring")
with rc4: st.metric("Low", counts.get("low", 0), "standard tracking")

st.divider()

# Risk register with consequences
st.markdown("#### Risk Register")
if consequences:
    rows = []
    for r in consequences:
        refs = r.get("reference_projects", [])
        rows.append({
            "ID": r.get("risk_id",""), "Risk": r.get("risk_name","")[:55],
            "Class": r.get("risk_class","").upper(), "RPN": r.get("rpn",0),
            "Category": r.get("category","").replace("_"," ").title(),
            "Key Mitigation": r.get("mitigation","")[:70],
            "Evidence": ", ".join(refs[:3]) if refs else "-",
        })
    df = pd.DataFrame(rows)
    def color_class(v):
        cs = {"CRITICAL":"background:#C62828;color:white;font-weight:600",
              "HIGH":"background:#EF6C00;color:white;font-weight:600",
              "MEDIUM":"background:#F9A825;color:#1B5E20;font-weight:600",
              "LOW":"background:#2E7D32;color:white;font-weight:600"}
        return cs.get(v, "")
    st.dataframe(df.style.map(color_class, subset=["Class"]),
                 use_container_width=True, hide_index=True,
                 column_config={"RPN": st.column_config.NumberColumn(format="%d")})

st.divider()

# Category breakdown bar chart
st.markdown("#### Risk by Category")
by_cat = risk.get("risks_by_category", {})
if by_cat:
    rc_names, rpns = [], []
    for cn, rl in by_cat.items():
        if rl:
            rc_names.append(cn.replace("_"," ").title())
            rpns.append(max(r["rpn"] for r in rl))
    if rc_names:
        st.bar_chart(pd.DataFrame({"Category": rc_names, "Max RPN": rpns}).set_index("Category"),
                     use_container_width=True, height=250)

# Risk deep dive
st.markdown("#### Risk Details")
for r in (consequences if consequences else top[:12]):
    with st.expander(f"[{r.get('risk_class','').upper()}] {r.get('risk_id','')} -- {r.get('risk_name','')[:80]} (RPN: {r.get('rpn',0)})"):
        st.markdown(f"**Category:** {r.get('category','').replace('_',' ').title()}")
        st.markdown(f"**Description:** {r.get('description','')[:300]}")
        if r.get("mitigation"): st.markdown(f"**Mitigation:** {r['mitigation'][:250]}")
        refs = r.get("reference_projects", [])
        if refs: st.caption(f"Evidence: {', '.join(refs[:4])}")
