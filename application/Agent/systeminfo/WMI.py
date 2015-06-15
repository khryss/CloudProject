import wmi
import time

class WMIManager(object):
	def __init__(self):
		   #WMI init
		self.wmiConnection = wmi.WMI()
		self.operatingSys = self.wmiConnection.Win32_OperatingSystem()[0]
		self.computerSys = self.wmiConnection.Win32_ComputerSystem()[0]		

	def getHostTime(self):
		return time.strftime('%X-%x')

	def getHostName(self):
		return self.computerSys.Name

	def getHostIp(self):
		return self.wmiConnection.Win32_NetworkAdapterConfiguration(IPEnabled=True)[0].IPAddress[0]

	def getHostFreeMem(self):
		return self.operatingSys.FreePhysicalMemory