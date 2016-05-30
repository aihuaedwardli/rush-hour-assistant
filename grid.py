#!/usr/bin/env python2.7

# Copyright 2016  Aihua Edward Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# grid.py: describe the grid state of the playing board
# part of Traffic Jam Assistant Project
# array would be used for fast comparison, the grid wrap array object
# so the details of how to indexing into two dimensions and other actions
# are abstracted

import array

import manager

# SPACE - 'A' would be negative, to avoid overflow
# so we replace the ord of 'Z' which is unused in the game
SPACE_CODE = ord('Z') - ord('A') + 2
X_CODE = ord('X') - ord('A')

# global color to code lookup table
def color_2_code(color):
    if color == ' ':
        return SPACE_CODE
    return ord(color) - ord('A')

def code_2_color(code):
    if code == SPACE_CODE:
        return ' '
    return chr(code + ord('A'))

class Grid(object):
    def __init__(self, size, grids=None):
        self.size = size
        self.array_size = size * size
        source = grids 
        if source is None:
            source = [SPACE_CODE for _ in range(self.array_size)]
        self.grids = array.array('B', source)
        self.manager = manager.Manager()
    
    def get_color(self, coordinate):
        row, col = coordinate
        # skip check for now
        return code_2_color(self.grids[row * self.size + col])
    
    def set_color(self, coordinate, color):
        row, col = coordinate
        # skip check for now
        self.grids[row * self.size + col] = color_2_code(color)
    
    def copy(self):
        return Grid(self.size, self.grids)

    def snapshot(self):
        return self.manager.snapshots(self.grids)
