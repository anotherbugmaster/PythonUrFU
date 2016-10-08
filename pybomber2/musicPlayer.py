#!/usr/bin/python3

from random import randrange
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
class MusicPlayer():
    def __init__(self):
        super().__init__()

        self.playlist = QMediaPlaylist()
        self.playlist.setPlaybackMode(QMediaPlaylist.Random & QMediaPlaylist.Loop)
        background_music = [
            QMediaContent(QUrl.fromLocalFile("music/background1.wav")),
            QMediaContent(QUrl.fromLocalFile("music/background2.wav")),
            QMediaContent(QUrl.fromLocalFile("music/background3.wav"))
        ]
        self.playlist.addMedia(background_music)
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)

    def play(self):
        seed = randrange(0, self.playlist.mediaCount())
        self.playlist.setCurrentIndex(seed)
        self.player.play()


