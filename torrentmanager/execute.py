import os
import sys
from argparse import ArgumentParser
from torrentmanager.window import start_gui
from torrentmanager.storage import JSONBackend
from torrentmanager.manager import TorrentManager


def main(args=None):
    if not args:
        args = sys.argv[1:]
    manager = TorrentManager(JSONBackend)
    start_gui(manager)
