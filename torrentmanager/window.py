from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *



class TableModel(QAbstractTableModel):
    def __init__(self, parent=None, manager=None):
        super().__init__(parent=parent)
        self.manager = manager
        self.torrents = manager.torrents
        self.headers = ['name', 'path', 'completed', 'date_added']
        self.manager.torrentAdded.connect(self.add_row)

    def add_row(self, row):
        index = QModelIndex()
        self.addRow(row, index)

    def rowCount(self, index):
        return len(self.torrents)

    def columnCount(self, index):
        return len(self.headers)

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            torrent = self.manager.torrents[index.row()]
            if role == Qt.DisplayRole:
                col = index.column()
                return torrent.__dict__[self.headers[col]]
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return ' '.join(self.headers[section].split('_')).title()

    def addRow(self, row, index):
        self.beginInsertRows(index, row, row)
        self.endInsertRows()
        return True

class Window(QMainWindow):
    """Window object."""

    def __init__(self, parent=None, manager=None) -> None:
        super().__init__(parent=parent)
        self.central = QWidget(parent=self)
        self.layout = QVBoxLayout(self.central)
        self.manager = manager
        self.resize(600,400)
        self.setCentralWidget(self.central)
        self.setObjectName('MainWindow')
        self.setupUi()

    def setupUi(self):
        self.table = QTableView()
        self.button = QPushButton("Search for torrents")
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.table)
        self.button.clicked.connect(self.torrent_search)
        self.tablemodel = TableModel(parent=self, manager=self.manager)
        self.table.setModel(self.tablemodel)

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
    window = Window(manager=manager, parent=None)
    window.show()
    app.exec()
