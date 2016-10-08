#!/usr/bin/python3

import sys, time
from threading import Thread
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, \
    QLabel, QSizePolicy, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPixmap
from board2 import Board
import entities2 as ent

class StartScreenWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow

        self.new_game_button = QPushButton("New game")
        self.new_game_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.continue_button = QPushButton("Continue")
        self.continue_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.options_button = QPushButton("Options")
        self.options_button.clicked.connect(
            lambda: mainWindow.showWidget(mainWindow.WidgetType.options_widget.value))
        self.options_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(sys.exit)
        self.exit_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        picture = QPixmap("icons/bomberman2.png")
        picture_lbl = QLabel()
        picture_lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        picture_lbl.setAlignment(Qt.AlignCenter)
        picture_lbl.setPixmap(picture)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(picture_lbl, 0, 0)

        self.setLayout(grid)

    def update(self):
        mainWindow = self.mainWindow

        def show_splash():
            time.sleep(2)
            mainWindow.showWidget(mainWindow.WidgetType.menu_widget.value)

        background_thread = Thread(target=show_splash)
        background_thread.start()

class MenuWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.new_game_button = QPushButton("New game")
        self.new_game_button.clicked.connect(
            lambda: mainWindow.showWidget(mainWindow.WidgetType.game_widget.value))
        self.new_game_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.continue_button = QPushButton("Continue")
        self.continue_button.clicked.connect(
            lambda: mainWindow.showWidget(mainWindow.WidgetType.game_widget.value))
        self.continue_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.options_button = QPushButton("Options")
        self.options_button.clicked.connect(
            lambda: mainWindow.showWidget(mainWindow.WidgetType.options_widget.value))
        self.options_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(sys.exit)
        self.exit_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        picture_lbl = QLabel()
        picture_lbl.setObjectName("menu_picture_lbl")
        picture_lbl.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        picture_lbl.setAlignment(Qt.AlignCenter)
        picture_lbl.setScaledContents(True)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.new_game_button, 1, 0)
        grid.addWidget(self.continue_button, 2, 0)
        grid.addWidget(self.options_button, 3, 0)
        grid.addWidget(self.exit_button, 4, 0)
        grid.addWidget(picture_lbl, 1, 1, 4, 1)

        self.setLayout(grid)

class GameWidget(QGraphicsView):
    def __init__(self, mainWindow):
        super().__init__()

        self.board = Board()

        self.mainWindow = mainWindow

        graphicsScene = QGraphicsScene(self)
        graphicsScene.addPixmap(QPixmap("icons/wall.png"))

        self.setScene(graphicsScene)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setSceneRect(QRectF(mainWindow.frameGeometry()))

        self.board.read_map("maps/1.map")
        self.drawBoard(self.board)

    def drawBoard(self, board):
        ent_to_image = {
            ent.Indestr_Wall : "icons/indest_wall.png",
            ent.Wall : "icons/wall.png",
            ent.Exit : "icons/exit.png",
            ent.Player : "icons/bomberman.png",
            ent.Bomb : "icons/bomb.png",
            ent.Monster : "icons/monster.png"
        }
        mainWindow = self.mainWindow
        self.scene().clear()

        row_amount = len(board.entities)
        column_amount = len(board.entities[0])

        coefficient = (mainWindow.height() - 100) / row_amount

        self.scene().setSceneRect(0, 0, column_amount * coefficient, mainWindow.height() - 100)

        for row_index, row in enumerate(board.entities):
            for column_index, column in enumerate(row):
                current_element = board.entities[row_index][column_index][-1]
                if current_element == None:
                    pixmap = QPixmap()
                else:
                    pixmap = QPixmap(ent_to_image[current_element])
                pixmap = pixmap.scaledToHeight((self.scene().height()) / row_amount)
                pixmap_item = QGraphicsPixmapItem(pixmap)
                self.scene().addItem(pixmap_item)
                pixmap_item.setPos(column_index * (pixmap.width()), row_index * (pixmap.height()))
                # print((row_index, column_index))

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        key = event.key()
        mainWindow = self.mainWindow

        if key == Qt.Key_Escape:
            # self.lbl.setText("#PAUSED_GAME")
            mainWindow.showWidget(mainWindow.WidgetType.menu_widget.value)


class OptionsWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        grid = QGridLayout()
        grid.setSpacing(10)

        fullscreen_button = QPushButton("Switch")
        fullscreen_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        fullscreen_button.clicked.connect(mainWindow.switchFullscreen)

        fullscreen_label = QLabel("Fullscreen")
        fullscreen_label.setAlignment(Qt.AlignCenter)

        back_to_menu_button = QPushButton("Back to menu")
        back_to_menu_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        back_to_menu_button.clicked.connect(
            lambda: mainWindow.showWidget(mainWindow.WidgetType.menu_widget.value))

        grid.addWidget(fullscreen_label, 0, 1)
        grid.addWidget(fullscreen_button, 0, 2)
        grid.addWidget(back_to_menu_button, 1, 1, 1, 2)

        self.setLayout(grid)

class SplashScreenWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
