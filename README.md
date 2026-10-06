# ⚽ Sports Analytics & Performance Lakehouse

Explore football data through a Streamlit dashboard built around European
competitions, team trends, and match predictions. The project brings together
an interactive app and data-ingestion and processing pipelines in one place.

## 🏆 Featured competitions

The **European Club Teams** dashboard view covers:

| Competition | Code |
| --- | --- |
| 🏴 Premier League | `PL` |
| 🇪🇸 La Liga | `PD` |
| 🇩🇪 Bundesliga | `BL1` |
| 🇮🇹 Serie A | `SA` |
| 🇫🇷 Ligue 1 | `FL1` |
| 🌍 UEFA Champions League | `CL` |

Browse the available club rosters, filter by competition, and search by team
name. Choose **Refresh teams from Football-Data.org** to fetch and save roster
data locally in `data/raw/`. Availability depends on your football-data.org API
plan.

## ✨ Explore the dashboard

- 🛡️ **European Club Teams** — browse teams across the five featured domestic
  leagues and the Champions League.
- 📈 **Team Performance Trends** — explore a sample cumulative-points chart for
  selected clubs.
- ⚔️ **Player H2H Comparison** — compare sample player metrics side by side.
- 🔮 **Match Predictor** — try a simple match-outcome estimate using adjustable
  team ratings.

> **Data note:** Team and player comparisons and the team-trends chart currently
> use sample or generated data. European club rosters are fetched from
> Football-Data.org when you refresh them; the dashboard does not yet calculate
> league standings from live match results.

## 🚀 Get started

### 1. Install dashboard dependencies

Use Python 3.10 or newer:

```powershell
python -m pip install streamlit pandas plotly numpy requests
```

### 2. Configure Football-Data.org access

Set your API key in PowerShell before launching the app:

```powershell
$env:FOOTBALL_DATA_API_KEY = "your-api-key"
```

This key is needed to download team rosters. Keep it private and do not commit
it to the repository.

### 3. Launch the dashboard

From the project root, run:

```powershell
streamlit run app/main.py
```

Open **European Club Teams**, then select **Refresh teams from
Football-Data.org**. Successfully fetched rosters are saved as competition JSON
files under `data/raw/` and remain available to the dashboard on later runs.
Some competitions may not be accessible on every API plan.

## 🧱 Project map

```text
app/                    Streamlit dashboard and views
config/settings.py      Data paths, API settings, featured competitions
pipelines/ingestion/    Football-Data.org and web ingestion
pipelines/processing/   Match-data transformation and team metrics
data/raw/               Downloaded raw payloads (local)
data/processed/         Processed outputs (local)
data/delta/             Delta Lake tables (local)
tests/                  Project tests
```

## 🧪 Run tests

```powershell
python -m unittest discover -s tests -v
```
