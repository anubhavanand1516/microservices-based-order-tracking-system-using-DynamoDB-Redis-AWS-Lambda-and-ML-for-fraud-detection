from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the model (make sure fraud_model.pkl exists in the same directory as this file)
try:
    model = joblib.load('fraud_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Root route for debugging purposes
@app.route('/')
def index():
    return "✅ Fraud Detection Service is running! Use POST /check to check fraud status."

# POST route for checking fraud
@app.route('/check', methods=['POST'])
def check_fraud():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        features = data['features']

        if not isinstance(features, list) or len(features) == 0:
            return jsonify({'error': 'Invalid or empty features'}), 400

        prediction = model.predict([features])[0]
        return jsonify({'fraud': bool(prediction)}), 200

    except KeyError:
        return jsonify({'error': 'Missing "features" in the request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Make sure the app is running on the right port
    app.run(port=5002)
