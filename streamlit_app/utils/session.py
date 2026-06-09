"""Session state management for the Streamlit application."""
import json
import os
from datetime import datetime
from pathlib import Path

EXPORTS_DIR = Path(__file__).resolve().parent.parent / "exports"

HISTORY_FILE = EXPORTS_DIR / "assessment_history.json"


def init_session():
    import streamlit as st

    defaults = {
        "report": None,
        "query": None,
        "assessment_complete": False,
        "current_assessment_id": None,
        "history": load_history(),
        "current_page": "input",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []


def save_assessment(query: dict, report: dict) -> str:
    import streamlit as st

    aid = f"ASSESS-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    record = {
        "assessment_id": aid,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "query": {
            "country": query.get("country", ""),
            "industry": query.get("industry", ""),
            "technology": query.get("technology", ""),
            "capacity_mw": query.get("capacity_mw", 0),
            "target_cod": query.get("target_cod", 2029),
        },
        "gate_outcome": report.get("pm_review", {}).get("gate_outcome", "UNKNOWN"),
        "confidence": report.get("pm_review", {}).get("overall_confidence", {}).get("score", 0),
        "capex_central_eur_m": report.get("capex_assessment", {}).get("total", {}).get("central_eur_m", 0),
        "lcoh_central_eur_per_kg": report.get("lcoh_assessment", {}).get("central_eur_per_kg", 0),
        "report": report,
    }

    history = st.session_state.get("history", [])
    history.insert(0, record)
    st.session_state["history"] = history[:50]

    os.makedirs(EXPORTS_DIR, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, default=str, ensure_ascii=False)

    return aid


def run_engine(query: dict, electricity_price: float = 40, full_load_hours: int = 4500) -> dict:
    import sys
    ROOT = Path(__file__).resolve().parent.parent.parent
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from src.main import FeasibilityEngine
    engine = FeasibilityEngine()
    return engine.run(
        country=query["country"],
        industry=query["industry"],
        technology=query["technology"],
        capacity_mw=query["capacity_mw"],
        target_cod=query["target_cod"],
        electricity_price=electricity_price,
        full_load_hours=full_load_hours,
    )
