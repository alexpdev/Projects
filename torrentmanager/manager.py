import pyben
import os
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class SearchThread(QThread):



    def __init__(self, path, container):
        super().__init__()
        self.path = path
        self.container = container
        self.count = 0

    def walk_path(self, root):
        if root.is_file():
            if root.suffix == ".torrent":
                try:
                    torrent = Torrent(root)
                except PermissionError:
                    print("Permission Error", root)
                    return
                self.container.append(torrent)
                self.count += 1
                if self.count and self.count % 50 == 0:
                    print(self.objectName, " - Count: ", self.count)
        elif root.is_dir():
            try:
                filelist = list(root.iterdir())
            except PermissionError:
                print("Permission Error", root)
                return
            for item in filelist:
                self.walk_path(item)

    def run(self):
        self.walk_path(Path(self.path))
        return self.container


class TorrentManager(QObject):

    dataReady = Signal()

    def __init__(self, backend, path=None):
        super().__init__()
        self.backend = backend(path=path)
        self.torrents = []
        if len(self.backend.archive) > 0:
            for item in self.backend.archive:
                self.torrents.append(Torrent.from_dict(item))

    def run_search(self, paths):
        self.threads = []
        for path in paths:
            container = []
            thread = SearchThread(path, container)
            self.threads.append(thread)
            thread.finished.connect(self.add_to_archive)
            thread.start()

    def add_to_archive(self):
        for thread in self.threads:
            if thread.isFinished():
                for torrent in thread.container:
                    if torrent not in self.torrents:
                        self.torrents.append(torrent)
                thread.container = []
                thread.deleteLater()
                self.dataReady.emit()

class Torrent:

    def __init__(self, path=None):
        self.path = str(path)
        self.name = None
        self.piece_length = None
        self.announce = None
        self.web_seeds = None
        self.http_seeds = None
        self.completed = "?"
        self.date_added = str(datetime.today())
        self.meta_version = None
        self.file_tree = None
        self.files = None
        self.length = None
        self.pieces = None
        self.piece_layers = None
        self.private = None
        self.comment = None
        self.source = None
        self.created_by = None
        if path is not None:
            self.file_size = os.path.getsize(self.path)
            self.extract()

    def extract(self):
        meta = pyben.load(self.path)
        meta.update(meta['info'])
        del meta['info']
        for key in meta:
            original_key = key
            if len(key.split()) > 1:
                key = '_'.join(key.split())
            elif len(key.split('-')) > 1:
                key = '_'.join(key.split('-'))
            self.__dict__.setdefault(key, None)
            self.__dict__[key] = meta[original_key]

    def to_dict(self):
        torrent = {}
        for k,v in self.__dict__.items():
            if isinstance(v, (dict, list, tuple, int, str, float)):
                torrent[k] = v
        return torrent

    @classmethod
    def from_dict(cls, item):
        torrent = cls(None)
        for k,v in item.items():
            torrent.__dict__.setdefault(k, v)

    def __eq__(self, other):
        return other.name == self.name and other.path == self.path
