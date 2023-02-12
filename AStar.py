# Astar.py, April 2017 
# Based on ItrDFS.py, Ver 0.3, April 11, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from queue import PriorityQueue

# DO NOT CHANGE THIS SECTION 
if sys.argv==[''] or len(sys.argv)<2:
    if(sys.argv[0] == "EightPuzzleWithHeuristics"):
        import EightPuzzleWithHeuristics as Problem
        heuristics = lambda s: Problem.HEURISTICS[sys.argv[1]](s)
    elif(sys.argv[0] == "TowerOfHanoi"):
        import TowerOfHanoi as Problem
        heuristics = lambda s: Problem.HEURISTICS[sys.argv[1]](s)
else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)

print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}
PRI = []

# DO NOT CHANGE THIS SECTION
def runAStar():
    #initial_state = Problem.CREATE_INITIAL_STATE(keyVal)
    initial_state = Problem.CREATE_INITIAL_STATE()
    print("Initial State:")
    print(str(initial_state) + ", F=10, G=0, H=10") #Change into F=5,G=0,H=10 if TowerOfHanoi_Manning3
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    PRI = []
    path, name = AStar(initial_state)
    print(str(COUNT)+" states examined.")
    return path, name

# A star search algorithm
# TODO: finish A star implementation
def AStar(initial_state):
    global COUNT, BACKLINKS
    # TODO: initialze and put first state into 
    # priority queue with respective priority
    # add any auxiliary data structures as needed
    OPEN = []
    CLOSED = []
    BACKLINKS[initial_state] = -1
    OPEN.append(initial_state)
    PRI.append(0)
    G = {}
    F = {}
    G[initial_state] = 0

    print("\nPattern: new_state", "F()", "G()", "H():")
    while len(OPEN) > 0:
        index = findMin()
        S = OPEN[index]
        del OPEN[index]
        del PRI[index]
        while S in CLOSED:
            index = findMin()
            S = OPEN[index]
            del OPEN[index]
            del PRI[index]
        CLOSED.append(S)
        
        # DO NOT CHANGE THIS SECTION: begining 
        if Problem.GOAL_TEST(S): #Defined in TowerOfHanoi as: If the first two pegs are empty, then s is a goal state. 
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
        # DO NOT CHANGE THIS SECTION: end

        # TODO: finish A* implementation
        COUNT += 1
        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not (new_state in OPEN) and not (new_state in CLOSED):
                    G[new_state] = G[S] + 1
                    H = heuristics(new_state)
                    F[new_state] = G[new_state] + H
                    BACKLINKS[new_state] = S
                    OPEN.append(new_state)
                    PRI.append(F[new_state])
                    print("\n" + str(new_state) + ", F="+ str(F[new_state]) + ", G=" + str(G[new_state]) + ", H=" + str(H))
                    print("OPEN: " + strList(OPEN))
                    print("PRI: " + strList(PRI))
                    print("BACKLINKS: " + strList(BACKLINKS))
                    #print("open:",strList(OPEN),"\npri:",strList(PRI),"\nbacklink:",strList(BACKLINKS))
                elif BACKLINKS[new_state] != -1:
                    other_parent = BACKLINKS[new_state]
                    temp = F[new_state]-G[other_parent]+G[S]
                    if temp < F[new_state]:
                        G[new_state] = G[new_state]-F[new_state]+temp
                        F[new_state] = temp
                        BACKLINKS[new_state] = S
                        if new_state in CLOSED:
                            OPEN.append(new_state)
                            PRI.append(F[new_state])
                            CLOSED.remove(new_state)

def findMin():
    min = PRI[0]
    index = 0
    for i in range(len(PRI)):
        if PRI[i] < min:
            min = PRI[i]
            index = i
    return index

def strList(l:list):
    out = ""
    for i in l:
        out = out + str(i) + "  "
    return out    

def printList(l:list):
    print(strList(l))

# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while not S == -1:
        path.append([S][0])
        S = BACKLINKS[S]
    path.reverse()
    print("\nSolution path: ")
    for s in path:
        print(s)
    print("\nPath length = "+str(len(path)-1))
    return path    

if __name__=='__main__':
    path, name = runAStar()



