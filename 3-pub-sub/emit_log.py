# 发布日志

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# 声明一个交换机，类型为fanout
# fanout类型的交换机会将消息广播到所有绑定的队列
channel.exchange_declare(exchange="logs", exchange_type="fanout")

message = " ".join(sys.argv[1:]) or "info: Hello World!"
# 发布消息到交换机，routing_key为空，因为fanout类型的交换机不需要routing_key
channel.basic_publish(exchange="logs", routing_key="", body=message)

print(f" [x] Sent {message}")

connection.close()
