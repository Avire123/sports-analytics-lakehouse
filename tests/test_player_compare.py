import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.components.player_compare import load_featured_players
from config.settings import FEATURED_COMPETITIONS


class PlayerComparisonTests(unittest.TestCase):
    def test_loads_player_profiles_from_saved_competition_squads(self):
        with tempfile.TemporaryDirectory() as directory:
            teams_path = Path(directory) / "raw_pl_teams.json"
            teams_path.write_text(
                json.dumps({
                    "teams": [{
                        "name": "Example FC",
                        "squad": [{
                            "name": "Example Player",
                            "position": "Midfielder",
                            "nationality": "Example",
                            "dateOfBirth": "2000-01-01",
                            "shirtNumber": 8,
                        }],
                    }]
                }),
                encoding="utf-8",
            )
            with patch(
                "app.components.player_compare.RAW_DATA_DIR",
                Path(directory),
            ):
                players, missing_codes = load_featured_players()

        self.assertEqual(len(players), 1)
        self.assertEqual(players[0]["Player"], "Example Player")
        self.assertEqual(players[0]["Club"], "Example FC")
        self.assertEqual(players[0]["Competition"], FEATURED_COMPETITIONS["PL"])
        self.assertEqual(players[0]["Position"], "Midfielder")
        self.assertEqual(len(missing_codes), len(FEATURED_COMPETITIONS) - 1)
        self.assertNotIn("PL", missing_codes)


if __name__ == "__main__":
    unittest.main()
