# THIS ALGORITHM ASSUMES PLAYER HAS THE FIRST MOVE.
# THIS ALGORITHM OUTPUTS ALL VALID TURNS FROM THE CURRENT TURN.
# EACH TURN IS MAXIMISED FOR AI TURNS AND MINIMISED FOR PLAYER TURNS.
# THE SCORE IS UPDATED AT EVERY NEW TURN SIMULATED, RATHER THAN BEING GENERATED AT THE END OF EACH POSSIBLE BRANCH.

class minimaxlogic:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 0, 0],
                      [0, 1, 2, 2, 2, 0, 0]]  # Current board with tokens.
        self.turns = '334421'  # Tracks moves made by AI and player.
        self.maxdepth = 5

    def checkcolumns(self, turns):
        possiblecolumns = []
        for col in range(7):
            if str(turns).count(str(col)) < 6:
                possiblecolumns.append(col)
        return possiblecolumns

    def simulatefutureturn(self, turns, board, depth, score):
        scoredict = {}
        depth += 1
        for nextturn in self.checkcolumns(turns):
            futureturns = turns + str(nextturn)  # Concatenate turns with the newest turn.
            tempboard = [row[:] for row in board]  # board copied by value.
            newboard, col, row = self.fillboard(futureturns, tempboard)  # newboard is a board will all tokens matching futureturns.
            newscore = self.evaluatescore(futureturns, newboard, int(col), int(row)) + score  # Checks score of the latest turn made.
            if depth < self.maxdepth:
                scoredict.update(self.simulatefutureturn(futureturns, newboard, depth, newscore))  # Concatenates two dictionaries together.
            else:
                scoredict[futureturns] = newscore

        return scoredict

    def fillboard(self, turns, board):
        rowposition = 6 - str(turns).count(str(turns[-1]))  # Checks what row index the token gets dropped in.
        if len(turns) % 2 == 1:
            board[rowposition][int(turns[-1])] = 1  # Adds player token to board.
        else:
            board[rowposition][int(turns[-1])] = 2  # Adds AI token to board.
        return board, turns[-1], rowposition  # Returns last move and which row it was placed in.

    def evaluatescore(self, turns, board, col, row):
        if len(turns) % 2 == 1:  # Minimise score.
            playerorai = 1
        else:  # Maximise score.
            playerorai = 2

        # Checks if a row of 4 successive tokens has been found.
        rowcount = self.checkif4inrow(board, col, 1, row, 0, playerorai) + self.checkif4inrow(board, col, -1, row, 0, playerorai) - 1
        # Checks if a column of 4 successive tokens has been found.
        colcount = self.checkif4inrow(board, col, 0, row, 1, playerorai) + self.checkif4inrow(board, col, 0, row, -1, playerorai) - 1
        # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        posdiagcount = self.checkif4inrow(board, col, 1, row, -1, playerorai) + self.checkif4inrow(board, col, -1, row, 1, playerorai) - 1
        # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        negdiagcount = self.checkif4inrow(board, col, -1, row, -1, playerorai) + self.checkif4inrow(board, col, 1, row, 1, playerorai) - 1
        score = rowcount + colcount + posdiagcount + negdiagcount

        return score if playerorai == 2 else -score

    def checkif4inrow(self, board, col, colincrement, row, rowincrement, playerorai):
        counter = 0
        while 0 <= col <= 6 and 0 <= row <= 5:
            if board[row][col] != playerorai:
                break
            counter += 1
            col += colincrement
            row += rowincrement
        return counter

    def aiturn(self):
        depth = 0
        score = 0
        scoredict = self.simulatefutureturn(self.turns, self.board, depth, score)

        #best_column = max(scoredict, key=scoredict.get)

        temp = max(scoredict.values())
        res = [key for key in scoredict if scoredict[key] == temp]  # Finds all the best turns.
        print("Keys with maximum values are : " + str(res))


instance = minimaxlogic()
instance.aiturn()
