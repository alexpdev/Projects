import atexit
import os
import json
from torrentmanager.manager import Torrent

class Current:
    _instance = None
    @classmethod
    def set(cls, value):
        cls._instance = value
    @classmethod
    def get(cls):
        return cls._instance


class StorageBackend:

    def __init__(self, *args, **kwargs):
        Current.set(self)

    def store(self, *items):
        raise NotImplemented

class JSONBackend(StorageBackend):

    def __init__(self, path=None):
        super().__init__(path=path)
        if not path:
            self.filepath = "./archive.json"
        else:
            self.filepath = path
        if os.path.exists(self.filepath):
            self.archive = json.load(open(self.filepath))
        else:
            self.archive = []

    def store(self, *items):
        for item in items:
            item = item.to_dict()
            self.archive.append(item)

def get_current_backend():
    return Current.get()

@atexit.register
def save_archive():
    backend = get_current_backend()
    json.dump(backend.archive, open(backend.filepath, 'wt', encoding='utf8'))
