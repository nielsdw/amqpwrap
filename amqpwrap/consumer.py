import threading
import pika
from functools import wraps
from amqpwrap.parameters import parameters


def amqp_listener(queue):
    def decorator(func):
        @wraps(func)
        def start_consuming():
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            channel.queue_declare(queue=queue, durable=True)

            def on_message(ch, method, properties, body):
                func(body, properties)
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)
            print(f"Starting to consume messages from {queue}...")
            channel.start_consuming()

        thread = threading.Thread(target=start_consuming)
        thread.start()

        return func

    return decorator
