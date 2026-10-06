# This module queries open REST APIs (e.g., Football-Data.org) to retrieve fixture lists,
# team standings, and match results, storing raw JSON responses in data/raw/.

import json
import logging
from pathlib import Path

import requests

from config.settings import (
    FOOTBALL_DATA_BASE_URL,
    FOOTBALL_DATA_API_KEY,
    FEATURED_COMPETITIONS,
    RAW_DATA_DIR,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FootballDataIngestor:
    def __init__(self, api_key: str = FOOTBALL_DATA_API_KEY):
        self.headers = {"X-Auth-Token": api_key} if api_key else {}
        self.base_url = FOOTBALL_DATA_BASE_URL

    def fetch_matches(self, competition_code: str = "PL") -> dict:
        """Fetch fixture and match result data for a given competition."""
        url = f"{self.base_url}/competitions/{competition_code}/matches"
        logging.info(f"Fetching matches from REST API: {url}")
        
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch match data: {e}")
            return {}

    def fetch_teams(self, competition_code: str) -> dict:
        """Fetch the participating teams for one competition."""
        url = f"{self.base_url}/competitions/{competition_code}/teams"
        logging.info("Fetching teams from REST API: %s", url)
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        if not isinstance(data, dict) or not isinstance(data.get("teams"), list):
            raise ValueError(
                f"Team response for {competition_code} has no teams list"
            )
        return data

    def fetch_featured_teams(self) -> tuple[dict[str, dict], dict[str, str]]:
        """Fetch team rosters for the five major leagues and Champions League."""
        payloads = {}
        errors = {}
        for code in FEATURED_COMPETITIONS:
            try:
                payloads[code] = self.fetch_teams(code)
            except (requests.exceptions.RequestException, ValueError) as exc:
                errors[code] = str(exc)
                logging.error("Failed to fetch teams for %s: %s", code, exc)
        return payloads, errors

    def save_raw_json(self, data: dict, filename: str) -> Path:
        """Save raw dictionary payload to data/raw directory."""
        output_path = RAW_DATA_DIR / filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved raw JSON payload to {output_path}")
        return output_path

if __name__ == "__main__":
    ingestor = FootballDataIngestor()
    matches_payload = ingestor.fetch_matches()
    if matches_payload:
        ingestor.save_raw_json(matches_payload, "raw_pl_matches.json")

    team_payloads, team_errors = ingestor.fetch_featured_teams()
    for competition_code, teams_payload in team_payloads.items():
        filename = f"raw_{competition_code.lower()}_teams.json"
        ingestor.save_raw_json(teams_payload, filename)
    if team_errors:
        logging.error("Some competition teams could not be fetched: %s", team_errors)