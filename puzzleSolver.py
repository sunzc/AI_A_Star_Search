#!/usr/bin/env python3

# Project: AI Assignment#1.
# Description: A* for pile puzzle
# Author: Zhichuang Sun
# SBUID: 110345185
# E-mail: zhisun@cs.stonybrook.edu

try:
	import Queue as Q # ver. < 3.0
except ImportError:
	import queue as Q

import sys

# definations for move, UP, RIGHT, DOWN, LEFT
U = 1
R = 2
D = 3
L = 4

move_map_letter = {U:'U',R:'R',D:'D',L:'L'}
move_map_action = {U:[-1, 0],R:[0, 1],D:[1, 0],L:[0, -1]}

class State:
	def __init__(self, board, heuristic_id):
		self.n = len(board)
		self.board = []
		self.h_id = heuristic_id
		for i in range(self.n):
			self.board.append([])
			for j in range(self.n):
				self.board[i].append(board[i][j])
		self.print_board()

	def print_board(self):
    		print("")
    		for row in self.board:
    		    row_str = ""
    		    for cell in row:
    		        row_str += str(cell) + " "
    		    print(row_str)
		
	# calculate h(n) for current state
	def get_h_val(self):
		if self.h_id == 1:
			return self.heuristic_func_1()
		elif self.h_id == 2:
			return self.heuristic_func_2()

	
	# use number of misplaced tiles as h()
	def heuristic_func_1(self):
		h = 0
		N = (self.n) * (self.n)
		for i in range(self.n):
			for j in range(self.n):
				if (self.board[i][j] % N) != ((i * self.n + j + 1) % N):
					h += 1
		return h

	# use sum of distance to end positions
	def heuristic_func_2(self):
		h = 0
		N = (self.n) * (self.n)
		for i in range(self.n):
			for j in range(self.n):
				if (self.board[i][j] % N) != ((i * self.n + j + 1) % N):
					v = self.board[i][j]
					if v == 0:
						x, y = (self.n - 1), (self.n - 1)
					else:
						x = (v - 1) / self.n
						y = (v - 1) % self.n

					h += abs(x - i) + abs(y - i)
		return h

	def find_gap(self):
    		for i in range(len(self.board)):
    		    for j in range(len(self.board[i])):
    		        if self.board[i][j] == 0:
    		            return i,j
    		return -1, -1

	def next_pos(self, x, y, move):
		next_x = x + move[0]
		next_y = y + move[1]

		return next_x, next_y

	def move_gap(self, move):
		x, y = self.find_gap()
		x2, y2 = self.next_pos(x, y, move)

		tmp = self.board[x][y]
		self.board[x][y] = self.board[x2][y2]
		self.board[x2][y2] = tmp	

	def is_goal(self):
		N = (self.n) * (self.n)
		for i in range(self.n):
			for j in range(self.n):
				if (self.board[i][j] % N) != ((i * self.n + j + 1) % N):
					return False
		return True

	def is_same(self, state):
		for i in range(self.n):
			for j in range(self.n):
				if self.board[i][j] != state.board[i][j]:
					return False
		return True

	def is_move_legal(self, x, y, move):
		x1, y1 = self.next_pos(x, y, move)
		return ((x1 >= 0) and (x1 < self.n) and (y1 >= 0) and (y1 < self.n))

	def actions(self):
		actions = []
		x, y = self.find_gap()

		if self.is_move_legal(x, y, move_map_action[U]):
			actions.append(U)
		elif self.is_move_legal(x, y, move_map_action[R]):
			actions.append(R)
		elif self.is_move_legal(x, y, move_map_action[D]):
			actions.append(D)
		elif self.is_move_legal(x, y, move_map_action[L]):
			actions.append(L)

		return actions

