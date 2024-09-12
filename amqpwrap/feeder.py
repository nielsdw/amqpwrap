import pika
from amqpwrap.parameters import parameters


def send_message(headers, message, queue_name):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                              headers=headers
                          ))

    connection.close()

