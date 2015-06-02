import pika
from sqlalchemy import create_engine
from Controller_config import *

class Controller():
	def __init__(self):
		   #AMQP init
		self.amqpConn = pika.BlockingConnection(pika.ConnectionParameters(AMQP_SERVER_IP))
		self.channel = self.amqpConn.channel()
		self.channel.queue_declare(queue = AMQP_QUEUE_NAME)
		try:
			self.channel.basic_consume(self.receiveCallBack, queue = AMQP_QUEUE_NAME, no_ack = True)
		except:
			print "Consume exception!"

		   #SQLAlchemy init
		engine = create_engine('sqlite:///C:\CloudProjectDB.sqlite')
		self.sqlConn = engine.connect()
		try:
			self.sqlConn.execute("create table mytable (host_name CHAR(100), host_ip CHAR(20), host_time CHAR(20),\
				FreeMemory INT(20))")
		except:
			print "Table allready exists."

	def receiveCallBack(self, ch, method, proprieties, body):
		#print body
		self.logIntoDB(body)

	def logIntoDB(self, body):
		tokens = body.split() #split the message. separator=' '

		if tokens[0] != "AGENT": #initial check for invalid message
			print "Not an agent raport!"
			return

		   #Parse host system info
		try:
			agentHostName = tokens[tokens.index("HOSTname:") + 1]
			agentHostIp = tokens[tokens.index("HOSTip:") + 1]
			agentHostTime = tokens[tokens.index("HOSTtime:") + 1]
			agentHostFreeMemory = tokens[tokens.index("FreeMemory-") + 1]
		except:
			print "Agent raport is invalid!"
			return

		try:
			#print "insert into mytable values ('%s', '%s', '%s', %s);" % (agentHostName, agentHostIp, agentHostTime, agentHostFreeMemory)
			self.sqlConn.execute("insert into mytable values ('%s', '%s', '%s', %s);" % (agentHostName, agentHostIp,
																						 agentHostTime, agentHostFreeMemory))
		except:
			print "Querry exception!"

	def run(self):
		try:
			self.channel.start_consuming()
		except KeyboardInterrupt:
			self.channel.stop_consuming()
		self.amqpConn.close()

controller = Controller()
controller.run()
print "DataBase:"
result = controller.sqlConn.execute("select * from mytable")
for row in result:
	print row['host_name'], row['host_ip'], row['host_time'], row['FreeMemory']

print "Controller shut down."