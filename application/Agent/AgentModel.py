import json

from configuration.Agent_config import *
from communication.AMQPManager import *
from systeminfo.WMI import *

class AgentModel(object):
	def __init__(self):
		   #Communication manager init
		self.commManager = AMQPManager()

		   #Systeminfo manager init. Can be used in specific Agent if needed
		self.sysInfoManager = WMIManager()
		print "Agent initiated"

	def run(self):
		print "Agent HOST name:" , self.sysInfoManager.getHostName() , ". Press Ctrl+C to close."
		try:
			while True:
				specificAgentData = self.getData()
				js = json.dumps({'agentHostName':self.sysInfoManager.getHostName(),
						 		 'agentHostIp':self.sysInfoManager.getHostIp(),
								 'agentHostTime':self.sysInfoManager.getHostTime(),
								 'agentType':specificAgentData['AgentName'],
								 'agentHostData':specificAgentData['AgentData']})
				self.commManager.send(js)

				print specificAgentData['AgentName'] , "sent frame"
				
				   #connection sleep until next update frame
				self.commManager.connectionSleep(SYS_INFO_UPDATE_TIME)
				

		except KeyboardInterrupt:
			self.stop()

	def stop(self):
		   #stop the other Agent components
		self.commManager.stop()
		print "Agent shut down."

	def getData(self):
		   #Method to be implemented by specific agent
		pass
