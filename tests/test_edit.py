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
"""Testing the edit torrent feature."""

import pyben
import pytest

from tests import dir1, dir2, rmpath
from torrentfile.edit import edit_torrent
from torrentfile.torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from torrentfile.utils import normalize_piece_length


def torrents():
    """Return seq of torrentfile objects."""
    return [TorrentFile, TorrentFileV2, TorrentFileHybrid]


@pytest.fixture(scope="function", params=torrents())
def meta1(dir1, request):
    """Create a standard metafile for testing."""
    args = {
        "path": dir1,
        "announce": "https://tracker1.org/announce https://tracker2.net/ann",
        "private": 1,
        "comment": "this is a comment",
        "source": "SomeSource",
        "piece_length": "18",
        "url_list": "www.someurl.net ftp://othersite.lua",
    }
    torrent_class = request.param
    torrent = torrent_class(**args)
    outfile, _ = torrent.write()
    yield outfile


def test_fix():
    """Testing dir fixtures."""
    assert dir2 and dir1


@pytest.mark.parametrize("announce", ["https://other.org/announce", ""])
def test_edit_torrent_announce(meta1, announce):
    """Test edit torrent function with announce."""
    outfile = meta1
    args = {
        "announce": announce,
    }
    edit_torrent(outfile, args)
    info = pyben.load(outfile)
    assert info["announce"] == announce
    rmpath(outfile)


@pytest.mark.parametrize("private", [1, 1])
def test_edit_torrent_private(meta1, private):
    """Test edit torrent function with private."""
    outfile = meta1
    args = {
        "private": private,
    }
    edit_torrent(outfile, args)
    data = pyben.load(outfile)
    try:
        assert "private" not in data["info"]
    except KeyError:
        assert data["info"]["private"] == private
    rmpath(outfile)


@pytest.mark.parametrize("source", ["", "othersource"])
def test_edit_torrent_source(meta1, source):
    """Test edit torrent function with source."""
    outfile = meta1
    args = {
        "source": source,
    }
    edit_torrent(outfile, args)
    meta = pyben.load(outfile)
    assert meta["info"]["source"] == source
    rmpath(outfile)


@pytest.mark.parametrize("comment", ["Nocomment", ""])
def test_edit_torrent_comment(meta1, comment):
    """Test edit torrent function with comment."""
    outfile = meta1
    args = {
        "comment": comment,
    }
    edit_torrent(outfile, args)
    meta = pyben.load(outfile)
    assert meta["info"]["comment"] == comment
    rmpath(outfile)


@pytest.mark.parametrize("url_list", ["item1 item2", "item5"])
def test_edit_torrent_urllist(meta1, url_list):
    """Test edit torrent function with url-list."""
    outfile = meta1
    args = {
        "url_list": url_list,
    }
    edit_torrent(outfile, args)
    meta = pyben.load(outfile)
    assert meta["url-list"] == url_list.split()
    rmpath(outfile)


@pytest.mark.parametrize("piece_length", ["18", "19", "25", "16384"])
def test_edit_torrent_piecelength(meta1, piece_length):
    """Test edit torrent function with piece length."""
    outfile = meta1
    args = {
        "piece_length": piece_length,
    }
    plen = normalize_piece_length(piece_length)
    edit_torrent(outfile, args)
    meta = pyben.load(outfile)
    assert meta["info"]["piece length"] == plen
    rmpath(outfile)
