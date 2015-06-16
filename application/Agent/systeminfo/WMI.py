import wmi
import time

class WMIManager(object):
	def __init__(self):
		   #WMI init
		self.wmiConnection = wmi.WMI()
		
	def getHostTime(self):
		return time.strftime('%X-%x')

	def getHostName(self):
		return self.wmiConnection.Win32_ComputerSystem()[0].Name

	def getHostIp(self):
		return self.wmiConnection.Win32_NetworkAdapterConfiguration(IPEnabled=True)[0].IPAddress[0]

	def getHostFreeMem(self):
		return self.wmiConnection.Win32_OperatingSystem()[0].FreePhysicalMemory

	def getHostCpuLoad(self):
		cpuLoad = self.wmiConnection.Win32_Processor()[0].LoadPercentage
		return 0 if cpuLoad is None else cpuLoad