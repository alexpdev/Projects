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
"""Testing functions for torrentfile module."""

import os
from pathlib import Path

import pytest

from tests.context import rmpath, testfile, mkfolder, Con
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2, utils
from torrentfile.torrent import MetaFile


@pytest.fixture(params=list(range(1, 6)))
def tdir(request):
    """Return temporary directory."""
    folder = mkfolder(request.param)
    return folder


@pytest.fixture()
def args():
    kwargs = {
        "announce": ["announce1", "announce2", "announce3"],
        "private": 1,
        "source": "source",
    }
    return kwargs


@pytest.fixture()
def smallfile():
    """Generate Sized file a tiny bit larger than BLOCK_SIZE."""
    path = testfile(exp=14)
    with open(path, "ab") as fd:
        fd.write(b"000000000000000")
    return path



def test_torrentfile_dir(tdir, args):
    """Test temporary directory."""
    print(tdir)
    print(args)
    args["path"] = tdir
    torrent = TorrentFile(**args)
    assert torrent.meta is not None  # nosec


def test_torrentfile_dir_private(tdir, args):
    """Test temporary dir with arguments."""
    args["path"] = tdir
    args["private"] = True
    args["piece_length"] = 1048576
    torrent = TorrentFile(**args)
    meta = torrent.meta
    assert "private" in meta["info"]  # nosec


def test_torrentfile_dir_comment(tdir, args):
    """Test temporary dir with arguments."""
    args["path"] = tdir
    args["private"] = True
    args["comment"] = "This is a comment"
    torrent = TorrentFile(**args)
    meta = torrent.meta
    assert "private" in meta["info"] and "comment" in meta["info"]  # nosec


def test_exception_path_error():
    """Test MissingPathError exception."""
    try:
        raise utils.MissingPathError("this is a message")
    except utils.MissingPathError:
        assert True  # nosec


def test_torrentfile_with_outfile(tdir, args):
    """Test TorrentFile class with output in kwargs."""
    outfile = tdir + ".torrent"
    args["path"] = tdir
    args["outfile"] = outfile
    torrent = TorrentFile(**args)
    torrent.write()
    assert os.path.exists(outfile)  # nosec


def test_torrentfile_write_outfile(tdir, args):
    """Test TorrentFile class with output in kwargs."""
    args["path"] = tdir
    outfile = tdir + ".torrent"
    torrent = TorrentFile(**args)
    torrent.write(outfile=outfile)
    assert os.path.exists(outfile)  # nosec


def test_torrentfilev2_outfile(tdir, args):
    """Test TorrentFile2 class with output as argument."""
    args["path"] = tdir
    outfile = tdir + ".torrent"
    torrent = TorrentFileV2(**args)
    torrent.write(outfile=outfile)
    assert os.path.exists(outfile)  # nosec


def test_torrentfilev2_with_outfile(tdir, args):
    """Test TorrentFileV2 class with output in kwargs."""
    args["path"] = tdir
    outfile = tdir + ".torrent"
    args["outfile"] = outfile
    torrent = TorrentFileV2(**args)
    torrent.write()
    assert os.path.exists(outfile)  # nosec


def test_hybrid_outfile(tdir, args):
    """Test Hybrid class with output as argument."""
    args["path"] = tdir
    outfile = tdir + ".torrent"
    torrent = TorrentFileHybrid(**args)
    torrent.write(outfile=outfile)
    assert os.path.exists(outfile)  # nosec


def test_hybrid_with_outfile(tdir, args):
    """Test Hybrid class with output in kwargs."""
    args["path"] = tdir
    outfile = tdir + ".torrent"
    args["outfile"] = outfile
    torrent = TorrentFileHybrid(**args)
    torrent.write()
    assert os.path.exists(outfile)  # nosec


def test_hybrid_0_length():
    """Test Hybrid with zero length file."""
    path = Path(Con.root) / "empty"
    path.touch()
    args = {
        "path": str(path),
        "announce": "announce",
    }
    torrent = TorrentFileHybrid(**args)
    assert torrent.meta["announce"] == "announce"  # nosec
    torrent.write()
    torpath = path.with_suffix(".torrent")
    assert os.path.exists(torpath)   # nosec


def test_v2_0_length():
    """Test TorrentFileV2 with zero length file."""
    path = Path(Con.root) / "empty"
    path.touch()
    args = {
        "path": str(path),
        "announce": "announce",
    }
    torrent = TorrentFileV2(**args)
    torrent.write()
    torpath = path.with_suffix(".torrent")
    assert os.path.exists(torpath)  # nosec


def test_metafile_assemble(tdir, args):
    """Test MetaFile assemble file Exception."""
    args["path"] = tdir
    meta = MetaFile(**args)
    try:
        meta.assemble()
    except NotImplementedError:
        assert True   # nosec


