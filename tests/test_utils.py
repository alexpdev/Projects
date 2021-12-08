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
