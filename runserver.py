import os
from ftp.ftpd import runserver


user = "user"
passwd = "1234"
home = os.path.abspath("./home")

runserver(user,passwd,home)
