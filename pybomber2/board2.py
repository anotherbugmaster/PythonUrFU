#!/usr/bin/python3

import entities2 as ent

class Board():
    def __init__(self):
        matrix_w = 10
        matrix_h = 10
        self.entities = [[[] for _ in range(matrix_h)] for _ in range(matrix_w)]

    def read_map(self, filepath):
        sign_to_entity = {
            "0" : None,
            "1" : ent.Indestr_Wall,
            "2" : ent.Wall,
            "3" : ent.Exit,
            "4" : ent.Bomb,
            "5" : ent.Player,
            "6" : ent.Monster
        }

        with open(filepath, 'r') as i_stream:
            self.entities = [[[sign_to_entity[x]] for x in line] for line in i_stream.read().splitlines()]
