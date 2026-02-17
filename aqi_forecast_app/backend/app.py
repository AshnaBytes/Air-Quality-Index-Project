import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(
    title="AQI Forecast API",
    description="Predict AQI for today and next 3 days",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # lock this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from inference.predict_next_3_days import predict_next_3_days

@app.get("/predict")
def predict():
    """
    Returns:
    {
        today: { date, aqi },
        model,
        version,
        forecast: [
            { date, aqi },
            { date, aqi },
            { date, aqi }
        ]
    }
    """
    try:
        return predict_next_3_days()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "aqi-forecast-backend"
    }
