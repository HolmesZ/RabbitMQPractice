# Topic Exchange

# Usage:
# python emit_log_topic.py "kern.critical" "A critical kernel error"


import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

# Declare a topic exchange
# The exchange name is "topic_logs" and the type is "topic"
channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

routing_key = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"
message = " ".join(sys.argv[2:]) or "Hello World!"

# Publish a message to the topic exchange with the specified routing key
channel.basic_publish(exchange="topic_logs", routing_key=routing_key, body=message)

print(f" [x] Sent {routing_key}:{message}")
connection.close()
