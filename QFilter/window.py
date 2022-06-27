import sys

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

class Window(QMainWindow):

    def __init__(self, parent=None, app=None):
        super().__init__(parent=parent)
        self.app = app
        self.central = QWidget()
        self.layout = QVBoxLayout()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)
        self.start_date = QDateEdit(parent=self)
        self.end_date = QDateEdit(parent=self)
        self.start_label = QLabel(parent=self)
        self.end_label = QLabel(parent=self)
        self.hlayout1 = QHBoxLayout()
        self.vlayout1 = QVBoxLayout()
        self.vlayout2 = QVBoxLayout()
        self.vlayout1.addWidget(self.start_label)
        self.vlayout1.addWidget(self.start_date)
        self.vlayout2.addWidget(self.end_label)
        self.vlayout2.addWidget(self.end_date)
        self.hlayout1.addLayout(self.vlayout1)
        self.hlayout1.addLayout(self.vlayout2)
        self.start_label.setText("Start Date")
        self.end_label. setText("End Date")
        self.view_start = QComboBox(parent=self)
        self.view_end = QComboBox(parent=self)
        self.view_start_label = QLabel(parent=self)
        self.view_end_label = QLabel(parent=self)
        self.hlayout2 = QHBoxLayout()
        self.vlayout3 = QVBoxLayout()
        self.vlayout4 = QVBoxLayout()
        self.vlayout3.addWidget(self.start_label)
        self.vlayout3.addWidget(self.start_date)
        self.vlayout4.addWidget(self.end_label)
        self.vlayout4.addWidget(self.end_date)
        self.hlayout2.addLayout(self.vlayout1)
        self.hlayout2.addLayout(self.vlayout2)
        self.view_start_label.setText("View Count Start")
        self.view_end_label. setText("View Count End")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window(parent=None, app=app)
    win.show()
    sys.exit(app.exec())
