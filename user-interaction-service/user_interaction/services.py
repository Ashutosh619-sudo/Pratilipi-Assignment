import pika
import json

def send_like_event(content_id):

    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue="like")
    channel.basic_publish(exchange="", routing_key="like", body=json.dumps({"content_id":content_id}))
    connection.close()