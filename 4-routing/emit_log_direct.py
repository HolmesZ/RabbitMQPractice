# 发送日志到direct类型的交换机

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# 声明一个direct类型的交换机
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

severity = sys.argv[1] if len(sys.argv) > 1 else "info"
message = " ".join(sys.argv[2:]) or "Hello World!"

# 发送消息到交换机
# routing_key为severity，消息体为message
channel.basic_publish(exchange="direct_logs", routing_key=severity, body=message)

print(f" [x] Sent {severity}:{message}")
connection.close()
