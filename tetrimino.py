import pygame
from colours import get_colours

class Position():
    def __init__(self, row, column):
        self.row = row
        self.column = column

class Tetrimino():
    def __init__(self, shape):
        self.shape = shape
        self.occupied_cells = {}
        self.cell_size = 30
        self.x = 3 #tetrimino starting in the centre of the board, column 5/10, absolute position
        self.y = 0 #tetrimino starting on the first row 1/10, absolute position
        self.row_offset = 0
        self.column_offset = 0
        self.rotation = 0
        self.colour = get_colours()

    #performs the same function as the draw_board function, but for each tetrimino square
    def draw_tet(self, screen, gameBoard):
        blocks = self.getOccupiedCells()
        for block in blocks:
            block_rect = pygame.Rect(
                gameBoard.xboardOffset + block.column * self.cell_size + 1,
                gameBoard.yboardOffset + block.row * self.cell_size + 1,
                #gameBoard is the GameBoard object passed in as a parameter when this function is called, allowing us
                #to use xboardOffset and yboardOffset attributes, and avoid using hardcoded variables
                self.cell_size - 1,
                self.cell_size - 1
                                     )
            pygame.draw.rect(screen, self.colour[self.shape],block_rect)

    def offset(self, rows, columns): #this method removes the need to modify and recalculate positions when checking for collisions
        self.row_offset += rows
        self.column_offset += columns

    def getOccupiedCells(self):  # returns the positions of the occupied cells with the offset
        blocks = self.occupied_cells[self.rotation]
        movedBlocks = []
        for position in blocks:
            position = Position(
                position.row + self.row_offset + self.y,
                position.column + self.column_offset + self.x
            ) #adding self.y and self.x returns absolute board coordinates for each cell
            movedBlocks.append(position)
        return movedBlocks

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def reverseRotate(self):
        self.rotation = (self.rotation - 1) % 4

#for simulating a piece for the opponent
    def simulatedPiece(self):
        #building a simulated piece that copies the type of tetrimino, position on the board, rotation and its occupied cells
        simulated_piece = type(self.shape)
        simulated_piece.x = self.x
        simulated_piece.y = self.y
        simulated_piece.row_offset = self.row_offset
        simulated_piece.column_offset = self.column_offset
        simulated_piece.rotation = self.rotation
        simulated_piece.occupied_cells = self.occupied_cells
        return simulated_piece





