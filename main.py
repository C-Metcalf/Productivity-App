import os
import sys
import time
import datetime
import traceback
import qdarktheme
import pyqtgraph as pg
from enum import Enum, auto
from queue import Queue
from random import randint
from PyQt5.QtCore import Qt, QSize, QRunnable, pyqtSlot, QObject, pyqtSignal, QThreadPool, QTimer, QDateTime
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
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
        self.setFixedSize(1200, 700)
        self.home = QWidget()
        self.setCentralWidget(self.home)
        #Main Layout
        self.layout = QVBoxLayout()
        self.home.setLayout(self.layout)
        #Top third of the layout
        top = QVBoxLayout()
        self.layout.addLayout(top)
        #middle third of the layout
        middle = QVBoxLayout()
        self.layout.addLayout(middle)
        self.grid = QGridLayout()
        self.grid.setRowMinimumHeight(0, 120)
        self.grid.setRowMinimumHeight(1, 120)
        middle.addLayout(self.grid)
        #bottom thrid of the layout
        bottom = QVBoxLayout()
        self.layout.addLayout(bottom)
        plot = pg.plot()
                # create list for y-axis
        y1 = [5, 5, 7, 10, 3, 8, 9, 1, 6, 2]

                # create horizontal list i.e x-axis
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        barGraph = pg.BarGraphItem(x = x, height = y1, width = 0.2, brush ='g')
        plot.addItem(barGraph)
        bottom.addWidget(plot)
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

        #Date edit Setup
        self.dateedit = QDateEdit(calendarPopup=True)
        self.dateedit.setDateTime(QDateTime.currentDateTime())

        a = QLabel("1")
        b = QLabel("2")
        c = QLabel("3")

        self.grid.addWidget(a, 0, 0)
        self.grid.addWidget(b, 1, 0)
        self.grid.addWidget(c, 1, 1)

        # Add objects to the layout
        top.addWidget(self.dateedit)

        self.file_read()

    def add(self):
        Input, ok = QInputDialog.getText(self, "New Goal", "Goal")
        if ok and Input:
            newGoal = QCheckBox(Input)
            self.goalList.append(newGoal)
            self.grid.addWidget(self.goalList[self.goalList.__len__() - 1], 0, 2, 1, 1)

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
                    i = 0
                    file.seek(0, 0) # put the pointer back to the top of the file
                    while(i != lines):
                        data = file.readline()
                        data = data.replace('\n', '')
                        goal = QCheckBox(data)
                        goalList.append(goal)
                        self.grid.addWidget(goalList[self.goalList.__len__() - 1], 0, 1)
                        i +=1
        except:
            print("no file")

    def file_delete(self):
        try:
            file = open('goals.txt', 'w')
            file.write("")
            file.close()
        except:
            print("f")

qdarktheme.enable_hi_dpi()
app = QApplication(sys.argv)
qdarktheme.setup_theme(corner_shape="sharp")
window = MainWindow()
window.show()
sys.exit(app.exec())