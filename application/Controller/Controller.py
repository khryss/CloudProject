import json

from communication.AMQPManager import *
from logger.Logger import *


class Controller(object):
	def __init__(self):
		   #Logging manager init
		self.logManager = Logger()
		   #Communication manager init
		self.commManager = AMQPManager(self.on_msg_recv, self.stop)

	def on_msg_recv(self, ch, method, proprieties, body):
		try:
			res = json.loads(body) 
		except:
			print "Json exception!"

		log = Log(agentHostName = res['agentHostName'],
				  agentHostIp = res['agentHostIp'],
				  agentHostTime = res['agentHostTime'],
				  agentHostFreeMemory = res['agentHostFreeMemory'],
				  agentHostCpuLoad = res['agentHostCpuLoad']
				  )
		
		self.logManager.addLog(log)		

	def run(self):
		print "Controller is running. Press Ctrl+C to close."
		   #run the other Controller components
		self.commManager.run()

	def stop(self):
		   #stop the other Controller components
		self.logManager.stop()
		print "Controller shut down."

	def getLogs(self):
		return self.logManager.getLogs()

controller = Controller()
controller.run()
print "data base:"
print controller.getLogs()