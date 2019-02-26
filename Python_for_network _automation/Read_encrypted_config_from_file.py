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
import binascii
import codecs
# Path of the backup's folder
def Select_directory():
    directory_list = []
    i=0
    for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
        for subdirname in dirnames:
            i+=1
            directory_list.append ([i,os.path.join(dirname,subdirname)])
    print (directory_list)
    return directory_list
def Ask_user_to_choose_directory(aDirectory_list):
    print (tabulate(aDirectory_list,headers=["#","Folder"],tablefmt="rst"))
    choosed_folder = int(input("Enter directory number of the desired folder: "))
    path_to_folder = aDirectory_list[choosed_folder-1][1]
    print (path_to_folder)
    return path_to_folder
directory_list = Select_directory()
path = Ask_user_to_choose_directory(directory_list)

dirs = os.listdir( path )
file_list = []
i=0
print (dirs)
for item in dirs:
    # this code print folder files that were created by script "Get_running_config.py"
    
    i+=1
    file_list.append ([i,item])
    
print (tabulate(file_list, headers=["#","File_Name"],tablefmt="rst"))
print (file_list[0][1])
user_choise = int(input("Enter number of file to decrypt it: "))
file = open(path+"/"+file_list[user_choise-1][1], "r")
file_content = file.read().encode()
print (file_content)
password_for_encryption = input ("Enter password for encrypting backups: ")
password_for_encryption_bytes = password_for_encryption.encode()
#This part of the code was taken from https://warsang.ovh/taking-bytes-as-input-in-python3/
# This code transfers input salt from string to bytes
salt_string = input('Please input salt bytes string such as \xca\xfe\xba\xbe >>> ')
def to_string(bytes_string) :
    return bytes_string.decode('ISO-8859-1')

def to_bytes(string) :
    return string.encode('ISO-8859-1')
def input_fix(string):
    return codecs.decode(string,"unicode_escape")
string_of_bytes = input_fix(salt_string)
print(" <---- String of bytes to bytesstring --->\n ")
salt_bytes = to_bytes(string_of_bytes)
#salt = b'*\xed2\xf1l\x16\xe0\x82\xc0p\xa7\xc5bPm.'
#This peace of the code decrypts the data with help of salt and password
print (salt_bytes)
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt_bytes,
    iterations=100000,
    backend=default_backend()
    )
key = base64.urlsafe_b64encode(kdf.derive(password_for_encryption_bytes))
f = Fernet(key)
token = f.decrypt(file_content)
token_string = token.decode()
print (token_string)