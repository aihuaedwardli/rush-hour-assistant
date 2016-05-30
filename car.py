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

# car.py : class car for the project 
# Traffic Jam Assistant

class Car(object):
    # orientation = '|' for vertical, '-', for horizontal
    def __init__(self, color, orientation, length, coordinate):
        #print "construct car: color %s, orientation %s, length %s"%(
        #        color_2_color(color), orientation, length)
        self.color = color
        self.orientation = orientation
        self.length = length
        self.coordinate = coordinate

    def __str__(self):
        return "car %s%s%s"%(self.color,
                self.orientation, self.length)

    def print_movement(self, sign):
        if self.orientation == "-":
            return "right" if sign == "+" else "left"
        return "down" if sign == "+" else "up"

    def get_covered_space(self, border):
        ''' 
            return a list of coordinates covered by the car
        '''
        row, col = self.coordinate
        coordinates = []
        if self.orientation == '-':
            for j in range(col, col + self.length):
                if j >= border:
                    raise Exception("place %s: (%d, %d) out of board"%(
                        self, row, j))
                coordinates.append((row, j))
        else:
            for i in range(row, row + self.length):
                if i >= border:
                    raise Exception("place %s: (%d, %d) out of board"%(
                        self, i, col))
                coordinates.append((i, col))
        return coordinates

    def move_right(self, border):
        row, col = self.coordinate
        new_col = col + self.length
        if new_col >= border:
            # not able to move 
            return None
        # update col since the car moved right
        self.coordinate = (row, col + 1)
        return ((row, col + self.length), (row, col))  
        
    def move_left(self):
        row, col = self.coordinate
        new_col = col - 1 
        if new_col < 0:
            # not able to move 
            return None
        self.coordinate = (row, col - 1)
        return ((row, col - 1), (row, col + self.length - 1))  
        
    def move_down(self, border):
        row, col = self.coordinate
        new_row = row + self.length
        if new_row >= border:
            # not able to move 
            return None
        self.coordinate = (row + 1, col)
        return ((row + self.length, col), (row, col))  
        
    def move_up(self):
        row, col = self.coordinate
        new_row = row - 1 
        if new_row < 0:
            # not able to move 
            return None
        self.coordinate = (row - 1, col)
        return ((row - 1, col), (row + self.length - 1, col))  
        
    def move(self, direction, border):
        '''
            returns a list of two coordinates
            the space to be occupied
            the space to be freed
        '''
        if self.orientation == '-':
            if direction == "+": 
                ret = self.move_right(border) 
            else:
                ret = self.move_left()
        else:
            if direction == "+": 
                ret = self.move_down(border) 
            else:
                ret = self.move_up()
        return ret

    def copy(self):
        return Car(self.color, self.orientation, self.length, self.coordinate)

