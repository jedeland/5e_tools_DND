import PyQt5 as qt; import sys
from PyQt5.QtWidgets import *
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *


# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.setWindowTitle("Main Menu")
#         self.create_menu()
#         #self.menu = self.menuBar()
#         #self.option = self.menu.addMenu("File")
#         #exit_action = QAction("Exit", self)
#
#         #exit_action.setShortcut(QKeySequence.Quit)
#         #exit_action.triggered.connect(self.close)
#
#         #self.option.addAction(exit_action)
#         self.status = self.statusBar()
#         #self.option = self.menu.addMenu("Tools")
#         #mutate_action = QAction("Mutate Monster", self)
#
#         #mutate_action = QAction()
#
#         self.status.showMessage("Data loaded")
#         self.create_npc_layout()
#
#     def create_menu(self):
#         mainMenu = self.menuBar()
#         fileMenu = mainMenu.addMenu("File")
#         toolMenu = mainMenu.addMenu("Tools")
#         downloadMenu = mainMenu.addMenu("Save Output")
#
#         quitAction = QAction("Exit" , fileMenu)
#         quitAction.setShortcut(QKeySequence.Quit)
#         quitAction.triggered.connect(self.close)
#         fileMenu.addAction(quitAction)
#
#         mutateAction = QAction("Mutate Monster", toolMenu)
#         toolMenu.addAction(mutateAction)
#         generateNames = QAction("Generate NPCs", toolMenu)
#         toolMenu.addAction(generateNames)
#
#
#
#     def create_npc_layout(self):
#         frameStyle = QFrame.Sunken | QFrame.Panel
#         self.integerLabel = QLabel()
#         self.integerLabel.setFrameStyle(frameStyle)
#         self.integerButton = QPushButton("QInputDialog.get&Integer()")
#         self.group_box = QGroupBox("Please choose the number of NPCs")
#         self.group_box.setFont(QFont("Leto", 11))
#         grid_layout = QGridLayout()
#         grid_layout.addWidget(self.integerButton, 0, 0)
#
#         text, ok = QInputDialog.getInt(self, "NPC Generator Options",
#                                       "Number of NPCs:", 10, 0, 100, 1)
#         if ok and text:
#             self.integerLabel.setText("%d%%" % text)

class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, df):
        super().__init__()

        self.table = QtWidgets.QTableView()
        data = df

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

#Alternative paths to GUI seem to be as follows:
#Make a web app that displays the data
#Make a temporary CSV / Excel file that displays the data
#Make a temporary google sheet that holds the data for a set amount of time
#Use QGrid


# app=QApplication(sys.argv)
# window=MainWindow()
# window.show()
# app.exec_()

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



