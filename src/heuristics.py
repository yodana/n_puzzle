from math import sqrt

class Heuristic(object):
	def __init__(self, Taquin, heuristic):
		self.Taquin = Taquin
		self.size = Taquin.size
		if heuristic == 'perso':
			self.function = self.perso
		elif heuristic == 'inversions':
			self.function = self.inversions
		elif heuristic == 'euclide':
			self.function = self.euclide
		elif heuristic == 'best':
			self.function = self.best
		else:
			self.function = self.manhatan

	# Calcule la somme des distances (manhatan) entre chaque tuile et sa destination 
	def manhatan(self, board):
		score = 0
		for line in board:
			for tuile in line:
				p =  self.Taquin.getCoor(tuile, board);
				d = self.Taquin.getDestCoor(tuile)
				score += abs(p['x'] - d['x']) + abs(p['y'] - d['y'])
		return score

	# Calcule la somme des distances (euclide) entre chaque tuile et sa destination 
	def euclide(self, board):
		score = 0
		for line in board:
			for tuile in line:
				p =  self.Taquin.getCoor(tuile, board);
				d = self.Taquin.getDestCoor(tuile)
				d1 = abs(p['x'] - d['x'])
				d2 = abs(p['y'] - d['y'])
				score +=  sqrt(d1*d1+d2*d2)
		return score


	# best map function
	def best_map(self, ctuile, ntuile, board):
		if ntuile['i'] < (self.size -1) * 4:
			if board[ntuile['x']][ntuile['y']] != board[ctuile['x']][ctuile['y']] + 1:
				return 2
		elif board[ntuile['x']][ntuile['y']] != 0:
			return 1

	#P(n) + 3 * S (n), où P(n)est la distance manhatan et S (n) est un score de séquence qui vérifie
	#les carrés non centraux à leur tour, attribuant 0 pour chaque tuile suivi de son propre
	#successeur et 2 pour chaque tuile qui ne l'est pas; avoir une pièce au centre marque 1.
	def best(self, board):
		return self.manhatan(board) + 3 * sum(self.Taquin.map(self.best_map,  board=board, seeNext=True))
		
	# Compte le nombre d'inversions nécéssaire à la résolution du taquin
	def inversions(self, board):
		return self.Taquin.inversionCount(board)

	# Un mix de toutes les heuristics 
	def perso(self, board):
		return self.best(board) + self.euclide(board) / 5 + self.inversions(board) / 2
