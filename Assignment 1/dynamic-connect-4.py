#!/usr/bin/python

from time import time
from DynamicConnect4Interface import draw_table_score
class game():
    def __init__(self):
        self.ROWS = 7
        self.COLS = 7
        self.board = [['_', '_', '_', '_', '_', '_', 'X'],
                      ['X', '_', '_', '_', '_', '_', 'O'],
                      ['O', '_', '_', '_', '_', '_', 'X'],
                      ['X', '_', '_', '_', '_', '_', 'O'],
                      ['O', '_', '_', '_', '_', '_', 'X'],
                      ['X', '_', '_', '_', '_', '_', 'O'],
                      ['O', '_', '_', '_', '_', '_', '_']]
        self.MinPlayer = False
        self.MaxPlayer = True
        self.MaxSym = 'X'
        self.MinSym = 'O'
        self.EmpSym = '_'
        self.depth_limit = 6
        self.time_limit = 20
        self.start_time = time()

    # Method of evaluation function. \
    # Returns 1000 for winning Maximizer and -1000 for winning Minimizer
    def is_winning(self, board):
        eval_value = 0
        # Assess vertical win for both players
        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col] \
                        and board[row][col] == board[row + 2][col] \
                        and board[row][col] == board[row + 3][col]:
                    if board[row][col] == self.MaxSym:
                        return 10
                    else:
                        return -10

        # Assess horizontal win for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row][col + 1] \
                        and board[row][col] == board[row][col + 2] \
                        and board[row][col] == board[row][col + 3]:
                    if board[row][col] == self.MaxSym:
                        return 10
                    else:
                        return -10

        # Assess diagonal win (increasing) for both players
        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col + 1] \
                        and board[row][col] == board[row + 2][col + 2] \
                        and board[row][col] == board[row + 3][col + 3]:
                    if board[row][col] == self.MaxSym:
                        return 10
                    else:
                        return -10

        # Assess vertical win (decreasing) for both players
        for row in range(self.ROWS - 3, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row - 1][col + 1] \
                        and board[row][col] == board[row - 2][col + 2] \
                        and board[row][col] == board[row - 3][col + 3]:
                    if board[row][col] == self.MaxSym:
                        return 10
                    else:
                        return -10
        return 0

    # Method to find every possible moves
    def move(self, board, player):
        moves = []
        if player == self.MaxPlayer:
            boardcase = self.MaxSym
        else:
            boardcase = self.MinSym
        # Scan all cells except border cells and returns the position if cell is empty and a player's token is nearby
        for row in range(1, self.ROWS - 1):
            for col in range(1, self.COLS - 1):
                if board[row][col] == boardcase:
                    if board[row - 1][col] == self.EmpSym:
                        moves.append([row, col, 'N'])
                    if board[row + 1][col] == self.EmpSym:
                        moves.append([row, col, 'S'])
                    if board[row][col + 1] == self.EmpSym:
                        moves.append([row, col, 'E'])
                    if board[row][col - 1] == self.EmpSym:
                        moves.append([row, col, 'W'])
        # Scan border cells of row 0
        row = 0
        for col in range(1, self.COLS - 1):
            if board[row][col] == boardcase:
                if board[row + 1][col] == self.EmpSym:
                    moves.append([row, col, 'S'])
                if board[row][col + 1] == self.EmpSym:
                    moves.append([row, col, 'E'])
                if board[row][col - 1] == self.EmpSym:
                    moves.append([row, col, 'W'])
        # Scan border cells of last row
        row = self.ROWS - 1
        for col in range(1, self.COLS - 1):
            if board[row][col] == boardcase:
                if board[row - 1][col] == self.EmpSym:
                    moves.append([row, col, 'N'])
                if board[row][col + 1] == self.EmpSym:
                    moves.append([row, col, 'E'])
                if board[row][col - 1] == self.EmpSym:
                    moves.append([row, col, 'W'])

        # Scan border cells of first column
        col = 0
        for row in range(1, self.ROWS - 1):
            if board[row][col] == boardcase:
                if board[row - 1][col] == self.EmpSym:
                    moves.append([row, col, 'N'])
                if board[row + 1][col] == self.EmpSym:
                    moves.append([row, col, 'S'])
                if board[row][col + 1] == self.EmpSym:
                    moves.append([row, col, 'E'])

        # Scan border cells of first column
        col = self.COLS - 1
        for row in range(1, self.ROWS - 1):
            if board[row][col] == boardcase:
                if board[row - 1][col] == self.EmpSym:
                    moves.append([row, col, 'N'])
                if board[row + 1][col] == self.EmpSym:
                    moves.append([row, col, 'S'])
                if board[row][col - 1] == self.EmpSym:
                    moves.append([row, col, 'W'])
        # Look for moves in the corners
        # TOP LEFT
        if board[0][0] == boardcase:
            if board[0][1] == self.EmpSym:
                moves.append([0, 0, 'E'])
            if board[1][0] == self.EmpSym:
                moves.append([0, 0, 'S'])
        # TOP RIGHT
        elif board[0][self.COLS - 1] == boardcase:
            if board[1][self.COLS - 1] == self.EmpSym:
                moves.append([0, self.COLS - 1, 'S'])
            if board[0][self.COLS - 2] == self.EmpSym:
                moves.append([0, self.COLS - 1, 'W'])
        # BOTTOM LEFT
        elif board[self.ROWS - 1][0] == boardcase:
            if board[self.ROWS - 2][0] == self.EmpSym:
                moves.append([self.ROWS - 1, 0, 'N'])
            if board[self.ROWS - 1][1] == self.EmpSym:
                moves.append([self.ROWS - 1, 0, 'E'])
        # BOTTOM RIGHT
        elif board[self.ROWS - 1][self.COLS - 1] == boardcase:
            if board[self.ROWS - 2][self.COLS - 1] == self.EmpSym:
                moves.append([self.ROWS - 1, self.COLS - 1, 'N'])
            if board[self.ROWS - 1][self.COLS - 2] == self.EmpSym:
                moves.append([self.ROWS - 1, self.COLS - 1, 'W'])

        return moves

    # Do the move and return the board for this move
    def do_move(self, board, move, player):
        if player == self.MaxPlayer:
            boardcase = self.MaxSym
        else:
            boardcase = self.MinSym
        board[move[0]][move[1]] = self.EmpSym
        if move[2] == 'N':
            board[move[0] - 1][move[1]] = boardcase
        elif move[2] == 'S':
            board[move[0] + 1][move[1]] = boardcase
        elif move[2] == 'E':
            board[move[0]][move[1] + 1] = boardcase
        elif move[2] == 'W':
            board[move[0]][move[1] - 1] = boardcase
        return board

    # Undo the move and return the board
    def undo_move(self, board, move, player):
        if self.MaxPlayer == player:
            boardcase = self.MaxSym
        else:
            boardcase = self.MinSym
        board[move[0]][move[1]] = boardcase
        if move[2] == 'N':
            board[move[0] - 1][move[1]] = self.EmpSym
        elif move[2] == 'S':
            board[move[0] + 1][move[1]] = self.EmpSym
        elif move[2] == 'E':
            board[move[0]][move[1] + 1] = self.EmpSym
        elif move[2] == 'W':
            board[move[0]][move[1] - 1] = self.EmpSym
        return board

    def minimax(self, board, depth, player):


        # Look if someone player is winning
        score = self.is_winning(board)
        if score == 10:
            return score
        if score == -10:
            return score
        if depth > self.depth_limit or time() - self.start_time > self.time_limit:
            return 0

        # Run for maximizer's turn
        if player == self.MaxPlayer:
            # Gather valid moves for max player
            moves = game.move(board, self.MaxPlayer)
            best = -1000
            # Do every possible move and run minimax recursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = game.do_move(board, move, player)
                best = max(best, game.minimax(board, depth + 1, not player))

                # Return board to previous state
                board = game.undo_move(board, move, player)
            return best
        # Run for minimizer's move
        else:
            # Gather valid moves for min player
            moves = game.move(board, self.MinPlayer)
            best = 1000
            # Do every possible move and run minimax reccursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = game.do_move(board, move, player)
                best = min(best, game.minimax(board, depth + 1, not player))

                # Return board to previous state
                board = game.undo_move(board, move, player)
            return best

    def alphabeta(self, board, depth, player, alpha, beta):


        # Look if someone player is winning
        score = self.is_winning(board)
        if score == 10:
            return score
        if score == -10:
            return score
        if depth > self.depth_limit or time() - self.start_time > self.time_limit:
            return 0

        # Run for maximizer's turn
        if player == self.MaxPlayer:
            # Gather valid moves for max player
            moves = game.move(board, self.MaxPlayer)
            best = -1000
            # Do every possible move and run minimax recursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = game.do_move(board, move, player)
                best = max(best, game.alphabeta(board, depth + 1, not player), alpha, beta)

                # Return board to previous state
                board = game.undo_move(board, move, player)
            return best
        # Run for minimizer's move
        else:
            # Gather valid moves for min player
            moves = game.move(board, self.MinPlayer)
            best = 1000
            # Do every possible move and run minimax reccursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = game.do_move(board, move, player)
                best = min(best, game.alphabeta(board, depth + 1, not player), alpha, beta)

                # Return board to previous state
                board = game.undo_move(board, move, player)
            return best

    def find_best_move(self, board, player):
        if self.MaxPlayer:
            bestvalue = -1000
        else:
            bestvalue = 1000
        bestmove = [-1, -1]
        self.start_time = time()
        print('Searching for best move')
        # Gather valid moves for player at this turn
        moves = game.move(board, player)

        for move in moves:
            #board = game.do_move(board, move, player)
            val_of_move = game.minimax(game.do_move(board, move, player), 0, not player)
            #board = game.undo_move(board, move, player)

            # Get best move for min or max player and returns it
            if self.MaxPlayer:
                if val_of_move > bestvalue:
                    bestvalue = val_of_move
                    bestmove = move
            else:
                if val_of_move < bestvalue:
                    bestvalue = val_of_move
                    bestmove = move
            if time() - self.start_time > self.time_limit:
                break

        if self.MaxPlayer:
            print('Best move for Max is ' + str(move))
        else:
            print('Best move for Min is ' + str(move))

        return bestmove


if __name__ == "__main__":
    game = game()
    player = game.MaxPlayer
    board = game.board
    while game.is_winning(game.board) != 10 or game.is_winning(game.board) != -10:
        # Update board with best move of each player
        board = game.do_move(board, game.find_best_move(board, player), player)
        draw_table_score(board)
        player = not player







