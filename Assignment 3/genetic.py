import board as bd
import numpy as np
import math
import random as rand
import time

def genetic(queens):
    states = []
    fitness = []

    # State creation and nonfitness calculator
    for i in range(len(queens)):
        states.append(construct_state(queens[i].get_map()))
        fitness.append(nonFitness(queens[i]))

    # Selection
    randomStates = selection(fitness, states)

    #print("Chosen States:", randomStates)
    
    # Cross-Over
    # Mix and match pairs on index pivot
    for i in range(0, len(randomStates), 2):
        # ????
        indexPivot = rand.randint(0, len(queens[0].map) - 1) + 1

        [randomStates[i], randomStates[i + 1]] = cross_over(randomStates[i], randomStates[i + 1], indexPivot)
    
    #print("Cross-Over:", randomStates)

    # Mutate state and copy it to board of queen[i]
    for i in range(len(queens)):
        randomStates[i] = mutation(randomStates[i])
        queens[i] = construct_map(queens[i], randomStates[i])

    return queens 

def construct_state(map):
    # State is made up of the column positions of all the 1's on the board
    state = ""
    for row in range(len(map)):
        for col in range(len(map)):
            if map[row][col] == 1:
                state += str(col + 1)
        
    return state

def construct_map(queen, state):
    for i in range(len(queen.get_map())):
        # Find position of current 1 in the map
        col = find_col(queen.get_map(), i)

        # Flip new position to 1 and old position to 0
        queen.flip(i, col)
        queen.flip(i, int(state[i]) - 1)

    return queen

def find_col(map, row):
    for col in range(len(map)):
        if map[row][col] == 1:
            return col

def nonFitness(queen):
    # Find non attacking
    # Non attacking = total possible attacking - attacking
    totalPossibleAttacks = math.comb(5, 2)
    hits = queen.get_fitness()

    #queens[i].show_map()
    #print("Hits: ", queens[i].get_fitness())

    nonAttack = totalPossibleAttacks - hits

    '''
    print(totalPossibleAttacks, " - ", hits, " = ", nonAttack)
    print()
    print("--------------------------")
    print()
    '''

    return nonAttack

def selection(fitness, states):
    randomStates = []
    percentSelections = []

    # Calculate percentage of each state being chosen (fitness[i] / total fitness)
    for i in range(len(fitness)):
        selectPercent = round(fitness[i] / sum(fitness), 2)

        #print(fitness[i], " / ", sum(fitness), " = ", selectPercent)

        percentSelections.append(selectPercent)

    # Randomly pick 8 states
    for i in range(len(states)):
        r = round(rand.random(), 2)

        if r < percentSelections[0]:
            #print("Picked state 1")
            randomStates.append(states[0])

        elif r < sum(percentSelections[:2]):
            #print("Picked state 2")
            randomStates.append(states[1])
        
        elif r < sum(percentSelections[:3]):
            #print("Picked state 3")
            randomStates.append(states[2])

        elif r < sum(percentSelections[:4]):
            #print("Picked state 4")
            randomStates.append(states[3])
        
        elif r < sum(percentSelections[:5]):
            #print("Picked state 5")
            randomStates.append(states[4])
        
        elif r < sum(percentSelections[:6]):
            #print("Picked state 6")
            randomStates.append(states[5])
        
        elif r < sum(percentSelections[:7]):
            #print("Picked state 7")
            randomStates.append(states[6])
        
        else:
            #print("Picked state 8")
            randomStates.append(states[7])
        
    return randomStates

def cross_over(state1, state2, indexPivot):
    # Slice everything before and not including the pivot and slice 
    # everything after and including the pivot to make a new mixed state
    combinationState1 = state1[:indexPivot] + state2[indexPivot:]
    combinationState2 = state2[:indexPivot] + state1[indexPivot:]

    return [combinationState1, combinationState2]

def mutation(state):
    # Generate a random index and number
    randIndex = rand.randint(0, len(state) - 1)
    randNum = rand.randint(1, len(state) - 1)
    
    # Replace index in state with number
    state = state[:randIndex] + str(randNum) + state[randIndex + 1:] 

    return state

if __name__ == '__main__':
    # 8 states
    start = time.time()
    milliseconds = 1000
    queen = 5

    queens = [bd.Board(queen), bd.Board(queen), bd.Board(queen), bd.Board(queen), bd.Board(queen),
                bd.Board(queen), bd.Board(queen), bd.Board(queen)]

    bestGene = None
    print("test")
    while bestGene is None:
        for i in range(len(queens)):
            if queens[i].get_fitness() == 0:
                bestGene = queens[i]
                break

        queens = genetic(queens)

    print("Running time", "{0:.2f}".format( (time.time() - start) * milliseconds), "ms")
    bestGene.show_map()