class Node:
	def __init__(self, state):
		self.state = state
		self.history_move = []
		self.g_val = 0
		self.h_val = state.get_h_val()
		self.f_val = self.g_val + self.h_val

	def transfer(old_node, action):
		state = State(old_node.state.board, old_node.state.h_id)
		state.move_gap(move_map_action[action])
		new_node = Node(state)

		# copy history
		for m in old_node.history_move:
			new_node.history_move.append(m)
		new_node.history_move.append(move_map_letter[action])

		# update g_val
		new_node.g_val = old_node.g_val + 1
		# update h_val
		new_node.h_val = new_node.state.get_h_val()
		# update f_val
		new_node.f_val = new_node.g_val + new_node.h_val

		return new_node

	def _cmp(self, other, method):
		try:
			return method(self._cmpkey(), other._cmpkey())
		except (AttributeError, TypeError):
			# _cmpkey not implemented, or return differnt type
			return NotImplemented

	def _cmpkey(self):
		return self.f_val
	def __lt__(self, other):
		return self._cmp(other, lambda s, o : s < o)
	def __le__(self, other):
		return self._cmp(other, lambda s, o : s <= o)
	def __gt__(self, other):
		return self._cmp(other, lambda s, o : s > o)
	def __ge__(self, other):
		return self._cmp(other, lambda s, o : s >= o)
	def __eq__(self, other):
		return self._cmp(other, lambda s, o : s == o)
	def __ne__(self, other):
		return self._cmp(other, lambda s, o : s != o)
	def __repr__(self):
		pass

class ExploredList:
	def __init__(self):
		self.explored = []
	def add_state(self, state):
		self.explored.append(state)
	def has_state(self, state):
		for s in self.explored:
			if s.is_same(state):
				return True
		return False

class AStar:
	def __init__(self, in_file, heuristic_id):
		# construct start node
		self.h_id = heuristic_id
		board = self.get_board_from_input(in_file)
		self.start_state = State(board, heuristic_id)
		self.frontier = Q.PriorityQueue()
		self.explored_list = ExploredList()
		self.target = None

	def get_board_from_input(self, in_file):
		lines = in_file.readlines()
		board = []
		i,j = 0,0
		n = len(lines)
		for line in lines:
			board.append([])
			fields = line.strip().split(',')

			assert(len(fields) == n)

			for j in range(n):
				if (fields[j] != ''):
					board[i].append(int(fields[j]))
				else:
					board[i].append(0)
			i += 1
		return board

	def generate_output(self, out_file):
		if self.target != None:
			for x in self.target.history_move:
				out_file.write(x)
				out_file.write(',')
		else:
			print('Error in generate_output(): no target found in A* saerch!')

	def search(self):
		start_node = Node(self.start_state)
		self.frontier.put(start_node)
		while not self.frontier.empty():
			current = self.frontier.get()
			if current.state.is_goal():
				self.target = current
				return current
			if not self.explored_list.has_state(current.state):
				self.explored_list.add_state(current.state)
				for action in current.state.actions():
					new = Node.transfer(current, action)
					self.frontier.put(new)
		return None
# errnum:
# 	0 means Invalid arguments
#	1 means Wrong number of arguments
def usage(errnum):
	if errnum == 1:
		print('Wrong number of arguments. Usage:')
	else:
		print('Invalid arguments. Usage:')
	print('\tpuzzleSolver.py <#Algorithm> <N> <INPUT_FILE_PATH> <OUTPUT_FILE_PATH>')

if __name__ == '__main__':

	alg = 0
	n = 0
	in_file = ''
	out_file = ''

	if len(sys.argv) == 5:
		try:
			alg = int(sys.argv[1]) # 1 = A* and 2 = Memory bounded variant
			n = int(sys.argv[2]) # 3 = 8-puzzle, 4 = 15-puzzle format
			in_file = open(sys.argv[3], 'r')
			out_file = open(sys.argv[4], 'w')
		except:
			usage(0)
			exit(1)
	else:
		usage(1)
		exit(1)

	# try heuristic_id == 1
	a_star = AStar(in_file, 1)
	if a_star.search() != None:
		a_star.generate_output(out_file)
		print("A-star search succeed!")
	else:
		print("Error: A-star search failed!")

	in_file.close()
	out_file.close()
