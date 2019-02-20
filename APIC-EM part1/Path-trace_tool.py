from GetServiceTicket import *
from tabulate import tabulate
import threading,time
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
def Select_First_IP (aNumerallist):
    Number_in_table = int (input("Select Sourse IP address by typing a number "))
    First_IP = aNumerallist[Number_in_table-1][2]
    return First_IP
def Select_Second_IP (aNumerallist):
    Number_in_table = int (input("Select Sourse IP address by typing a number "))
    Second_IP = aNumerallist[Number_in_table-1][2]
    return Second_IP
def PathTrace (aTicket, aSourse_IP, aDestinationIP, url):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    h_data = {"sourceIP": str(aSourse_IP), "destIP": str(aDestinationIP)}
    r = requests.post (url, data = json.dumps(h_data), headers = header, verify = False)
    response_json = r.json()
    flowAnalisysID = response_json["response"] ["flowAnalysisId"]
    print (r.status_code)
    return flowAnalisysID
def Check_For_Response(aTicket, url,aFlowanalisysID):
    header = {"X-Auth-Token":aTicket,"content-type":"application/json"}
    r = requests.get (url, headers = header, verify = False)
    response_list = r.json()["response"]
    response_status = response_list["request"]["status"]
    count = 0
    while response_status != "COMPLETED":
        if response_status == "FAILED":
            print ("Path trace failed")
        else:
            r = requests.get (url, headers = header, verify = False)
            response_list = r.json()["response"]
            response_status = response_list["request"]["status"]
            time.sleep(1)
            print (response_status)
            count+=1
            if count >30:
                print ("Connection error")
                exit
    final_request = requests.get (url,headers = header, verify = False)
    path_trace_data = final_request.json() ["response"]
    list_of_data = []
    i=0
    path_trace_data_response = path_trace_data ["networkElementsInfo"]
    print (path_trace_data_response[0]["egressInterface"]["physicalInterface"]["name"])
    for item in path_trace_data_response:
        i+=1
        try :
            list_of_data.append([i,item ["name"], item["ip"], item["ingressInterface"]["physicalInterface"].get("name", "NO SUCH INTERFACE") , item["egressInterface"]["physicalInterface"].get("name","none")  ])
        except KeyError:
                list_of_data.append([i,item ["name"], item["ip"], item["egressInterface"]["physicalInterface"].get("name","none")  ])
                list_of_data.append([i,item ["name"], item["ip"], item["ingressInterface"]["physicalInterface"].get("name", "NO SUCH INTERFACE")])
                
    print (list_of_data)
    print (path_trace_data_response)
    print (list_of_data)
    Sourse_IP = path_trace_data["request"]["sourceIP"]
    Dest_IP = path_trace_data["request"]["destIP"]
    print ("\n","Path Trace is completed. Sourse IP:", Sourse_IP, "Destination IP:", Dest_IP)
    print (tabulate(list_of_data, headers=["name","ip","Egress Interface", "Ingress Interface"],tablefmt="rst"))
    return (path_trace_data)
  
        
def main():
    ticket = GetServiceTicket ()
    hosts = GetHosts(ticket,"https://"+ControllerIP+"/api/v1/host")
    devices=GetNetworkDevices (ticket, "https://"+ControllerIP+"/api/v1/network-device")
    numerallist = MergeHostsAndDevicesLists (devices,hosts)
    print (tabulate(numerallist,headers=["number","type of a device","IP"]))
    Sourse_IP = Select_First_IP (numerallist)
    Destination_IP = Select_Second_IP (numerallist)
    flowAnalisysID = PathTrace (ticket, Sourse_IP, Destination_IP,"https://"+ControllerIP+"/api/v1/flow-analysis")
    Check_For_Response (ticket,"https://"+ControllerIP+"/api/v1/flow-analysis"+"/"+flowAnalisysID,flowAnalisysID )


main ()
