from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path

from feature_pipeline.load_features_mongodb import load_features
from utils.metrics import evaluate
from register_model.model_register import register_model

# Load data
X, y1, y2, y3 = load_features()

def train_for_target(y, label, version):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae, rmse, r2 = evaluate(f"XGB {label}", y_test, preds)

    Path("models").mkdir(exist_ok=True)
    model_path = f"models/xgboost_{label}.pkl"
    joblib.dump(model, model_path)



# 🔁 Train all horizons
train_for_target(y1, "aqi_t_plus_1", "v1")
train_for_target(y2, "aqi_t_plus_2", "v1")
train_for_target(y3, "aqi_t_plus_3", "v1")
