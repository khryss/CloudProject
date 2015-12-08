import unittest,thread,json,pika.exceptions as exceptions

from communication.AMQPManager import *
from AgentModel import *


class TestAgent_communication(unittest.TestCase):
	def testAMQPManager_init(self):
		try:
			amqpm = AMQPManager("localhost","queue")
		except:
			self.fail("Unnexpected Exception!")
		self.assertIsInstance(amqpm, AMQPManager)
			
	def testAMQPManager_send(self):
		amqpm = AMQPManager("localhost","queue")
		try:
			amqpm.send("datadata")
		except:
			self.fail("Unnexpected Exception!")

	def testAMQPManager_stop(self):
		amqpm = AMQPManager("localhost","queue")
		amqpm.stop()
		with self.assertRaises(exceptions.ChannelClosed):
			amqpm.send("datadata")

	def testAMQPManager_connectionSleep(self):
		amqpm = AMQPManager("localhost","queue")
		try:
			amqpm.connectionSleep(1)
			amqpm.send("datadata")
		except:
			self.fail("Unnexpected Exception!")


class TestAgent_systeminfo(unittest.TestCase):
	def testWMIManager_init(self):
		try:
			wmim = WMIManager()
		except:
			self.fail("Unnexpected Exception!")
		self.assertIsInstance(wmim, WMIManager)

	def testWMIManager_getHostName(self):
		wmim = WMIManager()
		try:
			wmim.getHostName()
		except:
			self.fail("Unnexpected Exception!")

	def testWMIManager_getHostIp(self):
		wmim = WMIManager()
		try:
			wmim.getHostIp()
		except:
			self.fail("Unnexpected Exception!")

	def testWMIManager_getHostTime(self):
		wmim = WMIManager()
		try:
			wmim.getHostTime()
		except:
			self.fail("Unnexpected Exception!")

	def testWMIManager_getHostFreeMem(self):
		wmim = WMIManager()
		try:
			wmim.getHostFreeMem()
		except:
			self.fail("Unnexpected Exception!")

	def testWMIManager_getHostCpuLoad(self):
		wmim = WMIManager()
		try:
			wmim.getHostCpuLoad()
		except:
			self.fail("Unnexpected Exception!")


class TestAgent_AgentModel(unittest.TestCase):
	def testAgentModel_init(self):
		AgentModel.CONFIG_FILE_PATH = 'inexistentFile.txt'
		with self.assertRaises(SystemExit):
			am = AgentModel()
		AgentModel.CONFIG_FILE_PATH = 'tests_Agent_Config.txt'

	def testAgentModel_init_2(self):
		AgentModel.CONFIG_FILE_PATH = 'tests_Agent_Config.txt'
		try:
			am = AgentModel()
		except:
			self.fail("Unnexpected Exception!")
		self.assertIsInstance(am, AgentModel)

	def testAgentModel_run(self):
		def stub_getData():
			return 3
		
		def stub_keyInterrupt(updateTime):
			time.sleep(updateTime*2+0.5)
			thread.interrupt_main()
		
		def stub_send(js):
			try:
				js = json.loads(js) 
			except Exception as ex:
				print ex
				self.fail("Unnexpected Exception!")
			self.assertTrue(3 == js['agentHostData'])

		AgentModel.CONFIG_FILE_PATH = 'tests_Agent_Config.txt'
		am = AgentModel()
		am.getData = stub_getData
		am.commManager.send = stub_send
		p = thread.start_new_thread(stub_keyInterrupt,(am.parameters['SYS_INFO_UPDATE_TIME'],))

		try:
			am.run()
		except:
			self.fail("Unnexpected Exception!")
			
	def testAgentModel_stop(self):
		am = AgentModel()
		try:
			am.stop()
		except:
			self.fail("Unnexpected Exception!")
		with self.assertRaises(exceptions.ChannelClosed):
			am.run()

	def testAgentModel_getConfig(self):
		AgentModel.CONFIG_FILE_PATH = 'tests_Agent_Config.txt'
		try:
			am = AgentModel()
		except:
			self.fail("Unnexpected Exception!")
		self.assertIsInstance(am.parameters['AMQP_SERVER_IP'], str)
		self.assertIsInstance(am.parameters['AMQP_QUEUE_NAME'], str)
		self.assertIsInstance(am.parameters['SYS_INFO_UPDATE_TIME'], int)
		



if __name__ == '__main__':
	unittest.main()