from flask import Flask, request, jsonify
import boto3
import uuid

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Orders')

@app.route('/')
def index():
    return "✅ Order Service is running. Use POST /order to create an order or GET /order/<id> to fetch one."

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    order_id = str(uuid.uuid4())
    item = data['item']
    order = {'id': order_id, 'item': item, 'status': 'placed'}
    table.put_item(Item=order)
    return jsonify(order)

@app.route('/order/<order_id>', methods=['GET'])
def get_order(order_id):
    response = table.get_item(Key={'id': order_id})
    return jsonify(response.get('Item', {}))

if __name__ == '__main__':
    app.run(port=5000)
