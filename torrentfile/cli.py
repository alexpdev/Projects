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
"""
Command Line Interface for TorrentFile project.

This module provides the primary command line argument parser for
the torrentfile package. The main_script function is automatically
invoked when called from command line, and parses accompanying arguments.

Functions:
    main_script: process command line arguments and run program.
"""

import logging
import sys
from argparse import ArgumentParser, HelpFormatter

import torrentfile

from .recheck import Checker
from .torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from .interactive import program_options


class HelpFormat(HelpFormatter):
    """Formatting class for help tips provided by the CLI.

    Parameters
    ----------
    prog : `str`
        Name of the program.
    width : `int`
        Max width of help message output.
    max_help_positions : `int`
        max length until line wrap.
    """

    def __init__(self, prog: str, width=75, max_help_pos=40):
        """Construct HelpFormat class."""
        super().__init__(prog, width=width, max_help_position=max_help_pos)

    def _split_lines(self, text, _):
        """Split multiline help messages and remove indentation."""
        lines = text.split("\n")
        return [line.strip() for line in lines if line]


def main_script(args=None):
    """Initialize Command Line Interface for torrentfile.

    Parameters
    ----------
    args : `list`
        Commandline arguments. default=None
    """
    if not args:
        args = sys.argv[1:]

    desc = (
        "Terminal based tool for creating, checking, or editing "
        "Bittorrent meta(.torrent) files. TorrentFile supports "
        "all meta file versions including hybrid files."
    )

    parser = ArgumentParser(
        "TorrentFile",
        description=desc,
        prefix_chars="-",
        formatter_class=HelpFormat,
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"torrentfile v{torrentfile.__version__}",
        help="show program version and exit",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="debug",
        help="output debug information",
    )

    parser.add_argument(
        "-p",
        "--private",
        action="store_true",
        dest="private",
        help="create file for private tracker",
    )

    parser.add_argument(
        "-s",
        "--source",
        action="store",
        dest="source",
        metavar="<source>",
        help="specify source tracker",
    )

    parser.add_argument(
        "-c",
        "--comment",
        action="store",
        dest="comment",
        metavar="<comment>",
        help="include a comment in file metadata",
    )

    parser.add_argument(
        "-o",
        "--out",
        action="store",
        dest="outfile",
        metavar="<path>",
        help="output path for created .torrent file",
    )

    parser.add_argument(
        "--meta-version",
        default="1",
        choices=["1", "2", "3"],
        action="store",
        dest="meta_version",
        metavar="<int>",
        help="""
        Bittorrent metafile version.
        Options = 1, 2 or 3.
        (1) = Bittorrent v1 (Default)
        (2) = Bittorrent v2
        (3) = Bittorrent v1 & v2 hybrid
        """,
    )

    parser.add_argument(
        "--piece-length",
        action="store",
        dest="piece_length",
        metavar="<int>",
        help="""
        Fixed amount of bytes for each chunk of data. (Default: None)
        Acceptable input values include integers 14-24, which
        will be interpreted as the exponent for 2^n, or any perfect
        power of two integer between 16Kib and 16MiB (inclusive).
        Examples:: [--piece-length 14] [-l 20] [-l 16777216]
        """,
    )

    parser.add_argument(
        "-t",
        "--tracker",
        action="store",
        dest="announce",
        metavar="<url>",
        nargs="+",
        default="",
        help="""
        One or more Bittorrent tracker announce url(s).
        Examples:: [-a url1 url2 url3]  [--anounce url1]
        """,
    )

    parser.add_argument(
        "-w",
        "--web-seed",
        action="store",
        dest="url_list",
        metavar="<url>",
        nargs="+",
        help="""
        One or more url(s) linking to a http server hosting
        the torrent contents.  This is useful if the torrent
        tracker is ever unreachable. Example:: [-w url1 [url2 [url3]]]
        """,
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        dest="interactive",
        help="""
        Activates Interactive Mode. Causes all other command line flags
        are ignored. User will respond to a series of prompts to specify
        program options.
        """
    )

    parser.add_argument(
        "-r",
        "--check",
        "--recheck",
        dest="checker",
        metavar="<.torrent>",
        help="""
        Activates the torrent checker mode.
        <.torrent> is the path to a torrent meta file.
        Check <content> data integrity with <.torrent> file.
        If this is active, all other options are ignored (except --debug)
        Ex:: :~$ torrentfile -r path/to/file.torrent path/to/contents
        """,
    )

    parser.add_argument(
        "content",
        action="store",
        metavar="<content>",
        nargs="?",
        help="path to content file or directory",
    )

    if not args:
        args = ["-h"]
    flags = parser.parse_args(args)

    if flags.debug:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    tlogger = logging.getLogger("tlogger")
    tlogger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(prog)s %(asctime)s %(message)s",
        datefmt="%m-%d-%Y %H:%M:%S",
        style="%",
    )

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)
    tlogger.addHandler(handler)

    if flags.interactive:
        return program_options()

    if flags.checker:
        tlogger.debug("Program as entered Recheck mode.")
        metafile = flags.checker
        content = flags.content
        tlogger.debug("Checking %s against %s contents", metafile, content)
        checker = Checker(metafile, content)
        tlogger.debug("Completed initialization of the Checker class")
        result = checker.results()
        tlogger.info("Final result for %s recheck:  %s", metafile, result)
        sys.stdout.write(str(result))
        sys.stdout.flush()
        return result

    kwargs = {
        "url_list": flags.url_list,
        "path": flags.content,
        "announce": flags.announce,
        "piece_length": flags.piece_length,
        "source": flags.source,
        "private": flags.private,
        "outfile": flags.outfile,
        "comment": flags.comment,
    }

    tlogger.debug("Program has entered torrent creation mode.")
    if flags.meta_version == "2":
        torrent = TorrentFileV2(**kwargs)
    elif flags.meta_version == "3":
        torrent = TorrentFileHybrid(**kwargs)
    else:
        torrent = TorrentFile(**kwargs)
    tlogger.debug("Completed torrent files meta info assembly.")
    outfile, meta = torrent.write()
    parser.kwargs = kwargs
    parser.meta = meta
    parser.outfile = outfile
    tlogger.debug("New torrent file (%s) has been created.", str(outfile))
    return parser


def main():
    """Initiate main function for CLI script."""
    main_script()
