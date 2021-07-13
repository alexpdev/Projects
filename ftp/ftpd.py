import pyftpdlib
# documentation @ https://pyftpdlib.readthedocs.io/en/latest/

import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def runserver(user,passwd):
    ftp_root = "/ftp_root"
    user_dir = os.path.join(ftp_root,user)
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
    auth = DummyAuthorizer()
    auth.add_user(user, passwd, user_dir, perm="elradfmwMT")
    handler = FTPHandler
    handler.authorizer = auth
    handler.banner = "BOO!"
    handler.passive_ports = range(2000,2250)
    server = FTPServer(("",20),handler)
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    server.serve_forever()
