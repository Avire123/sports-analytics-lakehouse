import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render_team_trends():
    st.header("📈 Team Performance & Form Trends")
    
    # Generating mock rolling trend data
    gameweeks = list(range(1, 21))
    teams = ["Arsenal", "Manchester City", "Liverpool", "Aston Villa"]
    
    data = []
    for team in teams:
        cumulative_points = np.cumsum(np.random.choice([3, 1, 0], size=20, p=[0.6, 0.25, 0.15]))
        for gw, pts in zip(gameweeks, cumulative_points):
            data.append({"Gameweek": gw, "Points": pts, "Team": team})
            
    df = pd.DataFrame(data)
    
    selected_teams = st.multiselect("Select Teams to Compare", teams, default=["Arsenal", "Manchester City"])
    
    filtered_df = df[df["Team"].isin(selected_teams)]
    
    fig = px.line(
        filtered_df, 
        x="Gameweek", 
        y="Points", 
        color="Team",
        title="Cumulative Points Trajectory over Season",
        markers=True
    )
    
    st.plotly_chart(fig, use_container_width=True)