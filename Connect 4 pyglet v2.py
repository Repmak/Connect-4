import pyglet
from pyglet import shapes
from pyglet.window import key
from pyglet.gl import *
import random


class Connect4(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]  # self.board is used to store the positions of tokens on the board.
        self.token = shapes.Circle(x=70, y=655, radius=40, color=(255, 45, 63))  # Token at top of grid.
        self.tokencurrentposition = 0  # Keeps track of the current position of the token at the top of the grid.
        self.gamestate = True  # True means that the game is still running, False means the game is over.
        self.moves = []  # Records all the moves made by the player and the AI.
        self.movenum = 0  # Records the current move number. It is incremented after every move.

    def on_draw(self):
        self.clear()  # Clears the previous frame.

        # Keyboard binds.
        keyboardbinds = pyglet.text.Label(text='A: move left   S: drop token   B: move right   ENTER: restart game', font_name='microsoft yi baiti', font_size=20, color=(110, 110, 110, 255), x=20, y=730)
        keyboardbinds.draw()

        # Background grid rectangle.
        backgroundgridrectangle = shapes.Rectangle(x=20, y=20, width=670, height=575, color=(200, 200, 200))
        backgroundgridrectangle.draw()

        # Grid, tokens and lines.
        for xpos in range(7):
            # Vertical lines.
            if xpos != 0:  # Doesn't draw the first line (since it's part of the border).
                xgrid = shapes.Rectangle(x=xpos * 95 + 20, y=20, width=5, height=575, color=(110, 110, 110))
                xgrid.draw()
            for ypos in range(6):
                # Horizontal lines.
                if ypos != 0:  # Doesn't draw the first line (since it's part of the border).
                    ygrid = shapes.Rectangle(x=20, y=ypos * 95 + 20, width=670, height=5, color=(110, 110, 110))
                    ygrid.draw()
                # Tokens that are drawn in the grid.
                if self.board[ypos][xpos] == 1:
                    tokensingrid = shapes.Circle(x=xpos * 95 + 70, y=(5 - ypos) * 95 + 70, radius=40, color=(255, 45, 63))  # Player's token.
                elif self.board[ypos][xpos] == 2:
                    tokensingrid = shapes.Circle(x=xpos * 95 + 70, y=(5 - ypos) * 95 + 70, radius=40, color=(255, 239, 81))  # AI's token.
                else:
                    tokensingrid = shapes.Circle(x=xpos * 95 + 70, y=(5 - ypos) * 95 + 70, radius=40, color=(110, 110, 110))  # Empty slot.
                tokensingrid.draw()

        # Token at the top of the grid.
        self.token.draw()

        # Recorded moves made by player and AI.
        backgroundmovesrectangle = shapes.Rectangle(x=710, y=20, width=450, height=680, color=(200, 200, 200))
        backgroundmovesrectangle.draw()
        for i in range(len(self.moves)):
            if self.moves[i][2] == 1:
                movenumlabel = pyglet.text.Label(text=f'Move #{self.moves[i][3]} (Player):', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=730, y=650-40*i)
            else:
                movenumlabel = pyglet.text.Label(text=f'Move #{self.moves[i][3]} (AI):', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=730, y=650-40*i)
            movenumlabel.draw()
            moveinfo = pyglet.text.Label(f'({self.moves[i][0]}, {self.moves[i][1]})', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=1050, y=650-40*i)
            moveinfo.draw()

        # Player/AI wins.
        if not self.gamestate:
            if 1 == self.moves[-1][2]:
                winlabel = pyglet.text.Label(text='Player wins', font_name='microsoft yi baiti', font_size=35, color=(255, 45, 63, 255), x=730, y=50)
            else:
                winlabel = pyglet.text.Label(text='AI wins', font_name='microsoft yi baiti', font_size=35, color=(255, 239, 81, 255), x=730, y=50)
            winlabel.draw()

    def recordmove(self, col, row, playerorai):
        self.moves.append((col+1, 6-row, playerorai, self.movenum))  # Records the moves made by the player and the AI.
        if len(self.moves) > 14:
            self.moves.pop(0)

    def checkrow(self, row, playerorai):
        for i in range(0, 4):
            if self.board[row][i] == playerorai and self.board[row][i + 1] == playerorai and self.board[row][i + 2] == playerorai and self.board[row][i + 3] == playerorai:
                return False
        return True

    def checkcol(self, col, playerorai):
        for i in range(0, 3):
            if self.board[i][col] == playerorai and self.board[i + 1][col] == playerorai and self.board[i + 2][col] == playerorai and self.board[i + 3][col] == playerorai:
                return False
        return True

    def findnewpoints(self, col, row, limit1, limit2, limit3, limit4, operation1, operation2, playerorai):
        diagonallinearray = [(col, row)]
        tempcol = col
        temprow = row
        while limit1 < temprow < limit2 and limit3 < tempcol < limit4:
            tempcol = tempcol + operation1
            temprow = temprow + operation2
            if self.board[temprow][tempcol] == playerorai:
                diagonallinearray.append((tempcol, temprow))
            else:
                break
        return diagonallinearray

    def checkdiag(self, col, row, limits, incrementordecrement, playerorai):
        diagonalpointsarray1 = self.findnewpoints(col, row, limits[0], limits[1], limits[2], limits[3], incrementordecrement[0], incrementordecrement[1], playerorai)
        diagonalpointsarray2 = self.findnewpoints(col, row, limits[4], limits[5], limits[6], limits[7], incrementordecrement[2], incrementordecrement[3], playerorai)
        diagonalpointsarray = list(set(diagonalpointsarray1 + diagonalpointsarray2))
        if len(diagonalpointsarray) >= 4:
            return False
        else:
            return True

    def isgameover(self, col, row, playerorai):  # Every time a play is made, the most recently added token is checked to see whether a row/column/diagonal of 4 is made.
        rowstate = self.checkrow(row, playerorai)  # Checking if there are 4 tokens in a row in the specified row.
        colstate = self.checkcol(col, playerorai)  # Checking if there are 4 tokens in a row in the specified column.
        # Checking diagonal (+ve gradient).
        positivediagstate = self.checkdiag(col, row, [0, 6, -1, 6, -1, 5, 0, 7], [1, -1, -1, 1], playerorai)
        # Checking diagonal (-ve gradient).
        negativediagstate = self.checkdiag(col, row, [-1, 5, -1, 6, 0, 6, 0, 7], [1, 1, -1, -1], playerorai)
        if not rowstate or not colstate or not positivediagstate or not negativediagstate:
            return False
        return True

    def aimove(self):
        aimove = random.randint(0, 6)
        nexttokenposition = None
        i = 5
        while i >= 0 and nexttokenposition is None:  # Checks if there is an empty slot in the grid.
            if self.board[i][aimove] == 0:
                nexttokenposition = i
            i -= 1
        self.board[nexttokenposition][aimove] = 2
        self.movenum += 1
        self.recordmove(aimove, nexttokenposition, 2)
        self.gamestate = self.isgameover(aimove, nexttokenposition, 2)  # Checks if the game is over.

    def iscolumnfull(self, symbol):  # Ensures that the sub array self.board[self.tokencurrentposition] is not empty. If empty, the token will be moved as required.
        nexttokenposition = None
        i = 5
        while i >= 0 and nexttokenposition is None:  # Checks if there is an empty slot in the grid.
            if self.board[i][self.tokencurrentposition] == 0:
                nexttokenposition = i
            i -= 1
        if nexttokenposition is None and symbol == 100:  # 100 is the symbol for the key D.
            self.on_key_press(symbol, 0)
        if nexttokenposition is None and symbol == 97:  # 97 is the symbol for the key A.
            self.on_key_press(symbol, 0)

    def movetoken(self, symbol):
        self.iscolumnfull(symbol)  # Checks that there is still space in the column selected.
        self.token.x = self.tokencurrentposition * 95 + 70

    def droptoken(self):
        nexttokenposition = None
        i = 5
        while i >= 0 and nexttokenposition is None:  # Finds the next empty slot in a column.
            if self.board[i][self.tokencurrentposition] == 0:
                nexttokenposition = i
            i -= 1
        self.board[nexttokenposition][self.tokencurrentposition] = 1
        self.movenum += 1
        self.recordmove(self.tokencurrentposition, nexttokenposition, 1)
        self.gamestate = self.isgameover(self.tokencurrentposition, nexttokenposition, 1)  # Checks if the game is over.
        if self.gamestate:  # gamestate is True, game continues.
            if nexttokenposition == 0:
                self.on_key_press(100, 0)  # Automatically moves the position of the token over to the right to ensure that the token is not above a full column.
            self.aimove()  # AI's turn.

    def resetgame(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]  # self.board is used to store the positions of tokens on the board.

    def on_key_press(self, symbol, modifiers):
        if self.gamestate:
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
                self.droptoken()
        if symbol == key.RETURN:
            self.resetgame()
            self.tokencurrentposition = 0
            self.gamestate = True
            self.moves = []
            self.movenum = 0
            self.token.x = 70

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = Connect4(width=1180, height=760, caption='Connect 4', resizable=False)
    pyglet.gl.glClearColor(0.95, 0.95, 0.95, 1)
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
