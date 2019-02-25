from netmiko import ConnectHandler
from cryptography.fernet import Fernet
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import time
import hashlib
# this function gets running config
def Get_running_config(IP_address,username,password,enable_secret):
    ssh_connection = ConnectHandler(
        device_type = "cisco_ios",
        ip = IP_address,
        username = username,
        password = password,
        secret  = enable_secret,
    )
    ssh_connection.enable()
    result = ssh_connection.find_prompt() + "\n"
    result += ssh_connection.send_command("terminal length 0", delay_factor=2)
    running_config = ssh_connection.send_command("show run", dealay_factor = 2)
    ssh_connection.send_command("terminal length 24", delay_factor=2)
    ssh_connection.disconnect()
    print (running_config)
    return running_config
    # this function creates dictionary with passwords and IP addresses
def Ask_for_username_and_password():
    yes_or_no = input ("Are all username and passwords are the same? print 'yes' or 'no'")
    if yes_or_no == "yes" or yes_or_no == "Yes":
        username = input ("Enter username ")
        password = input ("Enter password ")
        enable_secret = input ("Enter enable_password ")
        intventory_list = [
            # you must add here ip addresses of the devices int the following manner
        {"IP":"10.1.1.1","Username":username,"Password":password,"Enable_secret":enable_secret},
        {"IP":"10.1.1.2","Username":username,"Password":password,"Enable_secret":enable_secret},
        {"IP":"10.1.1.3","Username":username,"Password":password,"Enable_secret":enable_secret}
        ]    
        return intventory_list
def main ():
    inventory_list = Ask_for_username_and_password()
    for item in inventory_list:
        running_config = Get_running_config (item["IP"],item["Username"],item["Password"],item["Enable_secret"])
    #Encryption part
        password_for_encryption = input ("Enter password for encrypting backups: ")
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_for_encryption))
        f = Fernet(key)
    #Write encrypted running config into file with date and time
        name_of_the_file = item["IP"]+"_"+time.asctime( time.localtime(time.time()) )
        token = f.encrypt(running_config)
        file = open (name_of_the_file+".txt","w+")
        file.write = token

main()