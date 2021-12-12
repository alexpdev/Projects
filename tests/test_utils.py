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

from tests import dir1
from torrentfile import utils


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


def test_get_path_length_mod(dir1):
    assert utils.path_piece_length(dir1) % (2**14) == 0


def test_get_path_length_min(dir1):
    assert utils.path_piece_length(dir1) >= (2**14)


def test_get_path_length_max(dir1):
    assert utils.path_piece_length(dir1) <= (2**27)


def test_path_stat(dir1):
    _, _, piece_length = utils.path_stat(dir1)
    assert piece_length % (2**14) == 0


def test_path_stat_size(dir1):
    _, totalsize, _ = utils.path_stat(dir1)
    assert totalsize == (2**18) * 4

def test_path_stat_filelist_size(dir1):
    filelist, _, _ = utils.path_stat(dir1)
    assert len(filelist) == 4


def test_get_filelist(dir1):
    filelist = utils.get_file_list(dir1)
    assert len(filelist) == 4


def test_get_path_size(dir1):
    pathsize = utils.path_size(dir1)
    assert pathsize == (2**18) * 4


def test_filelist_total(dir1):
    total, _ = utils.filelist_total(dir1)
    assert total == (2**18) * 4


def test_piecelengthvalueerror():
    try:
        raise utils.PieceLengthValueError("message")
    except utils.PieceLengthValueError:
        assert True


def test_missingpatherror():
    try:
        raise utils.MissingPathError("message")
    except utils.MissingPathError:
        assert True


@pytest.mark.parametrize("amount, result", [(100, "100"), (1100, "1 KiB"),
                                            (1_100_000, "1 MiB"),
                                            (1_100_000_000, "1 GiB")])
def test_humanize_bytes(amount, result):
    assert utils.humanize_bytes(amount) == result
