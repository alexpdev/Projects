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
"""Test main module functionality."""

import os
import sys
from datetime import datetime

import pytest

from tests.context import Con, rmpath, testfile
from torrentfile import TorrentFile, TorrentFileHybrid, TorrentFileV2
from torrentfile import main_script as main


@pytest.fixture(params=list(range(14, 26)))
def tfile(request):
    """Create fixture for tests."""
    t_file = testfile(exp=request.param)
    args = [
        "torrentfile",
        "--private",
        "--announce",
        "https://tracker1.to/announce",
        "--source",
        "TFile",
        t_file
    ]
    return args, t_file


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_func(tfile, version):
    """Test main script function."""
    args, _ = tfile
    opath = os.path.join(Con.root, "test.torrent")
    sys.argv = args + ["-o", opath, "--meta-version", version]
    main()
    assert os.path.exists(opath)   # nosec


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_announce_list(tfile, version):
    """Test main function with announce list flag."""
    args, _ = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "https://tracker3/announce",
        "https://tracker4/announce",
        "--meta-version",
        version,
    ]
    parser = main()
    url = "https://tracker4/announce"
    announce_list = parser.meta["announce list"]
    seq = [item for sub in announce_list for item in sub]
    assert url in seq  # nosec


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_annlist_single(tfile, version):
    """Test main function with announce list flag."""
    args, _ = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "--meta-version",
        version
    ]
    parser = main()
    assert os.path.exists(parser.outfile)   # nosec


@pytest.mark.parametrize("creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid])
def test_class_with_annlist(tfile, creator):
    """Test TorrentFile Class with announce list arguement."""
    _, path = tfile
    kwargs = {
        "path": path,
        "announce": (
            "https://tracker1.to/announce",
            "https://tracker2/announce",
            "https://tracker3/announce",
            "https://tracker4/announce",
        )
    }
    torrent = creator(**kwargs)
    url = "https://tracker3/announce"
    announce_list = torrent.meta["announce list"]
    seq = [item for sub in announce_list for item in sub]
    assert url in seq  # nosec


@pytest.mark.parametrize("creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid])
def test_class_tuple_annlist(tfile, creator):
    """Test TorrentFile Class with tuple announce list arguement."""
    _, path = tfile
    kwargs = {
        "path": path,
        "announce": (
            "https://tracker1.to/announce",
            "https://tracker2/announce",
            "https://tracker3/announce",
            "https://tracker4/announce",
        )
    }
    torrent = creator(**kwargs)
    url = "https://tracker3/announce"
    announce_list = torrent.meta["announce list"]
    seq = [item for sub in announce_list for item in sub]
    assert url in seq  # nosec


@pytest.mark.parametrize("creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid])
def test_class_list_annlist(tfile, creator):
    """Test TorrentFile Class with tuple announce list arguement."""
    _, path = tfile
    kwargs = {
        "path": path,
        "announce": [
            "https://tracker1.to/announce",
            "https://tracker2/announce",
            "https://tracker3/announce",
            "https://tracker4/announce",
        ],
    }
    torrent = creator(**kwargs)
    url = "https://tracker2/announce"
    announce_list = torrent.meta["announce list"]
    seq = [item for sub in announce_list for item in sub]
    assert url in seq  # nosec


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_annlist_v2(tfile, version):
    """Test main function with announce list flag."""
    args, path = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "https://tracker3/announce",
        "https://tracker4/announce",
        "--meta-version",
        version,
    ]
    parser = main()
    url = "https://tracker2/announce"
    assert url in parser.meta["announce"]  # nosec
    rmpath(parser.outfile)


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_source_matches(tfile, version):
    """Test main function with announce list flag."""
    args, path = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "https://tracker3/announce",
        "https://tracker4/announce",
        "--meta-version",
        version,
        "--source",
        "tracker"
    ]
    parser = main()
    assert parser.meta["info"]["source"] == "tracker"  # nosec


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_source_single(tfile, version):
    """Test main function with announce list flag."""
    args, path = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "--meta-version",
        version,
        "--source",
        "tracker"
    ]
    parser = main()
    assert "source" in parser.meta["info"]  # nosec


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_annlist_single_v3(tfile, version):
    """Test main function with announce list flag."""
    args, path = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "--meta-version",
        version,
        "--comment",
        "Some kind of commment"
    ]
    parser = main()
    assert "comment" in parser.meta["info"] or parser.meta


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_main_created_by_flag(tfile, version):
    """Test main function with announce list flag."""
    args, path = tfile
    sys.argv = args + [
        "-a",
        "https://tracker2/announce",
        "--meta-version",
        version,
    ]
    parser = main()
    assert "TorrentFile" in parser.meta["created by"]  # nosec


@pytest.mark.parametrize("creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid])
def test_class_timestamps(tfile, creator):
    """Test TorrentFile Class with announce list arguement."""
    _, path = tfile
    kwargs = {
        "path": path,
        "announce": (
            "https://tracker1.to/announce",
            "https://tracker2/announce",
            "https://tracker3/announce",
            "https://tracker4/announce",
        ),
    }
    torrent = creator(**kwargs)
    timestamp = torrent.meta["creation date"]
    ts = datetime.fromtimestamp(float(timestamp))
    now = datetime.now()
    assert (ts.day, ts.month, ts.year) == (now.day, now.month, now.year)  # nosec


@pytest.mark.parametrize("creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid])
def test_class_tuple_annlist_private(tfile, creator):
    """Test TorrentFile Class with tuple announce list arguement."""
    _, path = tfile
    kwargs = {
        "path": path,
        "private": 1,
        "announce": (
            "https://tracker1.to/announce",
            "https://tracker2/announce",
            "https://tracker3/announce",
            "https://tracker4/announce",
        ),
    }
    torrent = creator(**kwargs)
    assert "private" in torrent.meta["info"]  # nosec


@pytest.mark.parametrize("creator", [TorrentFile, TorrentFileV2, TorrentFileHybrid])
def test_class_list_annlist_v(tfile, creator):
    """Test TorrentFile Class with tuple announce list arguement."""
    _, path = tfile
    kwargs = {
        "path": path,
        "announce": [
            "https://tracker1.to/announce",
            "https://tracker2/announce",
            "https://tracker3/announce",
            "https://tracker4/announce",
        ],
    }
    torrent = creator(**kwargs)
    url = "https://tracker2/announce"
    announce_list = torrent.meta["announce list"]
    seq = [item for sub in announce_list for item in sub]
    assert url in seq  # nosec


@pytest.mark.parametrize("hasher", [TorrentFileV2, TorrentFileHybrid])
def test_class_single_file_small(hasher):
    """Test when single file is slightly larger than piece length."""
    path = testfile(exp=15)
    with open(path, "ab") as binfile:
        binfile.write((Con.seq * 2).encode("utf-8"))
    args = {
        "path": path,
        "piece_length": 15,
        "source": "example1"
    }
    torrent = hasher(**args)
    tpath, _ = torrent.write()
    assert os.path.exists(tpath)   # nosec
