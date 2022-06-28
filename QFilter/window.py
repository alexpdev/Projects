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
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setStyleSheet("font-size: 9pt;")
        self.setColumnCount(6)
        self.labels = ["TITLE", "VIEWS", "COUNT", "ADDED", "RATING", "URL"]
        for i in range(len(self.labels)):
            self.setHorizontalHeaderLabel(i,self.labels[i])
        self.verticalHeader().setHidden(True)
        self.data = []
        self.loadData()
        self.inputData()
        # hheaders = self.horizontalHeader()
        # for i in range(6):
        #     hheaders.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def inputData(self):
        self.clear()
        for entry in self.data:
            rownum = self.rowCount()
            self.insertRow(rownum)
            for k,v in entry.items():
                if k in ["count", "views"]:
                    v = int(v.split()[0])
                i = self.labels.index(k.upper())
                item = QTableWidgetItem(v, type=0)
                self.setItem(rownum, i, item)

    def loadData(self):
        for file in os.listdir(DATADIR):
            if not file.endswith(".json"):
                continue
            with open(os.path.join(DATADIR,file),"rt",encoding="utf-8") as js:
                contents = json.load(js)
                self.data += contents


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
        self.countbox = QSpinBox(parent=self)
        self.addedbox = QSpinBox(parent=self)
        self.viewbox = QSpinBox(parent=self)
        self.ratingbox = QSpinBox(parent=self)
        self.keywords = QLineEdit(parent=self)
        self.titleslabel = QLabel(parent=self)
        self.table = TableWidget(parent=self)
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
        self.setCentralWidget(self.central)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window(parent=None, app=app)
    win.show()
    sys.exit(app.exec())
