import pyglet
from pyglet import shapes
from pyglet.window import key
from pyglet.gl import *


class Connect4(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.board = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]  # self.board is used to store the positions of tokens on the board.

        self.batch = pyglet.graphics.Batch()  # Used to optimise the process of drawing the board.
        #self.label = pyglet.text.Label('Hello, world!')
        self.token = shapes.Circle(x=70, y=655, radius=40, color=(255, 45, 63))  # Token at top of grid.
        self.tokencurrentposition = 0  # Keeps track of the current position of the token at the top of the grid.
        #self.gamestate = True  # True means that the game is still running, False means the game is over.

    def on_draw(self):
        self.clear()  # Clears the previous frame.
        backgroundrectangle = shapes.Rectangle(x=20, y=20, width=670, height=575, color=(200, 200, 200))  # Background rectangle.
        backgroundrectangle.draw()

        for xpos in range(7):
            # Vertical lines.
            if xpos != 0:  # Doesn't draw the first line (since it's part of the border).
                xgrid = shapes.Rectangle(x=xpos*95+20, y=20, width=5, height=575, color=(110, 110, 110))
                xgrid.draw()
            for ypos in range(6):
                # Horizontal lines.
                if ypos != 0:  # Doesn't draw the first line (since it's part of the border).
                    ygrid = shapes.Rectangle(x=20, y=ypos*95+20, width=670, height=5, color=(110, 110, 110))
                    ygrid.draw()
                # Tokens that are drawn in the grid.
                if self.board[xpos][ypos] == 1:
                    tokensingrid = shapes.Circle(x=xpos * 95 + 70, y=ypos * 95 + 70, radius=40, color=(255, 45, 63))  # Player's token.
                elif self.board[xpos][ypos] == 2:
                    tokensingrid = shapes.Circle(x=xpos * 95 + 70, y=ypos * 95 + 70, radius=40, color=(255, 239, 81))  # AI's token.
                else:
                    tokensingrid = shapes.Circle(x=xpos * 95 + 70, y=ypos * 95 + 70, radius=40, color=(110, 110, 110))  # Empty slot.
                tokensingrid.draw()

        self.token.draw()  # Draws the token at the top of the grid.

    def isgameover(self, tokencolumnindex, tokenrowindex):  # Every time a play is made, the most recently added token is checked to see whether a row/column/diagonal of 4 is made.
        for i in range(0, 4):
            # Checking column.
            if self.board[tokencolumnindex][i] == 1 and self.board[tokencolumnindex][i+1] == 1 and self.board[tokencolumnindex][i+2] == 1 and self.board[tokencolumnindex][i+3] == 1:
                return False
            # Checking row.
            if self.board[tokencolumnindex][tokenrowindex] == 1 and self.board[tokencolumnindex+1][tokenrowindex] == 1 and self.board[tokencolumnindex+2][tokenrowindex] == 1 and self.board[tokencolumnindex+3][tokenrowindex] == 1:
                return False
            # Checking diagonal (+ve gradient).
            if self.board[tokencolumnindex][tokenrowindex] == 1 and self.board[tokencolumnindex][tokenrowindex] == 1 and self.board[tokencolumnindex][tokenrowindex] == 1 and self.board[tokencolumnindex][tokenrowindex] == 1:
                return False
            # Checking diagonal (-ve gradient).
            if True:
                return False
        return True

    def checkcolumn(self, symbol):  # Ensures that the sub array self.board[self.tokencurrentposition] is not empty. If empty, the token will be moved as required.
        if 0 not in self.board[self.tokencurrentposition] and symbol == 100:  # 100 is the symbol for the key D.
            self.on_key_press(symbol, 0)
        elif 0 not in self.board[self.tokencurrentposition] and symbol == 97:  # 97 is the symbol for the key A.
            self.on_key_press(symbol, 0)

    def movetoken(self, symbol):
        self.checkcolumn(symbol)  # Checks that there is still space in the column selected.
        self.token.x = self.tokencurrentposition * 95 + 70

    def on_key_press(self, symbol, modifiers):
        if symbol == key.D:  # Moving token right.
            self.tokencurrentposition += 1
            if self.tokencurrentposition > 6:  # Loops back to start of the board.
                self.tokencurrentposition = 0
            self.movetoken(symbol)  # Moves token by calculating new coordinates.
        if symbol == key.A:  # Moving token left.
            self.tokencurrentposition -= 1
            if self.tokencurrentposition < 0:  # Loops back to end of the board.
                self.tokencurrentposition = 6
            self.movetoken(symbol)  # Moves token by calculating new coordinates.
        if symbol == key.S:  # Dropping token.
            nexttokenindex = self.board[self.tokencurrentposition].index(0)
            self.board[self.tokencurrentposition][nexttokenindex] = 1
            print(str(self.board[0]) + '\n' + str(self.board[1]) + '\n' + str(self.board[2]) + '\n' + str(self.board[3]) + '\n' + str(self.board[4]) + '\n' + str(self.board[5]) + '\n' + str(self.board[6]))
            #gamestate = self.isgameover(self.tokencurrentposition, nexttokenindex)  # Checks if the game is over.
            gamestate = True
            if gamestate:  # gamestate is True, game continues.
                if nexttokenindex == 5:
                    self.on_key_press(100, 0)  # Automatically moves the position of the token over to the right to ensure that the token is not above a full column.
                # todo run AIs turn
                # todo also check that board isnt full
            else:  # gamestate is False, game is over.
                pass

    def update(self, dt):
        pass

    #def on_mouse_motion(self, x, y, dx, dy):
        #print(x, y)


if __name__ == '__main__':
    window = Connect4(width=1280, height=720, caption='Connect 4', resizable=False)
    pyglet.clock.schedule_interval(window.update, 1/60)
    pyglet.app.run()
