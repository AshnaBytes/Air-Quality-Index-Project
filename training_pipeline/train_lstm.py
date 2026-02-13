import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from feature_pipeline.load_features_mongodb import load_features
from utils.metrics import evaluate

# ----------------------
# Load and scale data
# ----------------------
X, y = load_features()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y.values, test_size=0.2, shuffle=False
)

# Convert to tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test  = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test  = torch.tensor(y_test, dtype=torch.float32)

# Add time dimension (samples, seq_len=1, features)
X_train = X_train.unsqueeze(1)
X_test  = X_test.unsqueeze(1)

# ----------------------
# LSTM Model
# ----------------------
class LSTMModel(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, 64, batch_first=True)
        self.fc = nn.Linear(64, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :]).squeeze()

model = LSTMModel(X_train.shape[2])
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# ----------------------
# Training loop
# ----------------------
for epoch in range(30):
    optimizer.zero_grad()
    preds = model(X_train)
    loss = criterion(preds, y_train)
    loss.backward()
    optimizer.step()

    if epoch % 5 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

# ----------------------
# Evaluation
# ----------------------
model.eval()
with torch.no_grad():
    preds = model(X_test).numpy()

mae, rmse, r2 = evaluate("PyTorch LSTM", y_test.numpy(), preds)
torch.save(model.state_dict(), "models/lstm_model.pth")
