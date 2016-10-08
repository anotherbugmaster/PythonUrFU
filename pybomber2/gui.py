#!/usr/bin/python3

import sys
# from threading import Thread
from enum import Enum
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from musicPlayer import MusicPlayer
from widgets import MenuWidget, GameWidget, OptionsWidget, \
    SplashScreenWidget, StartScreenWidget
from board2 import Board

class MainWindow(QMainWindow):
    class WidgetType(Enum):
        start_screen_widget = 0
        menu_widget = 1
        game_widget = 2
        options_widget = 3
        splash_screen_widget = 4

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyBomber')
        # self.setFixedSize(500, 500)
        self.showFullScreen()

        self.music_player = MusicPlayer()
        self.music_player.play()

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(StartScreenWidget(self))
        self.central_widget.addWidget(MenuWidget(self))
        self.central_widget.addWidget(GameWidget(self))
        self.central_widget.addWidget(OptionsWidget(self))
        self.central_widget.addWidget(SplashScreenWidget(self))

        self.start()

    def showWidget(self, widgetType):
        # print(self.central_widget.currentIndex())
        # print(self.central_widget.currentWidget())
        self.central_widget.setCurrentIndex(widgetType)

    def switchFullscreen(self):
        if self.windowState() == Qt.WindowFullScreen:
            self.setWindowState(Qt.WindowNoState)
        else:
            self.setWindowState(Qt.WindowFullScreen)

    def start(self):
        self.central_widget.setCurrentIndex(0)
        self.central_widget.currentWidget().update()

app = QApplication(sys.argv)
with open("stylesheet.qss", 'r') as i_stream:
    app.setStyleSheet(i_stream.read())
mainWindow = MainWindow()
status = app.exec_()
sys.exit(status)
