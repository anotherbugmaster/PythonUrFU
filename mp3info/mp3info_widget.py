#!/usr/bin/python3

from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QRect, QSettings, QSize,
        Qt, QTextStream, QUrl)
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QWidget,
        QMessageBox, QTextEdit, QFormLayout, QGridLayout, QLabel, QSizePolicy, QPushButton,
        QTableWidget, QTableWidgetItem)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
import os
import id3v1
import id3v2
import frame
import binascii
import os

class Mp3InfoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        self.cur_filename = ''
        self.player = QMediaPlayer()

        self.play_pause_button = QPushButton()
        self.play_pause_button.setText("PLAY")
        # self.play_pause_button.setSizePolicy(
        #     QSizePolicy.Expanding,
        #     QSizePolicy.Expanding)
        self.play_pause_button.clicked.connect(self.play_pause)
        self.layout.addWidget(self.play_pause_button, 0, 0, 1, 2)

        self.mp3info = QTableWidget()
        self.mp3info.setColumnCount(2)
        self.mp3info.setRowCount(100)
        self.mp3info.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.mp3info, 1, 1, 3, 1)

        self.cover_label = QLabel()
        self.cover_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding)
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setMinimumSize(240, 160)
        self.layout.addWidget(self.cover_label, 1, 0, 6, 1)

        self.hex_view = QTextEdit()
        self.hex_view.setReadOnly(True)
        self.layout.addWidget(self.hex_view, 4, 1, 3, 1)

        self.originalPixmap = QPixmap("cage.jpg")

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        scaledSize = self.originalPixmap.size()
        scaledSize.scale(self.cover_label.size(), Qt.KeepAspectRatio)
        if not self.cover_label.pixmap() or scaledSize != self.cover_label.pixmap().size():
            self.update_cover_label()

    def update_cover_label(self):
        self.cover_label.setPixmap(
            self.originalPixmap.scaled(
                self.cover_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation))

    def play_pause(self):
        if self.cur_filename == '':
            return
        if self.player.state() == QMediaPlayer.PlayingState:
            self.play_pause_button.setText('PLAY')
            self.player.pause()
        else:
            self.play_pause_button.setText('PAUSE')
            self.player.play()

    def load_info(self):

        if os.path.isfile("cover.jpg"):
            os.remove("cover.jpg")

        self.mp3info.clear()

        id3v1_items = sorted(id3v1.get_info(self.cur_filename).items())
        id3v2_items = sorted(id3v2.get_info(self.cur_filename).items())
        frame_items = sorted(frame.get_info(self.cur_filename).items())

        cur_row = 0
        try:
            if id3v1_items:
                id3v1_item = QTableWidgetItem("ID3v1:")
                id3v1_item.setFlags(id3v1_item.flags() ^ Qt.ItemIsEditable)
                self.mp3info.setItem(cur_row, 0, id3v1_item)
                for key, value in id3v1_items:
                    key_item = QTableWidgetItem(str(key))
                    key_item.setFlags(key_item.flags() ^ Qt.ItemIsEditable)
                    value_item = QTableWidgetItem(str(value))
                    value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)
                    cur_row += 1
                    self.mp3info.setItem(cur_row, 0, key_item)
                    self.mp3info.setItem(cur_row, 1, value_item)
            else:
                id3v1_item = QTableWidgetItem("No ID3v1")
                id3v1_item.setFlags(id3v1_item.flags() ^ Qt.ItemIsEditable)
                self.mp3info.setItem(cur_row, 0, id3v1_item)
            cur_row += 2

            if id3v2_items:
                id3v2_item = QTableWidgetItem("ID3v2:")
                id3v2_item.setFlags(id3v2_item.flags() ^ Qt.ItemIsEditable)
                self.mp3info.setItem(cur_row, 0, id3v2_item)
                for key, value in id3v2_items:
                    key_item = QTableWidgetItem(str(key))
                    key_item.setFlags(key_item.flags() ^ Qt.ItemIsEditable)
                    value_item = QTableWidgetItem(str(value))
                    value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)
                    cur_row += 1
                    self.mp3info.setItem(cur_row, 0, key_item)
                    self.mp3info.setItem(cur_row, 1, value_item)
            else:
                id3v2_item = QTableWidgetItem("No ID3v2")
                id3v2_item.setFlags(id3v2_item.flags() ^ Qt.ItemIsEditable)
                self.mp3info.setItem(cur_row, 0, id3v2_item)
            cur_row += 2

            if frame_items:
                frame_item = QTableWidgetItem("Frame:")
                frame_item.setFlags(frame_item.flags() ^ Qt.ItemIsEditable)
                self.mp3info.setItem(cur_row, 0, frame_item)
                for key, value in frame_items:
                    key_item = QTableWidgetItem(str(key))
                    key_item.setFlags(key_item.flags() ^ Qt.ItemIsEditable)
                    value_item = QTableWidgetItem(str(value))
                    value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)
                    cur_row += 1
                    self.mp3info.setItem(cur_row, 0, key_item)
                    self.mp3info.setItem(cur_row, 1, value_item)
            else:
                frame_item = QTableWidgetItem("No frame info")
                frame_item.setFlags(frame_item.flags() ^ Qt.ItemIsEditable)
                self.mp3info.setItem(cur_row, 0, frame_item)
            cur_row += 2

        except FileNotFoundError:
            item = QTableWidgetItem('error: file is not found')
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.mp3info.setItem(cur_row, 0, frame_item)
        except RuntimeError:
            item = QTableWidgetItem('error: file is corrupted. By sin')
            item.setFlags(item.flags() ^ Qt.ItemIsEditable)
            self.mp3info.setItem(cur_row, 0, frame_item)

    def load_hex(self):
        self.hex_view.clear()

        with open(self.cur_filename, 'rb') as f:
            while f.read(1):
                self.hex_view.append(self.get_hex_view(f.read(10000)))
            # self.hex_view.append(self.get_hex_view(binary_string))
            # print(str(binascii.hexlify(f.read(32))))

    def get_hex_view(self, string):
        bin_string = binascii.hexlify(string)
        char_string = str(bin_string)
        char_string = char_string.replace('\\x', "")
        substring = char_string[2:-1]
        hex_view_string = ''
        for char_index, char in enumerate(substring):
            hex_view_string += char
            if (char_index + 1) % 2 == 0:
                hex_view_string += ' '
            if (char_index + 1) % 32 == 0:
                hex_view_string += '\n'

        return hex_view_string

    def load_file(self):
        self.play_pause_button.setText("PLAY")
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.cur_filename)))
        self.load_info()
        # self.load_hex()
        if os.path.isfile("cover.jpg") and not QPixmap("cover.jpg").isNull():
            self.originalPixmap = QPixmap("cover.jpg")
            os.remove("cover.jpg")
        else:
            self.originalPixmap = QPixmap("picard.jpg")
        self.update_cover_label()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
