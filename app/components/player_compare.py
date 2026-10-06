import json

import streamlit as st

from config.settings import FEATURED_COMPETITIONS, RAW_DATA_DIR


def load_featured_players() -> tuple[list[dict], list[str]]:
    """Load all player profiles available in saved featured-team squads."""
    players = []
    missing_codes = []

    for competition_code, competition_name in FEATURED_COMPETITIONS.items():
        teams_path = RAW_DATA_DIR / f"raw_{competition_code.lower()}_teams.json"
        if not teams_path.exists():
            missing_codes.append(competition_code)
            continue

        with teams_path.open(encoding="utf-8") as file:
            payload = json.load(file)

        teams = payload.get("teams") if isinstance(payload, dict) else None
        if not isinstance(teams, list):
            raise ValueError(f"Team data in {teams_path} has no teams list")

        competition_players = 0
        for team in teams:
            if not isinstance(team, dict):
                continue
            squad = team.get("squad")
            if not isinstance(squad, list):
                continue

            for player in squad:
                if not isinstance(player, dict) or not isinstance(player.get("name"), str):
                    continue
                players.append({
                    "Player": player["name"],
                    "Club": team.get("name", "Unknown club"),
                    "Competition": competition_name,
                    "Position": player.get("position") or "Not listed",
                    "Nationality": player.get("nationality") or "Not listed",
                    "Date of birth": player.get("dateOfBirth") or "Not listed",
                    "Shirt number": player.get("shirtNumber") or "Not listed",
                })
                competition_players += 1

        if competition_players == 0 and competition_code not in missing_codes:
            missing_codes.append(competition_code)

    return players, missing_codes


def render_player_comparison() -> None:
    st.header("⚔️ Player Head-to-Head Comparison")
    st.caption(
        "Compare player profiles from the five featured domestic leagues and "
        "the UEFA Champions League. Available players depend on your API plan "
        "and the squad data returned by Football-Data.org."
    )

    players, missing_codes = load_featured_players()
    if missing_codes:
        missing_names = ", ".join(
            FEATURED_COMPETITIONS[code] for code in missing_codes
        )
        st.info(
            f"Player squads are unavailable for: {missing_names}. Refresh team "
            "and squad data in the European Club Teams view."
        )

    if not players:
        st.warning(
            "No player squads are available yet. Open European Club Teams and "
            "refresh the competition rosters."
        )
        return

    player_options = {
        (
            f"{player['Player']} — {player['Club']} "
            f"({player['Competition']})"
        ): player
        for player in players
    }
    options = list(player_options)

    col1, col2 = st.columns(2)
    with col1:
        player_a_label = st.selectbox("Select Player A", options, index=0)
    with col2:
        player_b_label = st.selectbox(
            "Select Player B",
            options,
            index=min(1, len(options) - 1),
        )

    player_a = player_options[player_a_label]
    player_b = player_options[player_b_label]
    st.subheader(f"{player_a['Player']} vs {player_b['Player']}")

    st.dataframe(
        [
            {
                "Profile": label,
                "Club": player["Club"],
                "Competition": player["Competition"],
                "Position": player["Position"],
                "Nationality": player["Nationality"],
                "Date of birth": player["Date of birth"],
                "Shirt number": player["Shirt number"],
            }
            for label, player in (
                (player_a_label, player_a),
                (player_b_label, player_b),
            )
        ],
        hide_index=True,
    )
