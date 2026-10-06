import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

from app.components.european_teams import load_featured_teams
from config.settings import FEATURED_COMPETITIONS


def render_team_trends():
    st.header("📈 Team Performance & Form Trends")
    st.caption(
        "Choose clubs from the Premier League, La Liga, Bundesliga, Serie A, "
        "and Ligue 1. The trend values are illustrative until match results "
        "are connected."
    )

    rows, missing_codes = load_featured_teams()
    domestic_competitions = {
        name for code, name in FEATURED_COMPETITIONS.items() if code != "CL"
    }
    clubs = {
        f"{row['Team']} ({row['Competition']})": row["Team"]
        for row in rows
        if row["Competition"] in domestic_competitions
    }

    if missing_codes:
        domestic_missing = [
            FEATURED_COMPETITIONS[code]
            for code in missing_codes
            if code in FEATURED_COMPETITIONS and code != "CL"
        ]
        if domestic_missing:
            st.info(
                "Download the five domestic-league rosters from the "
                "**European Club Teams** view to populate club choices."
            )

    if not clubs:
        st.warning("No top-five-league team rosters are available yet.")
        return

    team_options = sorted(clubs)
    preferred_defaults = [
        label for label in team_options
        if clubs[label] in {"Arsenal", "Real Madrid"}
    ]
    default_teams = preferred_defaults[:2] or team_options[:2]
    selected_teams = st.multiselect(
        "Select clubs to compare",
        team_options,
        default=default_teams,
    )
    if not selected_teams:
        st.info("Select at least one club to display the form chart.")
        return

    gameweeks = list(range(1, 21))
    data = []
    for team_label in selected_teams:
        rng = np.random.default_rng(sum(ord(character) for character in team_label))
        cumulative_points = np.cumsum(
            rng.choice([3, 1, 0], size=20, p=[0.6, 0.25, 0.15])
        )
        for gw, pts in zip(gameweeks, cumulative_points):
            data.append({"Gameweek": gw, "Points": pts, "Team": team_label})

    df = pd.DataFrame(data)

    fig = px.line(
        df,
        x="Gameweek",
        y="Points",
        color="Team",
        title="Cumulative Points Trajectory over Season",
        markers=True
    )

    st.plotly_chart(fig, width="stretch")