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
"""Edit torrent meta file."""

import pyben

from .utils import normalize_piece_length


def edit_torrent(metafile, args):
    """
    Edit the properties of provided torrent meta file.

    Parameters
    ----------
    metafile : `str`
        path to an existing torrent meta file
    args : `dict`
        dictionary of meta file properties and their values
    """
    meta = pyben.load(metafile)
    info = meta["info"]
    print(args)

    if "piece_length" in args:
        info["piece length"] = normalize_piece_length(args["piece_length"])

    if "private" in args:
        if "private" in info:
            del info["private"]
        else:
            info["private"] = 1

    if "comment" in args:
        info["comment"] = args["comment"]

    if "source" in args:
        info["source"] = args["source"]

    if "url_list" in args:
        meta["url-list"] = args["url_list"].split(" ")

    if "announce" in args:
        alist = args["announce"].split(" ")
        meta["announce"] = alist[0]
        meta["announce list"] = [alist]

    meta["info"] = info
    pyben.dump(meta, metafile)
