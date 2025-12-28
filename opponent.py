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
            if (simulated_board.checkBoundary(piece.row, piece.column) == False and
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
            sim_rotation = piece.simulatedBoard() #creates a simulated piece for each rotation on the simulated board
            sim_rotation.rotation = rotation #will loop for each rotation state
            for column in range(opponentBoard.columns):
                simulated_board = opponentBoard.simulatedBoard() #creating a simulated version of the opponent board
                simulated_piece = sim_rotation.simulatedBoard() #simulating the piece again, in order to correctly iterate
                                                                #through each column without error
                #for each column, these two lines ensure that the piece starts from the top of the board in the next column
                simulated_piece.column = column
                simulated_piece.row = 0
                if simulated_board.isValid(simulated_piece) == True: #if the movement is valid...
                    full_lines = simulated_board.dropPiece(simulated_piece) #drop the piece and return the amount of full lines
                    #append all of these four factors into boardPlacements, which will then be examined as required by the GBFS algorithm
                    boardPlacements.append((simulated_board,full_lines,column,rotation))
        return boardPlacements

    def greedy_best_first_search(self, problem, heuristic):
        start_node = problem.initial_state #evaluating the initial problem state that the search will start from
        if problem.is_goal_state(start_node):
            return start_node #if the initial state evaluated satisfies the goal, return it

        priority_queue = [] #creates an empty list that python will treat as a priority queue using heapq
        #uses the heappush function to find the heuristic of the start_node, and place that heuristic into the priority queue
        heapq.heappush(priority_queue, heuristic(start_node))
        visited = set() #keeps track of states that have been visited, prevents the same state from being evaluated in an infinite loop

        while priority_queue: #while the priority queue is not empty
            current_node = heapq.heappop(priority_queue) #removes and returns the item with the lowest heuristic
            visited.add(current_node) #add this current_node to the set of visited states

            #this loop creates a list, with get_successor, of all possible next states. the loop goes through each possible state,
            #and evaluates the heuristic. if the state has not been visited yet and is the 'goal' state, return that state,
            #and push it into the priority queue
            for successor in problem.get_successor(current_node):
                if successor not in visited:
                    if problem.is_goal_state(successor):
                        return successor
                    heapq.heappush(priority_queue, heuristic(successor))

        return None #if the search concludes without finding a 'goal', return None





