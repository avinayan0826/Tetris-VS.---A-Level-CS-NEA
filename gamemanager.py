import pygame.time

from gameBoard import GameBoard
from pieces import *
from score import Score
from opponent import Opponent
import random

class GameManager:
    def __init__(self):
        #instances of GameBoard object, one for the user one for the opponent
        self.gameBoard = GameBoard(80,80)
        self.opponentBoard = GameBoard(650,80)
        self.opponent = Opponent(self.opponentBoard)
        self.pieces = [I_Tet(),O_Tet(),T_Tet(),S_Tet(),Z_Tet(),J_Tet(),L_Tet()]
        self.currentPiece = self.genNewPiece()
        self.nextPiece = self.genNewPiece()
        self.opponentPiece = self.genNewPiece()
        self.opponentTargetCol = None
        self.opponentTargetRot = None
        self.nextQ = [self.genNewPiece() for i in range(3)] #list of 3 pieces in 'next pieces' queue
        self.gameOver = False
        self.opponentMoveSet = False
        self.targetAligned = False
        self.score = Score()
        self.AUTOMATIC_FALL = pygame.USEREVENT #avoids circular import
        self.setOpponentMove()


    def genNewPiece(self): #randomly chooses a tetrimino to spawn
        if len(self.pieces) == 0:
            self.pieces = [I_Tet(),O_Tet(),T_Tet(),S_Tet(),Z_Tet(),J_Tet(),L_Tet()]
        piece = random.choice(self.pieces)
        self.pieces.remove(piece) #removes piece from list temporarily so it can't be called until the list is recreated
        return piece

    def draw(self,screen): #draws the random tetrimino on the board
        self.gameBoard.draw_board(screen)
        self.currentPiece.draw_tet(screen, self.gameBoard)
        self.drawNextQ(screen, x=400, y=350)
        self.opponentBoard.draw_board(screen)
        self.opponentPiece.draw_tet(screen, self.opponentBoard)

    def drawNextQ(self, screen, x, y):
        for i, piece in enumerate(self.nextQ):
            offsetQ = y + i*100
            for block in piece.getOccupiedCells():
                rect = pygame.Rect(x + block.column*20, offsetQ + block.row*20, 20, 20)
                pygame.draw.rect(screen, piece.colour[piece.shape], rect)

    def shiftLeft(self):
        self.currentPiece.offset(0,-1)
        if self.pieceInside() == False or self.checkCellsManager() == False: #checks if the piece is about to go beyond
                                                                            # the grid, or if there is already an occupied cell
            self.currentPiece.offset(0,1)

    def shiftRight(self):
        self.currentPiece.offset(0,1)
        if self.pieceInside() == False or self.checkCellsManager() == False: #checks if the piece is about to go beyond
                                                                            # the grid, or if there is already an occupied cell
            self.currentPiece.offset(0,-1)

    def softDrop(self, manual=False):
        self.currentPiece.offset(1,0)
        if self.pieceInside() == False or self.checkCellsManager() == False: #checks if the piece is about to go beyond
                                                                            # the grid, or if there is already an occupied cell
            self.currentPiece.offset(-1,0)
            self.lockPiece()
        elif manual == True:
                self.score.softDropScore(1)

    def hardDrop(self):
        rowsMoved = 0
        while self.pieceInside() == True and self.checkCellsManager() == True:
            self.currentPiece.offset(1,0)
            rowsMoved += 1
        self.currentPiece.offset(-1,0)
        rowsMoved -= 1
        self.lockPiece()
        self.score.hardDropScore(rowsMoved)

    def lockPiece(self):

        blocks = self.currentPiece.getOccupiedCells()
        for block in blocks:
            self.gameBoard.board[block.row][block.column] = self.currentPiece.shape #storing the corresponding values of the tetrimino
                                                                                    #into the grid
        numberCleared = self.gameBoard.clearAllFull()
        self.score.lineClearScore(numberCleared,(type(self.currentPiece).__name__)) #checking the number of lines cleared, and whether it is a T piece
        newSpeed = max(100, 700-((self.score.level-1)*50)) #for each level up, speed of automatic fall increases by 50ms
        pygame.time.set_timer(self.AUTOMATIC_FALL,newSpeed) #changes automatic fall to the new speed for each level up
        if numberCleared > 0 and self.gameBoard.perfectClear() == True:
            self.score.perfectClearScore(numberCleared)
        self.score.comboScore(numberCleared) #checking for combo score
        self.currentPiece = self.nextQ.pop(0)
        self.nextQ.append(self.genNewPiece()) #add a new piece to the queue
        if self.checkCellsManager() == False:
            self.gameOver = True

    def pieceInside(self):
        blocks = self.currentPiece.getOccupiedCells()
        for block in blocks:
            if not self.gameBoard.checkBoundary(block.row,block.column):
                return False
        return True #taking return True out of the loops should mean that it only returns True if ALL blocks are inside the grid

    def rotateManager(self):
        self.currentPiece.rotate()
        if self.pieceInside() == False and self.checkCellsManager() == False:
            self.currentPiece.reverseRotate()

    def checkCellsManager(self):
        blocks = self.currentPiece.getOccupiedCells()
        for block in blocks:
            if self.gameBoard.checkOccupiedCells(block.row,block.column) == False:
                return False
        return True

    def restart(self):
        self.gameBoard.restart()
        self.pieces = [I_Tet(), O_Tet(), T_Tet(), S_Tet(), Z_Tet(), J_Tet(), L_Tet()]
        self.currentPiece = self.genNewPiece()
        self.nextPiece = self.genNewPiece()

#specifically for opponent bot
    def setOpponentMove(self):
        bestMove = self.opponent.GBFS_bestMove(self.opponentBoard,self.opponentPiece)
        if bestMove:
            self.opponentTargetCol,self.opponentTargetRot = bestMove
            self.opponentPiece.rotation = self.opponentTargetRot
            self.opponentMoveSet = True


    def moveOpponent(self):
        if self.opponentMoveSet == False:
            return
        #get the actual current column, and see whether this matches the target
        currentColumn = self.opponentPiece.x + self.opponentPiece.column_offset
        if currentColumn < self.opponentTargetCol:
            self.opponentPiece.offset(1,0) #automatic fall
            self.opponentPiece.offset(0,1)
            return #don't drop yet, wait for next frame
        elif currentColumn > self.opponentTargetCol:
            self.opponentPiece.offset(1,0) #automatic fall
            self.opponentPiece.offset(0,-1)
            return #don't drop yet, wait for the next frame
        #only hard drop once we're at the target column, and if the board position is valid
        while currentColumn == self.opponentTargetCol and self.opponent.isValid(self.opponentPiece, self.opponentBoard) == True:
            self.opponentPiece.offset(1,0)
        if self.opponent.isValid(self.opponentPiece, self.opponentBoard) == False: #lock the piece once it reaches the bottom
            self.opponentPiece.offset(-1,0)
            self.lockOpPiece()


    def lockOpPiece(self):
        blocks = self.opponentPiece.getOccupiedCells()
        for block in blocks:
            self.opponentBoard.board[block.row][block.column] = self.opponentPiece.shape  #storing the corresponding values of the tetrimino
                                                                                     #into the grid
        numberCleared = self.opponentBoard.clearAllFull()
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
        self.targetAligned = False
        self.opponentTargetCol = None
        self.opponentTargetRot = None
        self.opponentMoveSet = False
        self.setOpponentMove()
        if self.checkCellsManager() == False:
            self.gameOver = True


