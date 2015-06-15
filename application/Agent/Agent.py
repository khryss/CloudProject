import json

from configuration.Agent_config import *
from communication.AMQPManager import *
from systeminfo.WMI import *

class Agent(object):
	def __init__(self):
		   #Communication manager init
		self.commManager = AMQPManager()

		   #Systeminfo manager init
		self.sysInfoManager = WMIManager()

	def run(self):
		print "Agent is runing on HOST name:" , self.sysInfoManager.getHostName() , ". Press Ctrl+C to close."
		try:
			while True:
				data = json.dumps({'agentHostName':self.sysInfoManager.getHostName(),
								   'agentHostIp':self.sysInfoManager.getHostIp(),
								   'agentHostTime':self.sysInfoManager.getHostTime(),
								   'agentHostFreeMemory':self.sysInfoManager.getHostFreeMem()}
								 )
				self.commManager.send(data)
				print "Agent sent frame with: %s" % data
				   #connection sleep until next update frame
				self.commManager.connectionSleep(SYS_INFO_UPDATE_TIME)
		except KeyboardInterrupt:
			self.stop()

	def stop(self):
		   #stop the other Agent components
		self.commManager.stop()
		print "Agent shut down."

agent = Agent()
agent.run()