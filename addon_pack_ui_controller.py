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
        self.create_npc_layout()

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
        generateNames = QAction("Generate NPCs", toolMenu)
        toolMenu.addAction(generateNames)



    def create_npc_layout(self):
        frameStyle = QFrame.Sunken | QFrame.Panel
        self.integerLabel = QLabel()
        self.integerLabel.setFrameStyle(frameStyle)
        self.integerButton = QPushButton("QInputDialog.get&Integer()")
        self.group_box = QGroupBox("Please choose the number of NPCs")
        self.group_box.setFont(QFont("Leto", 11))
        grid_layout = QGridLayout()
        grid_layout.addWidget(self.integerButton, 0, 0)

        text, ok = QInputDialog.getInt(self, "NPC Generator Options",
                                      "Number of NPCs:", 10, 0, 100, 1)
        if ok and text:
            self.integerLabel.setText("%d%%" % text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())


