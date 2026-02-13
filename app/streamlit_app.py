import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


from inference.predict_next_3_days import predict_next_3_days

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AQI Forecast",
    page_icon="🌫️",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
with open("app/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def aqi_category(aqi):
    if aqi <= 50:
        return "Good", "good"
    elif aqi <= 100:
        return "Moderate", "moderate"
    elif aqi <= 150:
        return "Unhealthy", "unhealthy"
    else:
        return "Hazardous", "hazardous"
    
def aqi_emoji(aqi):
    if aqi <= 50:
        return "🌤️"
    elif aqi <= 100:
        return "🌥️"
    elif aqi <= 150:
        return "🌫️"
    else:
        return "☠️"


# ---------------- HEADER ----------------
st.markdown("""
<div class="header-card">
    <h1>🌫️ Karachi Air Quality Forecast</h1>
    <p>AI-powered 3-day AQI prediction</p>
</div>
""", unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
data = predict_next_3_days()

today_aqi = data["aqi_today"]
today_label, today_class = aqi_category(today_aqi)

# ---------------- TODAY CARD ----------------
st.markdown(f"""
<div class="aqi-card {today_class}">
    <h2>Today</h2>
    <h1>{today_aqi:.1f}</h1>
    <p>{today_label}</p>
    <p>{data["date"]}</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- 3 DAY FORECAST ----------------
st.subheader("📅 Next 3 Days Forecast")

days = [
    ("Tomorrow", data["aqi_day_1"]),
    ("Day 2", data["aqi_day_2"]),
    ("Day 3", data["aqi_day_3"]),
]

cols = st.columns(3)
for col, (label, value) in zip(cols, days):
    cat, css = aqi_category(value)
    icon = aqi_emoji(value)
    with col:
        st.markdown(f"""
        <div class="aqi-card {css}">
            <h2>{icon}</h2>
            <h3>{label}</h3>
            <h1>{value:.1f}</h1>
            <p>{cat}</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------- HAZARD ALERT ----------------
max_aqi = max(today_aqi, data["aqi_day_1"], data["aqi_day_2"], data["aqi_day_3"])

if max_aqi > 150:
    st.markdown("""
    <div class="hazard-banner">
        🚨 Hazardous AQI Expected — Avoid Outdoor Activity
    </div>
    """, unsafe_allow_html=True)

# ---------------- TREND PLACEHOLDER ----------------
from pymongo import MongoClient
import os

def load_aqi_trend(days=30):
    mongo_uri = os.getenv("MONGO_URI")
    
    if not mongo_uri:
        st.warning("⚠️ MongoDB connection not configured. Using sample data from CSV.")
        try:
            df = pd.read_csv("data/historical/openmeteo_air_quality.csv")
            df["date"] = pd.to_datetime(df["date"])
            return df.sort_values("date").tail(days)
        except Exception as e:
            st.error(f"Could not load historical data: {e}")
            return pd.DataFrame()
    
    try:
        client = MongoClient(mongo_uri)
        collection = client["aqi_feature_store"]["aqi_features"]

        data = list(
            collection.find({}, {"_id": 0, "date": 1, "aqi": 1})
            .sort("date", -1)
            .limit(days)
        )

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        return df.sort_values("date")
    except Exception as e:
        st.error(f"MongoDB connection failed: {e}")
        return pd.DataFrame()



st.subheader("📈 AQI Trend")

trend_df = load_aqi_trend()

st.markdown("""
<p style="opacity:0.7">
Green: Good · Yellow: Moderate · Orange: Unhealthy · Red: Hazardous
</p>
""", unsafe_allow_html=True)


st.line_chart(
    trend_df.set_index("date")["aqi"],
    height=300
)


# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<p style="text-align:center;opacity:0.6">
Model: Random Forest · Target: AQI Δ 3 Days · Updated Automatically
</p>
""", unsafe_allow_html=True)

