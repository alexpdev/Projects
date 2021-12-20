#! /usr/bin/python3
# -*- coding: utf-8 -*-

#####################################################################
# THE SOFTWARE IS PROVIDED AS IS WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN commentION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#####################################################################
"""
Module contains the procedures used for Interactive Mode.

Functions
---------
`program_Options`
    gather program behaviour Options.
"""

import os
import shutil
import sys

from .torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from .utils import MissingPathError


def get_options_from_input():
    """Operate TorrentFile program interactively through terminal."""
    printheader("TorrentFile: Starting Interactive Mode\n")

    action = Options.interaction(
        "Enter the action you wish to perform.\n"
        "Action (Create | Edit | Recheck): ",
        lambda x: x.lower() in ["create", "edit", "recheck"],
    )

    if action.lower() == "create":
        create_torrent()

    elif action.lower() == "recheck":
        recheck_torrent()

    else:
        edit_torrent()


def edit_torrent():
    """Edit the editable values of the torrent meta file."""
    print(os.getcwd())


def recheck_torrent():
    """Check torrent download completed percentage."""
    print(os.getcwd())


def printheader(header):
    """Print the header text to the terminal.

    Parameters
    ----------
    header : `str`
        Heading text describing the new section.
    """
    sys.stdout.write("\n")
    termlen = shutil.get_terminal_size().columns
    padding = (termlen - len(header)) / 2
    sys.stdout.write(" " * int(padding) + header + "\n")


def create_torrent():
    """Create new torrent file interactively."""
    printheader("\nCreate Torrent\n")
    Options.reset()
    sys.stdout.write(
        "\nEnter values for each of the options for the torrent creator, "
        "or leave blank for program defaults.\nSpaces are considered item "
        "seperators for options that accept a list of values.\nValues "
        "enclosed in () indicate the default value, while {} holds all "
        "valid choices available for the option.\n\n"
    )

    piece_length = Options.interaction(
        "Piece Length (auto-calculated): ", lambda x: x.isdigit()
    )
    if piece_length:
        Options.set_piece_length(piece_length)

    announce = Options.interaction(
        "Tracker list (empty): ", lambda x: isinstance(x, str)
    )
    if announce:
        Options.set_announce(announce)

    url_list = Options.interaction(
        "Web Seed list (empty): ", lambda x: isinstance(x, str)
    )
    if url_list:
        Options.set_url_list(url_list)

    comment = Options.interaction("\nComment (empty): ", None)
    if comment:
        Options.set_comment(comment)

    source = Options.interaction("\nSource (empty): ", None)
    if source:
        Options.set_source(source)

    private = Options.interaction(
        "Private Torrent? {Y/N}: (N)",
        lambda x: x.isalpha() and x in "yYnN",
    )
    if private and private.lower() == "y":
        Options.set_private()

    contents = Options.interaction("Content Path: ", os.path.exists)
    Options.set_path(contents)

    outfile = Options.interaction(
        f"Output Path ({contents}.torrent): ",
        lambda x: os.path.exists(os.path.dirname(x)),
    )
    if outfile:
        Options.set_outfile(outfile)

    meta_version = Options.interaction(
        "Meta Version {1,2,3}: (1)", lambda x: x in "123"
    )

    printheader(f"creating {outfile}")
    kwargs = Options.items()
    if meta_version == "3":
        torrent = TorrentFileHybrid(**kwargs)
    elif meta_version == "2":
        torrent = TorrentFileV2(**kwargs)
    else:
        torrent = TorrentFile(**kwargs)
    torrent.write()


