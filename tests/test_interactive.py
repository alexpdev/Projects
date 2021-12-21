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
"""Testing functions for the command line interface."""

import os
import sys

import pytest

import torrentfile
from tests import dir1, dir2, rmpath
from torrentfile.cli import main
from torrentfile.interactive import (edit_torrent, get_options_from_input,
                                     recheck_torrent)
from torrentfile.utils import MissingPathError


def alt_input(mapping):
    """Insert Dummy data intop class method."""

    def get_input(output, mapping=mapping):
        """Get dummy user input and return it."""
        for key, val in mapping.items():
            if key in output:
                return val
        return ""

    torrentfile.interactive.Options.get_input = get_input


def test_fix():
    """Test for unused imports."""
    assert dir1 and dir2


def test_interactive_empty():
    """Test interactive module with different parameters."""
    mapping = {"Content": "", "Action": "create"}
    alt_input(mapping)
    try:
        get_options_from_input()
    except MissingPathError:
        assert True


@pytest.mark.parametrize("action", ["recheck", "edit"])
def test_interactive_actions(action):
    """Test interactive module with different parameters."""
    mapping = {"Action": action}
    alt_input(mapping)
    get_options_from_input()
    assert True


@pytest.mark.parametrize("piece", [16, 18])
@pytest.mark.parametrize("private", ["Y", "N"])
@pytest.mark.parametrize("comment", ["this comment", "also this"])
@pytest.mark.parametrize("version", ["1", "2"])
@pytest.mark.parametrize("webseed", ["url1", "ftp2 ftp1"])
def test_interactive_options(
    dir1,
    piece,
    private,
    version,
    comment,
    webseed,
):
    """Test interactive module with different parameters."""
    outfile = dir1 + "1.torrent"
    mapping = {
        "Action": "create",
        "Content": str(dir1),
        "Piece": str(piece),
        "Private": private,
        "Comment": comment,
        "Version": version,
        "Web": webseed,
        "Output": outfile,
    }
    alt_input(mapping)
    get_options_from_input()
    assert os.path.exists(outfile)
    rmpath(outfile)


@pytest.mark.parametrize("piece", [18])
@pytest.mark.parametrize("source", ["this source"])
@pytest.mark.parametrize("version", ["3", "1"])
@pytest.mark.parametrize("announce", ["url4 url5"])
def test_inter_params1(dir2, piece, version, announce, source):
    """Test interactive module with different parameters."""
    outfile = str(dir2) + ".torrent"
    mapping = {
        "Action": "create",
        "Content": str(dir2),
        "Piece": str(piece),
        "Version": version,
        "Tracker": announce,
        "Source": source,
    }
    alt_input(mapping)
    get_options_from_input()
    assert os.path.exists(outfile)
    rmpath(outfile)


@pytest.mark.parametrize("piece", [15])
@pytest.mark.parametrize("version", ["1", "2", "3"])
@pytest.mark.parametrize("announce", ["url1", "http://a.b ftp://b.a"])
def test_interactive_cli(dir2, piece, version, announce):
    """Test interactive module with different parameters."""
    outfile = str(dir2) + ".torrent"
    mapping = {
        "Action": "create",
        "Content": str(dir2),
        "Piece": str(piece),
        "Version": version,
        "Tracker": announce,
    }
    alt_input(mapping)
    sys.argv[1:] = ["-i", "--private"]
    main()
    assert os.path.exists(outfile)
    rmpath(outfile)


def test_recheck_torrent():
    """Test recheck function."""
    assert recheck_torrent() is None


def test_edit_torrent():
    """Test edit function."""
    assert edit_torrent() is None
