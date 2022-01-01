import os
from pathlib import Path
import inspect

def load_env(path):
    with open(str(path),"rt") as fp:
        envargs = fp.read()
    lines = envargs.split("\n")
    for line in lines:
        split = line.split("=")
        if len(split) == 2:
            key, val = split
            os.environ[key] = val

def path_to_file():
    mfile = inspect.stack()[1].filename
    return Path(mfile)

def discover():
    mfile = path_to_file()
    hierarchy = list(mfile.parents)
    for parent in hierarchy:
        if ".env" in os.listdir(parent):
            load_env(parent / ".env")
            break

LOAD_ENVARS = discover
