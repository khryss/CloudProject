import json
import ast

from communication.AMQPManager import *
from systeminfo.WMI import *

class AgentModel(object):
	CONFIG_FILE_PATH = 'configuration\Agent_config.txt'

	def __init__(self):
		   #Configuration file parse
		self.config = self.getConfig()
		   #Communication manager init
		self.commManager = AMQPManager(self.parameters['AMQP_SERVER_IP'],
									   self.parameters['AMQP_QUEUE_NAME'])
		   #Systeminfo manager init. Can be used in specific Agent if needed
		self.sysInfoManager = WMIManager()

	def run(self):
		print "\nAgent HOST name:" , self.sysInfoManager.getHostName() , ". Press Ctrl+C to close."
		try:
			while True:
				specificAgentData = self.getData()
				js = json.dumps({'agentHostName':self.sysInfoManager.getHostName(),
						 		 'agentHostIp':self.sysInfoManager.getHostIp(),
								 'agentHostTime':self.sysInfoManager.getHostTime(),
								 'agentType':type(self).__name__,
								 'agentHostData':specificAgentData})
				self.commManager.send(js)

				print type(self).__name__ , "sent data"
				
				   #connection sleep until next update frame
				self.commManager.connectionSleep(self.parameters['SYS_INFO_UPDATE_TIME'])
		except KeyboardInterrupt:
			self.stop()

	def stop(self):
		   #stop the other Agent components
		self.commManager.stop()
		print "Agent shut down."

	def getData(self):
		   #Method to be implemented by specific agent
		pass

	def getConfig(self):
		try:
			f = open(self.CONFIG_FILE_PATH,'r')
		except IOError as ex:
			print "Exception: ", ex
			exit()

		self.parameters = {}
		while 1:
			l = f.readline()
			if(l == ''):
				break
			r = l.split()
			self.parameters[r[0]] = ast.literal_eval(r[1])
		f.close()


