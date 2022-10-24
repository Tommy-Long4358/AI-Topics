import random as rand
from random import choice, random

'''
MCMC algorithm:
    - Generate each sample by making a random change to the preceding sample
        - aka generate the next state by making random changes to the current state
'''
def MCMCsample(state):
    # Generate random number between 0 and 1 and round to 4 places
    randNum =  round(rand.random(), 4)

    #print("The random number:", randNum)

    # sum of the chances of switching to a state
    stateSum = 0

    # State to return if the rand is less than or equal to a probability
    stateCount = 1
    for num in (transitionList[state - 1]):
        #print(num)
        # Skip state if its 0.0000 and increment stateCount as there is 0% chance of transistioning to it
        if num == 0.0000:
            stateCount += 1
            continue

        stateSum += num
        
        if randNum <= stateSum:
            #print("State Sum: ", stateSum)
            break
        
        stateCount += 1
    
    return stateCount

# 4 x 4 matrix of the transition probability table
transitionList = [[0.9322, 0.0068, 0.0610, 0.0000],
                  [0.4932, 0.1620, 0.0000, 0.3448],
                  [0.4390, 0.0000, 0.4701, 0.0909],
                  [0.0000, 0.1552, 0.4091, 0.4357]]

'''
for testing 
num = 2

print("Initial State:", num)

num = MCMCsample(num)

print("The state chosen:", num)
'''

# Generate a random initial state
state = rand.randint(1, 4)

# List to keep track of each state picked
stateCounts = [0, 0, 0, 0]
for i in range(1000000):
    # Do MCMC sampling
    state = MCMCsample(state)
    
    # Increment state count that is chosen
    stateCounts[state - 1] += 1

trueCount = "{:.4f}".format((stateCounts[0] + stateCounts[1]) / 1000000)
falseCount = "{:.4f}".format((stateCounts[2] + stateCounts[3]) / 1000000)


# Hard coding is fine
# print the answers to part A and B
print("Part A. The sampling probabilities")
print("P(C|-s,r) = <0.8784, 0.1220>")
print("P(C|-s,-r) = <0.3105, 0.6900>")
print("P(R|c,-s,w) = <0.9863, 0.0137>")
print("P(R|-c,-s,w) = <0.8182, 0.1818>")
print("")

print()

print("Part B. The transition probability matrix")
print("       S1      S2      S3      S4")
print("S1  0.9322   0.0068   0.0610   0.0000")
print("S2  0.4932   0.1620   0.0000   0.3448")
print("S3  0.4390   0.0000   0.4701   0.0909")
print("S4  0.0000   0.1552   0.4091   0.4357")

print()

print("Part C. The probability for the query")
print(f'P(C|-s, w) = <{trueCount}, {falseCount}>')
# answer should be around <0.85, 0.14>
