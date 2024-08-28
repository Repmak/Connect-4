import pyglet
from pyglet import shapes
from pyglet.window import key
from backend import gamelogic


class connect4window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gamelogic = gamelogic(True)
        self.token = shapes.Circle(x=70, y=655, radius=40, color=(255, 54, 54))
        self.isplayerturn = True  # Flag to indicate if it's the player's turn.

    def on_draw(self):
        self.clear()  # Clears the GUI.
        self.drawgrid()
        self.drawtokens()
        self.token.draw()
        self.drawmoves()
        self.drawcurrentmove()
        if self.gamelogic.gamestate != 0:
            self.drawwinner()

    def drawgrid(self):
        keyboardbinds = pyglet.text.Label(text='A: move left   S: drop token   D: move right   ENTER: restart game', font_name='microsoft yi baiti', font_size=20, color=(110, 110, 110, 255), x=20, y=730)
        keyboardbinds.draw()
        backgroundgridrectangle = shapes.Rectangle(x=20, y=20, width=670, height=575, color=(200, 200, 200))
        backgroundgridrectangle.draw()
        for xpos in range(7):
            if xpos != 0:
                shapes.Rectangle(x=xpos * 95 + 20, y=20, width=5, height=575, color=(110, 110, 110)).draw()
            for ypos in range(6):
                if ypos != 0:
                    shapes.Rectangle(x=20, y=ypos * 95 + 20, width=670, height=5, color=(110, 110, 110)).draw()

    def drawtokens(self):
        self.token.x = self.gamelogic.tokencurrentposition * 95 + 70
        for xpos in range(7):
            for ypos in range(6):
                colour = (110, 110, 110)
                if self.gamelogic.board[ypos][xpos] == 1:
                    colour = (255, 54, 54)
                elif self.gamelogic.board[ypos][xpos] == 2:
                    colour = (235, 222, 52)
                shapes.Circle(x=xpos * 95 + 70, y=(5 - ypos) * 95 + 70, radius=40, color=colour).draw()

    def drawcurrentmove(self):
        if self.isplayerturn and self.gamelogic.gamestate == 0:
            pyglet.text.Label(text='Your move...', font_name='microsoft yi baiti', font_size=20, italic=True, color=(247, 40, 40, 255), x=710, y=730).draw()
        elif not self.isplayerturn and self.gamelogic.gamestate == 0:
            pyglet.text.Label(text='Opponent is thinking...', font_name='microsoft yi baiti', font_size=20, italic=True, color=(255, 230, 0, 255), x=710, y=730).draw()

    def drawmoves(self):
        backgroundmovesrectangle = shapes.Rectangle(x=710, y=20, width=450, height=680, color=(200, 200, 200))
        backgroundmovesrectangle.draw()
        if self.gamelogic.movenum < 14:
            text = 'Player starts' if self.gamelogic.playerstart else 'AI starts'
            colour = (247, 40, 40, 255) if self.gamelogic.playerstart else (255, 230, 0, 255)
            pyglet.text.Label(text=text, font_name='microsoft yi baiti', font_size=25, color=colour, x=730, y=650).draw()
        for i, move in enumerate(self.gamelogic.moves):
            ypos = (650 - 40 * (i + 1)) if self.gamelogic.movenum < 14 else (650 - 40 * i)
            playerorai = 'Player' if move[2] == 1 else 'AI'
            movenumlabel = pyglet.text.Label(text=f'Move #{move[3]} ({playerorai}):', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=730, y=ypos)
            movenumlabel.draw()
            moveinfo = pyglet.text.Label(text=f'({move[0]}, {move[1]})', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=1050, y=ypos)
            moveinfo.draw()

    def drawwinner(self):
        if self.gamelogic.gamestate == 1:
            winlabel = pyglet.text.Label(text='Player wins!', font_name='microsoft yi baiti', font_size=35, bold=True, color=(247, 40, 40, 255), x=730, y=50)
        elif self.gamelogic.gamestate == 2:
            winlabel = pyglet.text.Label(text='AI wins!', font_name='microsoft yi baiti', font_size=35, bold=True, color=(255, 230, 0, 255), x=730, y=50)
        else:
            winlabel = pyglet.text.Label(text='This round is a draw.', font_name='microsoft yi baiti', font_size=35, bold=True, color=(110, 110, 110, 255), x=730, y=50)
        winlabel.draw()

    def on_key_press(self, symbol, modifiers):
        if (symbol == key.D or symbol == key.RIGHT) and self.gamelogic.gamestate == 0:
            self.gamelogic.movetoken(1)
        elif (symbol == key.A or symbol == key.LEFT) and self.gamelogic.gamestate == 0:
            self.gamelogic.movetoken(-1)
        elif (symbol == key.S or symbol == key.DOWN) and self.gamelogic.gamestate == 0:
            self.gamelogic.movenum += 1
            self.gamelogic.drop_token(self.gamelogic.tokencurrentposition, 1)
            if self.gamelogic.movenum != 42:
                self.isplayerturn = False  # Switch to AI turn.
        elif symbol == key.RETURN:
            self.gamelogic.reset_game()
            self.isplayerturn = True

    def update(self, dt):
        if not self.isplayerturn and self.gamelogic.gamestate == 0:
            self.isplayerturn = True  # Switch back to player's turn.
            self.gamelogic.movenum += 1
            print(self.gamelogic.movenum)
            self.gamelogic.aiturn()  # Run AI turn.


if __name__ == '__main__':
    window = connect4window(width=1180, height=760, caption='Connect 4', resizable=False)
    window.set_icon(pyglet.resource.image("icon.png"))
    pyglet.gl.glClearColor(0.95, 0.95, 0.95, 1)
    pyglet.clock.schedule_interval(window.update, 1/30)
    pyglet.app.run()
