from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


def register_model(
    model_name,
    version,
    model_type,
    target,
    features,
    metrics,
    model_path,
    status="production"
):
    
    client = MongoClient(os.getenv("MONGO_URI"))
    collection = client["aqi_model_registry"]["models"]

    doc = {
        "model_name": model_name,
        "version": version,
        "model_type": model_type,
        "target": target,
        "features": features,
        "metrics": metrics,
        "model_path": model_path,
        "status": status,
        "created_at": datetime.utcnow()
    }

    collection.insert_one(doc)
    print("✅ Model registered successfully")

