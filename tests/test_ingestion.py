import unittest
from unittest.mock import Mock, patch

from pipelines.ingestion.api_scraper import FootballDataIngestor


class FootballDataIngestorTests(unittest.TestCase):
    @staticmethod
    def response(payload):
        response = Mock()
        response.json.return_value = payload
        response.raise_for_status.return_value = None
        return response

    @patch("pipelines.ingestion.api_scraper.requests.get")
    def test_fetch_european_matches_includes_catalogued_leagues_and_champions_league(
        self, get
    ):
        get.side_effect = [
            self.response({
                "competitions": [
                    {"code": "PL", "type": "LEAGUE", "area": {"code": "ENG"}},
                    {"code": "PD", "type": "LEAGUE", "area": {"code": "ESP"}},
                    {"code": "BSA", "type": "LEAGUE", "area": {"code": "BRA"}},
                    {"code": "DFB", "type": "CUP", "area": {"code": "GER"}},
                ],
            }),
            self.response({"competition": {"code": "CL"}, "matches": []}),
            self.response({"competition": {"code": "PD"}, "matches": []}),
            self.response({"competition": {"code": "PL"}, "matches": []}),
        ]

        payloads = FootballDataIngestor().fetch_european_matches()

        self.assertEqual(set(payloads), {"CL", "PD", "PL"})
        self.assertEqual(get.call_count, 4)
        requested_urls = {call.args[0] for call in get.call_args_list}
        self.assertIn(
            "https://api.football-data.org/v4/competitions/CL/matches",
            requested_urls,
        )
        self.assertNotIn(
            "https://api.football-data.org/v4/competitions/BSA/matches",
            requested_urls,
        )

    @patch("pipelines.ingestion.api_scraper.requests.get")
    def test_invalid_competition_catalog_is_reported(self, get):
        get.return_value = self.response({"competitions": None})

        with self.assertRaises(ValueError):
            FootballDataIngestor().fetch_european_competitions()


if __name__ == "__main__":
    unittest.main()