# ALTER THE STATE OF playerstart IF REQUIRED TO ALTER WHO STARTS.
# THIS ALGORITHM OUTPUTS ALL VALID TURNS FROM THE CURRENT TURN.
# EACH TURN IS MAXIMISED FOR AI TURNS AND MINIMISED FOR PLAYER TURNS.
# THE SCORE IS UPDATED AT EVERY NEW TURN SIMULATED, RATHER THAN BEING GENERATED AT THE END OF EACH POSSIBLE BRANCH.
# ONLY THE BEST SCORE FOR THE PLAYER (MOST NEGATIVE SCORE) IS CONTINUED DOWN THE TREE.
# AN IDENTIFIED WIN WILL STILL PERMIT FUTURE TURNS TO BE GENERATED.
# THIS VERSION HAS ALPHA-BETA PRUNING.

import copy


class gamelogic:
    def __init__(self, playerstart=False):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.turns = '325434254304130141'
        self.movenum = len(self.turns) + 1  # +1 to simulate the increment before calling aiturn method in the code.
        self.gamestate = True
        self.maxdepth = 7
        self.evaluatedboards = []  # This is used to store turns that have already been evaluated (for alpha-beta pruning).
        self.playerstart = playerstart
        self.remainder = 1 if self.playerstart else 0
        tempcounter = 0
        for turn in self.turns:  # Fills the board according to self.turns.
            tempcounter += 1
            if tempcounter % 2 == self.remainder:
                self.board[5 - int(self.turns[:tempcounter-1].count(turn))][int(turn)] = 1  # Adds player token to board.
            else:
                self.board[5 - int(self.turns[:tempcounter-1].count(turn))][int(turn)] = 2  # Adds AI token to board.
        for row in self.board:  # Print board.
            print(row)

    # AI LOGIC.

    def aiturn(self):
        if self.movenum > 42 - self.maxdepth:  # Decrements self.maxdepth if the board starts running out of space.
            self.maxdepth = 42 - self.movenum
        depth = 0
        score = 0
        scoredict = self.simulatefutureturn(self.turns, self.board, score, depth)
        bestmoves = max(scoredict.values())

        self.evaluatedboards = []

        print('\n-----------------------------------------------------------------------------------------\n')
        print('BEST MOVES: ')
        print([key for key in scoredict if scoredict[key] == bestmoves])

    def checkcolumns(self, turns):
        possiblecolumns = []
        for col in range(7):
            if str(turns).count(str(col)) < 6:
                possiblecolumns.append(col)
        return possiblecolumns

    def simulatefutureturn(self, turns, board, score, depth):
        scoredict = {}
        depth += 1
        futureturnsarray = []
        playerorai = 2 if len(turns) % 2 == self.remainder else 1
        bestplayerscore = float('inf')  # Only used for finding the best player move. Unused when generating AI turns.

        for nextturn in self.checkcolumns(turns):
            futureturns = turns + str(nextturn)  # Concatenate turns with the newest turn.
            tempboard = copy.deepcopy(board)  # board copied by value.
            newboard, col, row = self.fillboard(futureturns, tempboard)  # newboard is a board will all tokens matching futureturns.
            if not self.alphabetapruning(newboard):
                nextturnscore, winidentified = self.evaluatescore(newboard, int(col), int(row), depth, playerorai)  # Checks score of the latest turn made.
                if playerorai == 1:
                    newscore = score - nextturnscore  # Find scores of all player turns.
                    if newscore < bestplayerscore:
                        bestplayerscore = newscore  # Updates bestplayerscore if a new lowest score is found. Only the best player moves are further branched out.
                else:
                    newscore = score + nextturnscore  # Find scores of all AI turns.
                futureturnsarray.append([futureturns, newboard, newscore, winidentified])

        if playerorai == 1:
            for playerturnsubarray in futureturnsarray:
                if playerturnsubarray[2] == bestplayerscore:  # Ensures that only the best player move is branched out. This ensures that only the best player moves are considered (since the player is smart).
                    if depth >= self.maxdepth:  # self.maxdepth is reached, so stop.
                        print(playerturnsubarray[0])
                        print(playerturnsubarray[2])
                        print('DEPTH: ' + str(depth))
                        print('PLAYER TURN ADDED')
                        print('------------')
                        scoredict[playerturnsubarray[0]] = bestplayerscore
                    else:  # self.maxdepth is not reached, so future turns are generated.
                        print(playerturnsubarray[0])
                        print(playerturnsubarray[2])
                        print('DEPTH: ' + str(depth))
                        print('PLAYER TURN BRANCHED OUT')
                        print('------------')
                        scoredict.update(self.simulatefutureturn(playerturnsubarray[0], playerturnsubarray[1], bestplayerscore, depth))
        else:
            for playerturnsubarray in futureturnsarray:
                if playerturnsubarray[3] and depth == 1:  # Immediate win is found, so move is returned automatically.
                    return {playerturnsubarray[0]: 0}
                elif depth >= self.maxdepth:  # self.maxdepth is reached, so stop.
                    print(playerturnsubarray[0])
                    print(playerturnsubarray[2])
                    print('DEPTH: ' + str(depth))
                    print('AI TURN ADDED')
                    print('------------')
                    scoredict[playerturnsubarray[0]] = playerturnsubarray[2]
                else:  # self.maxdepth is not reached, so future turns are generated.
                    print(playerturnsubarray[0])
                    print(playerturnsubarray[2])
                    print('DEPTH: ' + str(depth))
                    print('AI TURN BRANCHED OUT')
                    print('------------')
                    scoredict.update(self.simulatefutureturn(playerturnsubarray[0], playerturnsubarray[1], playerturnsubarray[2], depth))
        return scoredict

    def alphabetapruning(self, board):
        if board in self.evaluatedboards:
            return True
        self.evaluatedboards.append(board)
        return False  # Returns True if the board has not already been evaluated.

    def fillboard(self, turns, board):  # MODIFIED IN THIS VERSION SO THAT THE ALL TOKENS ARE ADDED.
        rowposition = 6 - str(turns).count(str(turns[-1]))  # Checks what row index the token gets dropped in.
        if len(turns) % 2 == self.remainder:
            board[rowposition][int(turns[-1])] = 1  # Adds player token to board.
        else:
            board[rowposition][int(turns[-1])] = 2  # Adds AI token to board.
        return board, turns[-1], rowposition  # Returns last move and which row it was placed in.

    def evaluatescore(self, board, col, row, depth, playerorai):
        winidentified = False
        rowcount, colcount, posdiagcount, negdiagcount = self.runcheckif4inrow(board, col, row, playerorai)
        score = rowcount + colcount + posdiagcount + negdiagcount
        if rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4:
            winidentified = True
            score += 10000000 / (depth * playerorai ** 3)
        elif not (rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4) and row != 0 and depth == 1:
            board[row-1][col] = 2
            rowcount, colcount, posdiagcount, negdiagcount = self.runcheckif4inrow(board, col, row, playerorai)
            if rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4:
                score -= 10000 / (depth * playerorai ** 3)
        return int(score), winidentified

    def checkif4inrow(self, board, col, colincrement, row, rowincrement, playerorai):
        counter = 0
        while 0 <= col <= 6 and 0 <= row <= 5:
            if board[row][col] != playerorai:
                break
            counter += 1
            col += colincrement
            row += rowincrement
        return counter

    def runcheckif4inrow(self, board, col, row, playerorai):
        # Checks if a row of 4 successive tokens has been found.
        rowcount = self.checkif4inrow(board, col, 1, row, 0, playerorai) + self.checkif4inrow(board, col, -1, row, 0, playerorai) - 1
        # Checks if a column of 4 successive tokens has been found.
        colcount = self.checkif4inrow(board, col, 0, row, 1, playerorai) + self.checkif4inrow(board, col, 0, row, -1, playerorai) - 1
        # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        posdiagcount = self.checkif4inrow(board, col, 1, row, -1, playerorai) + self.checkif4inrow(board, col, -1, row, 1, playerorai) - 1
        # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        negdiagcount = self.checkif4inrow(board, col, -1, row, -1, playerorai) + self.checkif4inrow(board, col, 1, row, 1, playerorai) - 1
        return rowcount, colcount, posdiagcount, negdiagcount


instance = gamelogic()
instance.aiturn()
