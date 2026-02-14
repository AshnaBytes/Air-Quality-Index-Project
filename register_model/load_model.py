from pymongo import MongoClient
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

def load_production_model(model_name):
    client = MongoClient(os.getenv("MONGO_URI"))
    collection = client["aqi_model_registry"]["models"]

    doc = collection.find_one(
        {"model_name": model_name, "status": "production"},
        sort=[("created_at", -1)]
    )

    if doc is None:
        raise ValueError("No production model found")

    model = joblib.load(doc["model_path"])
    return model, doc
