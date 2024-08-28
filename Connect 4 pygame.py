import pygame
import sys


class Token:
    def __init__(self, position):
        self.position = pygame.Vector2(position)

    def draw(self, surface):
        pygame.draw.circle(surface, 'red', self.position, 45)

    def move(self, newposition):
        print(self.position)
        self.position.x = newposition * 120 + 70


class Connect4:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 850))
        self.clock = pygame.time.Clock()
        self.screen.fill("grey")
        self.board = [[], [], [], [], [], [], []]
        self.gameover = False
        self.currentposition = 0
        self.initialboard()
        #self.tokenobject = Token((self.currentposition * 120 + 70, 60))
        self.tokenobject = Token((70, 60))

    def initialboard(self):
        pygame.draw.rect(self.screen, 'blue', (10, 120, 840, 720))
        for column in range(7):
            for row in range(6):
                pygame.draw.circle(self.screen, 'grey', (int(column * 120 + 140 / 2), int(row * 120 + 360 / 2)), 45)

    def selectcolumn(self):  # INCREMENTS TOKEN TO THE NEXT COLUMN TO THE RIGHT.
        self.currentposition = self.currentposition + 1
        if self.currentposition >= 7:
            self.currentposition = 0
        self.checkcolumn()
        pygame.display.flip()
        self.tokenobject.move(self.currentposition)  # MOVES TOKEN BY ONE POSITION TO THE RIGHT.

    def checkcolumn(self):  # ENSURES THERE IS AT LEAST ONE FREE SPACE IN THE COLUMN.
        if len(self.board[self.currentposition]) == 6:
            self.selectcolumn()

    def droptoken(self):
        self.board[self.currentposition].append(1)
        print(self.board)
        pygame.draw.circle(self.screen, 'red', (int(self.currentposition * 120 + 140 / 2), 940 - int(len(self.board[self.currentposition]) * 120 + 80 / 2)), 45)
        #self.aimove(self)
        self.checkcolumn()

    def aimove(self):
        pass

    def update(self):
        self.clock.tick(60)
        pygame.display.update()

    def checkevents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # optimise this bit dunno if u need two if statements
                    self.droptoken()
            if event.type == pygame.KEYDOWN and self.gameover == False:
                if event.key == pygame.K_w:
                    self.selectcolumn()

    def run(self):
        while True:
            self.checkevents()
            self.update()
            self.tokenobject.draw(self.screen)


if __name__ == '__main__':
    pygame.init()
    game = Connect4()
    game.run()
