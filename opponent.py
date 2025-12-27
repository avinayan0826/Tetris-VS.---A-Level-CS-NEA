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





