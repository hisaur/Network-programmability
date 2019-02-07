from GetServiceTicket import *
from tabulate import tabulate
def GetNetworkDevices(aTicket,url,aData=None):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requestdevices=requests.get(url,data=None,headers=header,verify=False)
    request_json=requestdevices.json()
    devices=request_json["response"]
    device_list=[]
    i=0
    for item in devices:
        i+=1
        device_list.append ([i ,item["hostname"],item["type"],item["managementIpAddress"],item["softwareVersion"],item["instanceUuid"]])
        
    print (tabulate(device_list, headers=["number","hostname","type","ip","softwareVersion","instanceUuid"],tablefmt ="rst"))
    return device_list
    
def ASK_USER_INPUT(aDevice_list):
    user_input=int(input("Введите номер для получения конфигурации: "))
    if user_input in range (1,len(aDevice_list)+1):
        return user_input
def RevealIFofaDevice(user_input,aDevice_list):
    id = aDevice_list[user_input-1][5]
    return id
def RevealTypeofaDevice(user_input,aDevice_list):
    TypeofaDevice = aDevice_list[user_input-1][2]
    return TypeofaDevice
def GetNetworkInterfacesSwitch(aTicket,url):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requestinterfaces=requests.get(url,data=None,headers=header,verify=False)
    request_json=requestinterfaces.json()
    interfaces=request_json["response"]
    interface_list = []
    i=0
    for item in interfaces:
        i+=1
        interface_list.append ([i,item["portName"],item["duplex"],item["speed"],item["adminStatus"],item["vlanId"]])
    print (tabulate(interface_list, headers=["PortName","duplex","speed","adminStatus","vlanID"]))
def GetNetworkInterfacesRouter(aTicket,url):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requestinterfaces=requests.get(url,data=None,headers=header,verify=False)
    request_json=requestinterfaces.json()
    interfaces=request_json["response"]
    interface_list = []
    i=0
    for item in interfaces:
        i+=1
        interface_list.append ([i,item["portName"],item["duplex"],item["speed"],item["adminStatus"],item["ipv4Address"],item["ipv4Mask"]])
    print (tabulate(interface_list, headers=["PortName","duplex","speed","adminStatus","ipv4Address","ipv4Mask"]))
    
def GetConfiguration(aTicket,url,aData=None):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requestdeviceconfig=requests.get(url,data=None,headers=header,verify=False)
    request_json=requestdeviceconfig.json()

    print (request_json["response"].replace("\r\n","\n"))
def main():
    ticket = GetServiceTicket()
    device_list=GetNetworkDevices (ticket, "https://"+ControllerIP+"/api/v1/network-device")
    user_input = ASK_USER_INPUT(device_list)
    id=RevealIFofaDevice(user_input,device_list)
    TypeofaDevice = RevealTypeofaDevice (user_input,device_list)
    print (TypeofaDevice)
    a=int(input("Введите 1 для получения полной конфигурации устройства или 2 для получения информации об интерфейсах: "))
    if a ==1:
        GetConfiguration(ticket,"https://"+ControllerIP+"/api/v1/network-device/"+id+"/config")
    elif a==2:
        if "Switch" in TypeofaDevice:
            GetNetworkInterfacesSwitch(ticket,"https://"+ControllerIP+"/api/v1/interface/network-device/"+id)
        elif "Router" in TypeofaDevice:
            GetNetworkInterfacesRouter(ticket,"https://"+ControllerIP+"/api/v1/interface/network-device/"+id)
    else:
        print ("Неправильная команда")
main()