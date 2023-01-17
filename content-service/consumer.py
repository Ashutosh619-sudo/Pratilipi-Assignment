import pika,json
import django
from sys import path
from os import environ
import time

path.append('C:\\Users\\ashut\\Desktop\\pratilipi\\content-service\\core\\settings.py') #Your path to settings.py file
environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 

django.setup()


from content.tasks import like_event


def wrapper_callback(ch, method, properties, body):
    body = json.loads(body)

    content_id = body["content_id"]

    like_event.delay(content_id)


def start_consuming():
    # Connect to RabbitMQ

    time.sleep(30)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    # Declare a queue for the content service
    channel.queue_declare(queue='like')
    # Tell RabbitMQ to call the update_likes function for each message
    channel.basic_consume(queue='like', on_message_callback=wrapper_callback, auto_ack=True)
    # Start consuming messages
    channel.start_consuming()

start_consuming()