"""Page 8 -- Assessment History."""
import streamlit as st
import pandas as pd
from utils.theme import apply_theme, apply_sidebar; apply_theme(); apply_sidebar()
import os

from utils.session import load_history, HISTORY_FILE

st.title("Assessment History")
st.caption("Previously run assessments stored locally.")

history = st.session_state.get("history", load_history())

if not history:
    st.info("No assessments yet. Run your first assessment from the **Project Input** page.")
    st.stop()

st.subheader(f"{len(history)} Assessment(s)")

rows = []
for h in history:
    q = h.get("query", {})
    rows.append({
        "ID": h.get("assessment_id", "-")[:18],
        "Date": h.get("date", "-"),
        "Country": q.get("country", "-"),
        "Tech": q.get("technology", "-"),
        "MW": q.get("capacity_mw", 0),
        "Industry": q.get("industry", "-"),
        "Gate": h.get("gate_outcome", "-"),
        "CAPEX (EUR M)": f"{h.get('capex_central_eur_m',0):.0f}",
        "LCOH (EUR/kg)": f"{h.get('lcoh_central_eur_per_kg',0):.2f}",
    })
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()

st.subheader("Reopen Previous Assessment")
ids = [h.get("assessment_id", "-") for h in history]
selected = st.selectbox("Select assessment to reload:", ids,
    format_func=lambda x: f"{x} - {next((h['date'] for h in history if h.get('assessment_id') == x), '')}")

if st.button("Load Selected Assessment", type="primary"):
    for h in history:
        if h.get("assessment_id") == selected:
            st.session_state["report"] = h.get("report", {})
            st.session_state["query"] = h.get("query", {})
            st.session_state["assessment_complete"] = True
            st.session_state["current_assessment_id"] = selected
            st.success(f"Loaded {selected}")
            st.rerun()

st.divider()

with st.expander("Manage History"):
    if st.button("Clear All History"):
        st.session_state["history"] = []
        if HISTORY_FILE.exists():
            os.remove(HISTORY_FILE)
        st.success("History cleared.")
        st.rerun()

st.caption(f"History stored in: {HISTORY_FILE}")
