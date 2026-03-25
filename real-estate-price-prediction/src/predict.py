"""
predict.py
Loads the saved model and encoders and runs predictions.
"""

import os
import joblib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from preprocess import preprocess_single

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model.joblib')
ENCODERS_PATH = os.path.join(os.path.dirname(__file__), '..', 'encoders.joblib')


def load_model():
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    return model, encoders


def predict_price(input_dict):
    """
    Predict price for a single property.
    
    input_dict keys:
        city, locality_tier, bhk, area_sqft,
        metro_dist_km, it_park_dist_km,
        rera_registered, ready_to_move, age_years
    
    Returns: predicted price in ₹ lakhs (float)
    """
    model, encoders = load_model()
    X = preprocess_single(input_dict, encoders)
    price = model.predict(X)[0]
    return round(float(price), 2)
