import sys
import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from torrentmanager.common import getIcon

class TableModel(QAbstractTableModel):

    rowAdded = Signal()

    def __init__(self, parent=None, manager=None):
        super().__init__(parent=parent)
        self.manager = manager
        self.torrents = self.manager.get()
        self.all_fields = {
            'name': 'Name',
            'path': 'Path',
            'completed': 'Completed',
            'date_added': 'Date Added',
            'length': 'Size',
            'content_path': 'Content',
            'meta_version': 'Version',
            'piece_length': 'Piece Length',
            'announce': 'Tracker',
            'private': 'Private',
            'source': 'Source'
        }
        self.fields = dict(list(self.all_fields.items()))
        self.manager.torrentAdded.connect(self.addRow)

    def addRow(self, torrent):
        index = QModelIndex()
        count = self.rowCount(index)
        self.insertRow(count, index, torrent=torrent)

    def insertRow(self, num, index, torrent=None):
        if torrent:
            self.beginInsertRows(index, num, num)
            self.torrents.insert(num, torrent)
            self.endInsertRows()
            self.rowAdded.emit()
            return True
        return False

    def rowCount(self, index):
        return len(self.torrents)

    def columnCount(self, index):
        return len(self.fields)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            torrent = self.torrents[index.row()]
            if role == Qt.DisplayRole:
                col = index.column()
                field = list(self.fields.items())[col][0]
                value = getattr(torrent, field)
                if field == "path":
                    value = os.path.dirname(value)
                return str(value)
        return None

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.DisplayRole:
                return list(self.fields.items())[section][1]


class ToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.widget = parent
        self.add_files_action = QAction(icon=getIcon("addFiles"))
        self.addAction(self.add_files_action)
        self.add_files_action.triggered.connect(self.add_torrent_files)
        self.add_dir_action = QAction(icon=getIcon("addFolder"))
        self.addAction(self.add_dir_action)
        self.add_dir_action.triggered.connect(self.add_torrent_dir)
        self.connect_source_action = QAction(icon=getIcon("connectSource"))
        self.connect_source_action.triggered.connect(self.connect_source)
        self.addAction(self.connect_source_action)

    def connect_source(self):
        
        selection = self.widget.table.currentSelection()
        for row in selection:
            item = self.widget.table.item(row, 0)

        print(selection)

    def add_torrent_dir(self):
        torrent_dir = QFileDialog.getExistingDirectory(
            parent=self.widget, caption="Select torrent folder"
        )
        if not torrent_dir:
            return self.widget.statusBar().showMessage("Nothing Selected", 10000)
        self.send_to_manager(torrent_dir)

    def add_torrent_files(self):
        torrent_files, _ = QFileDialog.getOpenFileNames(
            parent=self.widget, caption="Select torrent file(s)",
            filter="Torrent (*.torrent);;Any (*)"
        )
        if not torrent_files:
            return self.widget.statusBar().showMessage("Nothing Selected", 10000)
        self.send_to_manager(*torrent_files)

    def send_to_manager(self, *args):
        self.widget.manager.run_search(args)


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.filemenu = QMenu("File", parent=self)
        self.exitAction = QAction(text="Exit")
        self.filemenu.addAction(self.exitAction)
        self.exitAction.triggered.connect(self.exit)
        self.addMenu(self.filemenu)

    def exit(self):
        self.parent().close()


class Table(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setSelectionBehavior(self.SelectRows)

    def currentSelection(self):
        smodel = self.selectionModel()
        indexes = smodel.selectedIndexes()
        return list(set([i.row() for i in indexes]))

    def item(self, row, col):
        return self.model().index(row, col)



class Window(QMainWindow):

    def __init__(self, parent=None, manager=None) -> None:
        super().__init__(parent=parent)
        self.central = QWidget(parent=self)
        self.resize(600,400)
        self.layout = QVBoxLayout(self.central)
        self.manager = manager
        self.statusbar = self.statusBar()
        self.menubar = MenuBar(parent=self)
        self.setMenuBar(self.menubar)
        self.setCentralWidget(self.central)
        self.setObjectName('MainWindow')
        self.setupUi()

    def setupUi(self):
        self.toolbar = ToolBar(parent=self)
        self.addToolBar(self.toolbar)
        self.splitter = QSplitter(Qt.Orientation.Vertical, parent=self)
        self.layout.addWidget(self.splitter)
        self.table = Table()
        self.tablemodel = TableModel(parent=self, manager=self.manager)
        self.tablemodel.rowAdded.connect(self.table.resizeColumnsToContents)
        self.table.setModel(self.tablemodel)
        self.splitter.addWidget(self.table)
        self.scrollArea = QScrollArea(parent=self)
        self.splitter.addWidget(self.scrollArea)

    def accept_paths(self, paths):
        paths = self.dialog_plainTextEdit.toPlainText()
        paths = paths.split("\n")
        self.manager.run_search(paths)
        self.dialog.close()

def start_gui(manager, *args, **kwargs):
    app = QApplication([])
    window = Window(parent=None, manager=manager)
    window.show()
    app.exec()
