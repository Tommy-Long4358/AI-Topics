import board as bd
import numpy as np
import time

def hill_climbing(board, queens):
    # Get a map of the board in list form
    map = board.get_map()

    while True:
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

        '''
        print("Final Board:")
        board.show_map()
        print("Current fitness:", board.get_fitness())
        print()
        '''

        if board.get_fitness() == 0:
            break

        board = bd.Board(queens)

        '''
        print("New Randomly Generated Board")
        board.show_map()
        print("New Random Generated fitness:", board.get_fitness())
        print()
        '''

    return board
    
def find_col(map, row):
    for col in range(len(map)):
        if map[row][col] == 1:
            return col

if __name__ == '__main__':
    start = time.time()
    queens = 5
    board = bd.Board(queens)
    milliseconds = 1000

    '''
    print("Initial Board:")
    board.show_map()
    print("Current Fitness:", board.get_fitness())
    print()
    '''
    
    board = hill_climbing(board, queens)

    print("Running time", "{0:.2f}".format( (time.time() - start) * milliseconds), "ms")
    board.show_map()

    #print("Hits:", board.get_fitness())
