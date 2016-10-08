#!/usr/bin/python3
'''Progress bar module'''

import sys

class ProgressBar:
    '''Main class'''
    def __init__(self, max_progress):
        self.progress = 0
        self.max_progress = max_progress
    def invoke(self, new_progress):
        '''Checks if some progress made and
calls print() if so'''
        new_progress = int(100*(new_progress)/(self.max_progress))
        if self.progress != new_progress:
            self.progress = new_progress
            self.print()
    def print(self):
        '''Prints progress bar'''
        sys.stdout.write(
            '\r[{0:10}] {1}%'.format(
                '#'*int(self.progress/10),
                self.progress)
            )
        sys.stdout.flush()
        if self.progress == 100:
            print()
