import pika

def receiveCallBack(ch, method, proprieties, body):
		print body

class Controller():
	def __init__(self):
		   #AMQP init
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue = 'serverRecv')
		self.channel.basic_consume(receiveCallBack, queue = 'serverRecv', no_ack = True)

	def run(self):
		try:
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.channel.stop_consuming()
		self.connection.close()

controller = Controller()
controller.run()