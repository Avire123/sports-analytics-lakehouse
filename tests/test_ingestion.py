import unittest
from unittest.mock import Mock, patch

import requests

from config.settings import FEATURED_COMPETITIONS
from pipelines.ingestion.api_scraper import FootballDataIngestor


class FootballDataIngestorTests(unittest.TestCase):
    @staticmethod
    def response(payload):
        response = Mock()
        response.json.return_value = payload
        response.raise_for_status.return_value = None
        return response

    @patch("pipelines.ingestion.api_scraper.requests.get")
    def test_fetches_teams_for_five_leagues_and_champions_league(self, get):
        get.side_effect = [
            self.response({"teams": [{"name": f"{code} Team"}]})
            for code in FEATURED_COMPETITIONS
        ]

        payloads, errors = FootballDataIngestor().fetch_featured_teams()

        self.assertEqual(set(payloads), set(FEATURED_COMPETITIONS))
        self.assertEqual(errors, {})
        self.assertEqual(get.call_count, 6)
        requested_urls = {call.args[0] for call in get.call_args_list}
        for code in FEATURED_COMPETITIONS:
            self.assertIn(
                f"https://api.football-data.org/v4/competitions/{code}/teams",
                requested_urls,
            )

    @patch("pipelines.ingestion.api_scraper.requests.get")
    def test_fetch_reports_unavailable_competitions_and_continues(self, get):
        get.side_effect = [
            requests.exceptions.HTTPError("forbidden"),
            *[
                self.response({"teams": [{"name": f"{code} Team"}]})
                for code in list(FEATURED_COMPETITIONS)[1:]
            ],
        ]

        payloads, errors = FootballDataIngestor().fetch_featured_teams()

        first_code = next(iter(FEATURED_COMPETITIONS))
        self.assertNotIn(first_code, payloads)
        self.assertEqual(errors, {first_code: "forbidden"})
        self.assertEqual(len(payloads), 5)

    @patch("pipelines.ingestion.api_scraper.requests.get")
    def test_invalid_team_payload_is_reported(self, get):
        get.return_value = self.response({"teams": None})

        with self.assertRaises(ValueError):
            FootballDataIngestor().fetch_teams("PL")


if __name__ == "__main__":
    unittest.main()
