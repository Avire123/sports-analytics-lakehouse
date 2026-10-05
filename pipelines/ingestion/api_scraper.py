# This module queries open REST APIs (e.g., Football-Data.org) to retrieve fixture lists, team standings, and match results, storing raw JSON responses in data/raw/.

import json
import logging
import requests
from pathlib import Path
from config.settings import FOOTBALL_DATA_BASE_URL, FOOTBALL_DATA_API_KEY, RAW_DATA_DIR

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

    def save_raw_json(self, data: dict, filename: str) -> Path:
        """Save raw dictionary payload to data/raw directory."""
        output_path = RAW_DATA_DIR / filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"Saved raw JSON payload to {output_path}")
        return output_path

if __name__ == "__main__":
    ingestor = FootballDataIngestor()
    matches_payload = ingestor.fetch_matches(competition_code="PL")
    if matches_payload:
        ingestor.save_raw_json(matches_payload, "raw_pl_matches.json")