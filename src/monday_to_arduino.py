import json
import boto3
import os

class Queue():
    def __init__(self, **kwargs):
        self.region = kwargs.get('region','us-east-1')
        self.queue_url = kwargs.get('queue_url')
        self.session = boto3.session.Session()
        self.queue = self.session.client(
            service_name='sqs',
            region_name=self.region
        )

    def enQueue(self, payload, **kwargs):
        self.response = self.queue.send_message(QueueUrl=self.queue_url, MessageBody=payload)
        return self.response

    def deQueue(self, **kwargs):
        number_of_messages_to_read = kwargs.get('number_of_messages_to_read',10)
        delete_read_messages = bool(kwargs.get('delete_read_messages',True))
        return_full_sqs_message = bool(kwargs.get('return_full_sqs_message',False))
        self.response = self.queue.receive_message(
           QueueUrl=self.queue_url,
           MaxNumberOfMessages=number_of_messages_to_read
        )
        messages = self.response.get('Messages', [])
        return_values = []
        for message in messages:
            # Delete the message from the queue
            if delete_read_messages:
                self.queue.delete_message(
                    QueueUrl=self.queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
            if return_full_sqs_message:
                return_values.append(message)
            else:
                return_values.append(json.loads(message['Body']))
            # 10 is the maximum number of returned messages in SQS,
            # so we clear the queue to be on the safe side
            if delete_read_messages and len(messages)>=10:
                self.purgeQueue()
        return return_values

    def purgeQueue(self):
        self.response = self.queue.purge_queue(self.queue)

def authorized(event):
    apikey = os.environ.get('APIKEY')
    authorization_object = event['headers'].get('authorization', 'no').split()
    authorization_qs = event.get('queryStringParameters', {}).get('key', '')
    if (len(authorization_object) == 2 and authorization_object[1] == apikey) or authorization_qs == apikey:
        return True
    else:
        return False


def handler(event=None, context=None):
    print(json.dumps(event))
    skip_authorization = os.environ.get('SKIP_AUTHORIZATION','false').lower()=='true'

    if not (authorized(event)) and not skip_authorization:
        return {
            'statusCode': 401,
            'body': 'unauthorized'
        }
    event_message = event.get('body', '{}')
    method = event['requestContext']['http']['method'].lower()
    challenge = json.loads(event_message).get('challenge')

    if challenge and method == 'post':
        response = dict(challenge=challenge)
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    path = event['rawPath'].lower()

    sqs = Queue(
        region=os.environ.get('AWS_REGION','us-east-1'),
        queue_url=os.environ['QUEUE_URL']
    )

    return_full_sqs_message = os.environ.get('RETURN_FULL_SQS_MESSAGE','false')=='true'

    if path == "/read" and method == 'get':
        messages = sqs.deQueue(
            return_full_sqs_message=return_full_sqs_message
        )
        response = json.dumps(messages, indent=4)
        response = len(messages)
        return {
            'statusCode': 200,
            'body': response
        }

    elif path == "/write" and method == 'post':
        sqs.enQueue(event_message)
        return {
            'statusCode': 200,
            'body': "ok"
        }

    else:
        return {
            'statusCode': 404,
            'body': "not found"
        }
