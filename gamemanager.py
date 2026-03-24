#This is the file where all other files have been imported into. This was created to avoid circular imports, and connects all the other files' functionality
# to the main file
import pygame.time

from gameBoard import GameBoard
from pieces import *
from score import Score
from opponent import Opponent
import random

#This class is responsible for connecting functions from all other files to the main file, without causing circular imports
class GameManager:
    def __init__(self):
        self.gameBoard = GameBoard(80,80)
        self.opponentBoard = GameBoard(650,80) #instances of GameBoard object, one for the user one for the opponent
        self.opponent = Opponent(self.opponentBoard) #instantiation of the Opponent class, which creates the opponent bot, and applies it to the opponent board
        self.pieces = [I_Tet(),O_Tet(),T_Tet(),S_Tet(),Z_Tet(),J_Tet(),L_Tet()]
        self.currentPiece = self.genNewPiece()
        self.nextPiece = self.genNewPiece()
        self.opponentPiece = self.genNewPiece() #genNewPiece() spawns a random piece onto user/opponent board
        self.opponentTargetCol = None
        self.opponentTargetRot = None #two null assignments, that will store the 'best move' that the opponent calculates
        self.nextQ = [self.genNewPiece() for i in range(3)] #list of 3 pieces in 'next pieces' queue
        self.gameOver = False
        self.opponentMoveSet = False #determines whether the opponent has planned a move or not
        self.targetAligned = False #determines whether the opponent piece has aligned with the target column before it hard drops
        self.score = Score()
        self.AUTOMATIC_FALL = pygame.USEREVENT #avoids circular import
        self.setOpponentMove() #ensures that the first opponent move is planned on the program's start


    def genNewPiece(self): #randomly chooses a tetrimino to spawn
        if len(self.pieces) == 0:
            self.pieces = [I_Tet(),O_Tet(),T_Tet(),S_Tet(),Z_Tet(),J_Tet(),L_Tet()] #recreates the list of tetriminos to spawn to prevent it from not spawning a piece
        piece = random.choice(self.pieces)
        self.pieces.remove(piece) #removes piece from list temporarily so it can't be called until the list is recreated
        return piece

    def draw(self,screen): #draws all the required elements on the board: the user board, user piece, next queue, opponent board and opponent piece
        self.gameBoard.draw_board(screen)
        self.currentPiece.draw_tet(screen, self.gameBoard)
        self.drawNextQ(screen, x=400, y=350)
        self.opponentBoard.draw_board(screen)
        self.opponentPiece.draw_tet(screen, self.opponentBoard)

    def drawNextQ(self, screen, x, y): #responsible for drawing the next queue
        for i, piece in enumerate(self.nextQ):
            offsetQ = y + i*100
            for block in piece.getOccupiedCells():
                rect = pygame.Rect(x + block.column*20, offsetQ + block.row*20, 20, 20)
                pygame.draw.rect(screen, piece.colour[piece.shape], rect)

#movement functions
    def shiftLeft(self):
        self.currentPiece.offset(0,-1) #moving a tetrimino one cell to the left
        if self.pieceInside() == False or self.checkCellsManager() == False: #checks if the piece is about to go beyond
                                                                            # the grid, or if there is already an occupied cell
            self.currentPiece.offset(0,1)

    def shiftRight(self):
        self.currentPiece.offset(0,1) #moving a tetrimino one cell to the right
        if self.pieceInside() == False or self.checkCellsManager() == False: #checks if the piece is about to go beyond
                                                                            # the grid, or if there is already an occupied cell
            self.currentPiece.offset(0,-1)

    def softDrop(self, manual=False):
        self.currentPiece.offset(1,0) #moving a tetrimino one cell down
        if self.pieceInside() == False or self.checkCellsManager() == False: #checks if the piece is about to go beyond
                                                                            # the grid, or if there is already an occupied cell
            self.currentPiece.offset(-1,0)
            self.lockPiece()
        elif manual == True:
                self.score.softDropScore(1) #if it was a manual soft drop, 1 point added per soft drop - needed to differentiate between soft drop and automatic fall

    def hardDrop(self):
        rowsMoved = 0
        while self.pieceInside() == True and self.checkCellsManager() == True:
            self.currentPiece.offset(1,0) #moving the tetrimino to the bottom of the bottom of the board
            rowsMoved += 1
        self.currentPiece.offset(-1,0) #ensures the tetrimino doesn't go beyond board boundaries
        rowsMoved -= 1
        self.lockPiece()
        self.score.hardDropScore(rowsMoved)

