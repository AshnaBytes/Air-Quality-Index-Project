from pymongo import MongoClient
import pandas as pd
import os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

def load_features():

    client = MongoClient(os.getenv("MONGO_URI"))
    collection = client[os.getenv("MONGO_DB")][os.getenv("MONGO_COLLECTION")]

    data = list(collection.find({}, {"_id": 0}))
    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError("No data found in MongoDB")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    
    df = df.replace([np.inf, -np.inf], np.nan)


    df = df.dropna(subset=[
        "aqi_target_1d",
        "aqi_target_2d",
        "aqi_target_3d",
        "aqi_delta_3d"
    ])

    if df.empty:
        raise ValueError("No valid training rows after dropping NaN targets")


    y_1d = df["aqi_target_1d"]
    y_2d = df["aqi_target_2d"]
    y_3d = df["aqi_target_3d"]

    DROP_COLS = [
        "date",
        "aqi_target_1d",
        "aqi_target_2d",
        "aqi_target_3d",
        "aqi_delta_3d",
    ]

    X = df.drop(columns=[c for c in DROP_COLS if c in df.columns])


    X = X.dropna()

    # Align targets with X index (important)
    y_1d = y_1d.loc[X.index]
    y_2d = y_2d.loc[X.index]
    y_3d = y_3d.loc[X.index]

    return X, y_1d, y_2d, y_3d


if __name__ == "__main__":
    X, y1, y2, y3 = load_features()
    print(f"X shape: {X.shape}")
