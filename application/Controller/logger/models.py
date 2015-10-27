from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import *


class BaseModel(object):
	id = Column(Integer, primary_key=True)


Base = declarative_base(cls = BaseModel)


class Log(Base):
	__tablename__ = 'logs'

	agentHostName = Column(String)
	agentHostTime = Column(String)
	agentHostIp = Column(String)
	agentType = Column(String)
	agentHostData = Column(String)

	def __repr__(self):
		return "log[%s]: time:%s name:%s ip:%s agentType:%s data:%s \n" % \
					    (self.id,
						 self.agentHostTime,
						 self.agentHostName,
						 self.agentHostIp,
						 self.agentType,
						 self.agentHostData)
