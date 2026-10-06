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

# Default League Targets (eg Premier League = PL)
DEFAULT_COMPETITION = "PL"
DEFAULT_SEASON = "2023"

# football-data.org area codes for UEFA member associations.
UEFA_AREA_CODES = frozenset({
    "ALB", "AND", "ARM", "AUT", "AZE", "BEL", "BIH", "BLR", "BUL",
    "CRO", "CYP", "CZE", "DEN", "ENG", "ESP", "EST", "FRO", "FIN",
    "FRA", "GEO", "GER", "GIB", "GRE", "HUN", "IRL", "ISL", "ISR",
    "ITA", "KAZ", "KOS", "LIE", "LTU", "LUX", "LVA", "MDA", "MKD",
    "MLT", "MNE", "NED", "NIR", "NOR", "POL", "POR", "ROU", "RUS",
    "SCO", "SMR", "SRB", "SVK", "SVN", "SWE", "SUI", "TUR", "UKR",
    "WAL",
})