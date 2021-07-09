import os

fp = open(".env","rt")
lines = fp.read().split("\n")
fp.close()
for line in lines:
    key, value = line.split("=")
    os.environ[key] = value
