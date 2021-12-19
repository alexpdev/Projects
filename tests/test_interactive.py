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

import datetime
import os
import sys
import shutil
from pathlib import Path

import pyben
import pytest

from tests import dir1, dir2, rmpath
from torrentfile.cli import main
import torrentfile
from torrentfile.interactive import program_options, create_torrent, printheader, recheck_torrent, edit_torrent

def get_input(output, arg=None):
    if "Action" in output:
        return "create"
    if "Piece" in output:
        return "18"
    if "Path" in output:
        return arg
    return ""

torrentfile.interactive.Options.get_input = get_input


def test_interactive_program_options(dir1):
    outfile = str(dir1) + ".torrent"
    program_options()
    assert os.path.exists(outfile)
