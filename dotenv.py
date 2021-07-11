import os
from pathlib import Path
import inspect

development = False

env = os.environ

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

def path_to_file():
    mfile = Path(inspect.stack()[1].filename)
    return mfile


def discover():
    mfile = Path(inspect.stack()[1].filename)
    cwd = Path(".").resolve()
    hierarchy = list(mfile.parents)
    for parent in hierarchy:
        if ".env" in os.listdir(parent):
            load_env(parent / ".env")
            break
    os.putenv("ENVTEST","1")

LOAD_ENVIRONMENT_VARIABLES = discover
