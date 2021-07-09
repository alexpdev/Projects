import sys
import os
from ftplib import FTP, error_perm
import dotenv

home = "~"
local_dir = os.path.join("/home/asp","HDisk","sync")
remote_dir = "/storage/downloads/rtorrent"
local_contents = os.listdir(local_dir)


def get_path(client,path,parent):
    name = os.path.split(path[-1])
    try:
        s = client.size(path)
        local = os.path.join(parent,name)
        with open(local,"wb") as fp:
            client.retrbinary(f'RETR {path}', fp.write)
    except error_perm:
        lst = client.nlst(path)
        child = os.path.join(parent,name)
        os.mkdir(child)
        for p in lst:
            get_path(client,p, child)

    return

host = os.environ.get("host")
port = os.environ.get("port")
passwd = os.environ.get("passwd")
uname = os.environ.get("uname")


client = FTP()
client.login(host=host,port=port)
client.login(user=uname,passwd=passwd)
client.set_debuglevel(2)

remote_contents = client.nlst(remote_dir)
for path in remote_contents:
    pathname = os.path.split[-1]
    if pathname not in local_contents:
        get_path(client,pathname,local_dir)

print("complete")
