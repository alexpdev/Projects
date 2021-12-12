import os
import shutil
from datetime import datetime
from pathlib import Path
import string
import atexit

import pytest

def tempfile(path=None, exp=18):
    seq = (string.printable + string.whitespace).encode("utf-8")
    root = Path(__file__).parent / "TESTDIR"
    if not os.path.exists(root):
        os.mkdir(root)
    if not path:
        path = root / (str(datetime.timestamp(datetime.now()))  + ".file")
    parts = Path(path).parts
    partial = root
    for i, part in enumerate(parts):
        partial = partial / part
        if i == len(parts) - 1:
            with open(partial, "wb") as binfile:
                size = 2**exp
                while size > 0:
                    if len(seq) < size:
                        binfile.write(seq)
                        size -= len(seq)
                        seq += seq
                    else:
                        binfile.write(seq[:size])
                        size -= size
        else:
            if not os.path.exists(partial):
                os.mkdir(partial)
    return partial


def rmpath(*args):
    if isinstance(args, (str, os.PathLike)):
        args = [args]
    for arg in args:
        if not os.path.exists(arg):
            continue
        if os.path.isdir(arg):
            try:
                shutil.rmtree(arg)
            except PermissionError:
                pass
        elif os.path.isfile(arg):
            try:
                os.remove(arg)
            except PermissionError:
                pass


def tempdir(ext="1"):
    files = [
        f"dir{ext}/file1.png",
        f"dir{ext}/file2.mp4",
        f"dir{ext}/file3.mp3",
        f"dir{ext}/file4.zip"
        ]
    paths = []
    for path in files:
        temps = tempfile(path=path, exp=18)
        paths.append(temps)
    return os.path.commonpath(paths)


@atexit.register
def teardown():
    root = Path(__file__).parent / "TESTDIR"
    if os.path.exists(root):
        rmpath(root)


@pytest.fixture(scope="package")
def dir1():
    root = tempdir()
    yield root
    rmpath(root)

@pytest.fixture
def dir2():
    root = tempdir(ext="2")
    yield root
    rmpath(root)
