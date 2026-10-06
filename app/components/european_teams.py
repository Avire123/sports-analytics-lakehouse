import json

import pandas as pd
import streamlit as st

from config.settings import FEATURED_COMPETITIONS, FOOTBALL_DATA_API_KEY, RAW_DATA_DIR
from pipelines.ingestion.api_scraper import FootballDataIngestor


def load_featured_teams() -> tuple[list[dict], list[str]]:
    """Load saved competition rosters and return team rows plus missing codes."""
    rows = []
    missing_codes = []

    for code, competition_name in FEATURED_COMPETITIONS.items():
        teams_path = RAW_DATA_DIR / f"raw_{code.lower()}_teams.json"
        if not teams_path.exists():
            missing_codes.append(code)
            continue

        with teams_path.open(encoding="utf-8") as file:
            payload = json.load(file)

        teams = payload.get("teams") if isinstance(payload, dict) else None
        if not isinstance(teams, list):
            raise ValueError(f"Team data in {teams_path} has no teams list")

        for team in teams:
            if not isinstance(team, dict) or not isinstance(team.get("name"), str):
                continue
            rows.append({
                "Competition": competition_name,
                "Team": team["name"],
                "Short name": team.get("shortName"),
                "Code": team.get("tla"),
                "Venue": team.get("venue"),
                "Founded": team.get("founded"),
            })

    return rows, missing_codes


def render_european_teams() -> None:
    st.header("European Club Teams")
    st.caption(
        "Team rosters for the Premier League, La Liga, Bundesliga, Serie A, "
        "Ligue 1, and UEFA Champions League."
    )

    if st.button("Refresh teams from Football-Data.org", type="primary"):
        if not FOOTBALL_DATA_API_KEY:
            st.error(
                "Set the FOOTBALL_DATA_API_KEY environment variable and restart "
                "the app before refreshing."
            )
        else:
            ingestor = FootballDataIngestor()
            with st.spinner("Fetching available competition teams..."):
                payloads, errors = ingestor.fetch_featured_teams()
                for code, payload in payloads.items():
                    ingestor.save_raw_json(payload, f"raw_{code.lower()}_teams.json")
            if payloads:
                st.success(f"Saved team lists for {len(payloads)} competitions.")
            for code, error in errors.items():
                st.warning(f"{FEATURED_COMPETITIONS[code]} ({code}): {error}")

    rows, missing_codes = load_featured_teams()
    if missing_codes:
        missing_names = ", ".join(
            f"{FEATURED_COMPETITIONS[code]} ({code})" for code in missing_codes
        )
        st.info(
            "Team data has not been downloaded for: "
            f"{missing_names}. Set FOOTBALL_DATA_API_KEY, then select "
            "'Refresh teams from Football-Data.org'. Access depends on your API plan."
        )

    if not rows:
        if not missing_codes:
            st.info("No teams were returned. Refresh the competition rosters to try again.")
        return

    teams = pd.DataFrame(rows)
    competition_options = ["All competitions", *FEATURED_COMPETITIONS.values()]
    selected_competition = st.selectbox("Competition", competition_options)
    search = st.text_input("Search teams").strip().casefold()

    filtered_teams = teams
    if selected_competition != "All competitions":
        filtered_teams = filtered_teams[
            filtered_teams["Competition"] == selected_competition
        ]
    if search:
        filtered_teams = filtered_teams[
            filtered_teams["Team"].str.casefold().str.contains(search, regex=False)
        ]

    team_metric, competition_metric = st.columns(2)
    team_metric.metric("Team entries", len(filtered_teams))
    competition_metric.metric(
        "Competitions shown", filtered_teams["Competition"].nunique()
    )
    if filtered_teams.empty:
        st.info("No teams match the selected competition and search.")
        return

    st.dataframe(
        filtered_teams.sort_values(["Competition", "Team"]),
        hide_index=True,
        use_container_width=True,
    )
