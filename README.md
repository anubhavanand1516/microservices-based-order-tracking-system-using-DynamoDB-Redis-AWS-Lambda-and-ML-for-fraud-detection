# Microservices-Based Order Tracking System 

This project implements a **complete order tracking system using Python**, built on a microservices architecture. It integrates:

- **Flask** APIs
- **DynamoDB** (for orders)
- **Redis** (for tracking)
- **Machine Learning** (for fraud detection)
- **AWS Lambda + SNS** (for notifications)

---
<img width="1440" alt="Screenshot 2025-05-06 at 5 12 34 AM" src="https://github.com/user-attachments/assets/6e2428bb-7286-452a-be75-d0fa3a6b7208" />


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
<img width="1440" alt="Screenshot 2025-05-06 at 5 12 06 AM" src="https://github.com/user-attachments/assets/ec788626-3970-431e-97e6-a4356db545d2" />

---

## 4. Start Redis Server

```bash
docker run -d --name redis -p 6379:6379 redis
```

---

## 5. Microservices 

### 5.1 Order Service (Port 5000)

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

#### Run API

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
