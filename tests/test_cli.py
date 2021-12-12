import os
import sys
import datetime

import pytest
import pyben

from tests import dir1, rmpath
from torrentfile.cli import main


def test_cli_v1(dir1):
    args = ["torrentfile", str(dir1)]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")
    rmpath(str(dir1) + ".torrent")


def test_cli_v2(dir1):
    args = ["torrentfile", str(dir1), "--meta-version", "2"]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")
    rmpath(str(dir1) + ".torrent")


def test_cli_v3(dir1):
    args = ["torrentfile", str(dir1), "--meta-version", "3"]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")
    rmpath(str(dir1) + ".torrent")


def test_cli_private(dir1):
    args = ["torrentfile", str(dir1), "--private"]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert "private" in meta["info"]
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_piece_length(dir1, piece_length, version):
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["info"]["piece length"] == piece_length
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_announce(dir1, piece_length, version):
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "--tracker", "https://announce.org/tracker"]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["announce"] == "https://announce.org/tracker"
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_announce_list(dir1, version):
    trackers = [
        "https://announce.org/tracker",
        "https://announce.net/tracker",
        "https://tracker.net/announce"
    ]
    args = [
        "torrentfile",
        str(dir1),
        "--meta-version",
        version,
        "--tracker"
    ] + trackers
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    for url in trackers:
        assert url in [j for i in meta["announce list"] for j in i]
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_comment(dir1, piece_length, version):
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "--comment", "this is a comment"]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert meta["info"]["comment"] == "this is a comment"
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_outfile(dir1, piece_length, version):
    outfile = str(dir1) + "test.torrent"
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "-o", outfile]
    sys.argv = args
    main()
    assert os.path.exists(outfile)
    rmpath(outfile)


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_creation_date(dir1, piece_length, version):
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "--comment", "this is a comment"]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    num = float(meta["creation date"])
    date = datetime.datetime.fromtimestamp(num)
    now = datetime.datetime.now()
    assert (date.day, date.month, date.year) == (now.day, now.month, now.year)
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_created_by(dir1, piece_length, version):
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "--comment", "this is a comment"]
    sys.argv = args
    main()
    meta = pyben.load(str(dir1) + ".torrent")
    assert "TorrentFile" in meta["created by"]
    rmpath(str(dir1) + ".torrent")


@pytest.mark.parametrize("piece_length", [2**exp for exp in range(14, 21)])
@pytest.mark.parametrize("version", ["1", "2", "3"])
def test_cli_with_debug(dir1, piece_length, version):
    args = ["torrentfile", str(dir1), "--piece-length",
            str(piece_length), "--meta-version", version,
            "--comment", "this is a comment", "-d"]
    sys.argv = args
    main()
    assert os.path.exists(str(dir1) + ".torrent")
    rmpath(str(dir1) + ".torrent")


def test_cli_help():
    args = ["-h"]
    sys.argv = args
    try:
        main()
    except:
        assert True
