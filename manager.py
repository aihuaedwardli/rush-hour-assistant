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

# manager.py manage global configuration and cooridination
# Traffic Jam Assistant

import hashlib
import array

def array_cmp(ref, target):
    # target is a pure array
    for i in range(len(ref)):
        delta = ref[i] - target[i]
        if delta != 0:
            return delta
    return 0

def singleton(cls):
    """Simple wrapper for classes that should only have a single instance."""
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

@singleton
class Manager(object):
    def __init__(self):
        # depth of recurrance
        self.depth = 0
        self.total_nodes = 0
        self.max_depth = 0
        self.args = None
        self.num_snapshots = 0
        self.table = {}
        self.widths = {}
        # error stats
        self.same_node = 0
        self.exhausted = 0
        self.too_deep = 0
        self.snapshots_full = 0
        # command line feature
        self.text_solution = []
        self.graph_solution = []

    def inc_depth(self):
        self.depth += 1
        self.max_depth = max(self.depth, self.max_depth)
        # for each node created, it would also call inc_depth
        # the difference is that depth would be cancelled by depth--
        # the total nodes would not
        self.total_nodes += 1
        if self.depth not in self.widths:
            self.widths[self.depth] = 0
        width = self.widths[self.depth] + 1
        self.widths[self.depth] = width

    def dec_depth(self):
        self.depth -= 1

    def failed_on_too_deep(self):
        self.too_deep += 1
        self.depth -= 1

    def failed_on_exhaustion(self):
        self.exhausted += 1
        self.depth -= 1

    def print_solution(self):
        while len(self.text_solution):
            print self.text_solution.pop()
            print self.graph_solution.pop()
        print "solution done"

    def report_stats(self):
        print "Game Stats:"
        print "    Max depth: %s"%self.max_depth
        print "    Max Width: %s"%self.widths[self.max_depth]
        print "    Total Nodes: %s"%self.total_nodes
        print "    Total snapshots: %s"%self.num_snapshots
        print "    Failed on depth: %s"%self.too_deep
        print "    Failed exhausted: %s"%self.exhausted
        print "    Failed same-node: %s"%self.same_node
        print "    Failed snapshots-full: %s"%self.snapshots_full

    def snapshots(self, grids):
        # grids is simple array
        if self.num_snapshots >= self.args.storage_limit:
            self.snapshots_full += 1
            print "snapshots full"
            return -1
        # return 0 for no error
        hash_val = hashlib.md5()
        hash_val.update(grids)
        key = hash_val.digest()
        # check if it already registered before making copies
        if key in self.table:
            for each in self.table[key]:
                saved_grids, depth = each
                if array_cmp(saved_grids, grids) == 0:
                    # had already registered
                    if depth <= self.depth:
                        # and that node was close to the root
                        self.same_node += 1
                        return -1
                    # current one is closer. simply update the depth
                    self.table[key].remove(each)
                    self.table[key].append((saved_grids, self.depth))
                    return 0
        grids_copy = array.array('B', grids) 
        self.num_snapshots += 1
        if key not in self.table:
            self.table[key] = [(grids_copy, self.depth)]
        else: 
            self.table[key].append((grids_copy, self.depth))
        return 0

