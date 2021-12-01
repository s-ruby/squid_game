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
        
    def getValidMoves(self, pos, avail):
        moves = []
        start1 = min(max(pos[0]-1, 0), 8)
        end1 = min(max(pos[0]+2, 0), 8) 
        start2 = min(max(pos[1]-1, 0), 8)
        end2 = min(max(pos[1]+2, 0), 8) 
        for i in range(start1, end1):
            for j in range(start2, end2):
                if (i, j) != pos and (i, j) in avail:
                    moves.append((i, j))
        return moves
    
    def heuristic(self, grid: Grid):
        """the difference between the current number of moves Player (You) can make 
        and the current number of moves the opponent can make."""
        avail = grid.getAvailableCells()
        opp_pos = grid.find(3 - self.player_num)
        opp_moves = len(self.getValidMoves(opp_pos, avail))
        p_moves = len(self.getValidMoves(self.getPosition(), avail))
        print(f"improved score: {p_moves-opp_moves}")
        print(f"aggressive is: {p_moves - (2*opp_moves)}")
        
        
                    

    def getMove(self, grid: Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player moves.

        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Trap* actions, 
        taking into account the probabilities of them landing in the positions you believe they'd throw to.

        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        self.heuristic(grid.clone())
        cur = self.getPosition()
        avail = grid.getAvailableCells()
        options = self.getValidMoves(cur, avail)
        r = random.randint(0, len(options)-1)
        return options[r]

    def getTrap(self, grid : Grid) -> tuple:
        """ 
        YOUR CODE GOES HERE

        The function should return a tuple of (x,y) coordinates to which the player *WANTS* to throw the trap.
        
        It should be the result of the ExpectiMinimax algorithm, maximizing over the Opponent's *Move* actions, 
        taking into account the probabilities of it landing in the positions you want. 
        
        Note that you are not required to account for the probabilities of it landing in a different cell.

        You may adjust the input variables as you wish (though it is not necessary). Output has to be (x,y) coordinates.
        
        """
        options = grid.getAvailableCells()
        r = random.randint(0, len(options)-1)
        return options[r]
        
        

    