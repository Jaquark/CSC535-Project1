#!/usr/bin/python
import argparse
import copy
from queue import PriorityQueue
import random

#Define the possible moves for 0 at any given location in the 3x3 grid
#The start location of 0 is defined as [x,y] that correspondes to the positions in the array
#a move can only fall within (x2 = x1+1 || x2= x1-1 || x2 = x1) && (y2 = y1+1 || y2=y1-1 || y2=y1)
#While x2 is between 0 and 2, inclusive; AND y2 is betwee 0 and 2, inclusive
#Given that we can only move up, down, left and right, the range of all valid moves can be described as:

vmDelta = {
            'L' : [0,-1],
            'R' : [0,1],
            'U' : [-1,0],
            'D' : [1,0]
}

#As we would in a video game, as a matter of preventing the need to process the location of valid move
#Let us predefine the valid moves in each location within the 3x3 gride

#This also looks like the 'branch factor' defined around 30:40 of Lecture 4.
validMovesPerGridLocation = {
    '0,0' : ['R','D'],          #TopLeft
    '0,1' : ['L','R','D'],      #TopMiddle
    '0,2' : ['L','D'],          #TopRight
    '1,0' : ['R','U','D'],      #MiddleLeft
    '1,1' : ['L','R','U','D'],  #Middle
    '1,2' : ['L','U','D'],      #MiddleRight
    '2,0' : ['R','U'],          #BottomLeft
    '2,1' : ['L','R','U'],      #BottomMiddle
    '2,2' : ['L','U']           #BottomRight
}

#Let's also define the goal state, so we can easily compare it to a given state
#So we can calculate the distance between any given misplaced tile and where it should be:
goalState = {
    '1' : [0,1],
    '2' : [0,2],
    '3' : [1,0],
    '4' : [1,1],
    '5' : [1,2],
    '6' : [2,0],
    '7' : [2,1],
    '8' : [2,2]
}


#And what's really cool about this is we can use goalState to help calculate the distance at any given time:

def calculateManhattanPoints ( board ): 
    points = 0
    for x in range(0,len(board)) :
        for y in range(0,len(board[x])) :
            #0 doesn't need to be calculated
            if board[x][y] == '0':
                continue
            current = [x,y]
            goal = goalState[str(board[x][y])]
            if current != goal :
                #Calculate points here
                #Which we can do by finding the |delta x| + |delta y| of
                #current --> goal
                points += abs(int(current[0]) - goal[0]) + abs(int(current[1]) - goal[1])
    return points       

#Iterate through the matrix and print out the location each number
#TODO: Print 0 as ' '
def getBoardStateAsString( board ):
    output = ''
    for row in board:
        output += "{0} {1} {2}\n".format(row[0],row[1],row[2])
    return output

#Convert the file input from our format of n,n,n|n,n,n|n,n,n
#to a 3x3 matrix
def parseInput( delimitedInputString ):
    newBoard = []
    for row in delimitedInputString.split('|'):
        row_value = []
        for value in row.split(','):
            row_value.append(value)
        newBoard.append(row_value)
    return newBoard

#Ensure that no values is used more than once, and all values are numbers and call between 0 and 8
def validateInput( board ):
    validValues = {0: False, 1: False, 2: False,
                   3: False, 4: False, 5: False,
                   6: False, 7: False, 8: False}

    if len(board) != 3:
        return False

    for row in board:
        if len(row) != 3:
            return False
        for val in row:
            if not val.isnumeric():
                return False
            if int(val) != float(val):
                return False
            val = int(val)
            if val < 0 or val > 8:
                return False
            isKeyInDict = val in validValues
            if isKeyInDict:
                if validValues[val]:
                    return False
                else:
                    validValues[val] = True
            else:
                return False
    return True
    

