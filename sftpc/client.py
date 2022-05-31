import sys
from types import Any
import os
import time
import logging
import paramiko


logging.basicConfig(level=logging.DEBUG)

class Client:

    def __init__(self, username=None, password=None, host=None, port=None):
        self.local = os.path.abspath(os.getcwd())
        self._user = username
        self._pass = password
        self.host = host
        self.port = port
        self.controller = None
        self.transport = None
        self.remote = None

    def set_credentials(self, username, password):
        self._user = username
        self._pass = password

    def connect(self, host=None, port=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = int(port)
        else:
            self.port = int(self.port)
        transport = paramiko.Transport((self.host, self.port))
        self.transport = transport
        self.transport.connect(username=self._user, password=self._pass)
        self.controller = self.transport.open_sftp_client()

    def __getattribute__(self, __name: str) -> Any:
        if __name not in dir(self):
            return self.controller.__getattribute__(__name)
        else:
            return self.__getattr__(__name)
