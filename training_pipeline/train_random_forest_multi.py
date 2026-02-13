import joblib
from pathlib import Path
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor

from feature_pipeline.load_features_mongodb import load_features
from utils.metrics import evaluate
from register_model.model_register import register_model


X, y1, y2, y3 = load_features()

Y = np.column_stack([y1, y2, y3])

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, shuffle=False
)


base_rf = RandomForestRegressor(
    n_estimators=400,
    max_depth=10,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)

model = MultiOutputRegressor(base_rf)
model.fit(X_train, Y_train)

preds = model.predict(X_test)


# Evaluation

labels = ["aqi_t_plus_1", "aqi_t_plus_2", "aqi_t_plus_3"]
metrics = {}

for i, label in enumerate(labels):
    mae, rmse, r2 = evaluate(
        f"RF MULTI {label}",
        Y_test[:, i],
        preds[:, i]
    )

    metrics[label] = {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2)
    }

    print(f"📊 {label}")
    print(f"   MAE : {mae:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    print(f"   R2  : {r2:.4f}")
    print("-" * 50)


# Save model

Path("models").mkdir(exist_ok=True)
model_path = "models/random_forest_multi_output.pkl"
joblib.dump(model, model_path)


# Register model in MongoDB


register_model(
    model_name="rf_multi_aqi",
    version="v1",
    model_type="RandomForestMultiOutput",
    target="aqi_t_plus_1, aqi_t_plus_2, aqi_t_plus_3",
    features=list(X.columns),
    metrics=metrics,
    model_path=model_path,
    status="production"
)

print("\n✅ Multi-output Random Forest saved and registered.")
