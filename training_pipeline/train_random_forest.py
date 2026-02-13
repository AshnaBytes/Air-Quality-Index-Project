from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib
from pathlib import Path
from feature_pipeline.load_features_mongodb import load_features
from utils.metrics import evaluate
from register_model.model_register import register_model

X, y1, y2, y3 = load_features()

def train_for_target(y, label, version):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    mae, rmse, r2  = evaluate(f"RF {label}", y_test, preds)

    Path("models").mkdir(exist_ok=True)
    model_path = f"models/random_forest_{label}.pkl"
    joblib.dump(model, model_path)


#  Train all horizons
train_for_target(y1, "aqi_t_plus_1", "v1")
train_for_target(y2, "aqi_t_plus_2", "v1")
train_for_target(y3, "aqi_t_plus_3", "v1")
