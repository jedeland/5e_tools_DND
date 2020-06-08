import PyQt5 as qt; import sys
from PyQt5.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Main Menu")

        self.menu = self.menuBar()
        self.option = self.menu.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.option.addAction(exit_action)
        self.status = self.statusBar()
        self.status.showMessage("Data loaded")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())


