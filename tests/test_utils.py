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
"""Utility functions and classes used throughout package.

Functions:
  get_piece_length: calculate ideal piece length for torrent file.
  sortfiles: traverse directory in sorted order yielding paths encountered.
  path_size: Sum the sizes of each file in path.
  get_file_list: Return list of all files contained in directory.
  path_stat: Get ideal piece length, total size, and file list for directory.
  path_piece_length: Get ideal piece length based on size of directory.
"""

import math
import os
from pathlib import Path

import pytest

from tests import rmpath, tempfile
from torrentfile import utils

@pytest.fixture(scope="module")
def dir1():
    files = ["folder1/folder2/file1.png", "folder1/folder2/file2.zip",
             "folder1/folder3/file3.mp4", "folder1/folder3/file4.m4a"]
    paths = []
    for fd in files:
        paths.append(tempfile(fd))
    return os.path.commonpath(paths)






@pytest.mark.parametrize("size", [156634528, 2**30, 67987, 16384, 8563945])
def test_get_piece_length(size):
    value = utils.get_piece_length(size)
    assert value % 1024 == 0


@pytest.mark.parametrize("size", [156634528, 2**30, 67987, 16384, 8563945])
def test_get_piece_length_max(size):
    value = utils.get_piece_length(size)
    assert value < 2**27


@pytest.mark.parametrize("size", [156634528, 2**30, 67987, 16384, 8563945])
def test_get_piece_length_min(size):
    value = utils.get_piece_length(size)
    assert value >= 2**14


def test_get_path_length_mod(tdir1):
    assert utils.path_piece_length(tdir1) % (2**16) == 0


def test_get_path_length_min(tdir1):
    assert utils.path_piece_length(tdir1) >= (2**16)


def test_get_path_length_max(tdir1):
    assert utils.path_piece_length(tdir1) <= (2**27)


def test_path_stat(tdir1):
    filelist, totalsize, piece_length = utils.path_stat(tdir1)
    assert piece_length % (2**16) == 0


def test_path_stat_size(tdir1):
    filelist, totalsize, piece_length = utils.path_stat(tdir1)
    assert totalsize == (2**18) * 4

def test_path_stat_filelist_size(tdir1):
    filelist, totalsize, piece_length = utils.path_stat(tdir1)
    assert len(filelist) == 4


def test_get_filelist(tdir1):
    filelist = utils.get_filelist(tdir1)
    assert len(filelist) == 4


def test_get_path_size(tdir1):
    pathsize = utils.path_size(tdir1)
    assert pathsize == (2**18) * 4


def test_filelist_total(tdir1):
    total, filelist = utils.filelist_total(tdir1)
    assert total == (2**18) * 4
