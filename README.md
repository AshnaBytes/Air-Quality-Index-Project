🌫️ Karachi Air Quality Forecasting System

An end-to-end machine learning system that forecasts the Air Quality Index (AQI) for the next 3 days using weather data, feature engineering, and automated pipelines.

This project integrates real-time weather data, feature engineering pipelines, model training, model registry, backend APIs, and a React frontend dashboard


🚀 Project Overview

This system:

. Fetches historical weather data from the Open-Meteo API

. Backfills missing historical records

. Performs feature engineering

. Stores processed data in MongoDB

. Trains machine learning models

. Registers models in a model registry

. Automates feature pipelines

. Serves predictions via backend API

. Displays results in a modern React dashboard

The goal is to predict AQI trends and provide a clean, real-time dashboard for visualization.


🏗️ Architecture

Open-Meteo API
        ↓
Data Backfill
        ↓
Feature Engineering
        ↓
MongoDB Storage
        ↓
Model Training
        ↓
Model Registry
        ↓
Feature Pipeline Automation
        ↓
Prediction API (Backend)
        ↓
React Frontend Dashboard


🧠 Technologies Used
--> Backend

. Python

. FastAPI

. Scikit-learn

. MongoDB

. Hopsworks (Feature Store)

. MLflow / Model Registry

. Pandas / NumPy

--> Frontend

. React (Vite)

. Recharts (Data Visualization)

. Modern Glassmorphism UI

--> APIs

Open-Meteo API (Weather Data)

📊 Features

.3-Day AQI Forecast

.Weather-based feature engineering

.Automated inference pipeline

.Model versioning & registry

.Interactive dashboard

.AQI trend visualization

.Today’s weather highlights

.Fully responsive UI



⚙️ Feature Engineering

Key engineered features include:

.Rolling averages

.Lag features

.Humidity influence

.Wind speed interactions

.Pressure variations

.Multi-output target engineering


🤖 Model Training

Initially trained using single-target regression, later shifted to multi-output regression for improved stability and performance.


📊 Exploratory Data Analysis (EDA)

Before model training, I performed detailed Exploratory Data Analysis to understand the structure and relationships within the data.

EDA Steps Included:

Checking missing values

Correlation analysis

Feature distribution visualization

Outlier detection

Trend analysis over time

AQI seasonal patterns

Weather feature impact exploration

Key Insights from EDA:

Humidity and wind speed showed noticeable correlation with AQI changes.

Rainfall had short-term impact in reducing AQI.

Certain lag features had stronger predictive value than raw features.

AQI showed temporal dependency, justifying lag-based feature engineering.

EDA helped guide feature engineering decisions and target design.



📊 Exploratory Data Analysis (EDA)

Before model training, I performed detailed Exploratory Data Analysis to understand the structure and relationships within the data.

EDA Steps Included:

.Checking missing values
.Correlation analysis
.Feature distribution visualization
.Outlier detection
.Trend analysis over time
.AQI seasonal patterns
.Weather feature impact exploration

Key Insights from EDA:

.Humidity and wind speed showed noticeable correlation with AQI changes.
.Rainfall had short-term impact in reducing AQI.
.Certain lag features had stronger predictive value than raw features.
.AQI showed temporal dependency, justifying lag-based feature engineering.
.EDA helped guide feature engineering decisions and target design.


🔄 Pipeline Automation

.Automated feature extraction
.Automated inference
.Correct feature ordering enforcement
.Target exclusion during inference


Frontend

. Built using React (first time switching from Streamlit)
. Animated gradient background
. Glassmorphism design
. Forecast + trend chart layout
. Responsive design


🚀 Deployment

Frontend: Vercel
Backend: Render


📌 Key Learnings

. Importance of feature ordering consistency

. Managing schema vs actual data in feature stores

. Handling inference-time missing targets

. Transitioning from Streamlit to React

. Debugging ML pipeline automation