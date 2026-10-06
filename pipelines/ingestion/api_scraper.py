# This module queries open REST APIs (e.g., Football-Data.org) to retrieve fixture lists,
# team standings, and match results, storing raw JSON responses in data/raw/.

import json
import logging
import re
import requests
from pathlib import Path
from config.settings import (
    FOOTBALL_DATA_BASE_URL,
    FOOTBALL_DATA_API_KEY,
    RAW_DATA_DIR,
    UEFA_AREA_CODES,
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

    def fetch_european_competitions(self) -> list[dict]:
        """Return available catalogued domestic leagues in UEFA member areas."""
        url = f"{self.base_url}/competitions"
        logging.info("Fetching available competitions from REST API: %s", url)
        response = requests.get(url, headers=self.headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        competitions = data.get("competitions")
        if not isinstance(competitions, list):
            raise ValueError("Competition catalog response has no competitions list")

        selected = []
        for competition in competitions:
            if not isinstance(competition, dict):
                continue

            code = competition.get("code")
            area = competition.get("area") or {}
            is_european_league = (
                competition.get("type") == "LEAGUE"
                and isinstance(area, dict)
                and area.get("code") in UEFA_AREA_CODES
            )
            if code == "CL" or is_european_league:
                selected.append(competition)

        return selected

    def fetch_european_matches(self) -> dict[str, dict]:
        """Fetch matches for catalogued European leagues and the Champions League."""
        competitions = self.fetch_european_competitions()
        codes = {
            competition["code"]
            for competition in competitions
            if isinstance(competition.get("code"), str)
            and re.fullmatch(r"[A-Z0-9]{2,8}", competition["code"])
        }
        codes.add("CL")

        payloads = {}
        for code in sorted(codes):
            payload = self.fetch_matches(competition_code=code)
            if payload:
                payloads[code] = payload
            else:
                logging.error("No match data retrieved for competition %s", code)
        return payloads

    def save_raw_json(self, data: dict, filename: str) -> Path:
        """Save raw dictionary payload to data/raw directory."""
        output_path = RAW_DATA_DIR / filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved raw JSON payload to {output_path}")
        return output_path

if __name__ == "__main__":
    ingestor = FootballDataIngestor()
    european_matches = ingestor.fetch_european_matches()
    for competition_code, matches_payload in european_matches.items():
        filename = f"raw_{competition_code.lower()}_matches.json"
        ingestor.save_raw_json(matches_payload, filename)