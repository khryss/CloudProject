import time

from models import *


class Logger(object):
	def __init__(self, loggerSQLiteDatabaseFile):
		   #save parameters
		self.loggerSQLiteDatabaseFile = loggerSQLiteDatabaseFile
		   #init sqlite engine and session
		self.engine = create_engine(self.loggerSQLiteDatabaseFile, echo=False)
		Base.metadata.create_all(self.engine)
		self.Session = sessionmaker(bind = self.engine, autoflush = False, expire_on_commit = True)
		self.session = self.Session()

		   #init log id with the next id based on the DB
		logs = self.session.query(Log).order_by(Log.id).all()
		self.logid = logs[-1].id if logs else 0

	def addLog(self, data):
		log = Log(agentHostName = data['agentHostName'],
				  agentHostIp = data['agentHostIp'],
				  agentHostTime = data['agentHostTime'],
				  agentType = data['agentType'],
				  agentHostData = data['agentHostData']
				  )
		   #set the next logid to the received log
		self.logid += 1
		log.id = self.logid

		try:
			   #add the log into DB
			self.session.add(log)
		except Exception as ex:
			print "logging exception: " , ex.message

	def stop(self):
		self.session.commit()

	def getLogs(self):
		try:
			   #get all logs from DB
			res = self.session.query(Log).all()
		except Exception as ex:
			print "query exception: " , ex.message
		return res