def test_hybrid_sized_file(smallfile):
    """Test pad_remaining function in hybrid FileHash class."""
    args = {"path": smallfile, "announce": "announce", "piece_length": 15}
    torrent = TorrentFileHybrid(**args)
    assert torrent.meta["announce"] == args["announce"]      # nosec
    assert torrent.meta["info"]["piece length"] == 2 ** 15   # nosec


def test_hybrid_under_block_sized():
    """Test pad_remaining function in hybrid FileHash class."""
    smallest = os.path.join(Con.root, "smallest")
    with open(smallest, "wb") as fd:
        letters = b"abcdefghijklmnopqrstuvwxyzABZDEFGHIJKLMNOPQRSTUVWXYZ"
        size = len(letters)
        while size < 16000:
            fd.write(letters)
            size += len(letters)
    args = {"path": smallest, "piece_length": 2**14}
    torrent = TorrentFileHybrid(**args)
    assert torrent.meta["info"]["piece length"] == 2 ** 14   # nosec


def maketorrent(args, v=None):
    """Torrent making factory."""
    if v not in [2, 3]:
        torrent = TorrentFile(**args)
    elif v == 2:
        torrent = TorrentFileV2(**args)
    elif v == 3:
        torrent = TorrentFileHybrid(**args)
    torrent.assemble()
    return torrent.write()


@pytest.fixture
def metav3d(tdir):
    """Return generated metadata v2 for directory."""
    args = {
        "private": True,
        "path": tdir,
        "announce": "http://announce.com/announce",
        "source": "tracker",
        "comment": "content details and purpose",
    }
    outfile, meta = maketorrent(args, v=3)
    return outfile, meta


@pytest.fixture
def metav2d(tdir):
    """Return generated metadata v2 for directory."""
    args = {
        "private": True,
        "path": tdir,
        "announce": "http://announce.com/announce",
        "source": "tracker",
        "comment": "content details and purpose",
    }
    outfile, meta = maketorrent(args, v=2)
    return outfile, meta


@pytest.fixture
def metav1d(tdir):
    """Return generated metadata v1 for directory."""
    args = {
        "private": True,
        "path": tdir,
        "announce": "http://announce.com/announce",
        "source": "tracker",
        "comment": "content details and purpose",
    }
    outfile, meta = maketorrent(args)
    return outfile, meta


@pytest.mark.parametrize('key', ["announce", "info", "piece layers",
                                 "creation date", "created by"])
def test_v2_meta_keys(metav2d, key):
    """Test metadata."""
    outfile, meta = metav2d
    assert key in meta  # nosec
    assert os.path.exists(outfile)  # nosec


@pytest.mark.parametrize('field', ["announce", "info", "piece layers",
                                   "creation date", "created by"])
def test_v3_meta_keys(metav3d, field):
    """Test metadata."""
    outfile, meta = metav3d
    assert field in meta  # nosec
    assert os.path.exists(outfile)  # nosec


@pytest.mark.parametrize('key', ["piece length", "meta version", "file tree",
                                 "name", "private", "source", "comment"])
def test_v2_info_keys_dir(metav2d, key):
    """Test metadata."""
    outfile, meta = metav2d
    assert key in meta["info"]  # nosec
    assert os.path.exists(outfile)  # nosec


@pytest.mark.parametrize('field', ["piece length", "meta version", "file tree",
                                   "name", "private", "source", "comment"])
def test_v3_info_keys_dir(metav3d, field):
    """Test metadata."""
    outfile, meta = metav3d
    assert field in meta["info"]  # nosec
    assert os.path.exists(outfile)  # nosec


@pytest.mark.parametrize('key', ["announce", "info",
                                 "creation date", "created by"])
def test_v1_meta_keys(metav1d, key):
    """Test metadata."""
    outfile, meta = metav1d
    assert key in meta  # nosec
    assert os.path.exists(outfile)  # nosec


@pytest.mark.parametrize('key', ["piece length", "name", "private",
                                 "source", "comment", "pieces"])
def test_v1_info_keys_dir(metav1d, key):
    """Test metadata."""
    outfile, meta = metav1d
    assert key in meta["info"]  # nosec
    assert os.path.exists(outfile)  # nosec


@pytest.mark.parametrize('key', ["piece length", "name", "private",
                                 "source", "comment", "pieces"])
def test_v3_info_keys_pieces(metav3d, key):
    """Test metadata."""
    outfile, meta = metav3d
    assert key in meta["info"]  # nosec
    assert os.path.exists(outfile)  # nosec


def test_meta_no_args_v2():
    """Test construct TorrentFileV2 with no arguments."""
    try:
        assert TorrentFileV2(private=True)   # nosec
    except utils.MissingPathError:
        assert True  # nosec


def test_meta_no_args_v1():
    """Test construct TorrentFile with no arguments."""
    try:
        assert TorrentFile(announce="url")   # nosec
    except utils.MissingPathError:
        assert True  # nosec
