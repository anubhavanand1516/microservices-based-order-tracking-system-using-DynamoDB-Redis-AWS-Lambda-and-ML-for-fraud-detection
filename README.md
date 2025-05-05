# Python Microservices-Based Order Tracking System (All-in-One)

This project implements a **complete order tracking system using Python**, built on microservices architecture. It integrates:

- **Flask** APIs
- **DynamoDB** (for orders)
- **Redis** (for tracking)
- **Machine Learning** (for fraud detection)
- **AWS Lambda + SNS** (for notifications)

All code is included below in this README file.

---

## 1. Prerequisites

- Python 3.8+
- AWS CLI
- Docker (for Redis)
- IAM user with access keys

### Install Required Python Packages:

```bash
pip install flask boto3 redis scikit-learn joblib
```

---

## 2. AWS Configuration

### Step 1: Login to AWS CLI

```bash
aws configure
```

Enter:

- Access Key ID  
- Secret Access Key  
- Default region: `us-east-1`  
- Output format: `json`

### Step 2: Required IAM Permissions

Ensure your IAM user has the following AWS managed policies:

- `AmazonDynamoDBFullAccess`
- `AmazonSNSFullAccess`
- `AWSLambda_FullAccess`
- `CloudWatchLogsFullAccess`

---

## 3. Create DynamoDB Table

```bash
aws dynamodb create-table   --table-name Orders   --attribute-definitions AttributeName=id,AttributeType=S   --key-schema AttributeName=id,KeyType=HASH   --billing-mode PAY_PER_REQUEST
```

---

## 4. Start Redis Server

```bash
docker run -d --name redis -p 6379:6379 redis
```

---

## 5. Microservices (Code Included Below)

### 5.1 Order Service (Port 5000)

```python
from flask import Flask, request, jsonify
import boto3, uuid

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Orders')

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

app.run(port=5000)
```

**Run:**

```bash
python order_service.py
```

**Test:**

```bash
curl -X POST http://localhost:5000/order -H "Content-Type: application/json" -d '{"item":"Phone"}'
```

---

### 5.2 Tracking Service (Port 5001)

```python
from flask import Flask, request, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.route('/track', methods=['POST'])
def update_status():
    data = request.json
    r.set(data['id'], data['status'])
    return jsonify({'message': 'Status updated'})

@app.route('/track/<order_id>', methods=['GET'])
def get_status(order_id):
    status = r.get(order_id)
    return jsonify({'id': order_id, 'status': status})

app.run(port=5001)
```

**Run:**

```bash
python tracking_service.py
```

**Test:**

```bash
curl -X POST http://localhost:5001/track -H "Content-Type: application/json" -d '{"id":"uuid-1", "status":"shipped"}'
curl http://localhost:5001/track/uuid-1
```

---

### 5.3 Fraud Detection Service (Port 5002)

#### Create Model

```python
from sklearn.ensemble import RandomForestClassifier
import joblib

X = [[0, 1], [1, 0], [0, 0], [1, 1]]
y = [0, 1, 0, 1]
model = RandomForestClassifier().fit(X, y)
joblib.dump(model, 'fraud_model.pkl')
```

#### Run API

```python
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load('fraud_model.pkl')

@app.route('/check', methods=['POST'])
def check_fraud():
    features = request.json['features']
    prediction = model.predict([features])[0]
    return jsonify({'fraud': bool(prediction)})

app.run(port=5002)
```

**Run:**

```bash
python create_model.py
python fraud_detection_service.py
```

**Test:**

```bash
curl -X POST http://localhost:5002/check -H "Content-Type: application/json" -d '{"features":[1, 0]}'
```

---

### 5.4 Notification Service (AWS Lambda + SNS)

#### Lambda Code

```python
import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):
    record = event['Records'][0]
    message = json.loads(record['Sns']['Message'])
    sns.publish(
        TopicArn='YOUR_TOPIC_ARN',
        Message=f"Order {message['id']} status is {message['status']}"
    )
    return {'statusCode': 200, 'body': 'Notification sent'}
```

**Deploy:**

```bash
zip function.zip notification_lambda.py

aws lambda create-function   --function-name NotifyLambda   --runtime python3.9   --handler notification_lambda.lambda_handler   --role <YOUR_IAM_ROLE_ARN>   --zip-file fileb://function.zip
```

Replace `YOUR_TOPIC_ARN` and `YOUR_IAM_ROLE_ARN`.

---

## 6. Sample Output

### Create Order

```json
{
  "id": "uuid-1",
  "item": "Phone",
  "status": "placed"
}
```

### Track Status

```json
{
  "id": "uuid-1",
  "status": "shipped"
}
```

### Fraud Check

```json
{
  "fraud": true
}
```

---

## 7. License

MIT License

---

## 8. Author

Built by [Your Name]