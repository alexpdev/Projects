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
"""Module container Checker Class.

The CheckerClass takes a torrentfile and tha path to it's contents.
It will then iterate through every file and directory contained
and compare their data to values contained within the torrent file.
Completion percentages will be printed to screen for each file and
at the end for the torrentfile as a whole.
"""

import logging
import math
import os
from hashlib import sha1  # nosec

import pyben
from tqdm import tqdm

from .hasher import HasherV2, HasherHybrid
from .utils import humanize_bytes

SHA1 = 20
SHA256 = 32


class Checker:
    """Check a given file or directory to see if it matches a torrentfile.

    Public constructor for Checker class instance.

    Parameters
    ----------
      metafile (`str`): Path to ".torrent" file.
      location (`str`): Path where the content is located in filesystem.

    Example
    -------
        >> metafile = "/path/to/torrentfile/content_file_or_dir.torrent"
        >> location = "/path/to/location"
        >> os.path.exists("/path/to/location/content_file_or_dir")
        Out: True
        >> checker = Checker(metafile, location)
    """

    _hook = None

    def __init__(self, metafile, path):
        """Validate data against hashes contained in .torrent file.

        Parameters
        ----------
            metafile (`str`): path to .torrent file
            path (`str`): path to content or contents parent directory.
        """
        self._result = None
        self.meta_version = None
        self.metafile = metafile
        self.last_log = None
        self.log_msg("Checking: %s, %s", metafile, path)
        self.info = self.parse_metafile()
        self.name = self.info["name"]
        self.piece_length = self.info["piece length"]
        self.root = self.find_root(path)
        self.total = 0
        self.paths = []
        self.fileinfo = {}
        self.check_paths()

    @classmethod
    def register_callback(cls, hook):
        """Register hooks from 3rd party programs to access generated info.

        Parameters
        ----------
            hook (`function`): callback function for the logging feature.
        """
        cls._hook = hook

    @property
    def result(self):
        """Generate result percentage and store for future calls."""
        iterations = None
        self.log_msg("Calulating completion percent.")
        if self.meta_version == 1:
            iterations = math.ceil(self.total / self.piece_length)
        else:
            for _, info in self.fileinfo.items():
                length = info["length"]
                if iterations is None:
                    iterations = 0
                iterations += length // self.piece_length
                if length % self.piece_length != 0:
                    iterations += 1
        if self._result:
            return self._result
        total = self.total
        for _, _, _, size in tqdm(
                iterable=self.iter_hashes(),
                desc="hash pieces",
                total=iterations,
                unit="piece hash",
                colour="blue"):
            total -= size
        self.log_msg("%s%% of torrent content available.", self._result)
        return self._result

    def parse_metafile(self):
        """Flatten Meta dictionary of torrent file.

        Returns
        -------
            `dict`: flattened meta dictionary.
        """
        if not os.path.exists(self.metafile):

            raise FileNotFoundError(self.metafile)

        info = {}
        has_pieces = has_meta_version = False

        for k, v in pyben.load(self.metafile).items():
            if k == "info":
                for key, val in v.items():
                    info[key] = val
                    if key == "pieces":
                        has_pieces = True
                    if key == "meta version":
                        has_meta_version = True
            else:
                info[k] = v

        if has_meta_version and has_pieces:
            self.meta_version = 3
        elif has_meta_version:
            self.meta_version = 2
        else:
            self.meta_version = 1

        self.log_msg("Detected Meta Version %s.", str(self.meta_version))
        return info

    def log_msg(self, *args, level=logging.INFO):
        """Log message `msg` to logger and send `msg` to callback hook.

        Parameters
        ----------
            `*args` (`Iterable`[`str`]): formatting args for log message
            level (`int`, default=`logging.INFO`) : Log level for this message
        """
        message = args[0]
        if len(args) >= 3:
            message = (message % tuple(args[1:]))
        elif len(args) == 2:
            message = (message % args[1])

        # Repeat log messages should be ignored.
        if message != self.last_log:
            self.last_log = message
            logging.log(level, message)
            if self._hook and level == logging.INFO:
                self._hook(message)

    def find_root(self, path):
        """Check path for torrent content.

        The path can be a relative or absolute filesystem path.  In the case
        where the content is a single file, the path may point directly to the
        the file, or it may point to the parent directory.  If content points
        to a directory.  The directory will be checked to see if it matches
        the torrent's name, if not the directories contents will be searched.
        The returned value will be the absolute path that matches the torrent's
        name.

        Returns
        -------
            `str`: root path to content
        """
        if not os.path.exists(path):
            self.log_msg("Could not locate torrent content %s.", path)
            raise FileNotFoundError(path)

        root = os.path.abspath(path)
        base = os.path.basename(root)

        if base == self.name:
            self.log_msg("Content found: %s.", root)
            return root

        self.log_msg("Searching for torrent root in %s", root)
        for name in os.listdir(root):
            if name == self.name:
                root = os.path.join(root, name)
                self.log_msg("Content Found: %s", root)
                return root

        self.log_msg("Could not locate torrent content in: %s", root)
        raise FileNotFoundError(root)

    def check_paths(self):
        """Gather all file paths described in the torrent file."""
        if os.path.isfile(self.root):
            self.log_msg("%s points to a single file", self.root)
            self.paths.append(self.root)
            if self.meta_version == 1:
                self.fileinfo[self.root] = {"length": self.info["length"]}
                self.total = self.info["length"]
                self.pieces = split_pieces(self.info["pieces"], SHA1)
            else:
                info = self.info["file tree"][self.name][""]
                info["partial"] = self.name
                self.total = info["length"]
                if self.total > self.piece_length:
                    layers = self.info["piece layers"][info["pieces root"]]
                    info["layer hashes"] = split_pieces(layers, SHA256)
                self.fileinfo[self.root] = info
            return

        # Otherwise Content is more than 1 file.
        self.log_msg("%s points to a directory", self.root)
        if self.meta_version == 1:
            for path in self.info["files"]:
                self.total += path["length"]
                rlpath = os.path.join(*path["path"])
                full = os.path.join(self.root, rlpath)
                self.log_msg("Including file path: %s", rlpath)
                self.fileinfo[full] = {"length": path["length"]}
                self.paths.append(full)

            # Split pieces into individual hash digests.
            self.pieces = split_pieces(self.info["pieces"], SHA1)
            return

        self.walk_file_tree(self.info["file tree"], [])

    def walk_file_tree(self, tree, partials):
        """Traverse File Tree dictionary to get file details.

        Extract full pathnames, length, root hash, and layer hashes
        for each file included in the .torrent's file tree.

        Parameters
        ----------
            tree (`dict`): File Tree dict extracted from torrent file.
            partials (`list`): list of intermediate pathnames.
        """
        for key, val in tree.items():

            # Empty string means the tree's leaf is value
            if "" in val:
                path = os.path.join(self.root, *partials, key)
                info = self.fileinfo[path] = val[""]
                info["partial"] = key
                size = val[""]["length"]

                # get layer hashes for this file
                if size > self.piece_length:
                    root = val[""]["pieces root"]
                    layer_hashes = self.info["piece layers"][root]
                    info["layer hashes"] = split_pieces(layer_hashes, SHA256)

                self.paths.append(path)
                self.total += size
                self.log_msg(
                    "Including: path - %s, length - %s",
                    path,
                    humanize_bytes(size)
                )

            else:
                self.walk_file_tree(val, partials + [key])

    def iter_hashes(self):
        """Produce results of comparing torrent contents piece by piece.

        Yields
        ------
        chunck : `bytes`
            hash of data found on disk
        piece : `bytes`
            hash of data when complete and correct
        path : `str`
            path to file being hashed
        size : `int`
            length of bytes hashed for piece
        """
        matched = consumed = 0
        if self.meta_version == 1:
            checker = FeedChecker
            args = (self.paths, self.piece_length, self.fileinfo, self.pieces)
        else:
            checker = HashChecker
            hasher = HasherV2 if self.meta_version == 2 else HasherHybrid
            args = (self.paths, self.piece_length, self.fileinfo, hasher)
        for chunk, piece, path, size in checker(*args):
            consumed += size
            msg = "Match %s: %s %s"
            humansize = humanize_bytes(size)
            if chunk == piece:
                matched += size
                logging.debug(msg, "Success", path, humansize)
            else:
                logging.debug(msg, "Fail", path, humansize)
            yield chunk, piece, path, size
            total_consumed = str(int(consumed / self.total * 100))
            percent_matched = str(int(matched / consumed * 100))
            self.log_msg("Processed: %s%%, Matched: %s%%",
                         total_consumed, percent_matched)
        if consumed:
            self.log_msg("Re-Check Complete:\n %s%% of %s found at %s",
                         percent_matched, self.metafile, self.root)
            self._result = percent_matched
        else:  # pragma: no cover
            self.log_msg("Re-Check Complete:\n 0%% of %s found at %s",
                         self.metafile, self.root)
            self._result = "0"


