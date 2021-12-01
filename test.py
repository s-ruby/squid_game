import random

x = [0, 1, 2, 3, 4]

r = random.randint(0, len(x)-1)
print(r)

def getValidMoves(pos):
    moves = []
    start1 = min(max(pos[0]-1, 0), 8)
    end1 = min(max(pos[0]+2, 0), 8) 
    start2 = min(max(pos[1]-1, 0), 8)
    end2 = min(max(pos[1]+2, 0), 8) 
    for i in range(start1, end1):
        for j in range(start2, end2):
            if (i, j) != pos:
                moves.append((i, j))
    return moves

                    