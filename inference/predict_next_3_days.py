import joblib
import pandas as pd
from pymongo import MongoClient
from pathlib import Path
import os
from dotenv import load_dotenv

from register_model.load_model import load_production_model

load_dotenv()

# -----------------------------
# Load latest feature row
# -----------------------------
def load_latest_features():
    client = MongoClient(os.getenv("MONGO_URI"))
    collection = client[os.getenv("MONGO_DB")][os.getenv("MONGO_COLLECTION")]

    data = list(
        collection.find({}, {"_id": 0})
        .sort("date", -1)
        .limit(1)
    )

    if not data:
        raise ValueError("No feature data found for inference")

    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    return df

from datetime import timedelta

def predict_next_3_days():

    df = load_latest_features()

    latest_date = df["date"].iloc[0]
    today_aqi = float(df["aqi"].iloc[0])

    DROP_COLS = [
        "date",
        "aqi_target_1d",
        "aqi_target_2d",
        "aqi_target_3d",
        "aqi_delta_1d",
        "aqi_delta_3d",
    ]

    X = df.drop(columns=[c for c in DROP_COLS if c in df.columns])

    # Load production model
    model, meta = load_production_model("rf_multi_aqi")

    preds = model.predict(X)[0]

    forecast = []
    for i in range(3):
        forecast.append({
            "date": (latest_date + timedelta(days=i + 1)).strftime("%Y-%m-%d"),
            "aqi": float(preds[i])
        })

    return {
        "today": {
            "date": latest_date.strftime("%Y-%m-%d"),
            "aqi": today_aqi
        },
        "model": meta["model_name"],
        "version": meta["version"],
        "forecast": forecast
    }



if __name__ == "__main__":
    preds = predict_next_3_days()

    print("\n📈 AQI Forecast\n")

    today = preds["today"]
    print(f"Today ({today['date']}): AQI {today['aqi']:.2f}\n")

    for item in preds["forecast"]:
        print(f"{item['date']}: AQI {item['aqi']:.2f}")
