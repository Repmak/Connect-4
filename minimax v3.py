# THIS ALGORITHM ASSUMES AI HAS THE FIRST MOVE.
# THIS ALGORITHM OUTPUTS ALL VALID TURNS FROM THE CURRENT.
# THIS SCORE IS ONLY MAXIMISED FOR THE AI.

class minimaxlogic:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0],
                      [0, 1, 2, 2, 2, 0, 0]]  # Current board with tokens.
        self.turns = '334421'  # Tracks moves made by AI and player.
        self.maxdepth = 3  # USE ODD NUMBERS FOR NOW. OTHERWISE THE ALGORITHM WILL MAXIMISE PLAYER SCORE.

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
                scoredict[futureturns] = self.evaluatescore(futureturns)
            elif depth < self.maxdepth:
                scoredict.update(self.simulatefutureturn(futureturns, depth))  # Concatenates two dictionaries together.
        return scoredict

    def checkif4inrow(self, board, col, colincrement, row, rowincrement):
        counter = 0
        while 0 <= col <= 6 and 0 <= row <= 5:
            if board[row][col] != 2:
                break
            counter += 1
            col += colincrement
            row += rowincrement
        return counter

    def findavailablerow(self, board, turntoadd):
        rowposition = None
        i = 5
        while i >= 0 and rowposition is None:  # Checks if there is an empty slot in the grid.
            if board[i][int(turntoadd)] == 0:
                rowposition = i
            i -= 1
        return rowposition

    def evaluatescore(self, turns):
        board = [row[:] for row in self.board]  # self.board copied by value.
        for i in range(self.maxdepth, 0, -1):
            turntoadd = turns[-i]  # Finds the turn to add to the board.
            rowposition = self.findavailablerow(board, turntoadd)
            row = rowposition
            if (len(turns)-i) % 2 == 1:
                board[rowposition][int(turntoadd)] = 1  # Adds player token to board.
            else:
                board[rowposition][int(turntoadd)] = 2  # Adds AI token to board.

        col = int(turns[-1])
        row = int(row)

        # Checks if a row of 4 successive tokens has been found.
        rowcount = self.checkif4inrow(board, col, 1, row, 0) + self.checkif4inrow(board, col, -1, row, 0) - 1
        # Checks if a column of 4 successive tokens has been found.
        colcount = self.checkif4inrow(board, col, 0, row, 1) + self.checkif4inrow(board, col, 0, row, -1) - 1
        # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        posdiagcount = self.checkif4inrow(board, col, 1, row, -1) + self.checkif4inrow(board, col, -1, row, 1) - 1
        # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        negdiagcount = self.checkif4inrow(board, col, -1, row, -1) + self.checkif4inrow(board, col, 1, row, 1) - 1
        # Returns False if 4 consecutive tokens were found, otherwise returns True.

        score = rowcount + colcount + posdiagcount + negdiagcount
        print(score)
        print(turns)
        for row in board:
            print(row)
        print('------------------------')
        return score

    def aiturn(self):
        depth = 0
        scoredict = self.simulatefutureturn(self.turns, depth)

        best_column = max(scoredict, key=scoredict.get)
        return best_column


instance = minimaxlogic()
print('Next best move: ' + str(instance.aiturn()))
