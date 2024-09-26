# import wmi

# c = wmi.WMI()

# # 获取主板序列号
# for board_id in c.Win32_BaseBoard():
#     print('主板序列号:', board_id.SerialNumber)
    

# # 获取操作系统信息
# for os in c.Win32_OperatingSystem():
#     print("操作系统: ", os.Caption)
#     print("版本: ", os.Version)
#     print("制造商: ", os.Manufacturer)

# # 获取CPU信息
# for cpu in c.Win32_Processor():
#     print("CPU型号: ", cpu.Name)
#     print("核心数: ", cpu.NumberOfCores)

# # 获取内存信息
# for mem in c.Win32_PhysicalMemory():
#     print("内存容量: ", mem.Capacity)

# # 获取硬盘信息
# for disk in c.Win32_DiskDrive():
#     print("硬盘型号: ", disk.Model)
#     print("硬盘容量: ", disk.Size)

import requests
import time

def get_beijing_time():
    response = requests.get("http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp")
    if response.status_code == 200:
        json_data = response.json()
        timestamp = json_data["data"]["t"]
        beijing_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timestamp)/1000))
        return beijing_time
    else:
        return None

print(get_beijing_time())
