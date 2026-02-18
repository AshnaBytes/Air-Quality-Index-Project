# 🌫️ Karachi Air Quality Intelligence System

End-to-end Machine Learning system for forecasting 3-day Air Quality Index (AQI) using weather-driven features, automated pipelines, model registry, and a production-ready React dashboard.

## 🚀 Live Demo

Frontend (Vercel):
https://air-quality-index-project-iqe8.vercel.app/

Backend API Docs (Railway):
https://air-quality-index-project-production.up.railway.app/docs

# 📌 Overview

This project is a full-stack ML system that predicts the next 3 days of AQI for Karachi using historical weather data and engineered temporal features.

It combines:

1. Real-time weather ingestion
2. Feature engineering pipelines
3. Automated training & inference
4. Model versioning & registry
5. REST API backend
6. Modern React dashboard frontend

The system is designed to simulate a production-grade ML pipeline, not just a notebook experiment.

# 🏗️ System Architecture

Open-Meteo API
        ↓
Historical Backfill
        ↓
Feature Engineering
        ↓
MongoDB Storage
        ↓
Model Training
        ↓
Model Registry (MLflow)
        ↓
Automated Inference Pipeline
        ↓
FastAPI Prediction API
        ↓
React Dashboard (Visualization)

# 🧠 Tech Stack

### Backend

Python
FastAPI
Scikit-learn
Pandas / NumPy
MongoDB
MLflow (Model Registry)
Hopsworks (Feature Store)

### Frontend

React (Vite)
Recharts
Glassmorphism UI
Responsive Layout

### Data Source

Open-Meteo API (Weather & AQI Data)

# ✨ Core Features

1. 3-Day AQI Forecast
2. Weather-based feature engineering
3. Automated inference pipeline
4. Model versioning & registry
5. AQI trend visualization
6. Real-time dashboard updates
7. Health advisory system (AQI-based alerts)
8. Fully responsive UI

# ⚙️ Feature Engineering

The model uses temporal and interaction-based features including:

Rolling averages
Lag features (time dependency modeling)
Humidity influence factors
Wind speed interactions
Pressure variation signals
Multi-output target engineering (Day+1, Day+2, Day+3)

Feature ordering consistency is strictly enforced during inference.

# 📊 Exploratory Data Analysis (EDA)

Before training, extensive EDA was performed to understand patterns and guide feature design.

## EDA Steps:

1. Missing value analysis
2. Correlation matrix evaluation
3. Feature distribution visualization
4. Seasonal AQI pattern analysis
5. Weather–AQI relationship exploration

## Key Insights

1. Humidity and wind speed correlate with AQI fluctuations.

2. Rainfall temporarily reduces AQI.

3. Lag features were stronger predictors than raw values.

4. AQI shows strong temporal dependency → justified lag engineering.

5. Multi-output regression improved stability over single-target models.

EDA directly influenced feature selection and target design.

# 🤖 Model Training Strategy

Initial Approach: Single-target regression

Improved Approach: Multi-output regression (predicting 3 future AQI values simultaneously)

Why multi-output?

Reduced prediction drift
Better temporal consistency
Improved generalization stability

# 🔄 Pipeline Automation

This system simulates real ML production constraints:

1. Automated feature extraction
2. Strict feature schema enforcement
3. Target exclusion during inference
4. Correct feature ordering validation
5. Backfill mechanism for missing historical records

# 🎨 Frontend Dashboard

 Built using React (transitioned from Streamlit).
 UI Features
 Animated gradient background
 Glassmorphism components
 AQI trend chart
 Environmental condition cards
 Health advisory panel
 Balanced two-panel SaaS layout

The dashboard transforms raw predictions into an intuitive decision-support interface.

# 🚀 Deployment

Frontend ---->  Vercel
Backend	 ---->  Railway
Database ---->	MongoDB Atlas

# 📚 Key Learnings

1. Importance of feature ordering consistency in ML pipelines

2. Managing schema vs stored data in feature stores

3. Handling inference-time target absence

4. Designing multi-output regression systems

5. Transitioning from rapid prototyping (Streamlit) to scalable frontend (React)

6. Debugging pipeline automation in distributed environments


# 🎯 Project Goal

To design a production-style ML forecasting system that integrates:

 Data engineering
 Feature engineering
 Model lifecycle management
 API serving
 Frontend visualization

This project demonstrates practical ML system design beyond model training.




