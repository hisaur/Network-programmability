import netmiko

def Get_cdp_neighbors(IP_address,username,password,enable_secret):
    return_list = []
    ssh_connection = netmiko.ConnectHandler(
        device_type = "cisco_ios",
        ip = IP_address,
        username = username,
        password = password,
        secret  = enable_secret,
    )
    ssh_connection.enable()
    result = ssh_connection.find_prompt() + "\n"
    result += ssh_connection.send_command("terminal length 0", delay_factor=2)
    return_list.append = ssh_connection.send_command("show cdp nei", delay_factor = 2)
    return_list.append = ssh_connection.send_command("show ip int brief", delay_factor = 2)
    ssh_connection.send_command("terminal length 24", delay_factor=2)
    ssh_connection.disconnect()
    return return_list
    # this function creates dictionary with passwords and IP addresses
def Ask_for_username_and_password():
    yes_or_no = input ("Are all username and passwords are the same? print 'yes' or 'no'")
    if yes_or_no == "yes" or yes_or_no == "Yes":
        username = input ("Enter username ")
        password = input ("Enter password ")
        enable_secret = input ("Enter enable_password ")
        intventory_list = [
            # you must add here ip addresses of the devices in the following manner
        {"IP":"10.1.1.1","Username":username,"Password":password,"Enable_secret":enable_secret},
        {"IP":"10.1.1.2","Username":username,"Password":password,"Enable_secret":enable_secret},
        {"IP":"10.1.1.3","Username":username,"Password":password,"Enable_secret":enable_secret}
        ]    
        return intventory_list
    elif yes_or_no == "no" or yes_or_no == "No":
        intventory_list = [
            # you must add here ip addresses of the devices in the following manner
        {"IP":"10.1.1.1","Username":input("Username1"),"Password":input("password1"),"Enable_secret":input("Enable secret1")},
        {"IP":"10.1.1.2","Username":input("Username2"),"Password":input("password2"),"Enable_secret":input("Enable secret2")},
        {"IP":"10.1.1.3","Username":input("Username3"),"Password":input("password3"),"Enable_secret":input("Enable secret3")}
        ]  
    
        print (intventory_list)  
        return intventory_list
        #You cand just hardcode Usernames and passwords, but i consider it insecure
        #in oreder to do this just remove if and elif statements
def parsing_info(cdp_table):
    lines = cdp_table.splitlines()
    #delete lines with text and legend
    del lines [0]
    del lines [0]
    del lines [0]
    del lines [0]
    del lines [0]
    del lines [0]
    list_of_interfaces_to_network_devices = []
    for item in lines:
        #in this line we devide string into lines and paste it into list
        list_with_equal_spaces=item.split(" ")
        #delete empty list's items
        list_without_empty_items = list(filter(None, list_with_equal_spaces)) # fastest
        #combine text to following type Gig0/0/0
        try:
            interface_name=list_without_empty_items[1]
            interface_number=list_without_empty_items[2]
            full_name = interface_name+interface_number
            list_of_interfaces_to_network_devices.append (full_name)
        except IndexError:
            print ("Empty box")
    print (list_of_interfaces_to_network_devices)
    return (list_of_interfaces_to_network_devices)
    #In this function we process information from show ip int brief
    #In order to create list of all interfaces on a switch
def all_interfaces_on_a_device (ip_int_brief):
    list_of_all_interfaces = []
    lines = ip_int_brief.splitlines() 
    del lines [0]
    del lines [0]
    lines = list(filter(None,lines))
    for item in lines:
        #in this line we devide string into lines and paste it into list
        list_with_equal_spaces=item.split(" ")
        #delete empty list's items
        list_without_empty_items = list(filter(None, list_with_equal_spaces)) # fastest
        #combine text to following type Gig0/0/0
        try:
            interface_name=list_without_empty_items[0]
            interface_number=list_without_empty_items[1]
            full_name = interface_name+interface_number
            list_of_all_interfaces.append (full_name)
            #sometimes an emty list's box is created in the end of the list. 
            # This exception helps to skip it 
        except IndexError:
            print ("Empty box")
    print (list_of_all_interfaces)
    return list_of_all_interfaces
    #This function calculate interfaces to which changes of configuration will be made 
def calculate_interfaces_for_changes(all_interfaces,cdp_interfaces):
    list_for_change_of_config = []
    for item in all_interfaces:
        if item not in cdp_interfaces:
            list_for_change_of_config.append (item)
    return list_for_change_of_config
    #In this function we connect to a device and we make it's interfaces, which don't have cdp neighbors nonnegotiable
    #and access. This will prevent DTP Exploitation
def make_all_interfaces_nonnegotiate_and_accees(IP_address,username,password,enable_secret,interface_list):
    ssh_connection = netmiko.ConnectHandler(
        device_type = "cisco_ios",
        ip = IP_address,
        username = username,
        password = password,
        secret  = enable_secret,
    )
    ssh_connection.enable()
    ssh_connection.find_prompt() + "\n"
    ssh_connection.send_command("conf t")
    for item in interface_list:
        ssh_connection.send_command("int "+item)
        ssh_connection.send_command ("switchport mode access")
        ssh_connection.send_command ("switchport nonegotiate")
    ssh_connection.send_command ("end")
    ssh_connection.send_command("terminal length 0")
    ssh_connection.send_command("wr",delay_factor=2)
    #runnning-config will be shown to the user
    run = ssh_connection.send_command("show run",delay_factor=2)
    ssh_connection.send_command("terminal length 24")
    ssh_connection.disconnect()
    return run
def main():
    inventory_list = Ask_for_username_and_password()
    run_list = []
    for item in inventory_list:
        cdp_neighbor = Get_cdp_neighbors (item["IP"],item["Username"],item["Password"],item["Enable_secret"])
        list_of_interfaces_to_network_devices = parsing_info(cdp_neighbor[0])
        all_interfaces_on_device = all_interfaces_on_a_device(cdp_neighbor[1])
        interfaces_for_change = calculate_interfaces_for_changes(all_interfaces_on_device,list_of_interfaces_to_network_devices)
        run_list.append = make_all_interfaces_nonnegotiate_and_accees(item["IP"],item["Username"],item["Password"],item["Enable_secret"],interfaces_for_change)
    for item in run_list:
        print ("\n","""
            -------------------------------------------------------------------------------
            ""","\n",item)
main()
