"""
app.py
Flask web application for Real Estate Price Prediction.

Run: python app.py
Then open: http://localhost:5000
"""

import os
import sys
from flask import Flask, render_template, request, jsonify

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from predict import predict_price

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form

        input_dict = {
            'city': data.get('city'),
            'locality_tier': data.get('locality_tier'),
            'bhk': int(data.get('bhk')),
            'area_sqft': int(data.get('area_sqft')),
            'metro_dist_km': float(data.get('metro_dist_km')),
            'it_park_dist_km': float(data.get('it_park_dist_km')),
            'rera_registered': int(data.get('rera_registered')),
            'ready_to_move': int(data.get('ready_to_move')),
            'age_years': int(data.get('age_years', 0)),
        }

        price = predict_price(input_dict)

        # Format nicely
        if price >= 100:
            price_display = f"₹{price:.2f} Lakhs (~₹{price/100:.2f} Crore)"
        else:
            price_display = f"₹{price:.2f} Lakhs"

        return jsonify({'success': True, 'price': price_display, 'raw': price})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    # Check if model exists, if not train it
    if not os.path.exists('model.joblib'):
        print("Model not found. Training now...")
        from model import train
        train()
    app.run(debug=True)