class Options:
    """Class namespace for interactive program options.

    Attributes
    ----------
    _piece_length : int
    _comment : str
    _source : str
    _url_list : list
    _path : str
    _outfile : str
    _announce : str
    _announce_list : list
    """

    _announce = None
    _comment = None
    _outfile = None
    _path = None
    _piece_length = None
    _private = None
    _source = None
    _url_list = None

    @classmethod
    def reset(cls):
        """Reset all options to empty."""
        for func in [
            cls.set_announce,
            cls.set_comment,
            cls.set_outfile,
            cls.set_path,
            cls.set_piece_length,
            cls.set_source,
            cls.set_url_list,
        ]:
            func(None)
        cls.unset_private()

    @classmethod
    def set_announce(cls, announce):
        """Set the announce attribute inside Options namespace.

        Parameters
        ----------
        announce : `str`
            The new value for Options.announce.
        """
        if isinstance(announce, str) and len(announce) > 0:
            cls._announce = announce.strip().split()
        else:
            cls._announce = announce

    @classmethod
    def set_comment(cls, comment):
        """Set the comment attribute inside Options namespace.

        Parameters
        ----------
        comment : `str`
            The new value for Options.comment.
        """
        cls._comment = comment

    @classmethod
    def set_outfile(cls, outfile):
        """Set the outfile attribute inside Options namespace.

        Parameters
        ----------
        outfile : `str`
            The new value for Options.outfile.
        """
        if isinstance(outfile, str) and len(outfile) > 0:
            cls._outfile = outfile
        elif outfile is None:
            cls._outfile = outfile

    @classmethod
    def set_path(cls, path):
        """Set the path attribute inside Options namespace.

        Parameters
        ----------
        path : `str`
            The new value for Options.path.
        """
        if path is None:
            cls._path = path
        elif path == "" or not os.path.exists(path):
            raise MissingPathError
        else:
            cls._path = path

    @classmethod
    def set_piece_length(cls, piece_length):
        """Set the piece_length attribute inside Options namespace.

        Parameters
        ----------
        piece_length : `str`
            The new value for Options.piece_length.
        """
        if isinstance(piece_length, str) and len(piece_length) > 0:
            cls._piece_length = int(piece_length)
        else:
            cls._piece_length = piece_length

    @classmethod
    def set_private(cls):
        """Set the private attribute inside Options namespace."""
        cls._private = 1

    @classmethod
    def unset_private(cls):
        """Unset the private attribute inside Options namespace."""
        cls._private = None

    @classmethod
    def set_source(cls, source: str):
        """Set the source attribute inside Options namespace.

        Parameters
        ----------
        source : `str`
            The new value for Options.source.
        """
        cls._source = source

    @classmethod
    def set_url_list(cls, url_list: str):
        """Set the url_list attribute inside Options namespace.

        Parameters
        ----------
        url_list : `str`
            The new value for Options.url_list.
        """
        if isinstance(url_list, str):
            cls._url_list = url_list.strip().split()
        else:
            cls._url_list = url_list

    @classmethod
    def _get_input(cls, arg: str) -> str:
        """Return user input."""
        return input(arg)  # pragma: no cover

    get_input = _get_input

    @classmethod
    def items(cls) -> dict:
        """Create a dictionary out of the class attributes and values.

        Returns
        -------
        `dict`
            Keyword arguments for any of the TorrentFile classes.
        """
        return {
            "announce": cls._announce,
            "comment": cls._comment,
            "outfile": cls._outfile,
            "path": cls._path,
            "piece_length": cls._piece_length,
            "private": cls._private,
            "source": cls._source,
            "url_list": cls._url_list,
        }

    @classmethod
    def interaction(cls, output: str, key=None) -> str:
        """Interact with user to get input values.

        Parameters
        ----------
        output : str
            The text input prompt with defaults or examples.
        key : function | None
            function that accepts one parameter, and outputs `True` if
            users input passes the function test otherwise it returns false
            and asks the user if they want to try again.

        Returns
        -------
        str
            Program option value received as input for user.
        """
        while True:
            response = cls.get_input(output)
            if not response or not key or key(response):
                break
            answer = cls.get_input(
                f"Invalid response ({response}): Try Again? (Y/N): "
            )  # pragma: no cover
            if not answer.lower().startswith("y"):  # pragma: no cover
                sys.exit(1)
        return response
