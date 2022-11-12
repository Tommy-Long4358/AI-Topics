import sys

'''
HMM Filtering is computing the belief state (posterior distribution over the most 
recent state) given all evidence to date.
aka use past data to calculate current data
'''
def alphaCompute(vect):
    return 1 / (vect[0] + vect[1])

# Ext ~p(Xt+1|xt) * p(xt|e1:t)
def sigmaCompute(probTable, sigmaPast):
    return [probTable[True] *  sigmaPast[0] + probTable[False] * sigmaPast[1], 
            (1 - probTable[True]) *  sigmaPast[0] + (1 - probTable[False]) * sigmaPast[1]]

def hmmFiltering():
    ans = []

    # Start off initially at x0
    sigmaPast = X0

    # Loop through all states to compute ->p(Xt+1|e1:t+1)
    for booleanState in eStates:
        # Accounts for different boolean evidence variables
        if booleanState:
            # Sensor: <p(et+1|xt+1), p(et+1|-xt+1)>
            ans = [probTable2[True], probTable2[False]]
        else:
            # Sensor: <1 - p(et+1|xt+1), 1 - p(et+1|-xt+1)>
            ans = [1 - probTable2[True], 1 - probTable2[False]]
        
        # (Transition * recursion) computation with sigmaPast keeping past state calculations
        sigmaAns = sigmaCompute(probTable1, sigmaPast)
        
        # <p(et+1|xt+1), p(et+1|-xt+1)> * sigmaAns
        ans = [ans[0] * sigmaAns[0], ans[1] * sigmaAns[1]]

        # Solve for alpha
        alpha = alphaCompute(ans)
        ans = [ans[0] * alpha, ans[1] * alpha]

        # Update sigmaPast with new calculation
        sigmaPast = ans
    
    return ans

# Get input from python terminal
# command: python hmm.py cpt.txt
fileInput = sys.argv[1]

# Read from file
cptFile = open(fileInput, 'r')

'''
FOR TESTING
cptFile = open("cpt.txt", "r")
'''

# Loop through each line in the file
for line in cptFile:
    # Remove spaces from line
    line = line.strip()
    
    # Split each element in the line at the ","
    independVariList = line.split(",")

    # ->P(X0) = <a, 1 - a>
    X0 = [float(independVariList[0]), 1 - float(independVariList[0])]

    # e1:t = <e1,e2,...,et>
    eStates = [True if boolean == "t" else False for boolean in independVariList[5:]]

    # p(xt | Xt-1) table:
    # Xt-1  P(xt)
    #  T     b
    #  F     c
    probTable1 = {True: float(independVariList[1]), False: float(independVariList[2])}

    # p(et | Xt) table:
    # Xt  P(et)
    # T     d
    # F     f
    probTable2 = {True: float(independVariList[3]), False: float(independVariList[4])}

    # Do HMM filtering calculation
    ans = hmmFiltering()

    # Display
    print(f'{line}--><{"{:.4f}".format(ans[0])},{"{:.4f}".format(ans[1])}>')
    
# Answer check
# 0.5,0.7,0.3,0.9,0.2,t,t--><0.8834,0.1166>
# 0.7,0.8,0.3,0.2,0.7,t,f--><0.7056,0.2943>
# 0.5,0.7,0.3,0.9,0.2,t,t,f--><0.1907,0.8093>
