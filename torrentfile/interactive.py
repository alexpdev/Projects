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

import pyben

from .edit import edit_torrent
from .torrent import TorrentFile, TorrentFileHybrid, TorrentFileV2
from .utils import humanize_bytes, normalize_piece_length


def get_input(*args):
    """
    Determine appropriate input function to call.

    Parameters
    ----------
    args : `tuple`
        Arbitrary number of args to pass to next function

    Returns
    -------
    `str`
        The results of the function call.
    """
    if len(args) == 2:
        return _get_input_loop(*args)
    return _get_input(*args)


def _get_input(txt):
    """
    Gather information needed from user.

    Parameters
    ----------
    txt : `str`
        The message usually containing instructions for the user.

    Returns
    -------
    `str`
        The text input received from the user.
    """
    value = input(txt)
    return value


def _get_input_loop(txt, func):
    """
    Gather information needed from user.

    Parameters
    ----------
    txt : `str`
        The message usually containing instructions for the user.
    func : function
        Validate/Check user input data, failure = retry, success = continue.

    Returns
    -------
    `str`
        The text input received from the user.
    """
    while True:
        value = input(txt)
        if func and func(value):
            return value
        if not func or value == "":
            return value
        showtext(f"Invalid input {value}: try again")


def showtext(txt):
    """
    Print contents of txt to screen.

    Parameters
    ----------
    txt : `str`
        text to print to terminal.
    """
    sys.stdout.write(txt)


def showcenter(txt):
    """
    Prints text to screen in the center position of the terminal.

    Parameters
    ----------
    txt : `str`
        the preformated message to send to stdout.
    """
    termlen = shutil.get_terminal_size().columns
    padding = " " * ((termlen - len(txt)) / 2)
    string = "".join(["\n", padding, txt, "\n"])
    showtext(string)


def select_action():
    """Operate TorrentFile program interactively through terminal."""
    showcenter("TorrentFile: Starting Interactive Mode")
    action = get_input(
        "Enter the action you wish to perform.\n"
        "Action (Create | Edit | Recheck): "
    )
    if action.lower() == "create":
        create_torrent()
    elif action.lower() == "recheck":
        recheck_torrent()
    else:
        edit_action()


def recheck_torrent():
    """Check torrent download completed percentage."""
    print(os.getcwd())


def create_torrent():
    """Create new torrent file interactively."""
    showcenter("Create Torrent")
    showtext(
        "\nEnter values for each of the options for the torrent creator, "
        "or leave blank for program defaults.\nSpaces are considered item "
        "seperators for options that accept a list of values.\nValues "
        "enclosed in () indicate the default value, while {} holds all "
        "valid choices available for the option.\n\n"
    )
    InteractiveCreator()


def edit_action():
    """Edit the editable values of the torrent meta file."""
    showcenter("Edit Torrent")
    metafile = get_input("Metafile(.torrent): ", os.path.exists)
    dialog = InteractiveEditor(metafile)
    dialog.show_current()
    dialog.edit_props()


