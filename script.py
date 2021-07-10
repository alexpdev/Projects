import os
from time import time
from ftplib import FTP, error_perm
import dotenv
dotenv.load_environment()
assert os.environ.get('ENVTEST') == 1

then = time()
host = os.environ.get("HOST")
port = int(os.environ.get("PORT"))
auth = os.environ.get("AUTH")
user = os.environ.get("USER")
remote = os.environ.get("REMOTE")
local = os.environ.get("LOCAL")

client = FTP()

def syncremote(client,remote,local):
    contents = os.listdir(local)
    for path in client.nlst(remote):
        name = os.path.split(path)[-1]
        if name not in contents:
            get_path(client,path,local)
        else:
            lpath = os.path.join(local,name)
            if os.path.isdir(lpath):
                find_incomplete(client,path,lpath)
    return "Completed"

def find_incomplete(client,remote,local):
    lst = os.listdir(local)
    for item in client.nlst(remote):
        name = os.path.basename(item)
        if name in lst:
            path = os.path.join(local,name)
            if os.path.isdir(path):
                find_incomplete(client,item,path)
        else:
            get_path(client, item, local)



def get_path(client,path,parent):
    name = os.path.split(path)[-1]
    try:
        s = client.size(path)
        local = os.path.join(parent,name)
        with open(local,"wb") as fp:
            client.retrbinary(f'RETR {path}', fp.write)
    except error_perm:
        client.dir(path)
        lst = client.nlst(path)
        child = os.path.join(parent,name)
        os.mkdir(child)
        for p in lst:
            get_path(client,p, child)


if __name__ == "__main__":
    client.set_debuglevel(1)
    client.connect(host=host,port=port)
    client.login(user=user,passwd=auth)
    client.pwd()
    client.dir()
    syncremote(client,remote,local)
    now = time()
    print("Time to complete ", now - then)
