# Sports Analytics Lakehouse

## European club teams

The Streamlit app's **European Club Teams** view lists teams from the Premier
League, La Liga, Bundesliga, Serie A, Ligue 1, and UEFA Champions League. It
loads rosters saved under `data/raw/`.

Set a football-data.org API key in the environment before starting the app:

```powershell
$env:FOOTBALL_DATA_API_KEY = "your-api-key"
streamlit run app/main.py
```

Select **Refresh teams from Football-Data.org** in the app to download and save
the available rosters. Competition access depends on the API account's plan.