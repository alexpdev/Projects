#! /usr/bin/python3
# -*- coding: utf-8 -*-

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

import pytest
import os

from torrentfile import utils
from tests import context

@pytest.fixture(params=list(range(1, 6)))
def tempdir(request):
    path = context.mkfolder(request.param)
    yield path
    context.rmpath(path)


@pytest.mark.parametrize("value, expected", context.bytesizes())
def test_humanize_bytes(value, expected):
    assert utils.humanize_bytes(value) == expected  # nosec


@pytest.mark.parametrize("value", list(range(14, 26)))
def test_normalize_length_exp(value):
    assert utils.normalize_piece_length(value) == 2**value  # nosec


@pytest.mark.parametrize("value", ["16384", 32768, "1048576", "2097152", 8388608])
def test_normalize_length_str(value):
    assert utils.normalize_piece_length(value) == int(value)  # nosec


@pytest.mark.parametrize("value", ["4", 29, "a", 16000, "8000000"])
def test_normalize_length_fail(value):
    try:
        assert utils.normalize_piece_length(value) == 0  # nosec
    except utils.PieceLengthValueError:
        assert True  # nosec


@pytest.mark.parametrize("value", [i[0] for i in context.bytesizes()])
def test_get_piece_length(value):
    result = utils.get_piece_length(value)
    assert result % 16384 == 0 and result < 2**28


def test_filelist_total(tempdir):
    total, lst = utils.filelist_total(tempdir)
    assert sorted(lst) == lst and total > 0


def test_filelist_total_sum(tempdir):
    total, lst = utils.filelist_total(tempdir)
    amount = 0
    for filepath in lst:
        amount += os.path.getsize(filepath)
    assert total == amount


def test_path_size(tempdir):
    size = utils.path_size(tempdir)
    amount = 0
    for dirname, _, names in os.walk(tempdir, followlinks=True):
        for name in names:
            amount += os.path.getsize(os.path.join(dirname, name))
    assert size == amount


def test_get_file_list(tempdir):
    filelist, pathlist = utils.get_file_list(tempdir), []
    for dirname, _, names in os.walk(tempdir, followlinks=True):
        for name in names:
            path = os.path.join(dirname, name)
            pathlist.append(path)
    assert filelist == sorted(pathlist)


def test_path_stat(tempdir):
    tsize, flist = utils.filelist_total(tempdir)
    plength = utils.get_piece_length(tsize)
    assert utils.path_stat(tempdir) == (flist, tsize, plength)


def path_piece_length(tempdir):
    tsize, _ = utils.filelist_total(tempdir)
    plength = utils.get_piece_length(tsize)
    assert plength == utils.path_piece_length(tempdir)
