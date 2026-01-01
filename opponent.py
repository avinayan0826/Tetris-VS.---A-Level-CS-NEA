#This is where I will create my opponent Tetris bot, the logic constructed through the Greedy Best-First Search algorithm.
#The bot's gameplay will occur on GameManager's opponentBoard attribute.


#Importing the GameBoard class from gameBoard.py in order for the algorithm to have a copy of board states
from gameBoard import GameBoard
#Importing each tetrimino to simulate board placements
from pieces import *
#Importing heapq for the greedy best-first implementation
import heapq


class Opponent():
    def __init__(self, board_state):
        self.board_state = board_state

    def heuristic(self, simulated_board):
        return (
            0.55 * simulated_board.aggregateHeight() +
            0.45 * simulated_board.holes() +
            0.35 * simulated_board.bumpiness() +
            -0.95 * simulated_board.fullLines()
        )

    def isValid(self,piece): #checks that a move is valid, using the logic from gameboard functions
        simulated_board = self.board_state.simulatedBoard() #using the simulated board when simulating moves
        for piece in piece.getOccupiedCells(): #checks each individual tile in the tetrimino
            if (simulated_board.checkBoundary(piece.row, piece.column) == False or
                simulated_board.checkOccupiedCells(piece.row, piece.column) == False):
                return False #rejects move immediately if one tile is out of bounds
        return True #accepts as valid move

    def dropPiece(self, piece):
        simulated_board = self.board_state.simulatedBoard()
        if self.isValid(piece) == True:
            piece.offset(1,0) #drops the piece to the bottom
        else:
            piece.offset(-1,0) #stops when it is invalid
        for piece in piece.getOccupiedCells():
            self.board_state[piece.row][piece.column] = piece.shape
        simulated_board.fullLines()

#this function is responsible for generating all the possible placements for a piece
    def generatePlacements(self, opponentBoard, piece):
        #creating the array where valid board placements can easily be retrieved from
        boardPlacements = []
        #checking each column, with each rotation state in this nested for loop
        for rotation in range(4):
            copy_piece = piece.simulatedPiece() #creates a simulated piece for each rotation on the simulated board
            copy_piece.rotation = rotation #will loop for each rotation state
            for column in range(opponentBoard.columns):
                simulated_board = opponentBoard.simulatedBoard() #creating a simulated version of the opponent board
                simulated_piece = copy_piece.simulatedBoard() #simulating the piece again, in order to correctly iterate
                                                                #through each column without error
                #for each column, these two lines ensure that the piece starts from the top of the board in the next column
                simulated_piece.column = column
                simulated_piece.row = 0
                if simulated_board.isValid(simulated_piece) == True: #if the movement is valid...
                    full_lines = simulated_board.dropPiece(simulated_piece) #drop the piece and return the amount of full lines
                    #append all of these four factors into boardPlacements, which will then be examined as required by the GBFS algorithm
                    boardPlacements.append((simulated_board,full_lines,column,rotation))
        return boardPlacements

    def GBFS_bestMove(self, opponentBoard, piece):
        start_node = opponentBoard #the start node is the initial state of the opponent board passed in
        bestHeuristic = 0 #set the initial value to 0, this will be replaced by the lowest heuristic as each move is evaluated
        bestMove = None #set initially to None, this will be replaced by the best move as each move is evaluated,
                        #and the lowest heuristic is found
        #calls generatePlacements, to find all valid moves for the current board state and piece on the board
        boardPlacements = self.generatePlacements(opponentBoard, piece)
        #then unpacking each element of the boardPlacements array, to find the column, rotation state and the
        #number of lines cleared from a specific move
        for simulated_board, full_lines, column, rotation in boardPlacements:
            heuristic = self.heuristic(simulated_board) #calculate the heuristic of the move
            if heuristic < bestHeuristic:
                bestHeuristic = heuristic #the lower the heuristic the better the move - gbfs looks for the lowest heuristic
                bestMove = (column, rotation) #the move with the lowest heuristic is the best move out of all generated placements
        return bestMove #return and play the best move


