#!/usr/bin/env python3

import sys

from puzzleSolver import State
from puzzleSolver import Node
from puzzleSolver import AStar

U = 1
R = 2
D = 3
L = 4

move_map_action = {'U':[-1, 0],'R':[0, 1],'D':[1, 0],'L':[0, -1]}
move_map_id = {'U':U, 'R':R,'D':D,'L':L}

if __name__ == '__main__':
	if len(sys.argv) == 3:
		in_file_board = open(sys.argv[1], 'r')
		in_file_moves = open(sys.argv[2], 'r')
	else:
		print('\treplay.py <INPUT_FILE_PATH> <MOVE_FILE_PATH>')
		exit(1)

	moves = in_file_moves.readline().split(',')
	astar = AStar(in_file_board, 1)

	start_node= Node(astar.start_state)
	start_node.state.print_board()
	current = start_node
	for m in moves:
		print(m)
		new = Node.transfer(current, move_map_id[m])
		new.state.print_board()
		current = new
	
