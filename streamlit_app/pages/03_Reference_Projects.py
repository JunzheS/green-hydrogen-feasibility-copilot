"""Page 3 -- Reference Projects matching results."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme; apply_theme()

if not st.session_state.get("report"):
    st.warning("No assessment yet. Go to **Project Input** to run one.")
    st.stop()

report = st.session_state["report"]
query = st.session_state.get("query", {})
matching = report.get("similar_projects", {})
ranked = matching.get("ranked_projects", [])

st.title("Reference Projects")
st.caption(f"Top {len(ranked)} projects matching: {query.get('capacity_mw','')} MW {query.get('technology','')} in {query.get('country','')} for {query.get('industry','')}")

if ranked:
    rows = []
    for p in ranked:
        rows.append({
            "Rank": p["rank"], "Project": p["project_name"],
            "Country": p["country"], "MW": p["capacity_mw"],
            "Technology": p["technology"], "Status": p["status"].replace("_", " ").title(),
            "Offtake": p["primary_offtake"].replace("_", " ").title(),
            "Score": f"{p['composite_score']:.2f}", "Tier": p["tier"],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()

st.subheader("Why Each Project Was Selected")
for p in ranked:
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**#{p['rank']} -- {p['project_name']}**")
            st.caption(f"{p['country']} | {p['capacity_mw']} MW {p['technology']} | {p['status'].replace('_',' ').title()} | {p['primary_offtake'].replace('_',' ').title()}")
        with col2:
            score = p["composite_score"]
            c = "#2E7D32" if score >= 0.70 else "#F9A825" if score >= 0.50 else "#C62828"
            st.markdown(f"<p style='font-size:1.8em;font-weight:700;color:{c};text-align:center;'>{score:.2f}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center;font-size:0.85em;'>{p['tier']}</p>", unsafe_allow_html=True)
        st.markdown(f"**Why selected:** {p.get('rationale','')[:250]}")
