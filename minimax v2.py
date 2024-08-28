# THIS ALGORITHM ASSUMES AI HAS THE FIRST MOVE.
# THIS ALGORITHM OUTPUTS ALL VALID TURNS FROM THE CURRENT TURN.

class minimaxlogic:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0],
                      [0, 1, 2, 2, 2, 0, 0]]  # Current board with tokens.
        self.turns = '334421'  # Tracks moves made by AI and player.
        self.maxdepth = 4

    def checkcolumns(self, turns):
        possiblecolumns = []
        for col in range(7):
            if str(turns).count(str(col)) < 6:
                possiblecolumns.append(col)
        return possiblecolumns

    def simulatefutureturn(self, turns, depth):
        scoredict = {}
        possiblenextturns = self.checkcolumns(turns)
        depth += 1
        for nextturn in possiblenextturns:
            futureturns = turns + str(nextturn)
            if len(futureturns) == self.maxdepth + len(self.turns):  # Only adds 'futureturns' to the dictionary if its length is equal to the number of turns in the game so far ('self.turns') + the number of predicted turns ('self.depth').
                scoredict[futureturns] = 0  # Assigns a score of 0 to each turn, these will be changed later when calculating scores.
            elif depth < self.maxdepth:
                scoredict.update(self.simulatefutureturn(futureturns, depth))  # Concatenates two dictionaries together.
        return scoredict

    def aiturn(self):
        depth = 0
        scoredict = self.simulatefutureturn(self.turns, depth)
        print(scoredict)

        best_column = max(scoredict, key=scoredict.get)
        return best_column


instance = minimaxlogic()
print('Next best move: ' + str(instance.aiturn()))