def split_pieces(pieces, hash_size):
    """Split bytes into 20 piece chuncks for sha1 digest.

    Parameters
    ----------
    pieces : `bytes`
        Initial data.

    Returns
    -------
    lst : `list`
        Pieces broken into groups of 20 bytes.
    """
    lst = []
    start = 0
    while start < len(pieces):
        lst.append(pieces[start: start + hash_size])
        start += hash_size
    return lst


class FeedChecker:
    """Validates torrent content.

    Seemlesly validate torrent file contents by comparing hashes in
    metafile against data on disk.

    Parameters
    ----------
    paths : `list`
        List of stirngs indicating file paths.
    piece_length : `int`
        Size of data blocks to split the data into.
    total : `int`
        Sum total in bytes of all files in file list.
    fileinfo : `dict`
        Info and meta dictionary from .torrent file.
    """

    def __init__(self, paths, piece_length, fileinfo, pieces):
        """Generate hashes of piece length data from filelist contents."""
        self.piece_length = piece_length
        self.paths = paths
        self.pieces = pieces
        self.fileinfo = fileinfo
        self.piece_map = {}
        self.index = 0
        self.piece_count = 0
        self.it = None

    def __iter__(self):
        """Assign iterator and return self."""
        self.it = self.iter_pieces()
        return self

    def __next__(self):
        """Yield back result of comparison."""
        partial = next(self.it)
        chunck = sha1(partial).digest()  # nosec
        try:
            piece = self.pieces[self.piece_count]
        except IndexError:
            raise StopIteration  # pragma: no cover
        path = self.paths[self.index]
        self.piece_count += 1
        return chunck, piece, path, len(partial)

    @property
    def current_length(self):
        """Length of current file contents in bytes."""
        return self.fileinfo[self.paths[self.index]]["length"]

    def iter_pieces(self):
        """Iterate through, and hash pieces of torrent contents.

        Yields
        ------
        piece : `bytes`
            hash digest for block of torrent data.
        """
        partial = bytearray()
        for i, path in enumerate(self.paths):
            self.index = i

            if os.path.exists(path):
                for piece in self.extract(path, partial):
                    if len(piece) == self.piece_length:
                        yield piece
                        partial = bytearray()
                    elif i + 1 == len(self.paths):
                        yield piece
                    else:
                        partial = piece
            else:
                for blank in self._gen_blanks(partial):
                    if len(blank) == self.piece_length:
                        yield blank
                        partial = bytearray()
                    else:
                        partial = blank

    def extract(self, path, partial):
        """Split file paths contents into blocks of data for hash pieces.

        Parameters
        ----------
        path : `str`
            path to content.
        partial : `bytes`
            any remaining content from last file.

        Yields
        ------
        partial : `bytes`
            Hash digest for block of .torrent contents.
        """
        read = 0
        size = os.path.getsize(path)
        length = self.fileinfo[path]["length"]
        with open(path, "rb") as current:
            while True:
                bitlength = self.piece_length - len(partial)
                part = bytearray(bitlength)
                amount = current.readinto(part)
                read += amount
                partial.extend(part[:amount])
                if amount < bitlength:
                    if size == read == length:
                        yield partial
                    break
                yield partial
                partial = bytearray(0)

        while length - size > 0:
            left = self.piece_length - len(partial)
            if length - size > left:
                padding = bytearray(left)
                size += left
                partial.extend(padding)
                yield partial
                partial = bytearray(0)
            else:
                partial.extend(bytearray(length - size))
                size += (length - size)
                yield partial

    def _gen_blanks(self, partial):
        """Create padded pieces where file sizes do not match.

        Parameters
        ----------
        partial : `bytes`
            any remaining data from last file processed.
        """
        left = self.current_length - len(partial)
        while left > self.piece_length - len(partial):
            arrlen = self.piece_length - len(partial)
            arr = bytearray(arrlen)
            partial.extend(arr)
            left -= arrlen
            yield partial
            partial = bytearray(0)
        if left > 0:
            partial.extend(bytearray(left))
        yield partial


