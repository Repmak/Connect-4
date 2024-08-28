# THIS ALGORITHM ASSUMES AI HAS THE FIRST MOVE.
# THIS ALGORITHM FINDS THE BEST MOVE BY CHECKING THE NEXT POSSIBLE TURNS.

class minimaxlogic:
    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 2, 2, 0],
                      [0, 0, 0, 2, 2, 1, 0],
                      [0, 1, 2, 1, 1, 1, 0]]  # Current board with tokens.
        self.turns = '2334454551'  # Tracks moves made by AI and player.

    def rowof4(self, board, col, colincrement, row, rowincrement):
        counter = 0
        while 0 <= col <= 6 and 0 <= row <= 5:
            if board[row][col] != 2:
                break
            counter += 1
            col += colincrement
            row += rowincrement
        return counter


    def calculatescores(self, board, col, row):
        score = 0
        # Checks if a row of 4 successive tokens has been found.
        rowcount = self.rowof4(board, col, 1, row, 0) + self.rowof4(board, col, -1, row, 0) - 1
        # Checks if a column of 4 successive tokens has been found.
        colcount = self.rowof4(board, col, 0, row, 1) + self.rowof4(board, col, 0, row, -1) - 1
        # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        posdiagcount = self.rowof4(board, col, 1, row, -1) + self.rowof4(board, col, -1, row, 1) - 1
        # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        negdiagcount = self.rowof4(board, col, -1, row, -1) + self.rowof4(board, col, 1, row, 1) - 1
        # Returns False if 4 consecutive tokens were found, otherwise returns True.
        if rowcount >= 4:
            score += 1
        if colcount >= 4:
            score += 1
        if posdiagcount >= 4:
            score += 1
        if negdiagcount >= 4:
            score += 1
        return score

    def checkcolumns(self):
        possiblecolumns = {}
        for col in range(7):
            if self.turns.count(str(col)) <= 6:
                possiblecolumns[col] = 0  # Assigns a score of 0. This will be used to store the score, which will be updated later.
        return possiblecolumns

    def simulatefutureturn(self, col):
        futureturns = self.turns
        futureturns += str(col)

        futureboard = [row[:] for row in self.board]  # futureboard copied by value.
        futureboard[6-futureturns.count(str(col))][col] = 2

        return futureboard, futureturns

    def aiturn(self):
        scoredict = self.checkcolumns()
        bestscore = 0
        bestmove = None
        for col in scoredict:
            futureboard, futureturns = self.simulatefutureturn(col)
            row = 6 - futureturns.count(str(col))
            print(col, row)

            score = self.calculatescores(futureboard, col, row)
            print('Score: ' + str(score))

            if score > bestscore:
                bestscore = score
                bestmove = futureturns
            print(futureturns)
            for row in futureboard:
                print(row)

            print('---------------------')
        return bestscore, bestmove


instance = minimaxlogic()
print('Next best move: ' + str(instance.aiturn()))