class InteractiveEditor:
    """Interactive dialog class for torrent editing."""

    def __init__(self, metafile):
        """
        Initialize the Interactive torrent editor guide.

        Parameters
        ----------
        metafile : `str`
            user input string identifying the path to a torrent meta file.
        """
        self.metafile = metafile
        self.meta = pyben.load(metafile)
        self.info = self.meta["info"]
        if "announce list" in self.meta:
            self.announce = self.meta["announce list"]
        else:
            self.announce = self.meta.get("announce", None)
        self.piece_length = self.info.get("piece length")
        self.comment = self.info.get("comment", None)
        self.source = self.info.get("source", None)
        self.private = self.info.get("private", None)
        self.url_list = self.meta.get("url-list", None)
        self.name = self.info.get("name")
        self.labels = {
            "piece length": "piece_length",
            "comment": "comment",
            "source": "source",
            "private": "private",
            "tracker": "announce",
            "webseed": "url_list",
        }

    def show_current(self):
        """Display the current met file information to screen."""
        out = "Current properties and values:\n"
        longest = max([len(label) for label in self.labels]) + 3
        for key, val in self.labels.items():
            val = self.__getattribute__(val)
            txt = (key.title() + ":").ljust(longest)
            if key == "trackers":
                if isinstance(val, str):
                    txt += self.announce
                else:
                    txt += " ".join([url for grp in val for url in grp])
            elif key == "web-seeds":
                txt += " ".join(val)
            elif key == "piece length":
                txt += humanize_bytes(val)
            else:
                txt += str(val)
            out += f"\t{txt}\n"
        sys.stdout.write(out)

    def sanatize_response(self, key, response):
        """
        Convert the input data into a form recognizable by the program.

        Parameters
        ----------
        key : `str`
            name of the property and attribute being eddited.
        response : `str`
            User input value the property is being edited to.
        """
        if key in ["announce", "url_list"]:
            val = response.split()
        elif key == "piece_length":
            val = normalize_piece_length(response)
        elif key == "private":
            if self.private:
                val = None
            else:
                val = 1
        else:
            val = response
        self.__setattr__(key, val)

    def edit_props(self):
        """Loop continuosly for edits until user signals DONE."""
        while True:
            showcenter(
                "Choose the number for a propert the needs editing."
                "Enter DONE when all editing has been completed."
            )
            props = {
                1: "comment",
                2: "source",
                3: "private",
                4: "tracker",
                5: "webseed",
                6: "piece length",
            }
            txt = ", ".join((str(k) + ": " + v) for k, v in props.items())
            prop = get_input(txt)
            if prop.lower() == "done":
                break
            if prop.isdigit() and 0 < int(prop) < 7:
                label = props[int(prop)]
                key = self.labels[label]
                val = self.__getattribute__(key)
                showtext(
                    "Enter new property value or leave empty for no value."
                )
                response = get_input(f"{key} ({val}): ")
                self.sanatize_response(key, response)
            else:
                showtext("Invalid input: Try again.")
        args = {
            "announce": self.announce,
            "piece_length": self.piece_length,
            "comment": self.comment,
            "source": self.source,
            "private": self.private,
            "url_list": self.url_list,
        }
        edit_torrent(self.metafile, args)

    def write_metafile(self):
        """Overwrite the metafile with newly edited information."""
        self.meta["announce list"] = [self.announce]
        self.meta["announce"] = self.announce[0]

        if self.url_list:
            self.meta["url-list"] = self.url_list
        elif "url-list" in self.meta:
            del self.meta["url-list"]

        if self.private:
            self.info["private"] = 1
        else:
            del self.info["private"]

        self.info["piece length"] = self.piece_length

        if self.comment:
            self.info["comment"] = self.comment
        elif "comment" in self.info:
            del self.info["comment"]

        if self.source:
            self.info["source"] = self.source
        elif "source" in self.info:
            del self.info["source"]

        self.meta["info"] = self.info

        pyben.dump(self.meta, self.metafile)


class InteractiveCreator:
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

    def __init__(self):
        """Initialize interactive meta file creator dialog."""
        self.kwargs = {
            "announce": None,
            "url_list": None,
            "private": None,
            "source": None,
            "comment": None,
            "piece_length": None,
            "outfile": None,
            "path": None,
        }
        self.get_props()

    def get_props(self):
        """Gather details for torrentfile from user."""
        piece_length = get_input(
            "Piece Length (empty=auto): ", lambda x: x.isdigit()
        )
        self.kwargs["piece_length"] = piece_length
        announce = get_input(
            "Tracker list (empty): ", lambda x: isinstance(x, str)
        )
        if announce:
            self.kwargs["announce"] = announce.split()
        url_list = get_input(
            "Web Seed list (empty): ", lambda x: isinstance(x, str)
        )
        if url_list:
            self.kwargs["url_list"] = url_list.split()
        comment = get_input("Comment (empty): ", None)
        if comment:
            self.kwargs["comment"] = comment
        source = get_input("Source (empty): ", None)
        if source:
            self.kwargs["source"] = source
        private = get_input(
            "Private Torrent? {Y/N}: (N)", lambda x: x in "yYnN"
        )
        if private and private.lower() == "y":
            self.kwargs["private"] = 1
        contents = get_input("Content Path: ", os.path.exists)
        self.kwargs["path"] = contents
        outfile = get_input(
            f"Output Path ({contents}.torrent): ",
            lambda x: os.path.exists(os.path.dirname(x)),
        )
        if outfile:
            self.kwargs["outfile"] = outfile
        meta_version = get_input(
            "Meta Version {1,2,3}: (1)", lambda x: x in "123"
        )

        showcenter(f"creating {outfile}")

        if meta_version == "3":
            torrent = TorrentFileHybrid(**self.kwargs)
        elif meta_version == "2":
            torrent = TorrentFileV2(**self.kwargs)
        else:
            torrent = TorrentFile(**self.kwargs)
        torrent.write()
