#!usr/bin/python3

from geometry import *
from constants import *

class Entity:
    def __init__(self):
        pass
    def next_step(self):
        pass
    def update(self, board):
        pass

class Mob(Entity):
    pass

class Indestr_Wall(Entity):
    pass

class Wall(Indestr_Wall):
    pass

class Exit(Entity):
    pass

class Bomb(Mob):
    pass

class Player(Mob):
    pass

class Monster(Mob):
    pass
