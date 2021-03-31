import re
from utils import *
from math import *
from copy import deepcopy

closed_list = [];

def get_hash(board):
	size = len(board[0]);
	hash = 0;
	m = 1;
	for line in board:
		for i in line:
			hash = hash + (i * m);
			m = m + 1;
	return hash;

def taquinToTuple(taquin):
	ret = []
	for line in taquin:
		ret.append(tuple(line))
	return tuple(ret)

def printBoard(board):
	for line in board:
		print(line,'\n')

class Position:
	def __init__(self, x, y):
		self.x = x;
		self.y = y;

class Score:
	def __init__(self, board, sol, size):
		self.h = self.init_h(board, sol, size)
		self.g = 1;
		self.score = self.h + self.g
	
	def init_h(self, board, sol, size):
		h = 0;
		for i in range(0, size * size - 1):
			p = Position([board.index(line) for line in board if i in line][0], [line.index(i) for line in board if i in line][0]);
			reel_position = Position([sol.index(line) for line in sol if i in line][0], [line.index(i) for line in sol if i in line][0])
			h = h + abs(p.x - reel_position.x) + abs(p.y - reel_position.y);
		return h;

class init_Board:
	def __init__(self, file):
		self.board = self.getBoard(file);
		self.sol = self.getSolBoard(self.size);

	#reel board for distance manathan
	def getSolBoard(self, size):
		size = self.size;
		board = [[0] * self.size for i in range(self.size)];
		k = 0;
		j = 0;
		b = 0;
		n = 0;
		i = 1;
		a = floor(size / 2);
		if size % 2 == 1:
			o = 1;
			minus = 0;
		else:
			o = -1;
			minus = -1;
		while(i <= size * size - 1):
			while b < n and i <= size * size - 1:
				if (b < n / 2):
					j = j + o;
				else:
					k = k + o;
				board[abs(k - a)][j + a + minus] = (size * size) - i;
				b = b + 1;
				i = i + 1;
			b = 0;
			o = o * -1;
			n = n + 2;
		return board;
					
	def checkBoard(self, board):
		size = len(board)
		if size < 3:
			error('minimal board size is 3')
		met = []
		for i in range(0, len(board)):
			for j in range(0, len(board[i])):
				if len(board[i]) != size or board[i][j] < 0 or board[i][j] > size*size or board[i][j] in met:
					error('invalid board')
				met.append(board[i][j])
		return True

	#return board from args
	def getBoard(self, f):
		try:
			file = open(f, 'r')
		except OSError:
			error("Could not open/read/find " + f)
		with open(f, 'r') as file:
			board = []
			self.size = 0;
			lines = re.sub(r'#.*', '', file.read()).split('\n')
			for i in range(0, len(lines)):
				line_arr = []
				line = lines[i].split(' ')
				for j in range(0, len(line)):
					if not self.size and line[j].isnumeric():
						self.size = int(line[j])
					elif line[j] and line[j].isnumeric():
						line_arr.append(int(line[j]))
				if len(line_arr) > 0 and len(line_arr) == self.size:
					board.append(line_arr)
		if self.checkBoard(board):
			return (board)
		
	#print board
	def printBoard(self):
		for line in self.board:
			print(line,'\n')
	
	def printSolBoard(self):
		for line in self.sol:
			print(line,'\n')

	#move 
	def test_move(self, direction, test):
		i = 0;
		if (test):
			t_board = deepcopy(self.board);
		else:
			t_board = self.board;
		for line in t_board:
			if 0 in line:
				p = Position(i, line.index(0));
			i = i + 1;
		if direction == "right":
			if p.y > 0:
				t_board[p.x][p.y] = t_board[p.x][p.y - 1];
				t_board[p.x][p.y - 1] = 0;
			else:
				return (-1);
		elif direction == "left":
			if p.y < self.size - 1:
				t_board[p.x][p.y] = t_board[p.x][p.y + 1];
				t_board[p.x][p.y + 1] = 0;
			else:
				return (-1);
		elif direction == "up":
			if p.x > 0:
				t_board[p.x][p.y] = t_board[p.x - 1][p.y];
				t_board[p.x - 1][p.y] = 0;
			else:
				return (-1);
		elif direction == "down":
			if p.x < self.size - 1:
				t_board[p.x][p.y] = t_board[p.x + 1][p.y];
				t_board[p.x + 1][p.y] = 0;
			else:
				return (-1);
		if (test == True):
			h = hash(taquinToTuple(t_board));
			if h in closed_list:
				return -1;
			else:
				return Score(t_board, self.sol, self.size);
		elif (test == False):
			h = hash(taquinToTuple(t_board))
			closed_list.append(h);
'''#check if board is or not valid
def checkBoard(board):
	size = len(board)
	if size < 3:
		error('minimal board size is 3')
	met = []
	for i in range(0, len(board)):
		for j in range(0, len(board[i])):
			if len(board[i]) != size or board[i][j] < 0 or board[i][j] > size*size or board[i][j] in met:
				error('invalid board')
			met.append(board[i][j])
	return True

#return board from args
def getBoard(filepath):
	try:
		file = open(filepath, 'r')
	except OSError:
		error("Could not open/read/find " + filepath)
	with open(filepath, 'r') as file:
		board = []
		size = 0;
		lines = re.sub(r'#.*', '', file.read()).split('\n')
		for i in range(0, len(lines)):
			line_arr = []
			line = lines[i].split(' ')
			for j in range(0, len(line)):
				if not size and line[j].isnumeric():
					size = int(line[j])
				elif line[j] and line[j].isnumeric():
					line_arr.append(int(line[j]))
			if len(line_arr) > 0:
				board.append(line_arr)
		if checkBoard(board):
			return (board)'''