class HashChecker:
    """Verify that root hashes of content files match the .torrent files.

    Parameters
    ----------
    paths : `list`
        List of files.
    piece_length : `int`
        Size of chuncks to split the data into.
    fileinfo : `dict`
        Info from .torrent file being checked.
    """

    def __init__(self, paths, piece_length, fileinfo, hasher):
        """Construct a HybridChecker instance."""
        self.paths = paths
        self.hasher = hasher
        self.piece_length = piece_length
        self.fileinfo = fileinfo
        self.it = None
        logging.debug(
            "Starting Hash Checker. piece length: %s",
            humanize_bytes(self.piece_length)
        )

    def __iter__(self):
        """Assign iterator and return self."""
        self.it = self.iter_paths()
        return self

    def __next__(self):
        """Provide the result of comparison."""
        try:
            value = next(self.it)
            return value
        except StopIteration as stopiter:
            raise StopIteration() from stopiter

    def iter_paths(self):
        """Iterate through and compare root file hashes to .torrent file.

        Parameters
        ----------
        hasher : class
            The class user to caluclate root hash.

        Yields
        ------
        results : `tuple`
            The size of the file and result of match.
        """
        for path in self.paths:
            info = self.fileinfo[path]
            length = info["length"]
            logging.debug("%s length: %s", path, str(length))
            roothash = info["pieces root"]
            logging.debug("%s root hash %s", path, str(roothash))

            if not os.path.exists(path):
                if "layer hashes" in info and info["layer hashes"]:
                    pieces = info["layer hashes"]
                else:
                    pieces = [roothash]
                for i, piece in enumerate(pieces):
                    if len(pieces) == 1:
                        size = length
                    elif i < len(pieces) - 1:
                        size = self.piece_length
                    else:
                        size = length - ((len(pieces) - 1) * self.piece_length)
                    logging.debug("Yielding: %s %s %s %s", str(bytes(SHA256)),
                                  str(piece), path, str(size))
                    yield bytes(SHA256), piece, path, size
                continue

            hashed = self.hasher(path, self.piece_length)
            if "layer hashes" in info:
                hash_pieces = split_pieces(hashed.piece_layer, SHA256)
                info_pieces = info["layer hashes"]
            else:
                hash_pieces = [hashed.root]
                info_pieces = [info["pieces root"]]

            diff = len(info_pieces) - len(hash_pieces)
            if diff > 0:
                hash_pieces += [bytes(SHA256)] * diff
            num_pieces = len(hash_pieces)
            size = self.piece_length
            for chunk, piece in zip(hash_pieces, info_pieces):
                if num_pieces == 1:
                    size = length - ((len(hash_pieces) - 1) * size)
                logging.debug("Yielding: %s, %s, %s, %s", str(chunk),
                              str(piece), str(path), str(size))
                yield chunk, piece, path, size
                num_pieces -= 1
