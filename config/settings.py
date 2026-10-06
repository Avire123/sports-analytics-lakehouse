# This file sets up workspace paths, raw storage targets, and API endpoints.

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
DELTA_DATA_DIR = DATA_DIR / 'delta'

# Ensure directories exist
for path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, DELTA_DATA_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Data Source Config
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY", "")
FOOTBALL_DATA_BASE_URL = "https://api.football-data.org/v4"

# European competitions available in football-data.org.
FEATURED_COMPETITIONS = {
    "PL": "Premier League",
    "PD": "La Liga",
    "BL1": "Bundesliga",
    "SA": "Serie A",
    "FL1": "Ligue 1",
    "CL": "UEFA Champions League",
}