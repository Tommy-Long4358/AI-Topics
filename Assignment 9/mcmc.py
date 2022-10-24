import random as rand
from random import choice

'''
MCMC algorithm:
    - Generate each sample by making a random change to the preceding sample
        - aka generate the next state by making random changes to the current state
'''

def MCMCsample():
    pass

transitionList = [[0.9322, 0.0068, 0.0610, 0.0000],
                  [0.4932, 0.1620, 0.0000, 0.3448],
                  [0.4390, 0.0000, 0.4701, 0.0909],
                  [0.0000, 0.1552, 0.4091, 0.4357]]

# Generate a random initial state
state = rand.randint(1, 4)

for i in range(1000000):
    # Do MCMC sampling
    pass

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
print("P(C|-s, w) = ", "<..., ...>")