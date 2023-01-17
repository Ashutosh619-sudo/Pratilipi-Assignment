import pika,json
import django
from sys import path
import os
import time


path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'core', 'settings.py'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') 

django.setup()


from content.tasks import like_event

def wrapper_callback(ch, method, properties, body):
    body = json.loads(body)

    content_id = body["content_id"]

    like_event.delay(content_id)


def start_consuming():

    time.sleep(30)
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='like')
    channel.basic_consume(queue='like', on_message_callback=wrapper_callback, auto_ack=True)
    channel.start_consuming()

start_consuming()