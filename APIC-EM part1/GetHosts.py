from GetServiceTicket import *
from tabulate import tabulate
def GetHosts(aTicket, url):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    requesthosts = requests.get (url,headers=header,data=None,verify=False)
    requesthosts_json = requesthosts.json()
    hosts= requesthosts_json["response"]
    hosts_list = []
    i=0
    print (hosts)
    for item in hosts:
        i+=1
        hosts_list.append ([i,item["hostIp"],item["hostMac"],item["hostType"],item["connectedNetworkDeviceIpAddress"],item["vlanId"]])
    print (tabulate(hosts_list,headers=["HostIP","HostMac","HostType","ConnectedtoDeviceWithIp","VlanId"],tablefmt="rst"))
def main():
    ticket = GetServiceTicket ()
    GetHosts(ticket,"https://"+ControllerIP+"/api/v1/host")

main()