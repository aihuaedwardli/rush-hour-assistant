Rush Hour Assistant
=====================

This package is a assistant to solve the popular rush hour game.

The game consists of a playing board with 6x6 grid. There are a number
of cars in different size and orientation on the board. The cars 
are all of different colors. In this program, I used a single 
color code for each color to speed up the internal search.

The cars can be horizontal or vertically placed on the board.
The horizontal car can only move left or right. The vertical cars
can only move up and down. 

The object is to move the target car red car ('X') to the exit 
grid. The board can start with any pattern, and the car to the exit
grid is blocked. One has to move the other cars around to clear the
passage for the red car to exit.

The program assigned coordinates to the board grid. Horizontal axis
starts from left to right. Vertical index starts from top to bottom.

car.py describe car with color, length, orientation and coordinates 
on the board.

grid keeps track of the occupied space with car's color or empty.
It internal uses array for fast comparison

board is the top level object that describe the game state.

The program uses depth search to find the answer. It does not find the
best answer. 

However, player can specify the option for recursive depth as an 
alternative way to find the best answer, i.e., you can start the depth
as 1 and increase the depth. Or you can use binary search to get
the best answer by specifying different depth.

Enjoy the game.

Aihua Edward Li
5/29/2016

Sample boards:
==============

Sample files for the inital game position are inside the folder.
jam_sovled.txt : board is in solved position
jam_last_1.txt : board is one step away from solved position
jam_sample.txt : beginner level sample board 
jam_beginner.txt : beginner level sample board 
jam_intermediate.txt : intermediate level sample 
jam_expert.txt:   expert level sample ( 2 minutes )

How to Play:
============
python rush-hour.py -f jam_solved.txt -d 3 -h
usage: rush-hour.py [-h] [-f FILE] [-d DEPTH]

Rush Hour Assistant

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  name of the file initial jam condition
  -d DEPTH, --depth DEPTH
                        limit the depth of occurance

Performance:
============
This program has been tested on expert level of of the game.
While it take a talent kid to spent hours on the solution,
this program took only 2 minutes to find a solution.

Sample output:
==============
time python rush_hour.py -f jam_expert.txt -d 74
....
step 74: move car x right 4 steps
+------+
|A DOOO|
|A DBB |
|XX    |
|EEFC R|
|GGFC R|
|  QQQR|
+------+

solution done
Game Stats:
    Max depth: 74
    Max Width: 8884
    Total Nodes: 177580
    Total snapshots: 3248
    Failed on depth: 8883
    Failed exhausted: 31357
    Failed same-node: 137266
    Failed snapshots-full: 0

