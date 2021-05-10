import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

class TaquinGame(object):
	def __init__(self, taquin, moves):
		self.launched = False
		self.taquin = taquin
		self.size = len(taquin)
		self.moves = moves
		self.emptyCaseCoor = {
			'x': [taquin.index(line) for line in taquin if 0 in line][0],
			'y': [line.index(0) for line in taquin if 0 in line][0]
		}
		self.setupPygame()
		self.gameLoop()

	def setupPygame(self):
		self.windowsSize = 500
		self.tuileSize = int(self.windowsSize / self.size)
		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode((self.windowsSize, self.windowsSize))
		self.font = pygame.font.SysFont('Comic Sans MS', 30)
		
	def getLegalMoves(self):
		ret = []
		if self.emptyCaseCoor['x'] != 0:
			ret.append('d')
		if self.emptyCaseCoor['x'] != self.size - 1: 
			ret.append('u')
		if self.emptyCaseCoor['y'] != 0: 
			ret.append('r')
		if self.emptyCaseCoor['y'] != self.size - 1: 
			ret.append('l')
		return ret

	def moveUp(self):
		left = self.tuileSize * self.emptyCaseCoor['y'] + self.tuileSize/3
		top = self.tuileSize*(self.emptyCaseCoor['x']+1) +self.tuileSize/3
		for add in range(0, self.tuileSize):
			self.screen.blit(self.tuiles[self.emptyCaseCoor['x']+1][self.emptyCaseCoor['y']],[left, top-add])
			pygame.display.update()
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = self.taquin[self.emptyCaseCoor['x']+1][self.emptyCaseCoor['y']]
		self.emptyCaseCoor['x'] += 1
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = 0
		
	def moveDown(self):
		left = self.tuileSize * self.emptyCaseCoor['y'] + self.tuileSize/3
		top = self.tuileSize*(self.emptyCaseCoor['x']-1) +self.tuileSize/3
		for add in range(0, self.tuileSize):
			self.screen.blit(self.tuiles[self.emptyCaseCoor['x']-1][self.emptyCaseCoor['y']],[left, top+add])
			pygame.display.update()
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = self.taquin[self.emptyCaseCoor['x']-1][self.emptyCaseCoor['y']]
		self.emptyCaseCoor['x'] -= 1
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = 0
		
	def moveRight(self):
		left = self.tuileSize *(self.emptyCaseCoor['y']-1)+self.tuileSize/3
		top = self.tuileSize*self.emptyCaseCoor['x']+self.tuileSize/3
		for add in range(0, self.tuileSize):
			self.screen.blit(self.tuiles[self.emptyCaseCoor['x']-1][self.emptyCaseCoor['y']],[left+add, top])
			pygame.display.update()
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']-1]
		self.emptyCaseCoor['y'] -= 1
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = 0
		
	def moveLeft(self):
		left = self.tuileSize*(self.emptyCaseCoor['y']+1)+self.tuileSize/3
		top = self.tuileSize*self.emptyCaseCoor['x']+self.tuileSize/3
		for add in range(0, self.tuileSize):
			self.screen.blit(self.tuiles[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']+1],[left-add, top])
			pygame.display.update()
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']+1]
		self.emptyCaseCoor['y'] += 1
		self.taquin[self.emptyCaseCoor['x']][self.emptyCaseCoor['y']] = 0

	def applyMove(self, move):
		if move in self.getLegalMoves():
			if move == 'u': 
				self.moveUp()
			if move == 'd': 
				self.moveDown()
			if move == 'l': 
				self.moveLeft()
			if move == 'r': 
				self.moveRight()
			self.showTaquin()
	
	def showTaquin(self):
		self.tuiles = []
		for i in range(self.size):
			rectsLine = []
			for j in range(self.size):
				tuile = self.font.render(str(self.taquin[i][j] if self.taquin[i][j] else  ''),0,[33,33,33])
				pygame.draw.rect(self.screen, (255,255,255),  [self.tuileSize * j, self.tuileSize * i, self.tuileSize, self.tuileSize], 0)
				self.screen.blit(tuile,[self.tuileSize * j + self.tuileSize/3, self.tuileSize * i + self.tuileSize/3])
				rectsLine.append(tuile)
			self.tuiles.append(rectsLine)
		pygame.display.update()
			
	def gameLoop(self):
		self.currentMoveIndex = 0
		self.play = True
		self.launched = True
		self.showTaquin()
		if self.moves:
			for move in self.moves:
				self.applyMove(move)
		while self.launched:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.launched = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_DOWN:
						self.applyMove('d')
					if event.key == pygame.K_UP:
					    self.applyMove('u')	 
					if event.key == pygame.K_LEFT:
					    self.applyMove('l')
					if event.key == pygame.K_RIGHT:
					    self.applyMove('r')