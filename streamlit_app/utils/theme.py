"""Shared theme CSS for consistent green energy styling across all pages."""
import streamlit as st


def apply_theme():
    """Inject the green energy theme CSS into the current page."""
    st.markdown("""
<style>
    .stApp { background: #FFFFFF; }
    h1, h2, h3 { color: #1B5E20; font-weight: 500; }
    p, li, .stMarkdown { color: #37474F; }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
    }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15); }
    section[data-testid="stSidebar"] .stCaption { color: #A5D6A7 !important; }

    [data-testid="stMetricValue"] { color: #2E7D32 !important; font-weight: 600; }
    [data-testid="stMetricLabel"] { color: #558B2F !important; }
    [data-testid="stMetricDelta"] { color: #1565C0 !important; }

    .stButton button {
        background: linear-gradient(135deg, #2E7D32, #388E3C);
        color: white !important; border: none; border-radius: 6px;
        font-weight: 500; padding: 8px 20px;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        box-shadow: 0 2px 8px rgba(46,125,50,0.3);
    }

    .stAlert { border-radius: 6px; border-left: 4px solid #2E7D32; }
    [data-testid="stInfo"] { background: #F1F8E9; color: #1B5E20; }
    hr { border-color: #E0E0E0; margin: 24px 0; }
    .stDataFrame { border: 1px solid #E8F5E9; border-radius: 6px; }

    .stTabs [data-baseweb="tab"] { border-radius: 6px 6px 0 0; color: #558B2F; }
    .stTabs [aria-selected="true"] { background: #F1F8E9 !important; color: #1B5E20 !important; }
</style>
""", unsafe_allow_html=True)
