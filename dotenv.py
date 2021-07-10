import os
from pathlib import Path
import inspect

development = False

class NoDotenv(Exception):
    pass

def load_env(path):
    with open(str(path),"rt") as fp:
        envargs = fp.read()
    lines = envargs.split("\n")
    for line in lines:
        split = line.split("=")
        if len(split) == 2:
            key, val = split
            os.putenv(key, val)

def discover():
    mfile = Path(inspect.stack()[1].filename)
    hierarchy = list(mfile.parents)
    for parent in hierarchy:
        if ".env" in os.listdir(parent):
            return load_env(parent / ".env")
    os.putenv("ENVTEST","1")

LOAD_ENVIRONMENT_VARIABLES = discover
