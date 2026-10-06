import sys
from pathlib import Path

# Ensure root directory is in sys.path for internal imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from app.components.player_compare import render_player_comparison
from app.components.team_trends import render_team_trends
from app.components.predictor import render_match_predictor
from app.components.european_teams import render_european_teams

st.set_page_config(
    page_title="Sports Analytics & Performance Lakehouse",
    page_icon="⚽",
    layout="wide"
)

st.title("🏆 Multi-Source Sports Analytics & Performance Lakehouse")

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View",
    [
        "European Club Teams",
        "Team Performance Trends",
        "Player H2H Comparison",
        "Match Predictor",
    ]
)

if page == "European Club Teams":
    render_european_teams()
elif page == "Team Performance Trends":
    render_team_trends()
elif page == "Player H2H Comparison":
    render_player_comparison()
elif page == "Match Predictor":
    render_match_predictor()
    