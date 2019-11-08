import pika

connection = pika.BlockingConnection(pika.URLParameters('amqp://root:password@localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='googlecast_events', exchange_type='topic')
channel.basic_publish(exchange='googlecast_events', routing_key='media', body='hello, world')
print(" [x] sent 'Hello, world!'")

channel.close()