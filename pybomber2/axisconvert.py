#!usr/bin/python3

from constants import SPRITE_W, SPRITE_H

def grid_to_screen(grid_x, grid_y):
    return (grid_x * SPRITE_W, grid_y * SPRITE_H)

def screen_to_grid(x, y):
    return (round(x // SPRITE_W), round(y // SPRITE_H))
