import json
import ast

from communication.AMQPManager import *
from logger.Logger import *


class Controller(object):
	CONFIG_FILE_PATH = 'configuration\Controller_config.txt'
	
	def __init__(self):
		   #Configuration file parse
		self.getConfig()
		   #Logging manager init
		self.logManager = Logger(self.parameters['LOGGER_SQLITE_DATABASE_FILE'])
		   #Communication manager init
		self.commManager = AMQPManager(self.parameters['AMQP_SERVER_IP'],
									   self.parameters['AMQP_QUEUE_NAME'],
									   self.on_msg_recv,
									   self.stop)

	def on_msg_recv(self, ch, method, proprieties, js):
		try:
			data = json.loads(js)
		except Exception as ex:
			print "Json exception!" , ex.message

		self.logManager.addLog(data)
		print "Message received from" , data['agentType'] , ":" , data["agentHostData"]

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


if __name__ == '__main__':
	controller = Controller()
	controller.run()
	print "data base:\n" , controller.getLogs()