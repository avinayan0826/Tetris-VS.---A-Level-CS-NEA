import pygame
import random
from pieces import I_Tet,O_Tet,T_Tet,S_Tet,Z_Tet,J_Tet,L_Tet




#This class is responsible for board logic, for both user and opponent
class GameBoard():
    def __init__(self, xboardOffset, yboardOffset):
        self.rows = 20
        self.columns = 10 #the board size will always be 20x10, so we can define this when initialising the class
        self.cell_size = 30 #size of each individual square on the game board
        self.board = [[0  for j in range(self.columns)] for i in range(self.rows)] #board made up of the 20x10 grid
        self.colour = self.get_colours() #refers to the static method following this constructor method
        self.pieces = [I_Tet(),O_Tet(),T_Tet(),S_Tet(),Z_Tet(),J_Tet(),L_Tet()] #takes each tetrimino from the pieces class
        self.xboardOffset = xboardOffset
        self.yboardOffset = yboardOffset #configurable attributes for board offsets to differ between user and opponent

#using a static method to avoid creating duplicate code, and as it doesn't require instance code this allows for easy retrieval from tetrimino.py
    @staticmethod
    def get_colours():
        # creates a list where the index corresponds to the colour codes below, which will also correspond to tetrimino shapes (in pieces.py, with the shape attribute)

        grey = (26, 31, 40)  # 0
        green = (47, 230, 23)  # 1
        red = (232, 18, 18)  # 2
        orange = (226, 116, 17)  # 3
        yellow = (237, 234, 4)  # 4
        purple = (166, 0, 247)  # 5
        cyan = (21, 204, 209)  # 6
        blue = (13, 64, 216)  # 7
        garbage = (128, 128, 128) # 8

        return [grey, green, red, orange, yellow, purple, cyan, blue, garbage]

    def print_board(self): #prints the 20x10 2D array of 0s into the console
        for row in range(self.rows):
            for column in range(self.columns):
                print(self.board[row][column], end  = " ")
            print()

    #drawing the full game board for every frame
    def draw_board(self,screen):
        for row in range(self.rows):
            for column in range(self.columns):
                cell_value = self.board[row][column] #iterates through each cell in the grid, and assigns the value of that cell to cell_value
                cell_rect = pygame.Rect(
                                        self.xboardOffset + column*self.cell_size + 1,
                                        self.yboardOffset + row*self.cell_size + 1,
                                        self.cell_size - 1,
                                        self.cell_size - 1
                                        ) #pygame.Rect(x, y, width, height)
                pygame.draw.rect(screen, self.colour[cell_value], cell_rect) #pygame.draw.rect(surface, colour, rect)

    def checkBoundary(self,row, column): #checks that tetrimino is within the boundaries of the board
        if row >= 0 and row < self.rows and column >= 0 and column < self.columns:
            return True
        else:
            return False

    def checkOccupiedCells(self,row,column): #checks that a tetrimino hasn't overlapped another tetrimino
        if self.checkBoundary(row,column) == True and self.board[row][column] == 0:
            return True #returns True if a cell is empty
        else:
            return False

    def lineFull(self,row): #checks if a line is full by checking grid values
        for column in range(self.columns):
            if self.board[row][column] == 0: #if a cell out of all the columns in that row is 0, the line isn't full
                return False
        return True

    def clear(self,row): #clears the full lines
        for column in range(self.columns):
            self.board[row][column] = 0 #setting the line to equal 0, meaning no cells in the line are filled

    def dropRows(self,row,rows): #moves the leftover lines down when a line is cleared
        for column in range(self.columns):
            self.board[row+rows][column] = self.board[row][column] #moves the row down
            self.board[row][column] = 0 #clears the original line after moving it down - prevents duplication

    def clearAllFull(self): #keeps track of how many rows have been filled - uses clear() to clear them all
        full = 0 #this variable will be called to clear the right amount of lines
        for row in range(self.rows - 1,-1,-1): #starts with last row, in steps of -1 to first row
           if self.lineFull(row) == True:
               self.clear(row)
               full = full+1
           elif full > 0:
               self.dropRows(row,full) #calls on full to see how many lines it needs to drop
        return full #necessary for updating levels, for both players

    def restart(self): #reset the gameboard
        for row in range(self.rows):
            for column in range(self.columns):
                self.board[row][column] = 0 #resets every cell to 0 (empty) to restart the game

    def perfectClear(self): #returns true if the whole board is clear, cell value 0
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] != 0: #occupied cell
                    return False
        #exit the loop if an occupied cell is found
        return True

#THE FOLLOWING FUNCTIONS ARE REQUIRED FOR THE OPPONENT LOGIC

#creates the copy of the game board which the opponent simulates positions of pieces
    def simulatedBoard(self):
        simulated_board = GameBoard(self.xboardOffset,self.yboardOffset)
        for row in range(self.rows):
            for column in range(self.columns):
                simulated_board.board[row][column] = self.board[row][column]
        return simulated_board

#the following 4 functions required for heuristic calculations
    def aggregateHeight(self): #the sum of the height of each column on the board
        height = 0
        for column in range(self.columns):
            for row in range(self.rows):
                if self.board[row][column] != 0: #for each column, find the first row (start from top) where the cell is filled
                    height += self.rows-row
                    break
        return height #height of column calculated and returned once each column has been checked

    def holes(self): #detection of an empty cell, after a filled cell has already been detected in the same column
        holesFound = 0
        for column in range(self.columns):
            cellFilled = False #resets it to False for each column
            for row in range(self.rows):
                if self.board[row][column] != 0:
                    cellFilled = True #detects a filled cell
                #if the next row checked is 0 while cellFilled has been set to True, this means there is a hole
                elif self.board[row][column] == 0 and cellFilled == True:
                    holesFound += 1
        return holesFound #return the number of holes found after each column is checked

    def bumpiness(self): #summing of the absolute differences between all columns
        heights = [] #will input all column heights into an array for easy comparison
        for column in range(self.columns):
            height = 0 #restarts height to 0 each time a new column is examined
            for row in range(self.rows):
                if self.board[row][column] != 0: #for each column, find the first row (start from top) where the cell is filled
                    height += self.rows-row
                    break #breaks out of inner for loop to restart height to 0
            heights.append(height)
        bumpiness = 0
        for i in range(len(heights)-1):
            #finds the absolute difference between each consecutive pair of heights in the array
            bumpiness += abs(heights[i]-heights[i+1])
        return bumpiness


    def fullLines(self): #detecting how many full lines will be created from a move - mirrors the clearAllFull functionality, but without actually clearing a line
        full = 0  # keeps track of how many rows have been filled - this variable will be called to track the right amount of lines
        for row in range(self.rows - 1, -1, -1):  # starts with last row, in steps of -1 to first row
            if self.lineFull(row) == True:
                full = full + 1
        return full

#garbage line logic - sends a line to the bottom of the opposing board
    def garbageLines(self, linesCleared):
        for i in range(linesCleared):
            hole = random.randint(0, self.columns-1) #creates a random hole in the garbage line
            garbageLine = [8 for i in range(self.columns)] #grey line - index 8 corresponds to the colour grey in the static method
            garbageLine[hole] = 0 #set the hole equal to 0 so that it's an empty cell that can be filled
            self.board.pop(0)# removes the top row of the board
            self.board.append(garbageLine) #adds the garbage line to the bottom of the board - treats the board as an array by using append()

