# 🌫️ Karachi Air Quality Intelligence System

End-to-end Machine Learning system for forecasting 3-day Air Quality Index (AQI) using weather-driven features, automated pipelines, model registry, and a production-ready React dashboard.

# 📌 Overview

This project is a full-stack ML system that predicts the next 3 days of AQI for Karachi using historical weather data and engineered temporal features.

It combines:

Real-time weather ingestion

Feature engineering pipelines

Automated training & inference

Model versioning & registry

REST API backend

Modern React dashboard frontend

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

##🔹 Backend

Python

FastAPI

Scikit-learn

Pandas / NumPy

MongoDB

MLflow (Model Registry)

Hopsworks (Feature Store)

##🔹 Frontend

React (Vite)

Recharts

Glassmorphism UI

Responsive Layout

##🔹 Data Source

Open-Meteo API (Weather Data)

# ✨ Core Features

 3-Day AQI Forecast

 Weather-based feature engineering

 Automated inference pipeline

 Model versioning & registry

 AQI trend visualization

 Real-time dashboard updates

 Health advisory system (AQI-based alerts)

 Fully responsive UI

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

EDA Steps

Missing value analysis

Correlation matrix evaluation

Feature distribution visualization

Outlier detection

Time-series trend inspection

Seasonal AQI pattern analysis

Weather–AQI relationship exploration

Key Insights

Humidity and wind speed correlate with AQI fluctuations.

Rainfall temporarily reduces AQI.

Lag features were stronger predictors than raw values.

AQI shows strong temporal dependency → justified lag engineering.

Multi-output regression improved stability over single-target models.

EDA directly influenced feature selection and target design.

# 🤖 Model Training Strategy

Initial Approach:

Single-target regression

Improved Approach:

Multi-output regression (predicting 3 future AQI values simultaneously)

Why multi-output?

Reduced prediction drift

Better temporal consistency

Improved generalization stability

# 🔄 Pipeline Automation

This system simulates real ML production constraints:

Automated feature extraction

Strict feature schema enforcement

Target exclusion during inference

Correct feature ordering validation

Backfill mechanism for missing historical records

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
Frontend	Vercel
Backend	        Railway
Database	MongoDB Atlas

# 📚 Key Learnings

Importance of feature ordering consistency in ML pipelines

Managing schema vs stored data in feature stores

Handling inference-time target absence

Designing multi-output regression systems

Transitioning from rapid prototyping (Streamlit) to scalable frontend (React)

Debugging pipeline automation in distributed environments



# 🎯 Project Goal

To design a production-style ML forecasting system that integrates:

Data engineering

Feature engineering

Model lifecycle management

API serving

Frontend visualization

This project demonstrates practical ML system design beyond model training.

