
import os
import string
from time import time
from pathlib import Path
import shutil
import atexit

ROOT = Path(__file__).parent / "TESTDIR"
os.mkdir(ROOT)
SEQ = (string.printable + string.whitespace).encode("utf-8")


def tempfile(path=None, exp=18):
    size = 2 ** exp
    if not path:
        path = ROOT / ("tfile" + str(time()))
    else:
        path = ROOT / path
    temp = path
    parts = []
    for _ in range(len(path.parts)):
        if os.path.exists(temp):
            break
        parts.append(temp.name)
        temp = temp.parent
    for part in parts[-1]:
        os.mkdir(temp / part)
        temp = temp / part
    seq = SEQ
    with open(path, "wb") as binfile:
        while size > 0:
            if len(seq) < size:
                binfile.write(seq)
                size -= len(seq)
                seq += seq
            else:
                binfile.write(seq[:size])
                size -= size
    return path


def rmpath(*args):
    if isinstance(args, (str, os.PathLike)):
        args = [args]
    for arg in args:
        if os.path.exists(arg):
            if os.path.isfile(arg):
                try:
                    os.remove(arg)
                except PermissionError:
                    pass
            else:
                try:
                    shutil.rmtree(arg)
                except PermissionError:
                    pass


@atexit.register
def teardown():
    try:
        shutil.rmdir(ROOT)
    except PermissionError:
        pass
