# 发送消息到 RabbitMQ 队列

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# 确保队列存在
channel.queue_declare(queue="hello")

# 发送消息
channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")

print(" [x] Sent 'Hello World!'")

connection.close()
