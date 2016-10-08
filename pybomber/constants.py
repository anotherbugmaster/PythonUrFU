#!usr/bin/python3

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

FPS = 60

SCREEN_W = 800
SCREEN_H = 600

FULLSCREEN = False

SPRITE_W = 72
SPRITE_H = 72

SPRITE_VEL_W = 2
SPRITE_VEL_H = 2

WALL = 1
BLOCK = 2
PLAYER = 3
MONSTER = 4
EXIT = 5

def matrix_to_screen(x, y):
    return (x * SPRITE_W, y * SPRITE_H)

def screen_to_matrix(x, y):
    return (int(x // SPRITE_W), int(y // SPRITE_H))
