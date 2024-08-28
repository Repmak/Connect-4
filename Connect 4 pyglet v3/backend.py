import random


class gamelogic:
    def __init__(self):
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.moves = []
        self.movenum = 0
        self.gamestate = True
        self.tokencurrentposition = 0

    def movetoken(self, operation, tokencurrentposition):
        self.tokencurrentposition = (tokencurrentposition + operation) % 7
        self.iscolumnfull(operation)
        return self.tokencurrentposition

    def iscolumnfull(self, operation):  # Ensures that the specified column is not full. If full, the token will be moved until a column that has space has been found.
        if not any(self.board[i][self.tokencurrentposition] == 0 for i in range(6)):
            self.movetoken(operation, self.tokencurrentposition)

    def record_move(self, col, row, playerorai):
        self.moves.append((col + 1, 6 - row, playerorai, self.movenum))
        if len(self.moves) > 14:
            self.moves.pop(0)

    def check_row(self, row, playerorai):
        for i in range(4):
            if all(self.board[row][i + j] == playerorai for j in range(4)):
                return False
        return True

    def check_col(self, col, playerorai):
        for i in range(3):
            if all(self.board[i + j][col] == playerorai for j in range(4)):
                return False
        return True

    def find_new_points(self, col, row, limits, ops, playerorai):
        diagonal = [(col, row)]
        tempcol, temprow = col, row
        while limits[0] < temprow < limits[1] and limits[2] < tempcol < limits[3]:
            tempcol += ops[0]
            temprow += ops[1]
            if self.board[temprow][tempcol] == playerorai:
                diagonal.append((tempcol, temprow))
            else:
                break
        return diagonal

    def check_diag(self, col, row, limits, ops, playerorai):
        diag1 = self.find_new_points(col, row, limits[:4], ops[:2], playerorai)
        diag2 = self.find_new_points(col, row, limits[4:], ops[2:], playerorai)
        diagpoints = set(diag1 + diag2)
        return len(diagpoints) < 4

    def is_game_over(self, col, row, playerorai):
        rowstate = self.check_row(row, playerorai)  # Checks if a row of 4 successive tokens has been found.
        colstate = self.check_col(col, playerorai)  # Checks if a column of 4 successive tokens has been found.
        posdiagstate = self.check_diag(col, row, [0, 6, -1, 6, -1, 5, 0, 7], [1, -1, -1, 1], playerorai)  # Checks if a diagonal line (with +ve gradient) of 4 successive tokens has been found.
        negdiagstate = self.check_diag(col, row, [-1, 5, -1, 6, 0, 6, 0, 7], [1, 1, -1, -1], playerorai)  # Checks if a diagonal line (with -ve gradient) of 4 successive tokens has been found.
        return rowstate and colstate and posdiagstate and negdiagstate

    def ai_move(self):
        while True:
            col = random.randint(0, 6)
            for row in range(5, -1, -1):
                if self.board[row][col] == 0:
                    self.board[row][col] = 2
                    self.movenum += 1
                    self.record_move(col, row, 2)
                    self.gamestate = self.is_game_over(col, row, 2)
                    return

    def drop_token(self, col, playerorai):
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = playerorai
                self.movenum += 1
                self.record_move(col, row, playerorai)
                self.gamestate = self.is_game_over(col, row, playerorai)
                return row
        return None

    def reset_game(self):
        self.__init__()  # Resets self.board, self.moves, self.movenum and self.gamestate to their original values.
