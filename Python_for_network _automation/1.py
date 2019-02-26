import os
directory_list = []
i=0
for dirname, dirnames, filenames in os.walk('.'):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        directory = (os.path.join(dirname, subdirname))
        i+=1
        directory_list.append ([i,os.path.join(dirname,subdirname)])
print (directory_list)
