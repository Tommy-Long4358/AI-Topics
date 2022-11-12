import sys

'''
Filtering is computing the belief state (posterior distribution over the most 
recent state) given all evidence to date.
aka use past data to calculate current data
'''
import sys

def alphaCompute(vectAnswer):
    return 1 / (vectAnswer[0] + vectAnswer[1])

def hmmFiltering(count):
    ans = []

    # Base case
    if count == 0:
        return x0

    # Accounts for different boolean evidence variables
    if eStates[count - 1] == True:
        ans = [probTable2[True], probTable2[False]]

    else:
        ans = [1 - probTable2[True], 1 - probTable2[False]]
    
    # Sigma Computation with recursion
    sigmaAns = [probTable1[True] *  hmmFiltering(count - 1)[0] + probTable1[False] * hmmFiltering(count - 1)[1], 
         (1 - probTable1[True]) *  hmmFiltering(count - 1)[0] + (1 - probTable1[False]) * hmmFiltering(count - 1)[1]]
    
    # <p(et|xt), p(et|-xt)> * sigma answer
    ans = [ans[0] * sigmaAns[0], ans[1] * sigmaAns[1]]

    # Solve for alpha
    ans = [ans[0] * alphaCompute(ans), ans[1] * alphaCompute(ans)]

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

    # x0 = <a, 1 - a>
    x0 = [float(independVariList[0]), 1 - float(independVariList[0])]

    # e1:t = <e0,e1,...,et>
    eStates = [True if boolean == "t" else False for boolean in independVariList[5:]]

    # p(xt | Xt-1) table: 
    probTable1 = {True: float(independVariList[1]), False: float(independVariList[2])}

    # p(et | xt) table
    probTable2 = {True: float(independVariList[3]), False: float(independVariList[4])}

    # Do HMM filtering calculaction
    ans = hmmFiltering(len(eStates))

    # Display
    print(f'{line}--><{"{:.4f}".format(ans[0])}, {"{:.4f}".format(ans[1])}>')
    
# Answer check
# 0.5,0.7,0.3,0.9,0.2,t,t--><0.8834,0.1166>
# 0.5,0.7,0.3,0.9,0.2,t,t,f--><0.1907,0.8093>
