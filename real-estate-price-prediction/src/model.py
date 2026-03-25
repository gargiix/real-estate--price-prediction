"""
model.py
Trains a Random Forest model on the real estate dataset and saves it.

Run this script once before starting the web app:
    python src/model.py
"""

import os
import sys
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error, r2_score

# Make sure we can import from src/
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import load_data, preprocess

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_data.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.joblib')
ENCODERS_PATH = os.path.join(os.path.dirname(__file__), '..', 'encoders.joblib')


def train():
    print("Loading data...")
    df = load_data(DATA_PATH)

    print(f"Dataset shape: {df.shape}")
    X, y, encoders = preprocess(df)

    # Split into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mape = mean_absolute_percentage_error(y_test, y_pred) * 100
    r2 = r2_score(y_test, y_pred)

    print(f"\n--- Model Performance ---")
    print(f"MAPE : {mape:.2f}%")
    print(f"R²   : {r2:.4f}")
    print(f"Benchmark from literature: 6.5–8.4% MAPE")

    # Save model and encoders
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)
    print(f"\nModel saved to: {MODEL_PATH}")
    print(f"Encoders saved to: {ENCODERS_PATH}")

    return model, encoders


if __name__ == '__main__':
    train()
