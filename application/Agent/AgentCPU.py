from AgentModel import AgentModel

class AgentCPU(AgentModel):
	def __init__(self):
		super(AgentCPU,self).__init__()

	def getData(self):
		return self.sysInfoManager.getHostCpuLoad()


agent = AgentCPU()
agent.run()