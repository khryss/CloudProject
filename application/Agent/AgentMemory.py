from AgentModel import AgentModel

class AgentMemory(AgentModel):
	def __init__(self):
		super(AgentMemory,self).__init__()

	def getData(self):
		return self.sysInfoManager.getHostFreeMem()


agent = AgentMemory()
agent.run()