#g is the cost to reach all previous nodes
#h is the cost to reach this node
class AStarNode:
    def __init__(self, nodeState, g, h, previousNode ):
        self.nodeState = nodeState
        self.g = g
        self.h = h
        self.parent = previousNode
        #print('previous Parent: {0}'.format(previousNode))
        self.childNodes = []

    #This is the equivalent of 'Expanding' on page 94
    def createChildren(self):
        #find the current location of 0
        #iterate through the matrix

        for x in range(0,len(self.nodeState)) :
            for y in range(0,len(self.nodeState[x])) :
                if self.nodeState[x][y] == '0':
                    self.locationOfZero = [x,y]    

        #get list of valid moves:
        self.validMoves = validMovesPerGridLocation[str(self.locationOfZero[0])+','+str(self.locationOfZero[1])]

        #with the valid move sets let us generate the child nodes:
        for vm in self.validMoves:
            #this is where get the values to apply to the 0 to find the new boardState
            valuesToDeltaZero = vmDelta[vm]
            #and then we find where 0 is going:
            locationOfDestinationTile = [abs(int(self.locationOfZero [0]) + int(valuesToDeltaZero[0])),abs( int(self.locationOfZero [1]) + int(valuesToDeltaZero[1]))]
            #Withwhich we get the value at the destination
            valueAtDestination = self.nodeState[locationOfDestinationTile[0]][locationOfDestinationTile[1]]
            #Now define the new board state and swap the values
            childBoardState = None
            #Is Python pass by ref, I had no idea?
            childBoardState = copy.deepcopy(self.nodeState)
            childBoardState[locationOfDestinationTile[0]][locationOfDestinationTile[1]] = '0'
            childBoardState[self.locationOfZero [0]][self.locationOfZero [1] ] = valueAtDestination

            
            h_val = calculateManhattanPoints(childBoardState)

            if self.parent is None:
                self.childNodes.append( AStarNode(childBoardState,self.g + h_val,h_val, self) )
                continue
            
            if getBoardStateAsString(childBoardState) != getBoardStateAsString(self.parent.nodeState):
                self.childNodes.append( AStarNode(childBoardState,self.g + h_val, h_val, self) )
        
        #print('child nodes created: {0}'.format(self.getNumberOfChildren()))
    def getNumberOfChildren(self) :
        return len(self.childNodes)

def main():
    parser = argparse.ArgumentParser("a_star_manhattan")
    parser.add_argument("start", help="The file which contains the numbers to generate the slide #,#,#|#,#,#|#,#,# where each # is a unique integer  between 0 and 8, inclusive", type=str)
    args = parser.parse_args()

    f = open(args.start, "r")

    line = f.readline()

    slideBoard = parseInput(line)

    boardIsValid = validateInput(slideBoard)


    if  not boardIsValid :
        print("I am sorry, but the board is not valid, please run the program again")
        print("If you do not know the format, please use -h")
        return

    head = AStarNode(slideBoard,0,0,None)

    #add into priority queue
    pq = PriorityQueue()

    #So on occassion we get to a point where we might have two choices
    #that have the same f value and the same board state
    #What does it matter then? Let's flip a coin
    #flip a coin
    pq.put((0,0,random.random(),head))

    foundTheEndState = False
    endNode = None

    iterations = 0 

    while not foundTheEndState and pq.qsize() > 0 and iterations < 1000:
        #let us get the current board state from the queue
        popVal = pq.get()
        #Because of tie breakers, we dereference the 4th element of the array
        node = popVal[3]
        #then create the places we can go to from there
        node.createChildren()
        numChildNodes = node.getNumberOfChildren()
        #printing out the current board state, prior to going to the next board
        print(getBoardStateAsString(node.nodeState).replace('0','_'))

        for cn in range(0,numChildNodes):
            childNode = node.childNodes[cn]
            #and we enqueue each of the children made
            pq.put( ( childNode.g + childNode.h, getBoardStateAsString(childNode.nodeState), random.random() , childNode) )
            #unless if we get to the end state
            if childNode.h == 0 :
                foundTheEndState = True
                endNode = childNode
                break 
                    
        if foundTheEndState:
            break


    if foundTheEndState :
        print("We made it!")
        print(getBoardStateAsString(endNode.nodeState).replace('0','_'))
    if iterations >= 1000 :
        print("I am sorry to say, that I can't realisticly find an answer on a first geneartion i3 with 2gb of ram")
    else :
        print('bad things happened')



main()





