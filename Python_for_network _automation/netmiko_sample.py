from netmiko import ConnectHandler
import netmiko
from datetime import datetime
def Get_IP_int_brief(IP_address,username,password,enable_secret):
    ssh_connection = ConnectHandler(
        device_type = "cisco_ios",
        ip = IP_address,
        username = username,
        password = password,
        secret  = enable_secret,
    )
    ssh_connection.enable()
    result = ssh_connection.find_prompt() + "\n"
    result += ssh_connection.send_command("show ip int brief", delay_factor=2)
    ssh_connection.disconnect()
    return result


def Ask_for_username_and_password():
    yes_or_no = input ("Are all username and passwords are the same? print 'yes' or 'no'")
    if yes_or_no == "yes":
        username = input ("Enter username ")
        password = input ("Enter password ")
        enable_secret = input ("Enter enable_password ")
        intventory_list = [
        {"IP":"10.1.1.1","Username":username,"Password":password,"Enable_secret":enable_secret},
        {"IP":"10.1.1.2","Username":username,"Password":password,"Enable_secret":enable_secret},
        {"IP":"10.1.1.3","Username":username,"Password":password,"Enable_secret":enable_secret}
        ]    
        return intventory_list
def main():
    inventory_list = Ask_for_username_and_password()
    i=0
    result_list = []
    time_on_start = datetime.now

    for item in inventory_list:
        try:
            for attemts in range(1,3):
                print ("Processing the commands")
                result= Get_IP_int_brief (item["IP"],item["Username"],item["Password"],item["Enable_secret"])
                i+=1
                print (i,"    ",result,"\n")
        except netmiko.ssh_exception.NetMikoTimeoutException:
            if attemts < 3:
                print ("Connection Error")
            
            
    
main()

