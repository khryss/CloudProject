from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class Log(Base):
    __tablename__ = 'myTable'
    
    id = Column(Integer, primary_key=True)
    data = Column(String)

    def __repr__(self):
    	return "log[%s]: %s" % (self.id, self.data)


log = []
log.append(Log(id='0', data="first log"))
log.append(Log(id='1', data="second log"))
#log[0] = Log(data="third log")

for i in range(len(log)):
	print log[i]
