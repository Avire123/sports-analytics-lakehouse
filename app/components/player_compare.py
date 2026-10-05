import streamlit as st
import pandas as pd

def render_player_comparison():
    st.header("⚔️ Player Head-to-Head Comparison")
    
    col1, col2 = st.columns(2)
    
    # Mock database for player metrics
    players_data = {
        "Erling Haaland": {"Goals": 27, "Assists": 5, "Shots on Target": 58, "Pass Accuracy %": 78.4, "Rating": 8.4},
        "Matheus Cunha": {"Goals": 18, "Assists": 10, "Shots on Target": 42, "Pass Accuracy %": 82.1, "Rating": 8.1},
        "Bukayo Saka": {"Goals": 14, "Assists": 11, "Shots on Target": 35, "Pass Accuracy %": 84.5, "Rating": 8.0},
        "Cole Palmer": {"Goals": 22, "Assists": 11, "Shots on Target": 49, "Pass Accuracy %": 81.0, "Rating": 8.2}
    }

    with col1:
        player_a = st.selectbox("Select Player A", list(player_data.keys()), index=0)
    with col2:
        player_b = st.selectbox("Select Player B", list(player_data.keys()), index=1)

    p1 = players_data[player_a]
    p2 = players_data[player_b]

    st.subheader(f"{player_a} vs {player_b}")

    # Render Comparison Grid
    for metric in ["Goals", "Assists", "Shots on Target", "Pass Accuracy %", "Rating"]:
        val_a = p1[metric]
        val_b = p2[metric]
        
        c1, c2, c3 = st.columns([2, 1, 2])
        c1.metric(label=f"{player_a} {metric}", value=val_a)
        c2.markdown(f"<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
        c3.metric(label=f"{player_b} {metric}", value=val_b)