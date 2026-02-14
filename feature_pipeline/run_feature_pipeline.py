import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

from feature_pipeline.build_features import build_features

load_dotenv()

LAT = 24.8607
LON = 67.0011

client = MongoClient(os.getenv("MONGO_URI"))
collection = client[os.getenv("MONGO_DB")][os.getenv("MONGO_COLLECTION")]

# -----------------------------
# Get last stored date
# -----------------------------
def get_last_feature_date():
    doc = collection.find_one(sort=[("date", -1)])
    if doc:
        return pd.to_datetime(doc["date"])
    return None

# -----------------------------
# Main runner
# -----------------------------
def run_feature_pipeline():

    last_date = get_last_feature_date()

    if last_date is None:
        raise ValueError(
            "❌ No historical data found. Run backfill first."
        )

    start_date = (last_date + timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = datetime.utcnow().strftime("%Y-%m-%d")

    if start_date > end_date:
        print("✅ No new data available")
        return

    print(f"📅 Fetching data from {start_date} to {end_date}")

    # -----------------------------
    # AIR QUALITY API
    # -----------------------------
    air_url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    air_params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "pm2_5",
            "pm10",
            "nitrogen_dioxide",
            "ozone",
            "sulphur_dioxide"
        ],
        "timezone": "UTC"
    }

    air_resp = requests.get(air_url, params=air_params).json()
    air_df = pd.DataFrame({
        "date": air_resp["hourly"]["time"],
        "pm25": air_resp["hourly"]["pm2_5"]
    })
    air_df["date"] = pd.to_datetime(air_df["date"]).dt.date

    # -----------------------------
    # WEATHER API
    # -----------------------------
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": LAT,
        "longitude": LON,
        "start_date": start_date,
        "end_date": end_date,
        "daily": [
            "temperature_2m_mean",
            "relative_humidity_2m_mean",
            "windspeed_10m_mean",
            "rain_sum",
            "surface_pressure_mean"
        ],
        "timezone": "UTC"
    }

    weather_resp = requests.get(weather_url, params=weather_params).json()
    weather_df = pd.DataFrame({
        "date": weather_resp["daily"]["time"],
        "temperature": weather_resp["daily"]["temperature_2m_mean"],
        "humidity": weather_resp["daily"]["relative_humidity_2m_mean"],
        "windspeed": weather_resp["daily"]["windspeed_10m_mean"],
        "rain": weather_resp["daily"]["rain_sum"],
        "pressure": weather_resp["daily"]["surface_pressure_mean"]
    })
    weather_df["date"] = pd.to_datetime(weather_df["date"]).dt.date

    # -----------------------------
    # Save temp CSVs for build_features
    # -----------------------------
    os.makedirs("data/historical", exist_ok=True)
    air_df.to_csv("data/historical/openmeteo_air_quality.csv", index=False)
    weather_df.to_csv("data/historical/openmeteo_weather.csv", index=False)

    # -----------------------------
    # Build features
    # -----------------------------
    df = build_features(
        weather_path="data/historical/openmeteo_weather.csv",
        air_path="data/historical/openmeteo_air_quality.csv"
    )

    records = df.to_dict("records")
    if records:
        collection.insert_many(records)

    print(f"✅ Feature pipeline ran successfully | Rows inserted: {len(records)}")


if __name__ == "__main__":
    run_feature_pipeline()
