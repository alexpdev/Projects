import os
import shutil
from datetime import datetime
from pathlib import Path
import atexit

import pytest

def tempfile(path=None, exp=18):
    root = Path(__file__).parent / "TESTDIR"
    if not os.path.exists(root):
        os.mkdir(root)
    if not path:
        path = root / (str(datetime.timestamp(datetime.now()))  + ".file")
    parts = Path(path).parts
    partial = root
    for i, part in enumerate(parts):
        if i == len(parts) - 1:
            with open(partial / part, "wb") as binfile:
                binfile.write(bytes(2**exp))
        else:
            partial = partial / part
            if not os.path.exists(partial):
                os.mkdir(partial)
    return partial


def rmpath(*args):
    if isinstance(args, str):
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


def tempdir1():
    files = [
        "dir1/file1.png",
        "dir1/file2.mp4",
        "dir1/file3.mp3",
        "dir1/file4.zip"
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
    root = tempdir1()
    yield root
    rmpath(root)
