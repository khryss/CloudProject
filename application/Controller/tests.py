import unittest,thread,time,json

from communication.AMQPManager import *
from logger.Logger import *
from Controller import *


class TestController_communication(unittest.TestCase):
	def testAMQPManager_init(self):
		def stub_recv():
			return 1
		def stub_stop():
			return 2

		try:
			amqpm = AMQPManager("localhost","queue",stub_recv, stub_stop)
		except:
			self.fail("Unexpected Exception!")
		self.assertIsInstance(amqpm, AMQPManager)
		self.assertTrue(1 == amqpm.on_msg_recv_CallBack())
		self.assertTrue(2 == amqpm.on_stop_CallBack())
		amqpm.amqpConn.close()

	def testAMQPManager_run(self):
		def stub_keyInterrupt(sleepTime):
			amqpConn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
			channel = amqpConn.channel()
			channel.queue_declare(queue = "queue")
			channel.basic_publish(exchange = '',
								  routing_key = "queue",
								  body = "abcdefg")
			amqpConn.sleep(sleepTime)
			thread.interrupt_main()

		def stub_recv(ch, method, proprieties, body):
			self.isCalled_stub_recv = True

		def stub_stop():
			self.isCalled_stub_stop = True
		
		self.isCalled_stub_recv = False
		self.isCalled_stub_stop = False
		
		amqpm = AMQPManager("localhost", "queue", stub_recv, stub_stop)
		thread.start_new_thread(stub_keyInterrupt,(3,))
		try:
			amqpm.run()
		except:
			self.fail("Unexpected Exception!")

		self.assertTrue(self.isCalled_stub_recv)
		self.assertTrue(self.isCalled_stub_stop)



class TestController_logger(unittest.TestCase):
	def testLogger_init(self):
		try:
			logger = Logger('sqlite:///testDB.db')
		except:
			self.fail("Unexpected Exception!")
		self.assertIsInstance(logger, Logger)
		logger.stop()

	def testLogger_addLog(self):
		logger = Logger('sqlite:///testDB.db')
		data = {'agentHostName':'test_addLog_HostName',
				'agentHostIp':'test_addLog_HostIp',
				'agentHostTime':'test_addLog_HostTime',
				'agentType':'test_addLog_AgentType',
				'agentHostData':'test_addLog_HostData'}
		try:
			logger.addLog(data)
		except:
			self.fail("Unexpected Exception!")
		logger.session.commit()
		logs = logger.session.query(Log).order_by(Log.id).all()

		self.assertTrue('test_addLog_HostName' == logs[-1].agentHostName)
		self.assertTrue('test_addLog_HostIp' == logs[-1].agentHostIp)
		self.assertTrue('test_addLog_HostTime' == logs[-1].agentHostTime)
		self.assertTrue('test_addLog_AgentType' == logs[-1].agentType)
		self.assertTrue('test_addLog_HostData' == logs[-1].agentHostData)
		logger.stop()

	def testLogger_stop(self):	
		logger = Logger('sqlite:///testDB.db')
		try:
			logger.stop()
		except:
			self.fail("Unexpected Exception!")

	def testLogger_getLogs(self):
		logger = Logger('sqlite:///testDB.db')
		data = {'agentHostName':'test_getLogs_HostName',
				'agentHostIp':'test_getLogs_HostIp',
				'agentHostTime':'test_getLogs_HostTime',
				'agentType':'test_getLogs_AgentType',
				'agentHostData':'test_getLogs_HostData'}
		logger.addLog(data)
		logger.stop()
		try:
			logs = logger.getLogs()
		except:
			self.fail("Unexpected Exception!")
		self.assertIsInstance(logs, list)
		self.assertTrue('test_getLogs_HostName' == logs[-1].agentHostName)


class TestController_Controller(unittest.TestCase):
	def testController_init(self):
		Controller.CONFIG_FILE_PATH = 'tests_Controller_config.txt'
		try:
			controller = Controller()
		except:
			self.fail("Unexpected Exception!")
		self.assertIsInstance(controller, Controller)
		   #close connection for other tests
		controller.commManager.amqpConn.close()
		controller.stop()

	def testController_on_msg_recv(self):
		Controller.CONFIG_FILE_PATH = 'tests_Controller_config.txt'
		controller = Controller()

		data = {'agentHostName':'test_on_msg_recv_HostName',
				'agentHostIp':'test_on_msg_recv_HostIp',
				'agentHostTime':'test_on_msg_recv_HostTime',
				'agentType':'test_on_msg_recv_AgentType',
				'agentHostData':'test_on_msg_recv_HostData'}
		js = json.dumps(data)
		try:
			controller.on_msg_recv(None,None,None,js)
		except:
			self.fail("Unexpected Exception!")
		controller.logManager.session.commit()
		logs = controller.logManager.session.query(Log).order_by(Log.id).all()
		self.assertTrue('test_on_msg_recv_HostName' == logs[-1].agentHostName)
		   #close connection for other tests
		controller.commManager.amqpConn.close()
		controller.stop()

	def testController_run(self):
		def stub_keyInterrupt(sleepTime):
			amqpConn = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
			channel = amqpConn.channel()
			channel.queue_declare(queue = "queue")
			js = json.dumps({'agentHostName':'test_run_HostName',
							 'agentHostIp':'test_run_HostIp',
							 'agentHostTime':'test_run_HostTime',
							 'agentType':'test_run_AgentType',
							 'agentHostData':'test_run_HostData'})
			time.sleep(3)
			channel.basic_publish(exchange = '',
								  routing_key = "queue",
								  body = js)
			amqpConn.sleep(sleepTime)
			thread.interrupt_main()

		Controller.CONFIG_FILE_PATH = 'tests_Controller_config.txt'
		controller = Controller()
		thread.start_new_thread(stub_keyInterrupt,(3,))

		try:
			controller.run()
		except:
			self.fail("Unexpected Exception!")
		controller.logManager.session.commit()
		logs = controller.logManager.session.query(Log).order_by(Log.id).all()
		self.assertTrue('test_run_HostName' == logs[-1].agentHostName)
		controller.stop()

	def testController_getConfig(self):
		Controller.CONFIG_FILE_PATH = 'tests_Controller_config.txt'
		try:
			controller = Controller()
		except:
			self.fail("Unexpected Exception!")
		self.assertIsInstance(controller.parameters['AMQP_SERVER_IP'],str)
		self.assertIsInstance(controller.parameters['AMQP_QUEUE_NAME'],str)
		self.assertIsInstance(controller.parameters['LOGGER_SQLITE_DATABASE_FILE'],str)
		   #close connection for other tests
		controller.commManager.amqpConn.close()
		controller.stop()




if __name__ == '__main__':
	unittest.main()