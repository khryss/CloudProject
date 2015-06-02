import pika
from Controller_config import *

def receiveCallBack(ch, method, proprieties, body):
		print body

class Controller():
	def __init__(self):
		   #AMQP init
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(AMQP_SERVER_IP))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue = AMQP_QUEUE_NAME)
		self.channel.basic_consume(receiveCallBack, queue = AMQP_QUEUE_NAME, no_ack = True)

	def run(self):
		try:
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.channel.stop_consuming()
		self.connection.close()

controller = Controller()
controller.run()
print "Controller shut down."