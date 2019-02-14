from GetServiceTicket import *
from tabulate import tabulate
def GetHosts(aTicket, url):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requesthosts = requests.get (url,headers=header,data=None,verify=False)
    requesthosts_json = requesthosts.json()
    hosts= requesthosts_json["response"]
    return hosts
def GetNetworkDevices(aTicket,url,aData=None):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requestdevices=requests.get(url,data=None,headers=header,verify=False)
    request_json=requestdevices.json()
    devices=request_json["response"]
    return devices
def MergeHostsAndDevicesLists(aDevices,AHosts):
    numerallist = []
    i=0
    for item in aDevices:
        i+=1
        numerallist.append ([i,"Network Device",item["managementIpAddress"]])
    idx=i
    for item in AHosts:
        idx+=1
        numerallist.append ([idx,"Host",item["hostIp"]])  
    return numerallist
def main():
    ticket = GetServiceTicket ()
    hosts = GetHosts(ticket,"https://"+ControllerIP+"/api/v1/host")
    devices=GetNetworkDevices (ticket, "https://"+ControllerIP+"/api/v1/network-device")
    numerallist = MergeHostsAndDevicesLists (devices,hosts)
    print (tabulate(numerallist,headers=["number","type of a device","IP"]))

main ()
