import os
import socket
import time




PORT = 21


class Server:

    def __init__(self,host=None,port=None):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 21 if not port else port
        if not host:
            self.addr = (socket.gethostbyname(socket.gethosname()), port)
        else:
            self.addr = (socket.gethostbyname(host),port)
        self.sock.bind(0)


class Connection:

    def __init__(self,port=21):
        self.port = port
        self.connected = False
