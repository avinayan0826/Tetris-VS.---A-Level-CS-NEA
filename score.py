class Score():
    def __init__(self):
        self.score = 0
        self.chain = 0 #consecutive line clear counter
        self.level = 1
        self.linesCleared = 0

    def softDropScore(self, rowsMoved):
        self.score += rowsMoved

    def hardDropScore(self, rowsMoved):
        self.score += (rowsMoved*2)

    def lineClearScore(self,numberCleared, piece):
        if numberCleared == 1:
            if piece == "T_Tet":
                self.score += 800
            else:
                self.score += 100
        elif numberCleared == 2:
            if piece == "T_Tet":
                self.score += 1200
            else:
                self.score += 300
        elif numberCleared == 3:
            if piece == "T_Tet":
                self.score += 1600
            else:
                self.score += 500
        elif numberCleared == 4:
            self.score += 800
        self.linesCleared += numberCleared
        self.levelUp()


    def comboScore(self, numberCleared):
        if numberCleared > 0: #if a line is cleared directly after a line clear, build the chain
            if self.chain > 0: #checking if a line was cleared
                self.chain += numberCleared #adding the number of lines cleared to the chain
                bonus = self.chain*50 #bonus score is calculated by multiplying the lines cleared in a row by 50
                self.score += bonus
            else:
                self.chain = 1 #first line clear - no bonus
        else:
            self.chain = 0 #if no lines are cleared, chain is broken

    def perfectClearScore(self, numberCleared):
        if numberCleared == 4:
            self.score += 3200
        else:
            self.score += 2000

    def levelUp(self):
        newLevel = (self.linesCleared // 10) + 1
        if newLevel > self.level:
            self.level = newLevel

