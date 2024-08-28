import pyglet
from pyglet import shapes
from pyglet.window import key
from backend import gamelogic


class connect4window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gamelogic = gamelogic()
        self.token = shapes.Circle(x=70, y=655, radius=40, color=(255, 45, 63))

    def on_draw(self):
        self.clear()
        self.drawgrid()
        self.drawtokens()
        self.token.draw()
        self.drawmoves()
        if not self.gamelogic.gamestate:
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
        for xpos in range(7):
            for ypos in range(6):
                color = (110, 110, 110)
                if self.gamelogic.board[ypos][xpos] == 1:
                    color = (255, 45, 63)
                elif self.gamelogic.board[ypos][xpos] == 2:
                    color = (255, 239, 81)
                shapes.Circle(x=xpos * 95 + 70, y=(5 - ypos) * 95 + 70, radius=40, color=color).draw()

    def drawmoves(self):
        backgroundmovesrectangle = shapes.Rectangle(x=710, y=20, width=450, height=680, color=(200, 200, 200))
        backgroundmovesrectangle.draw()
        for i, move in enumerate(self.gamelogic.moves):
            player = 'Player' if move[2] == 1 else 'AI'
            movenumlabel = pyglet.text.Label(text=f'Move #{move[3]} ({player}):', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=730, y=650 - 40 * i)
            movenumlabel.draw()
            moveinfo = pyglet.text.Label(f'({move[0]}, {move[1]})', font_name='microsoft yi baiti', font_size=25, color=(110, 110, 110, 255), x=1050, y=650 - 40 * i)
            moveinfo.draw()

    def drawwinner(self):
        if self.gamelogic.moves[-1][2] == 1:
            winlabel = pyglet.text.Label(text='Player wins', font_name='microsoft yi baiti', font_size=35, color=(255, 45, 63, 255), x=730, y=50)
        else:
            winlabel = pyglet.text.Label(text='AI wins', font_name='microsoft yi baiti', font_size=35, color=(255, 239, 81, 255), x=730, y=50)
        winlabel.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.D and self.gamelogic.gamestate:
            self.gamelogic.movetoken(1)
        elif symbol == key.A and self.gamelogic.gamestate:
            self.gamelogic.movetoken(-1)
        elif symbol == key.S and self.gamelogic.gamestate:
            self.gamelogic.drop_token(self.gamelogic.tokencurrentposition, 1)
            if self.gamelogic.gamestate:  # Runs AI if game is still running.
                self.gamelogic.aiturn()

        elif symbol == key.RETURN:
            self.gamelogic.reset_game()

        self.token.x = self.gamelogic.tokencurrentposition * 95 + 70

    def update(self, dt):
        pass


if __name__ == '__main__':
    window = connect4window(width=1180, height=760, caption='Connect 4', resizable=False)
    pyglet.gl.glClearColor(0.95, 0.95, 0.95, 1)
    pyglet.clock.schedule_interval(window.update, 1 / 60)
    pyglet.app.run()
