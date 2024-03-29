import board as bd
import numpy as np
import math
import random as rand
import time

def genetic(queens):
    bestGene = None
    while not bestGene:
        states = []
        fitness = []

        # State creation and nonfitness calculator
        for i in range(len(queens)):
            states.append(construct_state(queens[i].get_map()))
            fitness.append(nonFitness(queens[i]))

        # Selection
        randomStates = selection(fitness, states)
        
        # Cross-Over
        for i in range(0, len(randomStates), 2):
            # Mix and match pairs on index pivot
            indexPivot = rand.randint(0, len(queens[0].map) - 1) + 1

            [randomStates[i], randomStates[i + 1]] = cross_over(randomStates[i], randomStates[i + 1], indexPivot)
            
        # Mutate state and match the queen[i] board to the new state
        for i in range(len(queens)):
            mutationChance = rand.randint(1, 10)
            
            if mutationChance == 3:
                randomStates[i] = mutation(randomStates[i])
                
            queens[i] = construct_map(queens[i], randomStates[i])

            if queens[i].get_fitness() == 0:
                bestGene = queens[i]

    return bestGene 

def construct_state(map):
    # State is made up of the column positions of all the 1's on the board
    state = ""
    for row in range(len(map)):
        for col in range(len(map)):
            if map[row][col] == 1:
                # Column positions start at 1 rather than 0
                state += str(col + 1)
        
    return state

def construct_map(queen, state):
    for i in range(len(queen.get_map())):
        # Find position of current 1 in the map
        col = find_col(queen.get_map(), i)

        # Ignore any state that is still in the original position
        if int(state[i]) - 1 == col:
            continue

        # Flip new position to 1 and old position to 0
        queen.flip(i, col)
        queen.flip(i, int(state[i]) - 1)

    return queen

# Find the column index of where 1 is on the board on a given row
def find_col(map, row):
    for col in range(len(map)):
        if map[row][col] == 1:
            return col

def nonFitness(queen):
    # Find non attacking
    # Non attacking = total possible attacking - attacking
    totalPossibleAttacks = math.comb(5, 2)
    hits = queen.get_fitness()

    nonAttacking = totalPossibleAttacks - hits
    return nonAttacking

def selection(fitness, states):
    randomStates = []
    percentSelections = []

    # Calculate percentage of each state being chosen (fitness[i] / total fitness)
    for i in range(len(fitness)):
        percentRate = round(fitness[i] / sum(fitness), 2)
        percentSelections.append(percentRate)

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
    randNum = rand.randint(1, len(state))
    
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

    bestGene = genetic(queens)

    print("Running time", "{0:.2f}".format( (time.time() - start) * milliseconds), "ms")
    bestGene.show_map()
