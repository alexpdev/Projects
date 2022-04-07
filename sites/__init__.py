from pathlib import Path
import os
import sys

def dotenv():
    current_path = Path(__file__).resolve()
    root, tail = os.path.splitdrive(current_path)
    env_vars = {}
    while str(current_path) != root:
        current_path = current_path.parent
        if ".env" in os.listdir():
            envfile = open(current_path / ".env","rt")
            for line in envfile.readlines():
                key, value = line.split("=")
                env_vars[key] = value
    for k,v in env_vars.items():
        sys.environ[k] = v
    return