# function responsible for locking the piece to the board, and carrying out the functions that are needed after that
    def lockPiece(self):
        blocks = self.currentPiece.getOccupiedCells()
        for block in blocks:
            self.gameBoard.board[block.row][block.column] = self.currentPiece.shape #storing the corresponding values of the tetrimino
                                                                                    #into the grid
        numberCleared = self.gameBoard.clearAllFull() #clears all the full lines, and records the number of lines cleared
        self.opponentBoard.garbageLines(numberCleared) #sends the required amount of garbage lines to the opponent board
        self.score.lineClearScore(numberCleared,(type(self.currentPiece).__name__)) #checking the number of lines cleared, and whether it is a T piece
        newSpeed = max(100, 700-((self.score.level-1)*50)) #for each level up, speed of automatic fall increases by 50ms
        pygame.time.set_timer(self.AUTOMATIC_FALL,newSpeed) #changes automatic fall to the new speed for each level up
        if numberCleared > 0 and self.gameBoard.perfectClear() == True:
            self.score.perfectClearScore(numberCleared)
        self.score.comboScore(numberCleared) #checking for combo score
        self.currentPiece = self.nextQ.pop(0) #spawning in the first piece in the next queue as the next one on the board
        self.nextQ.append(self.genNewPiece()) #add a new piece to the queue
        if self.checkCellsManager() == False: #if the tetrimino has no choice but to overlap, game over.
            self.gameOver = True


    def pieceInside(self): #links checkBoundary() from gameboard.py to the main file
        blocks = self.currentPiece.getOccupiedCells()
        for block in blocks:
            if not self.gameBoard.checkBoundary(block.row,block.column):
                return False #returns False as soon as one block is outside the board boundaries
        return True #taking return True out of the loops should mean that it only returns True if ALL blocks are inside the grid

    def rotateManager(self): #links rotate() and reverseRotate() from tetrimino.py to the main file
        self.currentPiece.rotate()
        if self.pieceInside() == False and self.checkCellsManager() == False:
            self.currentPiece.reverseRotate()

    def checkCellsManager(self): #links checkOccupiedCells() from gameboard.py to the main file
        blocks = self.currentPiece.getOccupiedCells()
        for block in blocks:
            if self.gameBoard.checkOccupiedCells(block.row,block.column) == False:
                return False
        return True

    def restart(self): #links restart() from gameboard.py to the main file
        self.gameBoard.restart()
        self.opponentBoard.restart()
        self.pieces = [I_Tet(), O_Tet(), T_Tet(), S_Tet(), Z_Tet(), J_Tet(), L_Tet()]
        self.currentPiece = self.genNewPiece()
        self.nextPiece = self.genNewPiece()

#specifically for opponent bot
    def setOpponentMove(self): #responsible for planning the best move, using GBFS_bestMove() and generatePlacements() from opponent.py
        bestMove = self.opponent.GBFS_bestMove(self.opponentBoard,self.opponentPiece) #using simulation of opponent board and opponent piece
        if bestMove:
            self.opponentTargetCol,self.opponentTargetRot = bestMove #setting the target column and target rotation state in the bestMove tuple
            self.opponentPiece.rotation = self.opponentTargetRot #setting the target rotation flag
            self.opponentMoveSet = True #the best move has been planned


    def moveOpponent(self):
        if self.opponentMoveSet == False:
            return #don't return anything if a move hasn't been planned
        currentColumn = self.opponentPiece.x + self.opponentPiece.column_offset #get the actual current column, and see whether this matches the target
        if currentColumn < self.opponentTargetCol:
            self.opponentPiece.offset(1,0) #automatic fall
            self.opponentPiece.offset(0,1) #move to the right
            return #don't drop yet, wait for next frame
        elif currentColumn > self.opponentTargetCol:
            self.opponentPiece.offset(1,0) #automatic fall
            self.opponentPiece.offset(0,-1) #move to the left
            return #don't drop yet, wait for the next frame
        #only hard drop once we're at the target column, and if the board position is valid
        while currentColumn == self.opponentTargetCol and self.opponent.isValid(self.opponentPiece, self.opponentBoard) == True:
            self.opponentPiece.offset(1,0)
        if self.opponent.isValid(self.opponentPiece, self.opponentBoard) == False: #lock the piece once it reaches the bottom
            self.opponentPiece.offset(-1,0)
            self.lockOpPiece()


    def lockOpPiece(self): #replicating the same logic as lockPiece(), but for the opponent side
        blocks = self.opponentPiece.getOccupiedCells()
        for block in blocks:
            self.opponentBoard.board[block.row][block.column] = self.opponentPiece.shape  #storing the corresponding values of the tetrimino
                                                                                     #into the grid
        numberCleared = self.opponentBoard.clearAllFull()
        self.gameBoard.garbageLines(numberCleared)
        self.score.lineClearScore(numberCleared, (
            type(self.opponentPiece).__name__))  # checking the number of lines cleared, and whether it is a T piece
        newSpeed = max(100, 700 - (
                    (self.score.level - 1) * 50))  # for each level up, speed of automatic fall increases by 50ms
        pygame.time.set_timer(self.AUTOMATIC_FALL,
                              newSpeed)  # changes automatic fall to the new speed for each level up
        if numberCleared > 0 and self.opponentBoard.perfectClear() == True:
            self.score.perfectClearScore(numberCleared)
        self.score.comboScore(numberCleared)  # checking for combo score
        self.opponentPiece = self.genNewPiece()
        #resetting all the flags back to original state for the next move
        self.targetAligned = False
        self.opponentTargetCol = None
        self.opponentTargetRot = None
        self.opponentMoveSet = False
        self.setOpponentMove()
        if self.checkCellsManager() == False: #if the tetrimino has no choice but to overlap, game over.
            self.gameOver = True







