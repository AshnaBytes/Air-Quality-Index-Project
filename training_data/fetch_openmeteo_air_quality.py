import requests
import pandas as pd
import os

# --------------------
# CONFIG
# --------------------
LAT = 24.8607   # Karachi
LON = 67.0011

START_DATE = "2025-06-01"
END_DATE   = "2026-01-20"

OUTPUT_DIR = "data/historical"
OUTPUT_FILE = f"{OUTPUT_DIR}/openmeteo_air_quality.csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------
# API CALL
# --------------------
url = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": LAT,
    "longitude": LON,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": [
        "pm2_5",
        "pm10",
        "nitrogen_dioxide",
        "ozone",
        "sulphur_dioxide"
    ],
    "timezone": "UTC"
}


print("Fetching Open-Meteo historical air quality...")

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()["hourly"]

# Create dataframe from hourly data
df = pd.DataFrame({
    "time": data["time"],
    "pm25": data["pm2_5"],
    "pm10": data["pm10"],
    "no2": data["nitrogen_dioxide"],
    "o3": data["ozone"],
    "so2": data["sulphur_dioxide"]
})

# Convert time to datetime
df["time"] = pd.to_datetime(df["time"])

# Extract date and aggregate to daily means
df["date"] = df["time"].dt.date
df_daily = df.groupby("date")[["pm25", "pm10", "no2", "o3", "so2"]].mean()
df_daily = df_daily.reset_index()

df_daily.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Saved {len(df_daily)} daily rows to {OUTPUT_FILE}")
