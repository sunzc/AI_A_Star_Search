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

# definations for move
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

class State:
	def __init__(self, board):
		n = len(board)
		self.board = []
		for i in range(n):
			self.board.append([])
			for j in range(n):
				self.board[i][j] = board[i][j]
	def get_h_val(self):
		pass
	def move_func(self, move):
		pass
	def is_goal(self):
		pass
	def is_same(self, state):
		pass
	def actions(self):
		pass

class Node:
	def __init__(self, state):
		self.state = state
		self.history_move = []
		self.g_val = 0
		self.h_val = state.get_h_val()
		self.f_val = self.g_val + self.h_val

	def __init__(self, old_node, move):
		self.state = State(old_node.board)
		self.state.move_func(move)
		# copy history
		self.history_move = []
		for m in old_state.history_move:
			self.history_move.append(m)
		self.history_move.append(move)
		# update g_val
		self.g_val = old_node.g_val + 1
		# update h_val
		self.h_val = self.state.get_h_val()
		# update f_val
		self.f_val = self.g_val + self.h_val

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


q = Q.PriorityQueue()

class ExploredList:
	def __init__(self):
		self.explored = []
	def add_state(self, state):
		self.explored.append(state)
	def has_state(self, state):
		for s in self.explored:
			if s.is_same(state):
				return True
		return True

class AStar:
	def __init__(self, in_file):
		# construct start node
		board = self.get_board_from_input(in_file)
		self.start_state = State(board)
		self.frontier = Q.PriorityQueue()
		self.explored = ExploredList()
		self.target = None

	def get_board_from_input(self, in_file):
		pass

	def generate_output(self, out_file):
		pass

	def search(self):
		start_node = Node(self.start_state)
		self.frontier.put(start_node)
		while not self.frontier.empty():
			current = self.frontier.get()
			if current.state.is_goal():
				self.target = current
				return current
			if not self.explored.has_state(current.state):
				explored.add(current.state)
				for action in current.state.actions():
					new = State(current, action)
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
	else:
		usage(1)


	a_star = AStar(in_file)
	if a_star.search() != None:
		a_star.generate_output(out_file)
		print("A-star search succeed!")
	else:
		print("Error: A-star search failed!")

	in_file.close()
	out_file.close()
