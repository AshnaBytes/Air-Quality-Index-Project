import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv

from feature_pipeline.build_features import apply_feature_engineering

load_dotenv()

LAT = 24.8607
LON = 67.0011

WEATHER_URL = "https://archive-api.open-meteo.com/v1/archive"
AQI_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

client = MongoClient(os.getenv("MONGO_URI"))
collection = client[os.getenv("MONGO_DB")][os.getenv("MONGO_COLLECTION")]


# ------------------------------------------------
# Get last stored feature date
# ------------------------------------------------
def get_last_feature_date():
    doc = collection.find_one(sort=[("date", -1)])
    if doc:
        return pd.to_datetime(doc["date"])
    return None



def run_feature_pipeline():

    last_date = get_last_feature_date()

    if last_date is None:
        raise ValueError("❌ No historical data found. Run backfill first.")
    
    
    # Sliding window context for feature engineering
   
    FEATURE_CONTEXT_DAYS = 45

    context_start_date = (last_date - timedelta(days=FEATURE_CONTEXT_DAYS))
    
    start_date = context_start_date.strftime("%Y-%m-%d")
    end_date = datetime.utcnow().strftime("%Y-%m-%d")

    if start_date > end_date:
        print("✅ No new data available")
        return

    print(f"📅 Fetching data from {start_date} to {end_date}")

    
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

    weather_resp = requests.get(WEATHER_URL, params=weather_params)
    weather_resp.raise_for_status()
    weather_data = weather_resp.json()["daily"]

    weather_df = pd.DataFrame({
        "date": weather_data["time"],
        "temperature": weather_data["temperature_2m_mean"],
        "humidity": weather_data["relative_humidity_2m_mean"],
        "wind_speed": weather_data["windspeed_10m_mean"],
        "rain": weather_data["rain_sum"],
        "pressure": weather_data["surface_pressure_mean"]
    })

    weather_df["date"] = pd.to_datetime(weather_df["date"])

    
    aqi_params = {
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

    aqi_resp = requests.get(AQI_URL, params=aqi_params)
    aqi_resp.raise_for_status()
    aqi_data = aqi_resp.json()["hourly"]

    aqi_df = pd.DataFrame({
    "datetime": aqi_data["time"],
    "pm25": aqi_data["pm2_5"],
    "pm10": aqi_data["pm10"],
    "no2": aqi_data["nitrogen_dioxide"],
    "o3": aqi_data["ozone"],
    "so2": aqi_data["sulphur_dioxide"]
    })


    aqi_df["datetime"] = pd.to_datetime(aqi_df["datetime"])
    aqi_df["date"] = aqi_df["datetime"].dt.floor("D")
    
    aqi_df = (
    aqi_df
    .groupby("date", as_index=False)
    .agg({
        "pm25": "mean",
        "pm10": "mean",
        "no2": "mean",
        "o3": "mean",
        "so2": "mean"
    })
    )


    # ==================================================
    # 3️⃣ MERGE RAW DATA
    # ==================================================
    df_new_raw = weather_df.merge(aqi_df, on="date", how="inner")

    if df_new_raw.empty:
        print("⚠️ No merged raw data available.")
        return

    # ==================================================
    # 5️⃣ FEATURE ENGINEERING
    # ==================================================
    combined_df = df_new_raw.sort_values("date").copy()

    combined_df = apply_feature_engineering(combined_df)

    # ==================================================
    # 6️⃣ KEEP ONLY NEW DATES
    # ==================================================
    # Only keep rows newer than last stored feature date
    df_final = combined_df[combined_df["date"] > last_date]


    print("Weather rows:", len(weather_df))
    print("AQI rows:", len(aqi_df))
    print("Merged raw rows:", len(df_new_raw))
    print("Rows after feature engineering:", len(combined_df))
    print("Final new rows to insert:", len(df_final))

    if df_final.empty:
        print("⚠️ No new rows after feature engineering.")
        return

    # ==================================================
    # 7️⃣ UPSERT INTO MONGODB
    # ==================================================
    inserted = 0

    for record in df_final.to_dict("records"):
        result = collection.update_one(
            {"date": record["date"]},
            {"$set": record},
            upsert=True
        )

        if result.upserted_id:
            inserted += 1

    print(f"✅ Feature pipeline ran successfully | New rows inserted: {inserted}")


if __name__ == "__main__":
    run_feature_pipeline()
