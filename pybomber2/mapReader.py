#!/usr/bin/python3

import entites2 as ent

def read_map(file):
    sign_to_entity = {
        "0" : ent.Indestr_Wall,
        "1" : ent.Wall
    }
    with open(file, 'r') as i_stream:
        lines = i_stream.read().splitlines()
        for index, line in enumerate(lines):
            self.matrix[index] = [int(x) for x in list(line)]
