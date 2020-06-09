import PyQt5 as qt; import sys
from PyQt5.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Main Menu")
        self.create_menu()
        #self.menu = self.menuBar()
        #self.option = self.menu.addMenu("File")
        #exit_action = QAction("Exit", self)

        #exit_action.setShortcut(QKeySequence.Quit)
        #exit_action.triggered.connect(self.close)

        #self.option.addAction(exit_action)
        self.status = self.statusBar()
        #self.option = self.menu.addMenu("Tools")
        #mutate_action = QAction("Mutate Monster", self)

        #mutate_action = QAction()

        self.status.showMessage("Data loaded")

    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        toolMenu = mainMenu.addMenu("Tools")
        downloadMenu = mainMenu.addMenu("Save Output")

        quitAction = QAction("Exit" , fileMenu)
        quitAction.setShortcut(QKeySequence.Quit)
        quitAction.triggered.connect(self.close)
        fileMenu.addAction(quitAction)

        mutateAction = QAction("Mutate Monster", toolMenu)
        toolMenu.addAction(mutateAction)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())


