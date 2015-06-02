from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///C:\CloudProjectDB.sqlite')
connection = engine.connect()

connection.execute("create table mytable (mycol1 INT(10), mycol2 CHAR(20))")

a = 1234
s = "'rowww'"
connection.execute("insert into mytable (mycol1, mycol2) values (%s, %s);" % (a, s))

result = connection.execute("select * from mytable where mycol1 = 1234")
for row in result:
	print row['mycol1'], row['mycol2']



exit()

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
