from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Root route for status
@app.route('/')
def index():
    return "📦 Order Tracking Service is running. Use POST /track or GET /track/<order_id>."

# POST to update status
@app.route('/track', methods=['POST'])
def update_status():
    data = request.json
    order_id = data['id']
    status = data['status']
    r.set(order_id, status)
    return jsonify({'message': 'Status updated'}), 200

# GET to retrieve status of an order
@app.route('/track/<order_id>', methods=['GET'])
def get_status(order_id):
    status = r.get(order_id)
    if status is None:
        return jsonify({'error': 'Order ID not found'}), 404
    return jsonify({'id': order_id, 'status': status}), 200

if __name__ == '__main__':
    app.run(port=5001)
