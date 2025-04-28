# 从 direct 类型的交换机接收日志

import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# 声明一个direct类型的交换机
channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# 绑定交换机和队列
# routing_key为severity，队列名为queue_name
for severity in severities:
    channel.queue_bind(exchange="direct_logs", queue=queue_name, routing_key=severity)

print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")
    sys.stdout.flush()  # 刷新输出缓冲区


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
