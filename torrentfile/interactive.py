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


def program_options():
    """Operate TorrentFile program interactively through terminal."""
    printheader("TorrentFile: Starting Interactive Mode\n")

    action = Options.interaction(
        "Please enter the action you wish to perform.\n"
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
        Options.piece_length = piece_length

    announce = Options.interaction(
        "Tracker list (empty): ", lambda x: isinstance(x, str)
    )
    if announce:
        Options.announce_list = announce.split()

    url_list = Options.interaction(
        "Web Seed list (empty): ", lambda x: isinstance(x, str)
    )
    if url_list:
        Options.url_list = url_list.split()

    comment = Options.interaction("\nComment (empty): ", None)
    if comment:
        Options.comment = comment

    source = Options.interaction("\nSource (empty): ", None)
    if source:
        Options.source = source

    private = Options.interaction(
        "Private Torrent? {Y/N}: (N)",
        lambda x: x.isalpha() and x.lower() in ["y", "n"],
    )
    if private and private.lower() == "y":
        Options.private = 1

    contents = Options.interaction("Content Path: ", os.path.exists)
    if not contents:
        raise MissingPathError
    Options.path = contents

    outfile = Options.interaction(
        f"Output Path ({contents}.torrent): ",
        lambda x: os.path.exists(os.path.dirname(x)),
    )
    if outfile:
        Options.outfile = outfile

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
    piece_length : int
    comment : str
    source : str
    url_list : list
    path : str
    outfile : str
    announce : str
    announce_list : list
    """

    announce = None
    comment = None
    outfile = None
    path = None
    piece_length = None
    private = None
    source = None
    url_list = None

    @classmethod
    def items(cls) -> dict:
        """Create a dictionary out of the class attributes and values.

        Returns
        -------
        dict
            Keyword arguments for any of the TorrentFile classes.
        """
        return {
            "announce": cls.announce,
            "comment": cls.comment,
            "outfile": cls.outfile,
            "path": cls.path,
            "piece_length": cls.piece_length,
            "private": cls.private,
            "source": cls.source,
            "url_list": cls.url_list,
        }

    @classmethod
    def _get_input(cls, arg: str) -> str:
        """Return user input."""
        return input(arg)

    get_input = _get_input

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
            )
            if not answer.lower().startswith("y"):
                sys.exit(1)  # pragma: no cover
        return response
