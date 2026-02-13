import requests
import pandas as pd
import os

# --------------------
# CONFIG
# --------------------
LAT = 24.8607     # Karachi
LON = 67.0011

START_DATE = "2025-06-01"
END_DATE = "2026-01-20"

OUTPUT_DIR = "data/historical"
OUTPUT_FILE = f"{OUTPUT_DIR}/openmeteo_weather.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------
# API CALL
# --------------------
url = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "daily": [
        "temperature_2m_mean",
        "relative_humidity_2m_mean",
        "windspeed_10m_mean",
        "rain_sum",
        "surface_pressure_mean"
    ],
    "timezone": "UTC"
}

print("Fetching Open-Meteo historical weather...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()["daily"]

df = pd.DataFrame({
    "date": data["time"],
    "temperature": data["temperature_2m_mean"],
    "humidity": data["relative_humidity_2m_mean"],
    "wind_speed": data["windspeed_10m_mean"],
    "rain": data["rain_sum"],
    "pressure": data["surface_pressure_mean"]
})

df.to_csv(OUTPUT_FILE, index=False)

print(f"Saved {len(df)} rows to {OUTPUT_FILE}")
