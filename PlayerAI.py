import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid

# TO BE IMPLEMENTED
# 
class PlayerAI(BaseAI):

    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num
    
    def heuristic(self, pos, grid: Grid):
        """One Cell Lookahead Score (OCLS): The difference between 
        the Player's sum of possible moves looking one step ahead and the
        Opponent's sum of possible moves looking one step ahead"""
        opp_pos = grid.find(3 - self.player_num)
        opp_moves = grid.get_neighbors(opp_pos, only_available=True)
        opp_total = 0
        for move in opp_moves:
            opp_total += len(grid.get_neighbors(opp_pos, only_available=True))
        p_total = 0
        p_moves = grid.get_neighbors(self.getPosition(), only_available=True)
        for move in p_moves:
            p_total += len(grid.get_neighbors(opp_pos, only_available=True))
        return p_total-opp_total
    
    def terminal_test(self, state, grid):
        if len(grid.get_neighbors(state, only_available=True)) > 0: 
            return False
        else:
            return True
    
    def minimize(self, state, grid, depth):
        if self.terminal_test(state, grid) or depth == 0:
            return None, self.heuristic(state, grid)
        minChild, minUtility = None, np.inf
        for child in grid.get_neighbors(self.getPosition(), only_available = True):
            c, utility = self.maximize(child, grid, depth -1)
            if utility  < minUtility:
                minChild, minUtility = child, utility
        return minChild, minUtility
    
    def maximize(self, state, grid, depth):
        if self.terminal_test(state, grid) or depth == 0:
            return None, self.heuristic(state, grid)
        maxChild, maxUtility = None, np.NINF
        for child in grid.get_neighbors(state, only_available = True):
            c, utility = self.minimize(child, grid, depth -1 )
            if utility > maxUtility:
                maxChild, maxUtility = child, utility
        return maxChild, maxUtility
            
        

    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        cur = self.getPosition()
        pos, utility = self.maximize(cur, grid, 5)
        return pos

    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        options = grid.get_neighbors(grid.find(3 - self.player_num), only_available=True)
        r = random.randint(0, len(options)-1)
        return options[r]
        
        

    