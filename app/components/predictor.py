import streamlit as st

def render_match_predictor():
    st.header("🔮 Match Outcome Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        home_team = st.text_input("Home Team", value="Arsenal")
        home_attack = st.slider("Home Team Attack Rating", 50, 99, 88)
        home_defense = st.slider("Home Team Defense Rating", 50, 99, 86)
        
    with col2:
        away_team = st.text_input("Away Team", value="Chelsea")
        away_attack = st.slider("Away Team Attack Rating", 50, 99, 82)
        away_defense = st.slider("Away Team Defense Rating", 50, 99, 79)
        
    if st.button("Predict Match Outcome", type="primary"):
        # Simple Poisson/heuristic calculation based on attack vs defense inputs
        home_score_exp = (home_attack / away_defense) * 1.4
        away_score_exp = (away_attack / home_defense) * 1.1
        
        home_win_prob = min(round((home_score_exp / (home_score_exp + away_score_exp)) * 100, 1), 90.0)
        away_win_prob = min(round((away_score_exp / (home_score_exp + away_score_exp)) * 100, 1), 90.0)
        draw_prob = round(100.0 - (home_win_prob + away_win_prob), 1)
        
        st.subheader("Match Probabilities")
        p1, p2, p3 = st.columns(3)
        p1.metric(f"{home_team} Win", f"{home_win_prob}%")
        p2.metric("Draw", f"{draw_prob}%")
        p3.metric(f"{away_team} Win", f"{away_win_prob}%")