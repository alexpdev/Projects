import os
import sys
from argparse import ArgumentParser
from torrentmanager.window import start_gui
from torrentmanager.manager import TorrentManager, JSONBackend


def main(args=None):
    if not args:
        args = sys.argv[1:]
    manager = TorrentManager(JSONBackend)
    start_gui(manager)
