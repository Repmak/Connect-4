import random


class gamelogic:
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.turns = ''
        self.moves = []
        self.movenum = 0
        self.gamestate = True
        self.tokencurrentposition = 0
        self.maxdepth = 5

    # PLAYER LOGIC.

    def movetoken(self, operation):
        self.tokencurrentposition = (self.tokencurrentposition + operation) % 7
        if str(self.turns).count(str(self.tokencurrentposition)) >= 6:  # Checks that the column is not full.
            self.movetoken(operation)

    def reset_game(self):
        self.__init__()  # Resets self.board, self.turns, self.moves, self.gamestate and self.tokencurrentposition to their original values.

    # AI LOGIC.

    def aiturn(self):
        depth = 0
        score = 0
        scoredict = self.simulateaifutureturn(self.turns, self.board, depth, score)
        print('-----------------------------------------------------------------------------------------\n\n')
        print(scoredict)
        try:  # Failsafe if no moves are generated (used when the board is nearly full).
            temp = max(scoredict.values())
            bestmoves = [key for key in scoredict if scoredict[key] == temp]  # Finds all the best turns.
            print("Keys with maximum values are : " + str(bestmoves))
            move = random.choice(bestmoves)
            print(move)
            self.drop_token(int(move[self.movenum]), 2)
        except:
            print('ERROR ENCOUNTERED. RANDOM POSITION CHOSEN.')
            move = random.choice(self.checkcolumns(self.turns))
            self.drop_token(move, 2)

    def checkcolumns(self, turns):
        possiblecolumns = []
        for col in range(7):
            if str(turns).count(str(col)) < 6:
                possiblecolumns.append(col)
        return possiblecolumns

    def simulateplayerfutureturn(self, turns, board, depth, score):
        print(str(depth) + '  **********************   PLAYER   **********************')
        scoredict = {}
        depth += 1
        bestplayerscore = 0
        arrayplayerturns = []
        possiblenextturns = self.checkcolumns(turns)
        if possiblenextturns:
            for nextturn in possiblenextturns:
                futureturns = turns + str(nextturn)  # Concatenate turns with the newest turn.
                print('------------------------')
                print(futureturns)
                tempboard = [row[:] for row in board]  # board copied by value.
                newboard, col, row = self.fillboard(futureturns, tempboard)  # newboard is a board will all tokens matching futureturns.
                newscore, aiwinguarantee = self.evaluatescore(futureturns, newboard, int(col), int(row), depth)  # Checks score of the latest turn made.
                newscore += score
                arrayplayerturns.append([futureturns, newboard, newscore])
                if newscore <= bestplayerscore:
                    bestplayerscore = newscore
                print(newscore)

            for playerturn in arrayplayerturns:
                if playerturn[2] == bestplayerscore:
                    print(playerturn)
                    scoredict.update(self.simulateaifutureturn(playerturn[0], playerturn[1], depth, bestplayerscore))  # Concatenates two dictionaries together.
        else:
            self.maxdepth -= depth

        return scoredict

    def simulateaifutureturn(self, turns, board, depth, score):
        scoredict = {}
        depth += 1
        print(str(depth) + '  **********************   AI   **********************')
        possiblenextturns = self.checkcolumns(turns)
        if possiblenextturns:
            for nextturn in possiblenextturns:
                futureturns = turns + str(nextturn)  # Concatenate turns with the newest turn.
                print('------------------------')
                print(futureturns)
                tempboard = [row[:] for row in board]  # board copied by value.
                newboard, col, row = self.fillboard(futureturns, tempboard)  # newboard is a board will all tokens matching futureturns.
                newscore, aiwinguarantee = self.evaluatescore(futureturns, newboard, int(col), int(row), depth)  # Checks score of the latest turn made.
                newscore += score
                print(newscore)
                if aiwinguarantee:
                    scoredict = {futureturns: newscore}
                    return scoredict
                elif depth < self.maxdepth:
                    scoredict.update(self.simulateplayerfutureturn(futureturns, newboard, depth, newscore))  # Concatenates two dictionaries together.
                else:
                    scoredict[futureturns] = newscore
        else:
            self.maxdepth -= depth

        return scoredict

    def fillboard(self, turns, board):
        rowposition = 6 - str(turns).count(str(turns[-1]))  # Checks what row index the token gets dropped in.
        if len(turns) % 2 == 1:
            board[rowposition][int(turns[-1])] = 1  # Adds player token to board.
        else:
            board[rowposition][int(turns[-1])] = 2  # Adds AI token to board.
        return board, turns[-1], rowposition  # Returns last move and which row it was placed in.

    def evaluatescore(self, turns, board, col, row, depth):
        aiwinguarantee = False
        if len(turns) % 2 == 0:  # Maximise score.
            playerorai = 2
            bonusscore = 100
        else:  # Minimise score.
            playerorai = 1
            bonusscore = 1000

        # Checks if a row of 4 successive tokens has been found.
        rowcount = self.checkif4inrow(board, col, 1, row, 0, playerorai) + self.checkif4inrow(board, col, -1, row, 0, playerorai) - 1
        # Checks if a column of 4 successive tokens has been found.
        colcount = self.checkif4inrow(board, col, 0, row, 1, playerorai) + self.checkif4inrow(board, col, 0, row, -1, playerorai) - 1
        # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        posdiagcount = self.checkif4inrow(board, col, 1, row, -1, playerorai) + self.checkif4inrow(board, col, -1, row, 1, playerorai) - 1
        # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        negdiagcount = self.checkif4inrow(board, col, -1, row, -1, playerorai) + self.checkif4inrow(board, col, 1, row, 1, playerorai) - 1
        score = rowcount + colcount + posdiagcount + negdiagcount
        if (rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4) and depth == 1:
            aiwinguarantee = True
        if rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4:
            score += bonusscore
        for row in board:
            print(row)
        if playerorai == 2:
            return score, aiwinguarantee
        else:
            return -3 * score, aiwinguarantee

    # PLAYER AND AI LOGIC.

    def record_move(self, col, row, playerorai):
        self.moves.append((col + 1, 6 - row, playerorai, len(self.turns)))
        if len(self.moves) > 14:
            self.moves.pop(0)

    def drop_token(self, col, playerorai):
        row = 5 - self.turns.count(str(col))  # Checks what row index the token gets dropped in.
        self.board[row][col] = playerorai
        self.turns = self.turns + str(col)
        self.record_move(col, row, playerorai)
        self.movenum += 1
        if self.tokencurrentposition == col and row == 0:  # Moves player token automatically if the column becomes full.
            self.movetoken(1)
        self.gamestate = self.is_game_over(col, row, playerorai)

    def checkif4inrow(self, board, col, colincrement, row, rowincrement, playerorai):
        counter = 0
        while 0 <= col <= 6 and 0 <= row <= 5:
            if board[row][col] != playerorai:
                break
            counter += 1
            col += colincrement
            row += rowincrement
        return counter

    def is_game_over(self, col, row, playerorai):
        # Checks if a row of 4 successive tokens has been found.
        rowcount = self.checkif4inrow(self.board, col, 1, row, 0, playerorai) + self.checkif4inrow(self.board, col, -1, row, 0, playerorai) - 1
        # Checks if a column of 4 successive tokens has been found.
        colcount = self.checkif4inrow(self.board, col, 0, row, 1, playerorai) + self.checkif4inrow(self.board, col, 0, row, -1, playerorai) - 1
        # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        posdiagcount = self.checkif4inrow(self.board, col, 1, row, -1, playerorai) + self.checkif4inrow(self.board, col, -1, row, 1, playerorai) - 1
        # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        negdiagcount = self.checkif4inrow(self.board, col, -1, row, -1, playerorai) + self.checkif4inrow(self.board, col, 1, row, 1, playerorai) - 1
        # Returns False if 4 consecutive tokens were found, otherwise returns True.

        return not (rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4)
