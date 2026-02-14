import os
import pandas as pd


# --------------------
# PM2.5 → AQI function (CORE LOGIC)
# --------------------
def pm25_to_aqi(pm):
    if pm <= 12:
        return (50 / 12) * pm
    elif pm <= 35.4:
        return 50 + (pm - 12) * (50 / 23.4)
    elif pm <= 55.4:
        return 100 + (pm - 35.4) * (50 / 20)
    elif pm <= 150.4:
        return 150 + (pm - 55.4) * (100 / 95)
    else:
        return 300


# --------------------
# CORE FEATURE ENGINEERING (REUSABLE)
# --------------------
def apply_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("date")

    df["aqi"] = df["pm25"].apply(pm25_to_aqi)

    df["aqi_lag_1"] = df["aqi"].shift(1)
    df["aqi_lag_2"] = df["aqi"].shift(2)
    df["aqi_lag_3"] = df["aqi"].shift(3)

    df["aqi_change_rate"] = df["aqi"] - df["aqi_lag_1"]
    df["aqi_change_rate_3d"] = df["aqi"] - df["aqi_lag_3"]

    df["aqi_roll_3"] = df["aqi"].rolling(3).mean()
    df["aqi_roll_7"] = df["aqi"].rolling(7).mean()

    df["aqi_target_1d"] = df["aqi"].shift(-1)
    df["aqi_target_2d"] = df["aqi"].shift(-2)
    df["aqi_target_3d"] = df["aqi"].shift(-3)

    df["aqi_delta_3d"] = df["aqi_target_3d"] - df["aqi"]

    return df.dropna()


# --------------------
# CSV-BASED PIPELINE (UNCHANGED BEHAVIOR)
# --------------------
def build_features(
    weather_path: str = os.path.join("data", "historical", "openmeteo_weather.csv"),
    air_path: str = os.path.join("data", "historical", "openmeteo_air_quality.csv"),
    output_path: str = "aqi_features_v1.csv"
):
    weather = pd.read_csv(weather_path)
    air = pd.read_csv(air_path)

    weather["date"] = pd.to_datetime(weather["date"])
    air["date"] = pd.to_datetime(air["date"])

    df = weather.merge(air, on="date", how="inner")

    df = apply_feature_engineering(df)

    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    df = build_features()
    print("Feature engineering completed.")
    print("Shape:", df.shape)
