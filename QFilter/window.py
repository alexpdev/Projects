import sys
import os
import json
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

DATADIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

class TableWidget(QTableWidget):

    setHidden = Signal([int, bool])
    itemReady = Signal([int, int, QTableWidgetItem])
    loadReady = Signal([list])
    rowReady = Signal([list])
    resizeReady = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("font-size: 9pt;")
        self.setColumnCount(5)
        self.setRowCount(0)
        self.labels = ["TITLE", "VIEWS", "COUNT", "ADDED", "URL"]
        self.verticalHeader().setHidden(True)
        self.data = []
        self.setHorizontalHeaderLabels(self.labels)
        self.setHidden.connect(self.hide)
        self.itemReady.connect(self.addItem)
        self.resizeReady.connect(self.resizeColumnsToContents)

    def setRow(self, items):
        index = self.rowCount()
        self.insertRow(index)
        for i, val in enumerate(items):
            item = QTableWidgetItem(str(val), 0)
            item.value = val
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
        self.labels = ["title", "views", "count", "added","url"]
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
                if k in self.ranges:
                    self.ranges[k].add(v)
                i = self.labels.index(k)
                items[i] = v
            self.rowReady.emit(items)
        for k,v in self.ranges.items():
            self.limitsChanged.emit(k,v)
        self.table.resizeReady.emit()
        self.finished.emit()

    def run2(self):
        addedval = int(self.widget.addedbox.value())
        text = list(self.widget.keywords.text())
        print(text)
        mapping = {
            1: int(self.widget.viewbox.value()),
            2: int(self.widget.countbox.value()),
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
            title = self.table.item(i,0).text().lower()
            text = [i for i in text if i.isalpha()]
            if len([i for i in text if i not in title]):
                self.table.setHidden.emit(i, True)
                continue
            self.table.setHidden.emit(i, False)
        self.finished.emit()


class LineFilter(QSpinBox):

    validated = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        # self.setReadOnly(True)
        # self.setButtonSymbols(self.PlusMinus)
        self.setAccelerated(True)
        self.setCorrectionMode(self.CorrectToNearestValue)
        self.valueChanged.connect(self.validateInput)

    def setRange(self, mn, mx):
        self.setMinimum(mn)
        self.setMaximum(mx)
        self.setValue(mn)

    def validateInput(self):
        self.validated.emit()



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
        self.keywordlabel = QLabel(parent=self)
        self.viewlabel.setText("Minimum Views")
        self.addedlabel.setText("Maximum Time")
        self.countlabel.setText("Minimum Count")
        self.keywordlabel.setText("Keywords")
        self.countbox = LineFilter(parent=self)
        self.addedbox = LineFilter(parent=self)
        self.viewbox = LineFilter(parent=self)
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
        self.filtergrid.addWidget(self.keywordlabel,1,0,1,1)
        self.filtergrid.addWidget(self.keywords, 1,1,-1,-1)
        self.layout.addLayout(self.filtergrid)
        self.layout.addWidget(self.titleslabel)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button)
        self.setCentralWidget(self.central)
        self.button.clicked.connect(self.loadData)
        self.viewbox.validated.connect(self.filter)
        self.countbox.validated.connect(self.filter)
        self.addedbox.validated.connect(self.filter)
        self.keywords.textChanged.connect(self.lookup)
        self.threads = []

    def setLimits(self, label, seq):
        widgets = {"added": self.addedbox,
                   "views": self.viewbox,
                   "count": self.countbox,
                   }
        box = widgets[label]
        mn,mx = min(seq), max(seq)
        if box == "rating":
            mn ,mx = mn*100, mx*100
        box.setRange(mn, mx)

    def filter(self):
        worker = Worker(self, self.table)
        thread = QThread()
        self.threads.append((thread, worker))
        worker.moveToThread(thread)
        thread.started.connect(worker.run2)
        worker.finished.connect(thread.quit)
        thread.finished.connect(self.destroyThread)
        thread.start()

    def destroyThread(self):
        for i, thread in enumerate(self.threads):
            if thread[0].isFinished():
                thread[0].deleteLater()
                del self.threads[i]

    def loadData(self):
        thread = QThread()
        worker = Worker(self, self.table)
        self.threads.append((thread, worker))
        worker.moveToThread(thread)
        worker.limitsChanged.connect(self.setLimits)
        worker.rowReady.connect(self.table.setRow)
        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        thread.finished.connect(self.destroyThread)
        thread.start()

    def lookup(self, text):
        self.table.lookup(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window(parent=None, app=app)
    win.show()
    sys.exit(app.exec())
