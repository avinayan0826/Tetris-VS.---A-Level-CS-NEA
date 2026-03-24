import pygame
from colours import get_colours


class Position(): #represents the grid positions in a contained way, prevents repetitive use of tuples
    def __init__(self, row, column):
        self.row = row
        self.column = column

#Base class responsible for the functionalities of the tetrimino pieces
class Tetrimino():
    def __init__(self, shape):
        self.shape = shape #corresponds to an index from 0-7; each will be assigned to a specific tetrimino shape and colour
        self.occupied_cells = {} #dictionary of coordinates defined in pieces.py, and allows for the occupied cells on the board to be retrieved
        self.cell_size = 30 #px size
        self.x = 3 #tetrimino starting in the centre of the board, column 5/10, absolute position
        self.y = 0 #tetrimino starting on the first row 1/10, absolute position
        self.row_offset = 0
        self.column_offset = 0 #row_offset and column_offset are used in the offset method to move the piece by a required amount of rows/columns
        self.rotation = 0 #corresponds to rotation states, with index 0-3, defined in pieces.py
        self.colour = get_colours() #refers to the function in the colours file (to avoid circular import from gameBoard.py)

    #performs the same function as the draw_board function, but for each tetrimino square
    def draw_tet(self, screen, gameBoard):
        blocks = self.getOccupiedCells() #defining the 'blocks' as all cells it occupies
        for block in blocks: #drawing the tetrimino for each block that it is made up of
            block_rect = pygame.Rect(
                gameBoard.xboardOffset + block.column * self.cell_size + 1,
                gameBoard.yboardOffset + block.row * self.cell_size + 1,
                #gameBoard is the GameBoard object passed in as a parameter when this function is called, allowing us
                #to use xboardOffset and yboardOffset attributes, and avoid using hardcoded variables
                self.cell_size - 1,
                self.cell_size - 1
                                     )
            pygame.draw.rect(screen, self.colour[self.shape],block_rect)

    #the offset() method is responsible for tracking how many rows/columns a piece has to be moved
    #it also removes the need to modify and recalculate positions when checking for collisions
    def offset(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def getOccupiedCells(self):  # returns the positions of the occupied cells with the offset
        blocks = self.occupied_cells[self.rotation] #uses the rotation state to determine coordinates from the dictionary of occupied cells
        movedBlocks = []
        for position in blocks:
            position = Position(
                position.row + self.row_offset + self.y,
                position.column + self.column_offset + self.x
            ) #adding self.y and self.x returns absolute board coordinates for each cell
            movedBlocks.append(position)
        return movedBlocks #returns position

    #increments the value for rotation state for every up arrow key press, using a mod function
    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    #prevents the rotation state from incrementing if it goes past a board boundary
    def reverseRotate(self):
        self.rotation = (self.rotation - 1) % 4

    def getWidth(self): #returning the full range of columns that the opponent piece can move to
        cells = self.occupied_cells[self.rotation]
        columns = [cell.column for cell in cells]
        return max(columns) - min(columns)+1

#for simulating a piece for the opponent
    def simulatedPiece(self):
        #building a simulated piece that copies the type of tetrimino, position on the board, rotation and its occupied cells
        simulated_piece = Tetrimino(self.shape)
        simulated_piece.x = self.x
        simulated_piece.y = self.y
        simulated_piece.row_offset = self.row_offset
        simulated_piece.column_offset = self.column_offset
        simulated_piece.rotation = self.rotation
        simulated_piece.occupied_cells = self.occupied_cells
        return simulated_piece





