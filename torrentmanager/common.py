import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

def getIcon(name: str) -> QIcon:
    parent = os.path.dirname(__file__)
    assets = os.path.join(parent, "assets")
    filename = os.path.join(assets, name)
    if not filename.lower().endswith(".png"):
        filename += ".png"
    return QIcon(filename)
