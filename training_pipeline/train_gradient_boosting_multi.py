import joblib
from pathlib import Path
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split

from feature_pipeline.load_features_mongodb import load_features
from utils.metrics import evaluate

# Load data
X, y1, y2, y3 = load_features()
Y = np.column_stack([y1, y2, y3])

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, shuffle=False
)

base_model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=4,
    random_state=42
)

model = MultiOutputRegressor(base_model)

model.fit(X_train, Y_train)
preds = model.predict(X_test)

labels = ["aqi_t_plus_1", "aqi_t_plus_2", "aqi_t_plus_3"]

print("\n========== MULTI-OUTPUT GRADIENT BOOSTING RESULTS ==========\n")

for i, label in enumerate(labels):
    mae, rmse, r2 = evaluate(
        f"GB MULTI {label}",
        Y_test[:, i],
        preds[:, i]
    )

    print(f"📊 {label}")
    print(f"   MAE : {mae:.4f}")
    print(f"   RMSE: {rmse:.4f}")
    print(f"   R2  : {r2:.4f}")
    print("-" * 50)

# Save
Path("models").mkdir(exist_ok=True)
joblib.dump(model, "models/gradient_boosting_multi.pkl")

print("\n✅ Multi-output Gradient Boosting trained and saved.")
