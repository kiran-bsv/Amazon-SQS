import os
import boto3
import pymongo
import json

from dotenv import load_dotenv

load_dotenv()

QUEUE_URL = os.getenv('QUEUE_URL')
sqs = boto3.client(
    'sqs',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

mongo_uri = os.getenv('MONGO_URI')
client = pymongo.MongoClient(mongo_uri)
db = client['conscience']
collection = db['users']

def receive_messages():
    print("Starting consumer service...")
    while True:
        try:
            response = sqs.receive_message(
                QueueUrl=os.getenv('QUEUE_URL'),
                MaxNumberOfMessages=1, 
                WaitTimeSeconds=10  
            )

            messages = response.get('Messages', [])
            for message in messages:
                user_data = json.loads(message['Body'])
                collection.insert_one(user_data)

                print(f"Stored user: {user_data}")

                sqs.delete_message(
                    QueueUrl=QUEUE_URL,
                    ReceiptHandle=message['ReceiptHandle']
                )
                print("Message processed and deleted from queue.")

        except Exception as e:
            print(f"Error receiving or processing messages: {e}")

if __name__ == '__main__':
    receive_messages()
