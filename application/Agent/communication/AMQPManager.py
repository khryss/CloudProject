import pika

from configuration.Agent_config import *


class AMQPManager(object):
	def __init__(self):
		   #init AMQP connection
		self.amqpConn = pika.BlockingConnection(pika.ConnectionParameters(AMQP_SERVER_IP))
		self.channel = self.amqpConn.channel()
		self.channel.queue_declare(queue = AMQP_QUEUE_NAME)

	def send(self, data):
		self.channel.basic_publish(exchange = '',
								   routing_key = AMQP_QUEUE_NAME,
								   body = data)

	def stop(self):
		self.amqpConn.close()

	def connectionSleep(self, seconds):
		self.amqpConn.sleep(seconds)