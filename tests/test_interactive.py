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

# import os
# import sys

# import pytest

# import torrentfile
# from tests import dir1, dir2, rmpath
# from torrentfile.cli import main
# from torrentfile.interactive import select_action, recheck_torrent
# from torrentfile.utils import MissingPathError


# @pytest.fixture(scope="function")
# def metafile(dir2):
#     out = str(dir2) + "t.torrent"
#     sys.argv = [
#         "torrentfile", "create", dir2, -0, out,
#         "--comment", "Some comment", "--source",
#         "Source1", "-t", "url1", "url2", "url3",
#         "--private", "-w", "ftp1", "url3"
#     ]
#     main()
#     yield out
#     rmpath(out)


# def input_map(mapping):
#     """Insert Dummy data intop class method."""

#     def get_input(output, mapping=mapping):
#         """Get dummy user input and return it."""
#         for key, val in mapping.items():
#             if key in output:
#                 return val
#         return ""

#     torrentfile.interactive.Options.get_input = get_input


# def input_iter(seq):
#     def get_input(output):
#         val = next(seq)
#         yield val
#         print(output, val)
#     torrentfile.interactive.Options.get_input = get_input


# def test_fix():
#     """Test for unused imports."""
#     assert dir1 and dir2


# def test_inter_empty():
#     """Test interactive module with different parameters."""
#     mapping = {"Content": "", "Action": "create"}
#     input_map(mapping)
#     try:
#         select_action()
#     except MissingPathError:
#         assert True


# @pytest.mark.parametrize("action", ["recheck"])
# def test_inter_actions(action):
#     """Test interactive module with different parameters."""
#     mapping = {"Action": action}
#     input_map(mapping)
#     select_action()
#     assert True


# @pytest.mark.parametrize("piece", [16, 18])
# @pytest.mark.parametrize("private", ["Y", "N"])
# @pytest.mark.parametrize("comment", ["this comment", "also this"])
# @pytest.mark.parametrize("version", ["1", "2"])
# def test_inter_options(dir1, piece, private, version, comment):
#     """Test interactive module with different parameters."""
#     outfile = dir1 + "1.torrent"
#     mapping = {
#         "Action": "create",
#         "Content": str(dir1),
#         "Piece": str(piece),
#         "Private": private,
#         "Comment": comment,
#         "Version": version,
#         "Output": outfile,
#     }
#     input_map(mapping)
#     select_action()
#     assert os.path.exists(outfile)
#     rmpath(outfile)


# @pytest.mark.parametrize("piece", [18, 22])
# @pytest.mark.parametrize("source", ["this source", ""])
# @pytest.mark.parametrize("version", ["3", "1"])
# @pytest.mark.parametrize("announce", ["url4 url5 url6", "url"])
# def test_inter_params1(dir2, piece, version, announce, source):
#     """Test interactive module with different parameters."""
#     outfile = str(dir2) + ".torrent"
#     mapping = {
#         "Action": "create",
#         "Content": str(dir2),
#         "Piece": str(piece),
#         "Version": version,
#         "Tracker": announce,
#         "Source": source,
#     }
#     input_map(mapping)
#     select_action()
#     assert os.path.exists(outfile)
#     rmpath(outfile)


# @pytest.mark.parametrize("piece", [15, 19])
# @pytest.mark.parametrize("version", ["1", "2", "3"])
# @pytest.mark.parametrize("announce", ["url1", "http://a.b ftp://b.a"])
# @pytest.mark.parametrize("webseed", ["url1", "ftp2 ftp1"])
# def test_interactive_cli(dir2, piece, version, announce, webseed):
#     """Test interactive module with different parameters."""
#     outfile = str(dir2) + ".torrent"
#     mapping = {
#         "Action": "create",
#         "Content": str(dir2),
#         "Piece": str(piece),
#         "Version": version,
#         "Tracker": announce,
#         "Web": webseed
#     }
#     input_map(mapping)
#     sys.argv[1:] = ["-i"]
#     main()
#     assert os.path.exists(outfile)
#     rmpath(outfile)


# def test_recheck_torrent():
#     """Test recheck function."""
#     assert recheck_torrent() is None


# @pytest.mark.parametrize("comment", ["", "some comment"])
# def test_edit_torrent(metafile):
#     """Test edit function."""
#     seq = ["edit", metafile, ]
