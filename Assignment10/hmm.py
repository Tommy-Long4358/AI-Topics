import sys

'''
Filtering is computing the belief state (posterior distribution over the most 
recent state) given all evidence to date.
aka use past data to calculate current data
'''
import sys

def alphaCompute(vectAnswer):
    return 1 / (vectAnswer[0] + vectAnswer[1])

def hmmFiltering():
    ans = []

    # Start off initially at x0
    sigmaPast = X0

    # Loop through all states
    for count in range(len(eStates)):
        # Accounts for different boolean evidence variables
        if eStates[count] == True:
            ans = [probTable2[True], probTable2[False]]

        else:
            ans = [1 - probTable2[True], 1 - probTable2[False]]
        
        # Sigma Computation with sigmaPast keeping past state calculations
        sigmaAns = [probTable1[True] *  sigmaPast[0] + probTable1[False] * sigmaPast[1], 
            (1 - probTable1[True]) *  sigmaPast[0] + (1 - probTable1[False]) * sigmaPast[1]]
        
        # <p(et|xt), p(et|-xt)> * sigma answer
        ans = [ans[0] * sigmaAns[0], ans[1] * sigmaAns[1]]

        # Solve for alpha
        ans = [ans[0] * alphaCompute(ans), ans[1] * alphaCompute(ans)]

        # Update sigmaPast with new calculation
        sigmaPast = ans
    
    return ans

# Get input from python terminal
# python hmm.py cpt.txt
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

    # P(X0) = <a, 1 - a>
    X0 = [float(independVariList[0]), 1 - float(independVariList[0])]

    # e1:t = <e0,e1,...,et>
    eStates = [True if boolean == "t" else False for boolean in independVariList[5:]]

    # p(xt | Xt-1) table:
    # Xt-1  P(xt)
    #  T     b
    #  F     c
    probTable1 = {True: float(independVariList[1]), False: float(independVariList[2])}

    # p(et | Xt) table
    #  Xt  P(et)
    #  T     d
    #  F     f
    probTable2 = {True: float(independVariList[3]), False: float(independVariList[4])}

    # Do HMM filtering calculaction
    ans = hmmFiltering()

    # Display
    print(f'{line}--><{"{:.4f}".format(ans[0])}, {"{:.4f}".format(ans[1])}>')
    
# Answer check
# 0.5,0.7,0.3,0.9,0.2,t,t--><0.8834,0.1166>
# 0.5,0.7,0.3,0.9,0.2,t,t,f--><0.1907,0.8093>
