import pika


class AMQPManager(object):
	def __init__(self, amqpServerIP, amqpQueueName, on_msg_recv_fnc=None, on_stop_fnc=None):
		   #save parameters
		self.amqpServerIP = amqpServerIP
		self.amqpQueueName = amqpQueueName
		   #save callback functions
		self.on_msg_recv_CallBack = on_msg_recv_fnc
		self.on_stop_CallBack = on_stop_fnc
		   #init AMQP connection
		self.amqpConn = pika.BlockingConnection(pika.ConnectionParameters(self.amqpServerIP,heartbeat_interval=1))
		self.channel = self.amqpConn.channel()
		self.channel.queue_declare(queue = self.amqpQueueName)
		try:
			self.channel.basic_consume(self.receiveCallBack, queue = self.amqpQueueName, no_ack = True)
		except Exception as ex:
			print "Consume exception: " , ex.message

	def receiveCallBack(self, ch, method, proprieties, body):
		self.on_msg_recv_CallBack(ch, method, proprieties, body)

	def run(self):
		try:
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.channel.stop_consuming()
			self.on_stop_CallBack()
		self.amqpConn.close()
