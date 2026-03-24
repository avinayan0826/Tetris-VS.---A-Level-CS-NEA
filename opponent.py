#This is where I will create my opponent Tetris bot, the logic constructed through the Greedy Best-First Search algorithm.
#The bot's gameplay will occur on GameManager's opponentBoard attribute.

#Importing the GameBoard class from gameBoard.py in order for the algorithm to have a copy of board states
from gameBoard import GameBoard

#Importing each tetrimino to simulate board placements
from pieces import *


#This class is responsible for the logic in developing the opponent bot
class Opponent():
    def __init__(self, board_state):
        self.board_state = board_state #this attribute will represent the board state of the chosen board during gameplay

    def heuristic(self, simulated_board): #building a heuristic based off of the following functions defined in gameboard.py
        return (
            0.55 * simulated_board.aggregateHeight() +
            0.45 * simulated_board.holes() +
            0.35 * simulated_board.bumpiness() + #positive heuristics for factors I want to minimise
            -0.95 * simulated_board.fullLines() #negative heuristic for factors I want to maximise - GBFS looks for the lowest heuristic
        )

    def isValid(self,piece, board): #checks that a move is valid, using the logic from gameboard functions
        for block in piece.getOccupiedCells(): #checks each individual tile in the tetrimino
            if (board.checkBoundary(block.row, block.column) == False or
                board.checkOccupiedCells(block.row, block.column) == False):
                return False #rejects move immediately if one tile is out of bounds
        return True #accepts as valid move

    def dropPiece(self, simulated_board, piece): #dropping the piece in the simulation to determine the result
        while self.isValid(piece, simulated_board) == True:
            piece.offset(1,0)
        piece.offset(-1,0) #doesn't allow the piece to go beyond the board
        for block in piece.getOccupiedCells():
            simulated_board.board[block.row][block.column] = piece.shape
        return simulated_board.fullLines() #returning the amount of full lines created from the dropping the piece

#this function is responsible for generating all the possible placements for a piece
    def generatePlacements(self, opponentBoard, piece):
        #creating the array where valid board placements can easily be retrieved from
        boardPlacements = []
        #checking each column, with each rotation state in this nested for loop
        for rotation in range(4):
            copy_piece = piece.simulatedPiece() #creates a simulated piece for each rotation on the simulated board
            copy_piece.rotation = rotation #will loop for each rotation state
            for column in range(-4, opponentBoard.columns +4):
                simulated_board = opponentBoard.simulatedBoard() #creating a simulated version of the opponent board
                simulated_piece = copy_piece.simulatedPiece() #simulating the piece again, in order to correctly iterate
                                                                #through each column without error
                #for each column, these two lines ensure that the piece starts from the top of the board in the next column
                simulated_piece.x = column
                simulated_piece.y = 0
                if self.isValid(simulated_piece, simulated_board) == True: #if the movement is valid...
                    full_lines = self.dropPiece(simulated_board,simulated_piece) #drop the piece and return the amount of full lines
                    #append all of these four factors into boardPlacements, which will then be examined as required by the GBFS algorithm
                    boardPlacements.append((simulated_board,full_lines,column,rotation))
        print("Best move found!") #debugging line
        return boardPlacements #return the array of possible board placements

#this function is responsible for implementing the greedy-best-first search, using the functions above to determine which move is the best out of all possible placements.
#stores the chosen target column and target rotation state in the tuple bestMove, which is used in setOpponentMove() in gamemanager.py to plan the opponent move.
    def GBFS_bestMove(self, opponentBoard, piece):
        start_node = opponentBoard #the start node is the initial state of the opponent board passed in
        bestHeuristic = float("inf") #set the initial value to infinity, this will be replaced by the lowest heuristic as each move is evaluated
        bestMove = None #set initially to None, this will be replaced by the best move as each move is evaluated,
                        #and the lowest heuristic is found
        #calls generatePlacements, to find all valid moves for the current board state and piece on the board
        boardPlacements = self.generatePlacements(opponentBoard, piece)
        #then unpacking each element of the boardPlacements array, to find the column, rotation state and the
        #number of lines cleared from a specific move
        for simulated_board, full_lines, column, rotation in boardPlacements:
            heuristic = self.heuristic(simulated_board) #calculate the heuristic of the move
            if heuristic < bestHeuristic:
                bestHeuristic = heuristic #the lower the heuristic the better the move - GBFS looks for the lowest heuristic
                bestMove = (column, rotation) #the move with the lowest heuristic is the best move out of all generated placements
        print("Best move calculated!") #debugging line
        return bestMove #return and play the best move


