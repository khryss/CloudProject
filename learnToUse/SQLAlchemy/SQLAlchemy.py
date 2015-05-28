from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class Log(Base):
    __tablename__ = 'myTable'
    
    id = Column(Integer, primary_key=True)
    data = Column(String)

    def __init__(self, id, data):
    	self.id = id
    	self.data = data

log = [3]
log[0] = Log(0, "first log")

print log[0].id, log[0].data
