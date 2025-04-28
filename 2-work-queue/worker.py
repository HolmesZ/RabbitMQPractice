# 从 RabbitMQ 队列中接收消息

import os
import sys
import time

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # 确保队列存在，持久化队列
    channel.queue_declare(queue="task_queue", durable=True)

    # 定义回调函数，处理接收到的消息
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        # time.sleep(body.count(b'.'))
        time.sleep(int(body.decode()))
        print(" [x] Done")
        ch.basic_ack(delivery_tag = method.delivery_tag)

    # 设置消费者，指定队列和回调函数
    # auto_ack=True 表示自动确认消息，RabbitMQ 会在接收到消息后自动删除它
    channel.basic_qos(prefetch_count=1) # 设置 QoS，确保每次只处理一个消息
    channel.basic_consume(queue="hello", on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
