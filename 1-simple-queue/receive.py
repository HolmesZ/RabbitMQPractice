# 从 RabbitMQ 队列中接收消息

import os
import sys

import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    # 确保队列存在
    channel.queue_declare(queue="hello")

    # 定义回调函数，处理接收到的消息
    def callback(ch, method, properties, body):
        print(f" [+] Received {body}")

    # 设置消费者，指定队列和回调函数
    # auto_ack=True 表示自动确认消息，RabbitMQ 会在接收到消息后自动删除它
    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)

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
