import wmi

conn = wmi.WMI()

obj = conn.Win32_OperatingSystem()[0]

print obj.TotalVisibleMemorySize
