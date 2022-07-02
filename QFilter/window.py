import os
import sys
import json
import webbrowser
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class Item:

    def __init__(self, value=0, text="0"):
        self.value = value
        self.text = text

    def setValue(self, value):
        self.value = value

    def setText(self, text):
        self.text = text

class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.headers = ["Title", "Count", "Views", "Added", "Url"]
        self.grid = []
        self.bluepen = QBrush()
        self.bluepen.setColor("#0000FF")

    def rowCount(self, index=QModelIndex()):
        return len(self.grid)

    def columnCount(self, index=QModelIndex()):
        return len(self.headers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]

    def data(self, index, role=Qt.DisplayRole):
        row, column = index.row(), index.column()
        item = self.grid[row][column]
        if role == Qt.DisplayRole or role == Qt.EditRole:
            return item.text
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter | Qt.AlignRight
        elif role == Qt.ToolTipRole:
            return str(item.value)
        elif role == Qt.ForegroundRole:
            if column == self.columnCount() - 1:
                return self.bluepen

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        if role == Qt.EditRole:
            row, column = index.row(), index.column()
            item = self.grid[row][column]
            item.setValue(value)
            self.dataChanged.emit(self.index(0,0), self.index(self.rowCount() - 1, self.columnCount() - 1))
            return True
        return False

    def insertRow(self, rownum, index=QModelIndex()):
        return self.insertRows(rownum, 1, index)

    def insertRows(self, rownum, count, index=QModelIndex()):
        self.beginInsertRows(index, rownum, rownum + count - 1)
        for _ in range(count):
            row = [Item() for _ in range(self.columnCount())]
            self.grid.insert(rownum, row)
        self.endInsertRows()
        return True

    def setRow(self, index, data):
        for i in range(len(self.grid[index])):
            self.grid[index][i] = data[i]
        self.dataChanged.emit(self.index(0,0), self.index(self.rowCount()-1,self.columnCount()-1))

    def flags(self, index):
        if index.column() == self.columnCount() - 1:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def column(self,index):
        return [self.grid[i][index] for i in range(self.rowCount())]


