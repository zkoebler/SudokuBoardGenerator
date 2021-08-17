########################################################
#   Current Bugs:
#       -backtracking hits recursion depth 40-60% of the time
#   Things to implement:
#       -backtracking algo to complete boards
#       -GUI
#       -Solving functionality
#
#
########################################################

import random
import sys
class SudokuCreator:
    def initializeTemplateBoard():      #initializes the board
        numList = [[0 for x in range(0,9)] for x in range(0,9)] 
        numList[0] = [x for x in range(1,10)]
        random.shuffle(numList[0])
        return numList
    m_Board = initializeTemplateBoard()
    
    def __init__(self):
        pass

def initializeTemplateBoard():      #initializes the board
    numList = [[0 for x in range(0,9)] for x in range(0,9)] 
    numList[0] = [x for x in range(1,10)]
    random.shuffle(numList[0])
    return numList
m_Board = initializeTemplateBoard()


def __getColSet(colIDX):  #returns possible numbers for the column 
    return set([1,2,3,4,5,6,7,8,9])-set([m_Board[i][colIDX] for i in range(0,9) if m_Board[i][colIDX] != 0])
def __getRowSet(rowIDX):  #returns possible numbers for the row
    s = set(m_Board[rowIDX])
    s.discard(0)
    return set([1,2,3,4,5,6,7,8,9])-s
def __getBlock(startRow, endRow, startCol, endCol):   #returns the block of numbers in the specified range
    s = set([])
    for i in range(startRow,endRow+1):
        for j in range(startCol,endCol+1):
            s.add(m_Board[i][j])
    return set([1,2,3,4,5,6,7,8,9])-s
def __getBlockSet(row,col):   #returns the set of possible values in the current block
    if (0 <= row <= 2 and 0 <= col <= 2):
        return __getBlock(0,2,0,2)
    if (3 <= row <= 5 and 0 <= col <= 2):
        return __getBlock(3,5,0,2)
    if (6 <= row <= 8 and 0 <= col <= 2):
        return __getBlock(6,8,0,2)

    if (0 <= row <= 2 and 3 <= col <= 5):
        return __getBlock(0,2,3,5)
    if (3 <= row <= 5 and 3 <= col <= 5):
        return __getBlock(3,5,3,5)
    if (6 <= row <= 8 and 3 <= col <= 5):
        return __getBlock(6,8,3,5)

    if (0 <= row <= 2 and 6 <= col <= 8):
        return __getBlock(0,2,6,8)
    if (3 <= row <= 5 and 6 <= col <= 8):
        return __getBlock(3,5,6,8)
    if (6 <= row <= 8 and 6 <= col <= 8):
        return __getBlock(6,8,6,8)
def __getPossNumsSet(row,col):    #returns the possible number values that can be entered into the matrix
    B = __getBlockSet(row,col)
    R = __getRowSet(row)
    C = __getColSet(col)
    return B.intersection(R,C)



def __place(row,col,val): #__places a number in a specified location
    m_Board[row][col] = val

def __getPlacementVal(row,col):   #returns a random value to be __placed into the board
    s = __getPossNumsSet(row,col)
    if(s == set()):
        return 0
    else:
        #return random.choice(tuple(s))
        return s

setOfDecsions = {}
def __resolve(row,col,target):
    #Base Case
    if (row,col) == target:
        if(m_Board[row][col] != 0):
            return
    #recursive step
    #####################-------Backwards Iteration---------#####################
    if setOfDecsions[(row,col)] == set():  #if there are no values that can be __placed 
                                            #iterate backwards and set the target equal 
                                            # to the current position
        m_Board[row][col] = 0
        __iterateresolve("Backward",row,col,target)
    #####################-------Fowards Iteration-----------#####################
    if len(setOfDecsions[(row,col)]) > 0:
        m_Board[row][col] = random.choice(tuple(setOfDecsions[(row,col)]))
        setOfDecsions[(row,col)].remove(m_Board[row][col])
        if (row,col) == target:
            if(m_Board[row][col] != 0):
                return
        __iterateresolve("Foward",row,col,target)

        

def __iterateresolve(command,row,col,target):
    if command == "Foward":
        if col == 8:
            val = __getPlacementVal(row+1,0)
            if(val == 0):
                setOfDecsions[(row+1,0)] = set()
            else:
                setOfDecsions[(row+1,0)] = val
            __resolve(row+1,0,target)
        elif col < 8:
            val = __getPlacementVal(row,col+1)
            if(val == 0):
                setOfDecsions[(row,col+1)] = set()
            else:
                setOfDecsions[(row,col+1)] = val
            __resolve(row,col+1,target)
    elif command == "Backward":
        if col == 0:
            __resolve(row-1,8,target)
        elif col > 0:
            __resolve(row,col-1,target)


    

def __placeVals(): #__places all values on the board.
    for row in range(1,9):
        for col in range(9):
            possibleValues = __getPlacementVal(row,col)
            if possibleValues == 0:
                setOfDecsions[(row,col)] = set()

                __resolve(row,col,(row,col))
                val = __getPlacementVal(row,col)
                if val == 0:
                    setOfDecsions[(row,col)] = set()
                else:
                    setOfDecsions[(row,col)] = val
            else:
                #add the value to the board and all of the other possible values to the set of decisions
                val = random.choice(tuple(possibleValues))
                setOfDecsions[(row,col)] = possibleValues - set([val])
                m_Board[row][col] = val
    
        
def __printBoard(board):  #prints the board
    for i in range(0,len(board)):
        print(board[i])

sys.setrecursionlimit(100)
def __makeBoard():
    #global m_Board
    while True:
        try:
            __placeVals()
            __printBoard(m_Board)
            return
        except:
            for i in range(1,9):
                for j in range(0,9):
                    m_Board[i][j] = 0

__makeBoard()


