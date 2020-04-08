# Alex Taradachuk
# Prof. Raja
# CSCI - 350
# Assignment 2 - 2048 AI
import random
import collections
import math
from BaseAI_3 import BaseAI


class PlayerAI(BaseAI):

	def getMove(self, grid):
		score = float('-inf')
		bestMove = 1 
		for i in range(3): #automatically prune up position given nature of heuristic - the snake pattern runs downwards leading to no necessary case where an up move is needed
			tempGrid = grid.clone() # clone the grid
			if tempGrid.move(i+1): #move in chosen direction
				emptyCells = len(tempGrid.getAvailableCells()) #get number of free cells to be used for iterative deepening
				if emptyCells > 12:
					moveScore = self.expectimax(tempGrid,2,False) #run at an effective depth of 3
				else:
					if emptyCells > 5:
						moveScore = self.expectimax(tempGrid,3,False) #run at an effective depth of 4
					else:
						moveScore = self.expectimax(tempGrid,4,False) #run at an effective depth of 5
				if moveScore > score:
					score = moveScore #check if score has been beaten
					bestMove = i+1 #update best move 
		return bestMove

	def expectimax(self, grid, depth, isPlayer): #expectimax algorithm used to determine best move
		if isPlayer and not grid.canMove():
			return -999999 #if grid cannot move then return worst score
		if depth == 0: #reached leaf node
			return self.getScore(grid) #evaluation function
		if not isPlayer: #expected layer
			scoreT = 0
			length = 0
			for cell in grid.getAvailableCells(): #set value of each cell to 2 or 4 and run expectimax on each variation
				temp = grid.clone()
				length += 1
				temp.setCellValue(cell, 2)
				scoreT += 0.9 * self.expectimax(temp,depth-1,True)
				temp = grid.clone()
				temp.setCellValue(cell, 4)
				scoreT += 0.1 * self.expectimax(temp,depth-1,True)
			return scoreT/length if length > 0 else -999999
		if isPlayer: #max node
			scoreT = -999999 #start with worst score
			for i in range(3): #check for each possible move
				temp = grid.clone()
				temp.move(i+1)
				scoreT = max(scoreT,self.expectimax(temp,depth-1,False)) #max of every possible successor
			return scoreT
	
	def getScore(self, grid):
		score = 1
		weightMatrix = [[0,1,2,3],        #use a snake weight matrix that keeps largest tiles in bottom corner
						[7,6,5,4],
						[8,9,12,14],
						[24,18,16,15]]
		penalty = 1
		previousPos = -1
		for i in range (4):    #iterate through grid to get weighted dot product and also evaluate the penalty based on differences between neighbors
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
		heur = score - penalty + len(grid.getAvailableCells()) #combine weighted dot product, smoothness, and available cells as final heuristic
		return heur
		 
				
