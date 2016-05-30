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

# Traffic Jam Assistant

import argparse

import car
import manager
import board

def main():
    mgr = manager.Manager()

    parser = argparse.ArgumentParser(description='Rush Hour Assistant')
    parser.add_argument("-c", "--confirm-only", action='store_true',
                        help="confirm the initial board only")
    parser.add_argument("-d", "--depth", type=int, default=10,
                        help="limit the depth of occurance")
    parser.add_argument("-f", "--file", default='jam.txt',
                        help="name of the file initial jam condition")
    parser.add_argument("-s", "--storage-limit", type=int, default=10000,
                        help="limit number of snapshots in storage")
    mgr.args = parser.parse_args()
    args = mgr.args

    my_board = board.Board()

    print "reading initial Jam condition (depth=%s)"%(args.depth)
    with open(args.file) as f_input:
        for line in f_input.readlines():
            if len(line.strip()) <= 0:
                continue
            if line.startswith("#"):
                continue
            color, orientation, length, row, col = line.strip().split(",")
            length = int(length)
            row = int(row)
            col = int(col)
            my_car = car.Car(color, orientation, length, (row, col))
            my_board.add_car(my_car)

    my_board.print_board()
    if mgr.args.confirm_only:
        exit(0)
    ret = my_board.solve()
    if ret >= 0:
        print "==============="
        print "Starting board:"
        print "==============="
        my_board.print_board()
        print "Solution steps:"
        mgr.print_solution()
    mgr.report_stats()

if __name__ == "__main__":
    main()

