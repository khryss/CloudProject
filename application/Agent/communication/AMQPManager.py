import pika


class AMQPManager(object):
	def __init__(self, amqpServerIP, amqpQueueName):
		   #save parameters
		self.amqpServerIP = amqpServerIP
		self.amqpQueueName = amqpQueueName
		   #init AMQP connection
		self.amqpConn = pika.BlockingConnection(pika.ConnectionParameters(self.amqpServerIP))
		self.channel = self.amqpConn.channel()
		self.channel.queue_declare(queue = self.amqpQueueName)

	def send(self, data):
		self.channel.basic_publish(exchange = '',
								   routing_key = self.amqpQueueName,
								   body = data)

	def stop(self):
		self.amqpConn.close()

	def connectionSleep(self, seconds):
		self.amqpConn.sleep(seconds)