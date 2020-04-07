import random
import collections
import math
from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):

	def getMove(self, grid):
		score = float('-inf')
		bestMove = 1
		for i in range(3):
			tempGrid = grid.clone()
			if tempGrid.move(i+1):
				emptyCells = len(tempGrid.getAvailableCells())
				if emptyCells > 7:
					moveScore = self.expectimax(tempGrid,2,False)
				else:
					if emptyCells > 3:
						moveScore = self.expectimax(tempGrid,3,False)
					else:
						moveScore = self.expectimax(tempGrid,4,False)
				if moveScore > score:
					score = moveScore
					bestMove = i+1
		return bestMove

	def expectimax(self, grid, depth, isPlayer):
		if isPlayer and not grid.canMove():
			return -999999
		if depth == 0:
			return self.getScore(grid)
		if not isPlayer:
			scoreT = 0
			length = 0
			for cell in grid.getAvailableCells():
				temp = grid.clone()
				length += 1
				temp.setCellValue(cell, 2)
				scoreT += 0.9 * self.expectimax(temp,depth-1,True)
				temp = grid.clone()
				temp.setCellValue(cell, 4)
				scoreT += 0.1 * self.expectimax(temp,depth-1,True)
				# grid.setCellValue(cell,0)
			return scoreT/length if length > 0 else -999999
		if isPlayer:
			scoreT = -999999
			for i in range(3):
				temp = grid.clone()
				temp.move(i+1)
				scoreT = max(scoreT,self.expectimax(temp,depth-1,False))
			return scoreT
	
	def getScore(self, grid):
		score = 1
		weightMatrix = [[0,1,2,3],
						[7,6,5,4],
						[8,9,12,14],
						[24,18,16,15]]
		penalty = 1
		previousPos = -1
		for i in range (4):
			for j in range(4):
				pos = grid.map[i][j]
				if previousPos != -1:
					penalty += 2*abs(pos-previousPos)
					previousPos = pos
				score += pos * weightMatrix[i][j]
				if (pos):
					if(i - 1 >= 0):
						penalty += abs(grid.map[i-1][j] - pos)
					if(i + 1 <= 3):
						penalty += abs(grid.map[i+1][j] - pos)
			previousPos = -1
		
		# print("SCORE ", math.log2(score*2))
		# print("PENALTY:", math.log2(penalty/8))			
		heur = score - penalty*2 + len(grid.getAvailableCells())**2
		#- math.log2(penalty/16)
		return heur
		 
				
