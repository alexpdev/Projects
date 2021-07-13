import sys
import os
from os.path import abspath, dirname
sys.path.insert(0,dirname(dirname(abspath(__file__))))

from ftp import dotenv


class TestDotenv:

    def test_get_caller_path(self):
        path = dotenv.path_to_file()
        thisfile = abspath(__file__)
        assert path == __file__

    def test_discover(self):
        dotenv.discover()
        assert os.environ.get("host") == self.host
        assert os.environ.get("user") == self.user
        assert os.environ.get("passwd") == self.passwd
