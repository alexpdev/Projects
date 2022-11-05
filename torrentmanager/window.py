import os
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class TableModel(QAbstractTableModel):

    rowAdded = Signal()

    def __init__(self, parent=None, manager=None):
        super().__init__()
        self.parent = parent
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

class Window(QMainWindow):

    def __init__(self, parent=None, manager=None) -> None:
        super().__init__(parent=parent)
        self.central = QWidget(parent=self)
        self.resize(600,400)
        self.layout = QVBoxLayout(self.central)
        self.manager = manager
        self.setCentralWidget(self.central)
        self.setObjectName('MainWindow')
        self.setupUi()

    def setupUi(self):
        self.toolbar = ToolBar(parent=self)
        self.layout.addWidget(self.toolbar)
        self.splitter = QSplitter(Qt.Orientation.Vertical, parent=self)
        self.layout.addWidget(self.splitter)
        self.table = QTableView()
        self.tablemodel = TableModel(parent=self, manager=self.manager)
        self.tablemodel.rowAdded.connect(self.table.resizeColumnsToContents)
        self.table.setModel(self.tablemodel)
        self.button = QToolButton()
        self.button.setText("Search for torrents")
        self.toolbar.addWidget(self.button)
        self.splitter.addWidget(self.table)
        self.scrollArea = QScrollArea(parent=self)
        self.splitter.addWidget(self.scrollArea)
        self.button.clicked.connect(self.torrent_search)

    def torrent_search(self):
        self.dialog = QDialog()
        dialogLayout = QVBoxLayout(self.dialog)
        dialoghlayout = QHBoxLayout()
        self.dialog_accept_button = QPushButton('accept')
        self.dialog_cancel_button = QPushButton('cancel')
        dialoghlayout.addWidget(self.dialog_cancel_button)
        dialoghlayout.addWidget(self.dialog_accept_button)
        self.dialog_plainTextEdit = QPlainTextEdit(self.dialog)
        dialogLayout.addWidget(self.dialog_plainTextEdit)
        dialogLayout.addLayout(dialoghlayout)
        self.dialog_accept_button.clicked.connect(self.accept_paths)
        self.dialog_cancel_button.clicked.connect(self.cancel_dialog)
        self.dialog.exec()

    def cancel_dialog(self):
        self.dialog.close()

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
