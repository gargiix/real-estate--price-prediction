"""
preprocess.py
Handles data cleaning and feature engineering for the real estate dataset.
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np


def load_data(filepath):
    """Load the CSV dataset."""
    df = pd.read_csv(filepath)
    return df


def preprocess(df):
    """
    Clean and encode the dataset for model training.
    Returns: X (features), y (target), and the encoders used.
    """
    df = df.copy()

    # Drop rows with missing values (simple approach)
    df = df.dropna()

    # Encode categorical columns
    encoders = {}
    for col in ['city', 'locality_tier']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    # Separate features and target
    feature_cols = [
        'city', 'locality_tier', 'bhk', 'area_sqft',
        'metro_dist_km', 'it_park_dist_km',
        'rera_registered', 'ready_to_move', 'age_years'
    ]
    X = df[feature_cols]
    y = df['price_lakhs']

    return X, y, encoders


def preprocess_single(input_dict, encoders):
    """
    Preprocess a single user input for prediction.
    input_dict should have the same keys as feature columns.
    """
    df = pd.DataFrame([input_dict])

    for col in ['city', 'locality_tier']:
        le = encoders[col]
        # Handle unseen labels gracefully
        try:
            df[col] = le.transform(df[col])
        except ValueError:
            df[col] = 0  # default fallback

    feature_cols = [
        'city', 'locality_tier', 'bhk', 'area_sqft',
        'metro_dist_km', 'it_park_dist_km',
        'rera_registered', 'ready_to_move', 'age_years'
    ]
    return df[feature_cols]
