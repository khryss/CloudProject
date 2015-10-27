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
			js = json.loads(body) 
		except Exception as ex:
			print "Json exception!" , ex.message

		self.logManager.addLog(js)
		print "Message received from" , js['agentType'] , ":" , js["agentHostData"]

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
print "data base:\n" , controller.getLogs()