class TableView(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.window = parent
        self.model_ = TableModel()
        self.setModel(self.model_)
        self.verticalHeader().hide()
        for i, label in enumerate(self.model_.headers):
            self.model_.setHeaderData(i, Qt.Orientation.Horizontal, label, Qt.DisplayRole)
        self.horizontalHeader().stretchLastSection()
        self.doubleClicked.connect(self.launchpage)

    def rowCount(self):
        return self.model_.rowCount()

    def columnCount(self):
        return self.model_.columnCount()

    def addRow(self, row):
        rownum = self.rowCount()
        self.model_.insertRow(rownum)
        self.model_.setRow(rownum, row)
        if rownum % 5000 == 0:
            if rownum % 10000 == 0:
                self.resizeColumnToContents(0)
                self.resizeColumnToContents(1)
            elif rownum % 15000 == 0:
                self.resizeColumnToContents(2)
                self.resizeColumnToContents(3)
            else:
                self.resizeColumnToContents(4)
                self.resizeColumnToContents(5)
            processEvents()

    def item(self, row, col):
        return self.model_.grid[row][col]

    def launchpage(self, index):
        row, col = index.row(), index.column()
        if col == self.columnCount() - 1:
            item = self.item(row, col)
            webbrowser.open(item.text)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1000,700)
        self.central = QWidget()
        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)
        self.setWindowTitle("QFilters")
        self.table = TableView()
        self.hlayout = QHBoxLayout()
        self.button = QPushButton("push")
        self.button.clicked.connect(self.table.addRow)
        self.button2 = QPushButton("load")
        self.button2.clicked.connect(self.loadData)
        self.hlayout.addWidget(self.button)
        self.hlayout.addWidget(self.button2)
        self.grid = QGridLayout()
        self.viewbox = QComboBox()
        self.addedbox = QComboBox()
        self.countbox = QComboBox()
        self.addedLabel = QLabel()
        self.countLabel = QLabel()
        self.viewLabel = QLabel()
        [i.setAlignment(Qt.AlignRight) for i in [self.addedLabel, self.countLabel, self.viewLabel]]
        self.addedLabel.setText("Added")
        self.viewLabel.setText("Views")
        self.countLabel.setText("Count")
        self.keywordsLabel = QLabel()
        self.keywordsLabel.setText("KeyWords")
        self.hlayout2 = QHBoxLayout()

        self.grid.addWidget(self.countLabel, 0,0,1,1)
        self.grid.addWidget(self.countbox, 0,1,1,1)
        self.grid.addWidget(self.viewLabel, 0,2,1,1)
        self.grid.addWidget(self.viewbox, 0,3,1,1)
        self.grid.addWidget(self.addedLabel, 0,4,1,1)
        self.grid.addWidget(self.addedbox, 0,5,1,1)
        self.layout.addLayout(self.grid)
        self.edit = QLineEdit()
        self.hlayout2.addWidget(self.keywordsLabel)
        self.hlayout2.addWidget(self.edit)
        self.layout.addLayout(self.hlayout2)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.hlayout)
        self.setCentralWidget(self.central)
        self.edit.editingFinished.connect(self.filter)

    def setFilters(self):
        labels = [self.countbox, self.viewbox, self.addedbox]
        for i in range(1,4):
            data = self.table.model_.column(i)
            options = set()
            for item in data:
                options.add((item.value, item.text))
            if i == 3:
                options = {b:a for a,b in sorted(options, reverse=True)}
            else:
                options = {b:a for a,b in sorted(options)}
            box = labels[i-1]
            box.options = options
            box.addItems(options.keys())
            box.setEditable(False)
            box.currentIndexChanged.connect(self.filter)

    def filter(self):
        count = self.countbox
        countvalue = count.options[count.currentText()]
        view = self.viewbox
        viewvalue = view.options[view.currentText()]
        added = self.addedbox
        addedvalue = added.options[added.currentText()]
        kws = self.edit.text().split()
        for i, row in enumerate(self.table.model_.grid):
            if row[1].value < countvalue or row[2].value < viewvalue:
                self.table.hideRow(i)
                continue
            if row[3].value > addedvalue:
                self.table.hideRow(i)
                continue
            for word in kws:
                if word not in row[0].text:
                    self.table.hideRow(i)
                    break
            else:
                self.table.showRow(i)
            processEvents()

    def loadData(self):
        self.worker = Worker(self.table)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.setRow.connect(self.table.addRow)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.thread.deleteLater)
        self.thread.started.connect(self.worker.run)
        self.thread.start()
        self.thread.finished.connect(self.setFilters)
        self.worker.run()

class Worker(QObject):

    setRow = Signal([list])
    finished = Signal()

    def __init__(self, table):
        super().__init__()
        self.table = table
        datadir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
        self.paths = [os.path.join(datadir, i) for i in os.listdir(datadir)]
        self.timeTable = {
            "second": 1,
            "minute": 60,
            "hour": 60 * 60,
            "day": 60 * 60 * 24,
            "week": 60 * 60 * 24 * 7,
            "month": 60 * 60 * 24 * 30,
            "year": 60 * 60 * 24 * 365
        }

    def getTime(self, added):
        for k,v in self.timeTable.items():
            if k in added:
                val = int(added.split(' ')[0])
                return val * v
        return 0

    def run(self):
        for path in self.paths:
            if not path.lower().endswith(".json"):
                continue
            data = json.load(open(path,"rt",encoding="utf-8"))
            out = []
            for row in data:
                count = int("".join(row["count"].split()[:-1]))
                views = int("".join(row["views"].split()[:-1]))
                countitem = Item(value=count, text=row["count"])
                viewsitem = Item(value=views, text=row["views"])
                added = self.getTime(row["added"])
                addeditem = Item(value=added, text=row["added"])
                titleitem = Item(value=row["title"], text=row["title"])
                urlitem = Item(value=row["url"], text=row["url"])
                out = [titleitem, countitem, viewsitem, addeditem, urlitem]
                # self.table.addRow(out)
                self.setRow.emit(out)
        self.finished.emit()


def processEvents():
    app.processEvents()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
