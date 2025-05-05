import json
import boto3

sns = boto3.client('sns')

TOPIC_ARN = 'arn:aws:sns:us-east-1:233356830334:OrderStatusTopic'

def lambda_handler(event, context):
    try:
        # Extract the first SNS record
        record = event['Records'][0]
        message = json.loads(record['Sns']['Message'])

        order_id = message.get('id')
        status = message.get('status')

        if not order_id or not status:
            return {
                'statusCode': 400,
                'body': 'Missing "id" or "status" in message'
            }

        # Publish update to SNS topic
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=f"Order {order_id} status is {status}"
        )

        return {
            'statusCode': 200,
            'body': 'Notification sent'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
