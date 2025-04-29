#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))

channel = connection.channel()

channel.queue_declare(queue="rpc_queue")


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


def on_request(ch, method, props, body):
    n = int(body)

    print(f" [.] fib({n})")
    response = fib(n)

    # This will send the response back to the client
    # The client will listen on the reply_to queue for the response
    ch.basic_publish(
        exchange="",
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)

# This will tell RabbitMQ to send only one message at a time to the worker
# This is called "fair dispatch"
# It prevents the worker from being overwhelmed with messages
channel.basic_qos(prefetch_count=1)

# This will tell RabbitMQ to send messages to this queue
# The queue will be created if it doesn't exist
channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
