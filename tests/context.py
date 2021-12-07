#####################################################################
# THE SOFTWARE IS PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#####################################################################
"""Helper functions for the testing suite."""

import os
import sys
import time
import shutil
import atexit
import string
import random
from pathlib import Path
from datetime import datetime

KIB = 2**10
MIB = 2**20
GIB = 2**30
TIB = 2**40


def bytesizes():
    """Return test cases and expected values for bytesizes."""
    cases = [
        (var, str(var)) for var in
        [random.randint(0, KIB) for _ in range(100)]
    ] + [
        (var, str(var // KIB) + " KiB") for var in
        [random.randint(KIB + 1, MIB) for _ in range(100)]
    ] + [
        (var, str(var // MIB) + " MiB") for var in
        [random.randint(MIB + 1, GIB) for _ in range(100)]
    ] + [
        (var, str(var // GIB) + " GiB") for var in
        [random.randint(GIB + 1, TIB) for _ in range(100)]
    ]
    return cases


def rmpath(paths):
    """Recursively remove path."""
    if isinstance(paths, (os.PathLike, str)):
        paths = [paths]
    no_errors = True
    for path in [p for p in paths if os.path.exists(p)]:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        except PermissionError:  # pragma: no cover
            no_errors = False
            continue
    return no_errors


def gen_seq():
    seq = list(string.printable + string.whitespace)
    random.shuffle(seq)
    return "".join(seq)


class Con:
    """Holds universal testing variables."""

    _parent = os.path.dirname(os.path.abspath(__file__))
    root = os.path.join(_parent, "TESTDIR")
    if os.path.exists(root):
        rmpath(root)
    os.mkdir(root)
    seq = gen_seq()
    padding = bytearray(1024)
    folders = {
        1: [("subdir1", ".png"), ("subdir1", ".zip"), ("subdir1", ".mp4"), ("subdir1", ".mp3"), ("subdir1", ".bin")],
        2: [(".svg"), (".rar"), (".r01"), (".doc"), (".xyz")],
        3: [("subdir1", ".jpg"), ("subdir1", ".tar"),
            ("subdir2", ".mp4"), ("subdir2", ".m4a")],
        4: [(".subdir", ".conf"), (".subdir", ""), (".PNG")],
        5: [("subdir1", "subdir2", "subdir3", "subdir4", ".7z")]
    }
    history = []


def stamp():
    """Return current time as timestamp."""
    return str(datetime.timestamp(datetime.now()))


def mkfolder(folder):
    """Create temporary folder structure and its parts.

    Parameters
    ----------
    folder : `dict` or `int`
        Directory structure or a reference to a directory structure.
    """
    if isinstance(folder, int) and folder < 6:
        folderint = folder
        folder = Con.folders[folder]
    root = os.path.join(Con.root, f"Folder{folderint}_{stamp()}")
    os.mkdir(root)
    Con.history.append(root)
    for parts in folder:
        last, path = len(parts) - 1, root
        for i, part in enumerate(parts):
            if i == last:
                path = os.path.join(path, "file" + part)
                if os.path.exists(path):
                    rmpath(path)
                testfile(path=path, exp=random.randint(14, 21))
            else:
                path = os.path.join(path, part)
                if not os.path.exists(path):
                    os.mkdir(path)
    return root


def testfile(path=None, exp=20):
    """Construct testfile out of given arguments.

    Parameters
    ----------
    path : `str`, optional
        files location in filesystem, by default None
    exp : int, optional
        exponent for power of 2, by default 20

    Returns
    -------
    `str`
        location on filesystem.
    """
    if not path:
        path = os.path.join(Con.root, "file" + stamp())
    size = 2 ** exp
    seq = Con.seq.encode("utf-8")
    binfile = open(path, "wb")
    while size > 0:
        if len(seq) > size:
            binfile.write(seq[:size])
            size -= size
        else:
            binfile.write(seq)
            size -= len(seq)
            seq *= 2
    binfile.close()
    Con.history.append(path)
    while len(Con.history) > 15:
        rmpath(Con.history[0])
        del Con.history[0]
    assert os.path.exists(path)  # nosec
    return path


@atexit.register()
def teardown(times=0):
    if times <= 3:
        try:
            rmpath(Con.root)
        except PermissionError:  # pragma: no cover
            time.sleep(1)
            sys.stderr.write("Sleeping")
            teardown(times+1)
