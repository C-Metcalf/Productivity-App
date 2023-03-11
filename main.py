import os
import sys
import time
import datetime
import traceback
import qdarktheme
from enum import Enum, auto
from queue import Queue
from random import randint
from PyQt5.QtCore import Qt, QSize, QRunnable, pyqtSlot, QObject, pyqtSignal, QThreadPool, QTimer, QDateTime
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QHBoxLayout,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QInputDialog,
    QDateEdit,
    QMessageBox,
    QDockWidget,
    QMenu,
    QToolBar,
    QComboBox,
    QTabWidget,
    QAction)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # MainWindow Setup
        self.setWindowTitle("Tasks")
        self.home = QWidget()
        self.setCentralWidget(self.home)
        self.layout = QVBoxLayout()
        self.home.setLayout(self.layout)
        self.goalList = list()

        #Menu Bar Setup
        menu_bar = self.menuBar()
        add_action = QAction("&Add Goal", self)
        add_action.setStatusTip("Create a new goal")
        add_action.setShortcut("Ctrl+a")
        add_action.triggered.connect(self.add)
        save_action = QAction("&Save Goals", self)
        save_action.setStatusTip("Save the goals you have added recently")
        save_action.setShortcut('Ctrl+s')
        save_action.triggered.connect(self.file_save)
        delete_action = QAction("&Delete Goals", self)
        delete_action.setStatusTip("Delete all of your goals")
        delete_action.setShortcut("Ctrl+d")
        delete_action.triggered.connect(self.file_delete)
        menu_bar.addAction(add_action)
        menu_bar.addSeparator()
        menu_bar.addAction(save_action)
        menu_bar.addSeparator()
        menu_bar.addAction(delete_action)

        #Date Setup
        date = datetime.datetime.now().date()
        week = date.isocalendar().week

        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QDateTime.currentDateTime())

        #QButtons
        showGoals = QPushButton("Show All Current Goals")

        # QButtons Connect
        # showGoals.clicked.connect(self.goals)

        # Add objects to the layout
        self.layout.addWidget(self.dateedit)
        self.layout.addWidget(showGoals)

        self.file_read()

    def add(self):
        Input, ok = QInputDialog.getText(self, "New Goal", "Goal")
        if ok and Input:
            newGoal = QCheckBox(Input)
            self.goalList.append(newGoal)
            self.layout.addWidget(self.goalList[self.goalList.__len__() - 1])

    def file_save(self):
        file = open('goals.txt', 'a')
        for txt in self.goalList:
            text = str(txt.text() + '\r')
            file.write(text)
        file.close()

    def file_read(self):
        try:
            file = open('goals.txt', 'r')
            goalList = list()
            if file:
                with file:
                    lines = len(file.readlines())
                    print(lines)
                    i = 0
                    file.seek(0, 0) # put the pointer back to the top of the file
                    while(i != lines):
                        data = file.readline()
                        data = data.replace('\n', '')
                        goal = QCheckBox(data)
                        goalList.append(goal)
                        self.layout.addWidget(goalList[self.goalList.__len__() - 1])
                        i +=1
        except:
            print("no file")

    def file_delete(self):
        os.remove("goals.txt")

qdarktheme.enable_hi_dpi()
app = QApplication(sys.argv)
qdarktheme.setup_theme(corner_shape="sharp")
window = MainWindow()
window.show()
sys.exit(app.exec())