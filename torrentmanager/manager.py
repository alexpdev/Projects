import atexit
import os
import json
import pyben
import shutil
import asyncio
from pathlib import Path
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Torrent:

    def __init__(self, path=None):
        self.fullpath = path
        self.path = str(path.parent)
        self.name = None
        self.piece_length = None
        self.announce = None
        self.category = None
        self.web_seeds = None
        self.http_seeds = None
        self.completed = ""
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
            self.file_size = os.path.getsize(path)
            self.extract()

    def extract(self):
        meta = pyben.load(self.fullpath)
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

class Worker(QObject):

    finished = Signal()
    torrentCreated = Signal(Torrent)

    def __init__(self, paths, manager, parent=None):
        super().__init__(parent=parent)
        self.paths = [Path(i) for i in paths]
        self.manager = manager
        self.threads = []
        self.count = 0

    def run(self):
        for path in self.paths:
            self.walk_path(path)
        self.finished.emit()

    def walk_path(self, root):
        if root.is_file():
            if root.suffix == ".torrent":
                try:
                    torrent = Torrent(root)
                except PermissionError:
                    print("Permission Error", root)
                    return
                self.torrentCreated.emit(torrent)
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

class TorrentManager(QObject):

    torrentAdded = Signal(Torrent)

    def __init__(self, backend, path=None):
        super().__init__()
        self.backend = backend(path=path)
        self.torrents = asyncio.run(self.backend.get())
        self.threads = []

    def run_search(self, paths):
        thread = QThread()
        self.worker = Worker(paths, manager=self)
        self.worker.moveToThread(thread)
        self.worker.torrentCreated.connect(self.add_torrent)
        self.worker.finished.connect(thread.quit)
        thread.started.connect(self.worker.run)
        thread.finished.connect(self.worker.deleteLater)
        thread.finished.connect(thread.deleteLater)
        thread.start()
        self.threads.append(thread)

    def add_torrent(self, torrent):
        self.backend.store(torrent)
        self.torrents.append(torrent)
        self.torrentAdded.emit(len(self.torrents))

class StorageBackend:

    def __init__(self, *args, **kwargs):
        Current.set(self)

    def store(self, *items):
        raise NotImplemented


class JSONBackend(StorageBackend):

    def __init__(self, path=None):
        super().__init__(path=path)
        self.path = path
        if not self.path:
            self.path = Path("./.torrentfilemanager/archive.json")
            archive = self.path
            create_path = []
            while not os.path.exists(str(archive)):
                create_path.append(archive.name)
                archive = archive.parent
            if len(create_path) > 1:
                os.makedirs(os.path.join(archive, *create_path[:-1]))
            json.dump([],open(self.path,'wt'))

    async def get(self):
        data = json.load(open(self.path))
        return data

    async def store(self, *items):
        data = asyncio.run(self.get())
        task1 = asyncio.create_task(store_items(items))
        item_list = await task1
        task2 = asyncio.create_task(
            json.dump(data+item_list, open(self.path, 'wt', encoding='utf8')))
        asyncio.run(task2)

def store_items(items):
    items = []
    for item in items:
        item = item.to_dict()
        items.append(item)
    return items

class Current:

    _instance = None

    @classmethod
    def set(cls, value): cls._instance = value

    @classmethod
    def get(cls): return cls._instance

def get_current_backend():
    return Current.get()

@atexit.register
def save_archive():
    backend = get_current_backend()
    json.dump(backend.archive, open(backend.filepath, 'wt', encoding='utf8'))
