# 发送消息到 RabbitMQ 队列

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# 确保队列存在，持久化队列
channel.queue_declare(queue="task_queue", durable=True)

# 发送消息
message = " ".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange="",
    routing_key="hello",
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent,  # 消息持久化
    ),
)

print(f" [x] Sent '{message}'")

connection.close()
