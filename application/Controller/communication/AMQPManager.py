import pika

from configuration.Controller_config import *


class AMQPManager(object):
	def __init__(self, on_msg_recv_fnc=None, on_stop_fnc=None):
		   #save callback functions
		self.on_msg_recv_CallBack = on_msg_recv_fnc
		self.on_stop_CallBack = on_stop_fnc
		   #init AMQP connection
		self.amqpConn = pika.BlockingConnection(pika.ConnectionParameters(AMQP_SERVER_IP,heartbeat_interval=1))
		self.channel = self.amqpConn.channel()
		self.channel.queue_declare(queue = AMQP_QUEUE_NAME)
		try:
			self.channel.basic_consume(self.receiveCallBack, queue = AMQP_QUEUE_NAME, no_ack = True)
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
