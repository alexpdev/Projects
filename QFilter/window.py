import sys
import os
import json

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
# URL
# VIEWS
# TITLE
# COUNT
# ADDED
# RATING

class TableWidget(QTableWidget):

    setHidden = Signal([int, bool])
    itemReady = Signal([int, int, QTableWidgetItem])
    loadReady = Signal([list])
    rowReady = Signal([list])

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("font-size: 9pt;")
        self.setColumnCount(6)
        self.setRowCount(0)
        self.labels = ["TITLE", "VIEWS", "COUNT", "ADDED", "RATING", "URL"]
        self.verticalHeader().setHidden(True)
        self.data = []
        self.setHorizontalHeaderLabels(self.labels)
        self.setHidden.connect(self.hide)
        self.itemReady.connect(self.addItem)

    def setRow(self, items):
        index = self.rowCount()
        self.insertRow(index)
        for i, item in enumerate(items):
            self.setItem(index, i, item)

    def hide(self, row, truth):
        self.setRowHidden(row, truth)

    def addItem(self, row, col, item):
        self.setItem(row, col, item)


    def lookup(self,text):
        for row in range(self.rowCount()):
            s = self.item(row,0).text()
            if text not in s:
                self.setRowHidden(row, True)
            else:
                self.setRowHidden(row, False)


class Worker(QObject):

    finished = Signal()
    rowReady = Signal([list])
    limitsChanged = Signal([str,set])

    def __init__(self, widget, table):
        super().__init__()
        self.widget = widget
        self.table = table
        self.data = []
        self.files = [os.path.join(DATADIR,i) for i in os.listdir(DATADIR)]
        self.timemap = {
            "second": 1,
            "minute": 60,
            "hour": 60*60,
            "day": 60*60*24,
            "week": 60*60*24*7,
            "month": 60*60*24*30,
            "year": 60*60*24*365
        }
        self.labels = ["title", "views", "count", "added", "rating", "url"]
        self.ranges = {i:set() for i in self.labels if i not in ["title", "url"]}

    def run(self):
        for file in self.files:
            if not file.endswith(".json"):
                continue
            with open(os.path.join(DATADIR,file),"rt",encoding="utf-8") as js:
                contents = json.load(js)
                self.data += contents
        times = self.timemap
        for entry in self.data:
            items = [None for _ in range(len(self.labels))]
            for k,v in entry.items():
                if k in ["count", "views"]:
                    parts = v.split()[:-1]
                    v = int("".join(parts))
                if k == "added":
                    parts = v.split()
                    denom = parts[1]
                    val = 0
                    for t in times:
                        if t in denom:
                            val = times[t]
                            break
                    total = int(parts[0]) * val
                    v = total
                if k == "rating":
                    v = int(v[:-1])/100
                if k in self.ranges:
                    self.ranges[k].add(v)
                i = self.labels.index(k)
                item = QTableWidgetItem(str(v), 0)
                item.value = v
                items[i] = item
            self.rowReady.emit(items)
        for k,v in self.ranges.items():
            self.limitsChanged.emit(k,v)
        self.table.setHorizontalHeaderLabels(self.table.labels)
        self.finished.emit()

class Validator(QIntValidator):

    def fixup(self, text):
        if not text or not text.isnumeric():
            # self.parent().setText("0")
            return "0"



class Window(QMainWindow):

    def __init__(self, parent=None, app=None):
        super().__init__(parent=parent)
        self.app = app
        self.resize(800,700)
        self.central = QWidget()
        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)
        self.viewlabel = QLabel(parent=self)
        self.countlabel = QLabel(parent=self)
        self.addedlabel = QLabel(parent=self)
        self.ratinglabel = QLabel(parent=self)
        self.keywordlabel = QLabel(parent=self)
        self.viewlabel.setText("Minimum Views")
        self.addedlabel.setText("Maximum Time")
        self.countlabel.setText("Minimum Count")
        self.ratinglabel.setText("Minimum Rating")
        self.keywordlabel.setText("Keywords")
        self.countbox = QLineEdit(parent=self)
        self.countbox.setValidator(Validator())
        self.countbox.setText("0")
        self.addedbox = QLineEdit(parent=self)
        self.addedbox.setValidator(Validator())
        self.addedbox.setText("0")
        self.viewbox = QLineEdit(parent=self)
        self.viewbox.setValidator(Validator())
        self.viewbox.setText("0")
        self.ratingbox = QLineEdit(parent=self)
        self.ratingbox.setValidator(Validator())
        self.ratingbox.setText("0")
        self.keywords = QLineEdit(parent=self)
        self.titleslabel = QLabel(parent=self)
        self.table = TableWidget(parent=self)
        self.button = QPushButton("Load Data", parent=self)
        self.filtergrid = QGridLayout()
        self.filtergrid.addWidget(self.addedlabel, 0,0,1,1)
        self.filtergrid.addWidget(self.addedbox, 0,1,1,1)
        self.filtergrid.addWidget(self.viewlabel, 0,2,1,1)
        self.filtergrid.addWidget(self.viewbox, 0,3,1,1)
        self.filtergrid.addWidget(self.countlabel, 0,4,1,1)
        self.filtergrid.addWidget(self.countbox, 0,5,1,1)
        self.filtergrid.addWidget(self.ratinglabel, 0,6,1,1)
        self.filtergrid.addWidget(self.ratingbox, 0,7,1,1)
        self.filtergrid.addWidget(self.keywordlabel,1,0,1,1)
        self.filtergrid.addWidget(self.keywords, 1,1,-1,-1)
        self.layout.addLayout(self.filtergrid)
        self.layout.addWidget(self.titleslabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.setCentralWidget(self.central)
        self.button.clicked.connect(self.loadData)
        self.viewbox.textChanged.connect(self.filter)
        self.countbox.textChanged.connect(self.filter)
        self.ratingbox.textChanged.connect(self.filter)
        self.addedbox.textChanged.connect(self.filter)
        self.keywords.textChanged.connect(self.lookup)


    def setLimits(self, label, seq):
        widgets = {"added": self.addedbox,
                   "views": self.viewbox,
                   "count": self.countbox,
                   "rating": self.ratingbox}
        box = widgets[label]
        mn,mx = min(seq), max(seq)
        if box == "rating":
            mn ,mx = mn*100, mx*100
        box.validator().setBottom(mn)
        box.validator().setTop(mx)

    def filter(self):
        addedval = int(self.addedbox.text())
        kws = self.keywords.text()
        mapping = {
            1: int(self.viewbox.text()),
            2: int(self.countbox.text()),
            4: int(self.ratingbox.text())
        }
        for i in range(self.table.rowCount()):
            hidden = False
            for k,v in mapping.items():
                if self.table.item(i, k).value < v:
                    hidden = True
                    self.table.setHidden.emit(i, True)
                    break
            if hidden: continue
            if self.table.item(i, 3).value > addedval:
                self.table.setHidden.emit(i,True)
                continue
            text = self.table.item(i,0).text().lower()
            if len([j for j in kws.lower() if j not in text and j.isalpha()]):
                self.table.setHidden.emit(i, True)
            self.table.setHidden.emit(i, False)

    def loadData(self):
        self.thread = QThread()
        self.worker = Worker(self, self.table)
        self.worker.moveToThread(self.thread)
        self.worker.limitsChanged.connect(self.setLimits)
        self.worker.rowReady.connect(self.table.setRow)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def lookup(self, text):
        self.table.lookup(text)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window(parent=None, app=app)
    win.show()
    sys.exit(app.exec())
