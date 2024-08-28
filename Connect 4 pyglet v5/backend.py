import random
import copy


class gamelogic:
    def __init__(self, playerstart):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.turns = ''
        self.moves = []
        self.movenum = 0
        self.gamestate = 0
        self.tokencurrentposition = 0
        self.maxdepth = 7
        self.playerstart = playerstart
        self.remainder = 1 if self.playerstart else 0

    # PLAYER LOGIC.

    def movetoken(self, operation):
        self.tokencurrentposition = (self.tokencurrentposition + operation) % 7
        if str(self.turns).count(str(self.tokencurrentposition)) >= 6:  # Checks that the column is not full.
            if self.movenum < 42:
                self.movetoken(operation)

    def reset_game(self):
        self.__init__(not self.playerstart)  # Resets self.board, self.turns, self.moves, self.movenum, self.gamestate, self.tokencurrentposition and self.maxdepth to their original values.
        if not self.playerstart:
            self.movenum += 1
            self.drop_token(3, 2)

    # AI LOGIC.

    def aiturn(self):
        if self.movenum < 5:
            movedict = {str(i): self.turns.count(str(i)) for i in range(1, 6)}
            bestmoves = [int(key) for key, value in movedict.items() if value == 0]
            move = random.choice(bestmoves)  # Finds all the best turns.
            self.drop_token(move, 2)
        else:
            if self.movenum > 42 - self.maxdepth:  # Decrements self.maxdepth if the board starts running out of space.
                self.maxdepth = 42 - self.movenum

            scoredict = self.simulatefutureturn(self.turns, self.board, 0, 0)
            maxvalue = max(scoredict.values())
            bestmoves = [key for key in scoredict if scoredict[key] == maxvalue]  # Finds turns with highest scores.
            move = random.choice(bestmoves)  # Randomly chooses a turn from the turns that have the highest scores.

            print('\n-----------------------------------------------------------------------------------------\n')
            [print(f"{key}: {value}") for key, value in scoredict.items()]
            print('BEST MOVES: ')
            print(bestmoves)

            self.drop_token(int(move[self.movenum - 1]), 2)

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
                        scoredict[playerturnsubarray[0]] = bestplayerscore
                    else:  # self.maxdepth is not reached, so future turns are generated.
                        scoredict.update(self.simulatefutureturn(playerturnsubarray[0], playerturnsubarray[1], bestplayerscore, depth))
        else:
            for playerturnsubarray in futureturnsarray:
                if playerturnsubarray[3] and depth == 1:  # Immediate win is found, so move is returned automatically.
                    return {playerturnsubarray[0]: 0}
                elif depth >= self.maxdepth:  # self.maxdepth is reached, so stop.
                    scoredict[playerturnsubarray[0]] = playerturnsubarray[2]
                else:  # self.maxdepth is not reached, so future turns are generated.
                    scoredict.update(self.simulatefutureturn(playerturnsubarray[0], playerturnsubarray[1], playerturnsubarray[2], depth))
        return scoredict

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

    # SHARED LOGIC.

    def record_move(self, col, row, playerorai):
        self.moves.append((col + 1, 6 - row, playerorai, self.movenum))
        if len(self.moves) > 14:
            self.moves.pop(0)

    def drop_token(self, col, playerorai):
        row = 5 - self.turns.count(str(col))  # Checks what row index the token gets dropped in.
        self.board[row][col] = playerorai
        self.turns = self.turns + str(col)
        self.record_move(col, row, playerorai)
        if self.tokencurrentposition == col and row == 0:  # Moves player token automatically if the column becomes full.
            self.movetoken(1)
        self.gamestate = self.isgameover(col, row, playerorai)

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

    def isgameover(self, col, row, playerorai):
        rowcount, colcount, posdiagcount, negdiagcount = self.runcheckif4inrow(self.board, col, row, playerorai)
        # Returns False if 4 consecutive tokens were found, otherwise returns True.
        if rowcount >= 4 or colcount >= 4 or posdiagcount >= 4 or negdiagcount >= 4:
            return playerorai
        elif self.movenum == 42:
            return 3
        else:
            return 0
