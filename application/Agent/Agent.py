import pika
import time
import wmi


class Agent():
	def __init__(self):
		   #AMQP init
		self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue = 'serverRecv')

		   #WMI init
		self.wmiConnection = wmi.WMI()
		self.OSInfo = self.wmiConnection.Win32_OperatingSystem()[0]

	def run(self):
		for i in range(100):
			time.sleep(2)
			self.OSInfo = self.wmiConnection.Win32_OperatingSystem()[0]
			self.channel.basic_publish(exchange = '', routing_key = 'serverRecv', body = ("Agent: log %d. FreeMem: %s." % (i, self.OSInfo.FreePhysicalMemory)))

agent = Agent()
try:
	agent.run()
except KeyboardInterrupt:
	agent.connection.close()