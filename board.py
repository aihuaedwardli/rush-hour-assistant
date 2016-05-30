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

# board.py: describe the playing board 
# Traffic Jam Assistant

import grid
import manager

SIZE = 6

class Board(object):
    def __init__(self):
        self.grids = grid.Grid(SIZE) 
        self.cars = []
        # exit index is 2, 5, save this since it is used often
        self.exit_row = 2
        self.exit_col = 5
        self.manager = manager.Manager()

    def copy(self, original):
        # copy all the car position form the original
        for car in original.cars:
            self.add_car(car.copy())

    def add_car(self, car):
        coordinates = car.get_covered_space(SIZE)
        for each in coordinates:
            row, col = each 
            color = self.grids.get_color(each)
            if color != ' ':
                raise Exception("place %s: collided at (%s, %s) with %s"%(
                        car, row, col, color))
            self.grids.set_color(each, car.color)
        self.cars.append(car)

    def graph_board(self):
        heading = "+" + "-"*(SIZE) + "+\n"
        graph = heading
        for i in range(SIZE):
            graph += "|"
            for j in range(SIZE):
                graph += self.grids.get_color((i, j))
            graph += "|\n"
        graph += heading
        return graph

    def print_board(self):
        print self.graph_board()

    def add_solution(self, text):
        self.manager.text_solution.append(text)
        self.manager.graph_solution.append(self.graph_board())

    def move(self, car, direction):
        # keep copy of current start position for all cases
        coordinates = car.move(direction, SIZE)
        if coordinates is None:
            return -1

        covered_space, freed_space = coordinates
        if self.grids.get_color(covered_space) != ' ':
            #msg = "would collide"
            return -1
        self.grids.set_color(covered_space, car.color)
        self.grids.set_color(freed_space, ' ')
        return 0 

    def clone_with_move(self, car, direction):
        # clone a copy of self after the move in the direction
        # self is not affected
        coordinate = car.coordinate
        grids_save = self.grids
        self.grids = grids_save.copy()
        if self.move(car, direction) == 0:
            board = Board()
            board.copy(self)
        else:
            board = None
        # restore to the origin state immediately after the copy
        car.coordinate = coordinate 
        self.grids = grids_save
        return board

    def is_solved(self):
        # there is no object between exit_col and car x
        num_space = 0
        for j in range(self.exit_col, 0, -1):
            color = self.grids.get_color((self.exit_row, j)) 
            if color == 'X':
                print "problem solved."
                text = "step %s: move car x right %s steps"%(
                        self.manager.depth, num_space)
                self.add_solution(text)
                return 1
            if color != ' ':
                return 0
            num_space += 1
        raise Exception("should not be here")

    def solve(self):
        self.manager.inc_depth()
        print "recursive depth = %s"%self.manager.depth
        
        if self.is_solved():
            self.manager.dec_depth()
            return self.manager.depth 

        if self.manager.depth >= self.manager.args.depth:
            print "recursive depth too deep (%s)"%self.manager.depth
            self.manager.failed_on_too_deep()
            return -1

        ret = self.grids.snapshot()
        if ret:
            # snapshot is taken care by manager, which knows how to
            # process the error. so we simply dec depth here
            self.manager.dec_depth()
            return -1 

        for car in self.cars:
            # there can only be two way to move the car, forward or backward
            for direction in ('+', '-'):
                print "depth %s, moving %s %s"%(self.manager.depth, 
                        car, car.print_movement(direction))
                new_board = self.clone_with_move(car, direction)
                if new_board:
                    # restore to the origin state immediately after the copy
                    msg = "moved %s %s"%(car, car.print_movement(direction))
                    print "depth %s, %s, new board:"%(self.manager.depth, msg)
                    new_board.print_board()
                    ret = new_board.solve()
                    if ret >= 0:
                        # solved by sub-problem. print
                        text = "step %s: move %s %s"%(self.manager.depth, 
                                car, car.print_movement(direction))
                        self.add_solution(text)
                        self.manager.dec_depth()
                        return ret 
        print "failed to solve: all nodes exhausted."
        self.manager.failed_on_exhaustion()
        return -1

