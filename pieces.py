from tetrimino import Tetrimino, Position

class I_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=1)
        self.occupied_cells = {
            0:[Position(1,0),Position(1,1),Position(1,2),Position(1,3)],
            1:[Position(0,2),Position(1,2),Position(2,2),Position(3,2)],
            2:[Position(2,0),Position(2,1),Position(2,2),Position(2,3)],
            3:[Position(0,1),Position(1,1),Position(2,1),Position(3,1)],
        }
#
#
#
class O_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=2)
        self.occupied_cells = {
            0:[Position(0,0), Position(0,1),Position(1,0), Position(1,1)],
            1:[Position(0,0), Position(0,1),Position(1,0), Position(1,1)],
            2:[Position(0,0), Position(0,1),Position(1,0), Position(1,1)],
            3:[Position(0,0), Position(0,1),Position(1,0), Position(1,1)],
        }
#
#
#
class T_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=3)
        self.occupied_cells = {
            0:[Position(0,1), Position(1,0),Position(1,1), Position(1,2)],
            1:[Position(0,1), Position(1,1),Position(1,2), Position(2,1)],
            2:[Position(1,0), Position(1,1),Position(1,2), Position(2,1)],
            3:[Position(0,1), Position(1,0),Position(1,1), Position(2,1)],
        }
#
#
#
class S_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=4)
        self.occupied_cells = {
            0:[Position(0,1), Position(0,2),Position(1,0), Position(1,1)],
            1:[Position(0,1), Position(1,1),Position(1,2), Position(2,2)],
            2:[Position(1,1), Position(1,2),Position(2,0), Position(2,1)],
            3:[Position(0,0), Position(1,0),Position(1,1), Position(2,1)],
        }
#
#
#
class Z_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=5)
        self.occupied_cells = {
            0:[Position(0,0), Position(0,1),Position(1,1), Position(1,2)],
            1:[Position(0,2), Position(1,1),Position(1,2), Position(2,1)],
            2:[Position(1,0), Position(1,1),Position(2,1), Position(2,2)],
            3:[Position(0,1), Position(1,0),Position(1,1), Position(2,0)],
        }
#
#
#
class J_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=6)
        self.occupied_cells = {
            0:[Position(0,0), Position(1,0),Position(1,1), Position(1,2)],
            1:[Position(0,1), Position(0,2),Position(1,1), Position(2,1)],
            2:[Position(1,0), Position(1,1),Position(1,2), Position(2,2)],
            3:[Position(0,1), Position(1,1),Position(2,0), Position(2,1)],
        }



class L_Tet(Tetrimino):
    def __init__(self):
        super().__init__(shape=7)
        self.occupied_cells = {
            0:[Position(0,2), Position(1,0),Position(1,1), Position(1,2)],
            1:[Position(0,1), Position(1,1),Position(2,1), Position(2,2)],
            2:[Position(1,0), Position(1,1),Position(1,2), Position(2,0)],
            3:[Position(0,0), Position(0,1),Position(1,1), Position(2,1)]
        }
