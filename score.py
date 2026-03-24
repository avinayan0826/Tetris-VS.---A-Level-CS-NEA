#This class is responsible for calculating scores and levels
class Score():
    def __init__(self):
        self.score = 0 #score tracker
        self.chain = 0 #consecutive line clear counter
        self.level = 1 #level tracker
        self.linesCleared = 0 #keeps track of lines cleared

    def softDropScore(self, rowsMoved):
        self.score += rowsMoved #1 point per row moved

    def hardDropScore(self, rowsMoved):
        self.score += (rowsMoved*2) #2 points per row moved

    def lineClearScore(self,numberCleared, piece): #scoring for line clears - T tetrimino clears earn more points
        if numberCleared == 1:
            if piece == "T_Tet":
                self.score += 800 #800 points for 1 line cleared if it is a T piece
            else:
                self.score += 100 #100 points for 1 line cleared
        elif numberCleared == 2:
            if piece == "T_Tet":
                self.score += 1200 #1200 points for 2 lines cleared if it is a T piece
            else:
                self.score += 300 #300 points for 2 lines cleared
        elif numberCleared == 3:
            if piece == "T_Tet":
                self.score += 1600 #1600 points for 3 lines cleared if it is a T piece
            else:
                self.score += 500 #500 points for 3 lines cleared
        elif numberCleared == 4:
            self.score += 800 #800 points for 4 lines cleared (Tetris clear)
        self.linesCleared += numberCleared #adding number cleared to the lines cleared counter
        self.levelUp() #level up if 10 lines have been cleared


    def comboScore(self, numberCleared): #responsible for combo scoring
        if numberCleared > 0: #if a line is cleared directly after a line clear, build the chain
            if self.chain > 0: #checking if a line was cleared
                self.chain += numberCleared #adding the number of lines cleared to the chain
                bonus = self.chain*50 #bonus score is calculated by multiplying the lines cleared in a row by 50
                self.score += bonus
            else:
                self.chain = 1 #first line clear - no bonus
        else:
            self.chain = 0 #if no lines are cleared, chain is broken

    def perfectClearScore(self, numberCleared): #scoring if the whole board is made clear from a move
        if numberCleared == 4:
            self.score += 3200 #perfect clear gives 3200 points if from a 4 line clear
        else:
            self.score += 2000 #perfect clear gives 2000 points if from any other number of lines cleared

    def levelUp(self): #updates the level for every 10 lines cleared
        newLevel = (self.linesCleared // 10) + 1 #using floor division to determine whether the total amount of lines cleared is a multiple of 10
        if newLevel > self.level:
            self.level = newLevel #update the level for every 10 lines cleared - corresponds to increase in speed per level in gamemanager.py

