from cryptography.fernet import Fernet
from tabulate import tabulate
import os
import sys
from os import walk
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
# Path of the backup's folder
path = "/Users/alextoktosunov/Documents/GitHub/Network programmability/Python_for_network _automation"
dirs = os.listdir( path )
file_list = []
i=0
for file in dirs:
    # this code print folder files that were created by script "Get_running_config.py"
    if ("running_config" in file) and (file != "Get_running_config.py"):
       i+=1
       file_list.append ([i,file])
    else:
        print ("No Files was found in directory")
        sys.exit
        break
print (tabulate(file_list, headers=["#","File_Name"],tablefmt="rst"))
print (file_list[0][1])
user_choise = int(input("Введите номер файла для расшифровки"))
file = open(file_list[user_choise-1][1], "r")
file_content = file.read()
print (file)
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
token = f.decrypt(file_content)
print (token)