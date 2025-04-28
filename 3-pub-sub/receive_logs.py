# 订阅日志
# python receive_logs.py > logs_from_rabbit.log 2>&1
# 该脚本会接收所有发送到 "logs" 交换机的消息
# 该脚本会创建一个临时队列，并将其绑定到 "logs" 交换机
# 该脚本会在接收到消息时调用回调函数，打印消息内容
import os
import sys
import pika


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    # 创建一个临时队列，RabbitMQ会自动为我们命名
    # exclusive=True表示该队列只在当前连接中有效，连接关闭后队列会自动删除
    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    # 将临时队列绑定到交换机，routing_key为空，因为fanout类型的交换机不需要routing_key
    # 该队列会接收所有发送到 "logs" 交换机的消息
    channel.queue_bind(exchange="logs", queue=queue_name)

    print(" [*] Waiting for logs. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        # message = body.decode()
        print(f" [x] 接收到消息: {body}")
        sys.stdout.flush()  # 确保输出立即刷新到文件

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

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
