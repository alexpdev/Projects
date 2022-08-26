import os
import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from FlashNotes.qss import theme_1

TOPICS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "topics")


class TermLabel(QLabel):
    """Label for the term."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(1)
        self.setMidLineWidth(0)
        self.setAlignment(Qt.AlignCenter)

class DefLabel(QLabel):
    """Label for the definition."""

    def __init__(self, text, parent=None):
        super().__init__(text, parent=parent)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setLineWidth(1)
        self.setMidLineWidth(0)
        self.setAlignment(Qt.AlignCenter)


class TopicLine(QLineEdit):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setPlaceholderText("Topic Goes Here")


class HeaderCombo(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.topic_line = TopicLine(self)
        self.setLineEdit(self.topic_line)
        self.add_topics()
        self.validator = Validator()

    def add_topics(self):
        for filename in os.listdir(TOPICS_DIR):
            fullpath = os.path.join(TOPICS_DIR, filename)
            if os.path.isfile(fullpath) and fullpath.endswith(".json"):
                with open(fullpath, "rt", encoding="utf-8") as fd:
                    data = json.load(fd)
                    name = data['name']
                    self.addItem(name, fullpath)


class Validator(QValidator):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.combo = parent

    def fixup(self, text):
        self.combo.setCurrentText(text[:-1])

    def validate(self, text, pos):
        textlen = len(text)
        intermed = False
        for i in range(self.combo.count()):
            itemtext = self.combo.itemText(i)
            size = len(itemtext)
            if textlen == size:
                if text == itemtext:
                    return self.Acceptable
            if textlen < size:
                if itemtext.startswith(text):
                    intermed == True
        if intermed:
            return self.Intermediate
        return self.Invalid


class DataHolder(QObject):
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)



class Window(QMainWindow):
    """Window object."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.resize(400, 200)
        self.central = QWidget(parent=self)
        self.central.setLayout(self.layout)
        self.hlayout = QHBoxLayout()
        self.header = HeaderCombo(self)
        self.left_label = TermLabel("Term", self)
        self.right_label = DefLabel("?", self)
        self.hlayout.addWidget(self.left_label)
        self.hlayout.addWidget(self.right_label)
        self.layout.addWidget(self.header)
        self.layout.addLayout(self.hlayout)
        self.setCentralWidget(self.central)
        self.setObjectName('MainWindow')
        self.header.currentIndexChanged.connect(self.swap_topics)

    def swap_topics(self, index):
        data = self.header.itemData(index, Qt.UserRole)
        with open(data,"rt",encoding="utf-8") as fd:
            info = json.load(fd)
        self.data = info




class Application(QApplication):
    def __init__(self, windowclass=Window, args=[]):
        super().__init__(args)
        self._window = windowclass()
        self.setStyleSheet(theme_1)

    @property
    def window(self):
        return self._window



if __name__ == "__main__":
    app = QApplication(Window, [])
    app.window.show()
    app.exec()
