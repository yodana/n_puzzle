from copy import deepcopy
from src.heuristics import Heuristic
from src.parserTools import error

class Taquin(object):
	def __init__(self, board, heuristic='manhatan'):
		
		self.deep = 0
		self.moves = []
		self.size = len(board)
		self.board = deepcopy(board)
		self.Heuristic = Heuristic(self, heuristic)
		if not self.isSolvable(board):
			error('Unsolvable')
		if self.isSolved(board):
			error('Already solved')
		

	#Permet d'appliquer une fonction (f) à toutes les tuiles du taquin en mappant le taquin en spirale
	# -> seeNext à true permet de donner à la f les
	def map(self,  f, board=None, begin=0, end=-1, seeNext=False):
		directions = [
			{'begin': 0, 'end': self.size -1, 'step': 1},	# r
			{'begin': 1, 'end': self.size -1, 'step': 1},	# d
			{'begin': self.size -2, 'end': 0, 'step': -1},	# l
			{'begin': self.size -2, 'end': 1, 'step': -1}	# up
		]
		board = self.board if board is None else board
		data = {'x': 0, 'y': 0, 'i': 0}
		prev = None;
		ret = []
		d = 0
		if end > self.size*self.size - 1:
			end = -1;
		while (end < 0 and data['i'] <= self.size*self.size - 1) or (end > 0 and data['i'] < end):
			r = None;
			if data['i'] >= begin:
				if seeNext:
					if data['i'] > 0:
						r = f(prev, data, board)
				else:
					r = f(data, board)
				if r is not None:
					ret.append(r)
			prev = data.copy();
			data['i'] += 1
			if d % 2 == 0:
				if data['y'] == directions[d]['end']:
					directions[d]['begin'] += directions[d]['step']
					directions[d]['end'] -= directions[d]['step']
					d = 0 if d >= len(directions) -1 else d + 1
					data['x'] = directions[d]['begin']
				else:
					data['y'] += directions[d]['step']
			else:
				if data['x'] == directions[d]['end']:
					directions[d]['begin'] += directions[d]['step']
					directions[d]['end'] -= directions[d]['step']
					d = 0 if d >= len(directions) -1 else d + 1
					data['y'] = directions[d]['begin']
				else:
					data['x'] += directions[d]['step']
		return ret

	# récupére le statut du taquin en cours (getStates) 
	def getState(self):
		return({
			'hash': self.getHash(),
			'score': self.getScore(),
			'moves': self.moves,
			'deep': self.deep,
			'board': self.board,
		})

	# change le taquin en cours par celui décris par le statut en paramétre
	def setState(self, state):
		self.board = state['board']
		self.hashage = state['hash']
		self.score = state['score']
		self.moves = state['moves']
		self.deep = state['deep']

	# récupére les statuts des enfants taquin en cours (getStates) 	
	def getChildsStates(self):
		ret = []
		for direction in self.getLegalMove():
			moves = self.moves.copy()
			moves.append(direction);
			board = self.move(direction)
			ret.append({
				'hash': self.getHash(board),
				'score': self.getScore(board) + self.deep + 1,
				'moves': moves,
				'deep': self.deep + 1,
				'board': board,
			});
		return ret


	# isSolved map function
	def isSolved_map(self, data, board=None):
		board = self.board if board is None else board
		if board[data['x']][data['y']] == data['i'] + 1 or (data['i'] == self.size*self.size-1 and board[data['x']][data['y']] == 0):
			return True
		return False

	# Vérifie si le taquin est résolu
	def isSolved(self, board=None):
		board = self.board if board is None else board
		return all(self.map(self.isSolved_map,  board=board))

	# inversionCount_map map function
	def inversionCount__map(self, data, board=None):
		board = self.board if board is None else board
		return 1 if self.toCmp > board[data['x']][data['y']] and board[data['x']][data['y']] != 0 else 0

	# inversionCount map function
	def inversionCount_map(self, data, board=None):
		self.toCmp = board[data['x']][data['y']]
		board = self.board if board is None else board
		return sum(self.map(self.inversionCount__map, board=board, begin=data['i']))

	# Compte le nombre d'inversions nécessaires à la résolution du taquin
	def inversionCount(self, board=None):
		board = self.board if board is None else board
		return sum(self.map(self.inversionCount_map, board=board))

	# Verifie si le taquin est solvable (si le nombre d'inversion est pair)
	def isSolvable(self, board=None):
		board = self.board if board is None else board
		return True if not self.inversionCount(board) % 2 else False

	# Retourne les coordonnées de la tuile de valeur égale à celle donné en paramétre
	def getCoor(self, value, board=None):
		board = self.board if board is None else board
		return {
			'x': [board.index(line) for line in board if value in line][0],
			'y': [line.index(value) for line in board if value in line][0]
		}

	# getDestCoor map function	
	def getDestCoor_map(self, data, board=None):
		board = self.board if board is None else board
		if data['i'] + 1 == self.toCmp or (self.toCmp == 0 and data['i'] == self.size*self.size-1):
			return {'x': data['x'], 'y': data['y']}

	# Retourne les coordonnées lorsque le taquin est résolu de la tuile de valeur égale à celle donné en paramétre 
	def getDestCoor(self, value, board=None):
		board = self.board if board is None else board
		self.toCmp = value;
		ret = self.map(self.getDestCoor_map, board=board)
		return ret[0] if len(ret) == 1 else None;

	# retourne un entier unique à chaque taquin
	def getHash(self, board=None):
		board = self.board if board is None else board
		tmp = []
		for line in board:
			tmp.append(hash(tuple(line)));
		return hash(tuple(tmp))

	# retourne le score d'un taquin calculé celon l'heuristique choisi
	def getScore(self, board=None):
		return self.Heuristic.function(self.board if board is None else board)

	# retourne les mouvements qui sont possibles et qui ne reviennent pas à l'etat préscédant
	# 'l' => left, 'r' => right , 'u' => up, 'd' => down
	def getLegalMove(self, board=None):
		board = self.board if board is None else board
		emptyCaseCoor = self.getCoor(0, board)
		ret = []
		if emptyCaseCoor['x'] > 0 and self.moves[-1:] != 'u':
			ret.append('d')
		if emptyCaseCoor['x'] < self.size - 1 and self.moves[-1:] != 'd': 
			ret.append('u')
		if emptyCaseCoor['y'] > 0 and self.moves[-1:] != 'l': 
			ret.append('r')
		if emptyCaseCoor['y'] < self.size - 1 and self.moves[-1:] != 'r': 
			ret.append('l')
		return ret

	# retourne la copie d'une board aprés lui avoir appliquer le mouvement donné
	def move(self, direction, board=None):
		board = self.board if board is None else board
		cpyboard = deepcopy(board)
		p =  self.getCoor(0, board);
		if direction == "r":
			cpyboard[p['x']][p['y']] = board[p['x']][p['y'] - 1];
			cpyboard[p['x']][p['y'] - 1] = 0;
		elif direction == "l":
			cpyboard[p['x']][p['y']] = board[p['x']][p['y'] + 1];
			cpyboard[p['x']][p['y'] + 1] = 0;
		elif direction == "d":
			cpyboard[p['x']][p['y']] = board[p['x'] - 1][p['y']];
			cpyboard[p['x'] - 1][p['y']] = 0;
		elif direction == 'u':
			cpyboard[p['x']][p['y']] = board[p['x'] + 1][p['y']];
			cpyboard[p['x'] + 1][p['y']] = 0;
		return cpyboard

