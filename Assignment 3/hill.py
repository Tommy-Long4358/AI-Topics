import board as bd
import numpy as np
import sys
import time

def hill_climbing(board, queens):
    # Get a map of the board in list form
    map = board.get_map()

    for i in range(queens):
        # Find the column that contains a "1"
        col = find_col(map, i)

        # Find number of initial hits
        leastHits = board.get_fitness()

        # Find row and col position of "1" with least hits
        [minRow, minCol] = [i, col]
        
        # Flip 1 to 0 
        board.flip(i, col)
        
        for j in range(queens):
            # Loop through all 0s, exclude the original position
            if map[i][j] == 0 and j != col:

                # Flip current position to 1
                board.flip(i, j)

                # Get number of hits at current position
                hits = board.get_fitness()

                # Compare hits with least number of hits for that row
                if hits < leastHits:
                    leastHits = hits

                    # Assign new row and column position for new minimum hits
                    [minRow, minCol] = [i, j]
                
                # Flip current position back to 0
                board.flip(i, j)
        
        # Once the row is fully searched, we flip the row and column position
        # that contained the least number of hits to a 1
        leastHits = None
        board.flip(minRow, minCol)

    return map
    
def find_col(map, row):
    for col in range(len(map)):
        if map[row][col] == 1:
            return col

if __name__ == '__main__':
    start = time.time()
    restart = 0
    queens = 5
    board = bd.Board(queens)
    
    board.show_map()
    print("Hits: ", board.get_fitness())
    print()
    print("-----------------------------")
    print()

    while board.get_fitness() != 0:
        hill_climbing(board, queens)
        restart += 1
        board = bd.Board(queens)
        
    
    # hill_climbing(board, queens)

    milliseconds = 1000
    print("Running time", "{0:.2f}".format( (time.time() - start) * milliseconds), "ms")
    board.show_map()
    print("Hits:", board.get_fitness())
    print("Restarts:", restart)
    
