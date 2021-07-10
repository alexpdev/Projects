import sys
import os
from os.path import abspath, dirname
sys.path.insert(0,dirname(dirname(abspath(__file__))))
from dotenv import LOAD_ENVIRONMENT_VARIABLES
LOAD_ENVIRONMENT_VARIABLES()
from ftp.client import Client

class TestClient:

    user = os.environ.get("user")
    passwd = os.environ.get("passwd")
    host = os.environ.get("host")
    port = 21

    def test_client_init(self):
        ftp = Client()
        assert ftp._encoding == "utf-8"

    def test_client_open(self):
        ftp = Client()
        ftp.open(host=self.host,port=self.port)
        assert ftp._host == self.host
        assert ftp._port == self.port

    def test_client_user(self):
        ftp = Client()
        ftp.open(host=self.host,port=self.port)
        ftp.user(user=self.user,passwd=self.passwd)
        assert ftp._host == self.host
        assert ftp._port == self.port
        assert ftp._user == self.user
        assert ftp._passwd == self.passwd

    def test_init_with_args(self):
        ftp = Client(host=self. host,user=self.user,
                    passwd=self.passwd, port=self.port)
        assert ftp._host == self.host
        assert ftp._port == self.port
        assert ftp._user == self.user
        assert ftp._passwd == self.passwd


    ftp = Client(host=host,user=user, passwd=passwd, port=port)

    def test_list_func(self):
        assert self.ftp.ls(".") != None
