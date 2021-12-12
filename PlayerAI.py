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
        
    def manhattanDistance(self, pos, target):
        return abs(pos[0]-target[0]) + abs(pos[1]-target[1])
    
    def chance(self, pos, target):
        return 1 - 0.05 * (self.manhattanDistance(pos, target)-1)
        
    
    def heuristic(self, pos, grid: Grid):
        """One Cell Lookahead Score (OCLS): The difference between 
        the Player's sum of possible moves looking one step ahead and the
        Opponent's sum of possible moves looking one step ahead"""
        opp_pos = grid.find(3 - self.player_num)
        opp_moves = grid.get_neighbors(opp_pos, only_available=True)
        # opp_total = 0
        # for move in opp_moves:
        #     opp_total += len(grid.get_neighbors(opp_pos, only_available=True))
        # p_total = 0
        p_moves = grid.get_neighbors(self.getPosition(), only_available=True)
        # for move in p_moves:
        #     p_total += len(grid.get_neighbors(opp_pos, only_available=True))
        return 2*len(p_moves)-len(opp_moves)
    
    def terminal_test(self, state, grid):
        if len(grid.get_neighbors(state, only_available=True)) > 0: 
            return False
        else:
            return True
    
    def minimize(self, state, grid, depth, alpha, beta):
        op_pos = grid.find(3 - self.player_num)
        if self.terminal_test(state, grid) or depth == 0:
            return None, self.heuristic(state, grid)
        child, utility = None, np.inf
        for child in self.best_moves(grid, self.getPosition()):
            chance = self.chance(op_pos, child)
            c, utility = self.maximize(child, grid, depth -1, alpha, beta)
            utility = chance * utility
            if utility <= alpha:
                break
            beta = min(beta, utility)
        return child, utility
    
    def best_moves(self, grid, state):
        all_moves = grid.get_neighbors(state, only_available = True)
        scores = {}
        for move in all_moves:
            scores[len(grid.get_neighbors(move, only_available=True))] = move
        best_moves = []
        for score in sorted(scores):
            best_moves.append(scores[score])
        return best_moves
            

    def maximize(self, state, grid, depth, alpha, beta):
        if self.terminal_test(state, grid) or depth == 0:
            return None, self.heuristic(state, grid)
        child, utility = None, np.NINF
        for child in self.best_moves(grid, state):
            c, utility = self.minimize(child, grid, depth -1, alpha, beta)
            if utility >= beta:
                break
            alpha = max(alpha, utility)
        return child, utility
            

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
        pos, utility = self.maximize(cur, grid, 5, np.NINF, np.inf)
        return pos
    
    def IS(self, grid : Grid, player_num):
    
        # find all available moves by Player
        player_moves    = grid.get_neighbors(grid.find(player_num), only_available = True)
        
        # find all available moves by Opponent
        opp_moves       = grid.get_neighbors(grid.find(3 - player_num), only_available = True)
        
        return len(player_moves) - len(opp_moves)

        def getTrap(self, grid: Grid) -> tuple:
        # find players
        opponent = grid.find(3 - self.player_num)

        # find all available cells in the grid
        available_neighbors = grid.get_neighbors(opponent, only_available=True)

        # edge case - if there are no available cell around opponent, then
        # player constitutes last trap and will win. throwing randomly.
        start_time = time.time()
        depth = 6

        move, trap, child, utility = self.maximizeTrap(start_time, depth, grid, -sys.maxsize - 1,
                                                       sys.maxsize)

        end_time = time.time()
        print(end_time - start_time, " seconds")
        return trap

    def minimizeTrap(self, start, depth, grid: Grid, alpha, beta):
        current_depth = depth - 1
        opponent = grid.find(3 - self.player_num)
        player = grid.find(self.player_num)
        available_moves = self.bestMovesTrap(grid.get_neighbors(opponent, only_available=True), grid)
        available_player_moves = grid.get_neighbors(player, only_available=True)
        min_child = None
        min_move = None
        min_trap = None
        min_utility = sys.maxsize

        if len(available_moves) == 0:
            utility = len(available_player_moves) - len(available_moves)
            return None, None, grid, utility
        if len(available_player_moves) == 0:
            utility = len(available_player_moves) - len(available_moves)
            return None, None, grid, utility
        now = time.time()
        if (now - start) >= 2.4:
            utility = len(available_player_moves) - len(available_moves)
            return None, None, grid, utility

        if depth == 0:
            utility = len(available_player_moves) - len(available_moves)
            return None, None, grid, utility

        for i in available_moves:
            temp_grid = grid.clone()
            temp_grid = temp_grid.move(i, 3 - self.player_num)
            available_traps = self.bestMovesTrap(temp_grid.get_neighbors(player, only_available=True), temp_grid)
            available_traps.reverse()
            if len(available_traps) == 0:
                available_traps = temp_grid.getAvailableCells()
            for j in available_traps:
                if i != j:
                    temp_grid = temp_grid.trap(j)

                    move, trap, child, utility = self.maximizeTrap(start, current_depth, temp_grid, alpha, beta)

                    if utility < min_utility:
                        min_utility = utility
                        min_child = child
                        min_move = i
                        min_trap = j

                    if min_utility <= alpha:
                        break

                    if min_utility < beta:
                        beta = min_utility

        return min_move, min_trap, min_child, min_utility

    def maximizeTrap(self, start, depth, grid: Grid, alpha, beta):
        current_depth = depth - 1
        opponent = grid.find(3 - self.player_num)
        player = grid.find(self.player_num)
        available_moves = self.bestMovesTrap(grid.get_neighbors(player, only_available=True), grid)
        # available_moves = grid.get_neighbors(player, only_available=True)
        available_opponent_moves = grid.get_neighbors(opponent, only_available=True)
        max_child = None
        max_move = None
        max_trap = None
        max_utility = -sys.maxsize - 1

        if len(available_moves) == 0:
            utility = len(available_moves) - len(available_opponent_moves)
            return None, None, grid, utility
        if len(available_opponent_moves) == 0:
            utility = len(available_moves) - len(available_opponent_moves)
            return None, None, grid, utility
        now = time.time()
        if (now - start) >= 2.4:
            utility = len(available_moves) - len(available_opponent_moves)
            return None, None, grid, utility
        if depth == 0:
            utility = len(available_moves) - len(available_opponent_moves)
            return None, None, grid, utility

        if depth == 5:
            temp_grid = grid.clone()
            available_traps = self.bestMovesTrap(temp_grid.get_neighbors(opponent, only_available=True), temp_grid)
            available_traps.reverse()
            if len(available_traps) == 0:
                available_traps = temp_grid.getAvailableCells()
            for j in available_traps:
                if self.getPosition() != j:
                    temp_grid = temp_grid.trap(j)

                    move, trap, child, utility = self.minimizeTrap(start, current_depth, temp_grid, alpha, beta)

                    if utility > max_utility:
                        max_utility = utility
                        max_child = child
                        max_move = self.getPosition()
                        max_trap = j

                    if max_utility >= beta:
                        break

                    if max_utility > alpha:
                        alpha = max_utility

            return max_move, max_trap, max_child, max_utility
        else:
            for i in available_moves:
                temp_grid = grid.clone()
                temp_grid = temp_grid.move(i, self.player_num)
                available_traps = self.bestMovesTrap(temp_grid.get_neighbors(opponent, only_available=True), temp_grid)
                available_traps.reverse()
                if len(available_traps) == 0:
                    available_traps = temp_grid.getAvailableCells()
                for j in available_traps:
                    if i != j:
                        temp_grid = temp_grid.trap(j)

                        move, trap, child, utility = self.minimizeTrap(start, current_depth, temp_grid, alpha, beta)

                        if utility > max_utility:
                            max_utility = utility
                            max_child = child
                            max_move = i
                            max_trap = j

                        if max_utility >= beta:
                            break

                        if max_utility > alpha:
                            alpha = max_utility

            return max_move, max_trap, max_child, max_utility

    def bestMovesTrap(self, available, grid):
        best = []
        best_score = []
        for i in available:
            score = len(grid.get_neighbors(i, only_available=True))
            if len(best) == 0:
                best.append(i)
                best_score.append(score)
            else:
                for j in range(len(best)):
                    if score > best_score[j]:
                        best.insert(j, i)
                        best_score.insert(j, score)

        return best
        
        

    