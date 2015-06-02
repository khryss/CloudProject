import pika
import time
import wmi
from Agent_config import *


class Agent():
	def __init__(self):
		   #AMQP init
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(AMQP_SERVER_IP))
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue = AMQP_QUEUE_NAME)

		   #WMI init
		self.wmiConnection = wmi.WMI()
		self.operatingSys = self.wmiConnection.Win32_OperatingSystem()[0]
		self.computerSys = self.wmiConnection.Win32_ComputerSystem()[0]
		
		   #HOST info init
		self.HOSTname = self.computerSys.Name
		wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
		wmi_out = self.wmiConnection.query(wmi_sql)
		self.HOSTipAddr = wmi_out[0].IPAddress[0]

	def run(self):
		print "HOST name:", self.HOSTname, ". HOST ip address:", self.HOSTipAddr
		for i in range(100):
			time.sleep(SYS_INFO_UPDATE_TIME)
			self.operatingSys = self.wmiConnection.Win32_OperatingSystem()[0]
			self.channel.basic_publish(exchange = '', routing_key = AMQP_QUEUE_NAME,
									   body = ("Agent on [%s:%s][%s]: FreeMem - %s." % (self.HOSTname,
									   		   self.HOSTipAddr, time.strftime('%X %x'), self.operatingSys.FreePhysicalMemory)))
			print "Agent sent log %d" % i

agent = Agent()
try:
	agent.run()
except KeyboardInterrupt:
	print 'Agent shut down.'
agent.connection.close()