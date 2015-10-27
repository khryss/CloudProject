from AgentModel import AgentModel

class AgentCPU(AgentModel):
	def __init__(self):
		super(AgentCPU,self).__init__()

	def getData(self):
		return {'AgentName':'AgentCPU', 'AgentData':self.sysInfoManager.getHostCpuLoad()}


agent = AgentCPU()
agent.run()