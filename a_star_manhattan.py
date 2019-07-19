#!/usr/bin/python
import argparse

#Define the possible moves for 0 at any given location in the 3x3 grid
#The start location of 0 is defined as [x,y] that correspondes to the positions in the array
#a move can only fall within (x2 = x1+1 || x2= x1-1 || x2 = x1) && (y2 = y1+1 || y2=y1-1 || y2=y1)
#While x2 is between 0 and 2, inclusive; AND y2 is betwee 0 and 2, inclusive
#Given that we can only move up, down, left and right, the range of all valid moves can be described as:

vm = {
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
    '0' : [0,0],
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
    #print(board)
    points = 0
    for x in range(0,len(board)) :
        for y in range(0,len(board[x])) :
            #the example in the video only counts a sum of 8 tiles
            #I don't think it's necessary to exclude tile 0
            #And whether 1 move away from goal state is 2 points or 1 point
            #Doesn't particularly matter as long as h*(n) is decreasing
            #But would this count as an overestimation?
            current = [x,y]
            goal = goalState[board[x][y]]
            if current != goal :
                #Calculate points here
                #Which we can do by finding the |delta x| + |delta y| of
                #current --> goal
                points += abs(int(current[0]) + goal[0]) + abs(int(current[1]) + goal[1])
    #print(points)             

#Iterate through the matrix and print out the location each number
#TODO: Print 0 as ' '
def printBoardState( board ):
    for row in board:
        print("{0} {1} {2}".format(row[0],row[1],row[2]))

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
    

class EightBlockNode:
    def __init__(self, boardState, costSoFare, estimatedDistance = -1):
        self.boardState = boardState
        self.g = costSoFare
        self.h = estimatedDistance
        self.locationOfZero = self.findZero(boardState)
        if estimatedDistance != 0:
            self.children = self.getChildren(self,self.findMovesForZero(locationOfZero),boardState)
        else:
            print("Solution found")
        
        print("Total Distance traversed: {0}".format(g+h))
    

    def findZero(self, board ) :
        #This code is reused a lot, I know
        #It could be done as a lambda or even as a numpy array
        #But this is just readable
        for x in range(0,len(board)) :
            for y in range(0,len(board[x])) :
                return [x,y]

    def findMovesForZero (self, zero) :

                return validMovesPerGridLocation[zero[0] + ',' + zero[1]]

    def getChildren( validMovesOfZero, boardState ):
        #We need to make a board state for each move
        childBoardStates = []
        for move in validMovesOfZero:
            #Dereference the values fromt he global that defines valid moves based on location
            valuesToDeltaZero = vm[move]
            #Here destinate location
            locationOfDestinationTile = [abs(self.locationOfZero[0] + vm[0]),abs(self.locationOfZero[1] + vm[1])]
            #Withwhich we get the value at the destination
            valueAtDestination = boardState[locationOfDestinationTile[0],locationOfDestinationTile[1]]
            #now we swap with 0
            childBoardState = boardState
            childBoardState[locationOfDestinationTile[0],locationOfDestinationTile[1]] = 0
            childBoardState[self.locationOfZero[0] , self.locationOfZero[1] ] = valueAtDestination
            #With this new board state we can calculate the manhattan distance:
            manhattanDistance = calculateManhattanPoints(childBoardState)
            #If the manhatta Distance is 0, pack it up, we found it
            
            childBoardStates.append( [childBoardState, costSoFare + manhattanDistance, manhattanDistance] )

        #only travel to the board that has the smallest manhattanDistance, I think
        smallestManhattan = -1
        for cb in range(0,len(ChildBoardStates)):
            if smallestManhattan == -1:
                smallestManhattan = cb
                continue
            
            if childBoardStates[cb][2] <= childBoardStates[smallestManhattan][2]:
                smallestManhattan = cb            



            



def main():
    parser = argparse.ArgumentParser("a_star_manhattan")
    parser.add_argument("start", help="The file which contains the numbers to generate the slide #,#,#|#,#,#|#,#,# where each # is a unique integer  between 0 and 8, inclusive", type=str)
    args = parser.parse_args()

    f = open(args.start, "r")

    line = f.readline()

    slideBoard = parseInput(line)

    boardIsValid = validateInput(slideBoard)

    #printBoardState(slideBoard)

    #calculateManhattanPoints(slideBoard)

    tree =  EightBlockNode(slideBoard, 0, -1)
    


'''
    while( boardIsValid == False ):
        print('Bad input please try again')
        print('Only the first like of the file will be read, and it must be formatted like this:')
        print('#,#,#|#,#,#|#,#,#')
        print('where each # is a unique integer  between 0 and 8, inclusive')
        print('Enter a new file to read:')

        #get new file
        f = open(args.start, "r")

        line = f.readline()
'''



main()





