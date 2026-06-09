"""Page 3 -- Reference Projects with score breakdown."""
import streamlit as st
import pandas as pd

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})
matching = report.get("similar_projects", {})
ranked = report.get("project_match_breakdown", [])
if not ranked:
    ranked = matching.get("ranked_projects", [])

st.title("Reference Projects")
st.caption(f"Top {len(ranked)} projects matching: {query.get('capacity_mw','')} MW {query.get('technology','')} in {query.get('country','')} for {query.get('industry','')}")

if ranked:
    rows = []
    for p in ranked:
        bd = p.get("score_breakdown", {})
        rows.append({
            "Rank": p.get("rank", 0),
            "Project": p.get("project_name", ""),
            "Country": p.get("country", ""),
            "MW": p.get("capacity_mw", 0),
            "Technology": p.get("technology", ""),
            "Status": p.get("status", "").replace("_", " ").title(),
            "Tech": bd.get("Technology", ""),
            "Industry": bd.get("Industry", ""),
            "Capacity": bd.get("Capacity", ""),
            "Country Score": bd.get("Country", ""),
            "Score": f"{p.get('composite_score',0):.2f}",
            "Tier": p.get("tier", ""),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()

st.subheader("Why Each Project Was Selected")
for p in ranked:
    with st.container(border=True):
        score = p.get("composite_score", 0)
        c = "#2E7D32" if score >= 0.70 else "#F9A825" if score >= 0.50 else "#C62828"
        bd = p.get("score_breakdown", {})

        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.markdown(f"**#{p.get('rank')} -- {p.get('project_name')}**")
            st.caption(f"{p.get('country','')} | {p.get('capacity_mw','')} MW {p.get('technology','')} | {p.get('status','').replace('_',' ').title()} | {p.get('offtake','').replace('_',' ').title()}")
        with col2:
            if bd:
                st.markdown("**Score breakdown:**")
                for dim, val in bd.items():
                    st.caption(f"  {dim}: {val}")
        with col3:
            st.markdown(f"<p style='font-size:2em;font-weight:700;color:{c};text-align:center;'>{score:.2f}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;font-size:0.85em;'>{p.get('tier','')}</p>", unsafe_allow_html=True)
        st.markdown(f"**Why selected:** {p.get('rationale','')[:300]}")
