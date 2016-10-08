#usr/bin/python3

from constants import SPRITE_W, SPRITE_H, WALL, BLOCK, MONSTER, PLAYER, EXIT
from entities import Wall, Block, Monster, Player, Exit
import random

class Board:
    def __init__(self, matrix_w=11, matrix_h=11):
        self.entities = []
        self.matrix_w = matrix_w
        self.matrix_h = matrix_h
        self.matrix = [[0 for x in range(self.matrix_w)] \
        for x in range(self.matrix_h)]
        self.width = self.matrix_w * SPRITE_W
        self.height = self.matrix_h * SPRITE_H
        self.coef_w = (self.width - SPRITE_W) / (self.matrix_w - 1)
        self.coef_h = (self.height - SPRITE_H) / (self.matrix_h - 1)

    def read_map(self, file):
        with open(file, 'r') as i_stream:
            lines = i_stream.read().splitlines()
            self.matrix_w = len(lines[0])
            self.matrix_h = len(lines)
            self.width = self.matrix_w * SPRITE_W
            self.height = self.matrix_h * SPRITE_H
            self.coef_w = (self.width - SPRITE_W) / (self.matrix_w - 1)
            self.coef_h = (self.height - SPRITE_H) / (self.matrix_h - 1)
            for index, line in enumerate(lines):
                self.matrix[index] = [int(x) for x in list(line)]

    def add_entities(self):
        for x in range(self.matrix_w):
            for y in range(self.matrix_h):
                if self.matrix[y][x] == WALL:
                    self.entities.append(Wall(
                        x * self.coef_w,
                        y * self.coef_h))
                if self.matrix[y][x] == BLOCK:
                    self.entities.append(Block(
                        x * self.coef_w,
                        y * self.coef_h))
                if self.matrix[y][x] == PLAYER:
                    self.entities.append(Player(
                        x * self.coef_w,
                        y * self.coef_h))
                if self.matrix[y][x] == MONSTER:
                    self.entities.append(Monster(
                        x * self.coef_w,
                        y * self.coef_h))
                if self.matrix[y][x] == EXIT:
                    self.entities.append(Exit(
                        x * self.coef_w,
                        y * self.coef_h))

    def gen_map(self):
        self.gen_walls()
        self.gen_player()
        self.gen_monster()
        self.gen_blocks()
        self.gen_exit()
    def gen_walls(self):
        for w_index in range((self.matrix_w + 1) // 2):
            for h_index in range((self.matrix_h + 1) // 2):
                self.matrix[w_index * 2][h_index * 2] = WALL

    def gen_player(self):
        x = random.randint(0, self.matrix_w - 1)
        y = random.randint(0, self.matrix_h - 1)
        while self.matrix[x][y] != 0:
            x = random.randint(0, self.matrix_w - 1)
            y = random.randint(0, self.matrix_h - 1)
        self.matrix[x][y] = PLAYER

    def gen_monster(self):
        x = random.randint(0, self.matrix_w - 1)
        y = random.randint(0, self.matrix_h - 1)
        while self.matrix[x][y] != 0:
            x = random.randint(0, self.matrix_w - 1)
            y = random.randint(0, self.matrix_h - 1)
        self.matrix[x][y] = MONSTER

    def gen_blocks(self):
        for number in range(30):
            x = random.randint(0, self.matrix_w - 1)
            y = random.randint(0, self.matrix_h - 1)
            while self.matrix[x][y] != 0:
                x = random.randint(0, self.matrix_w - 1)
                y = random.randint(0, self.matrix_h - 1)
            self.matrix[x][y] = BLOCK

    def gen_exit(self):
        x = random.randint(0, self.matrix_w - 1)
        y = random.randint(0, self.matrix_h - 1)
        while self.matrix[x][y] != 0:
            x = random.randint(0, self.matrix_w - 1)
            y = random.randint(0, self.matrix_h - 1)
        self.matrix[x][y] = EXIT
