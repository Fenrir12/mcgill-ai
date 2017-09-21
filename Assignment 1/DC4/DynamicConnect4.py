#!/usr/bin/python

from time import time

from DynamicConnect4Interface import draw_table_score


class game():
    def __init__(self):
        self.ROWS = 7
        self.COLS = 7
        self.MaxSym = 'X'
        self.MinSym = 'O'
        self.EmpSym = ' '
        self.board = [[self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, 'X'],
                      ['X', self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, 'O'],
                      ['O', self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, 'X'],
                      ['X', self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, 'O'],
                      ['O', self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, 'X'],
                      ['X', self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, 'O'],
                      ['O', self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym, self.EmpSym]]
        self.MinPlayer = False
        self.MaxPlayer = True
        self.depth_limit = 4
        self.time_limit = 10
        self.start_time = time()
        self.MIN = -1000
        self.MAX = 1000
        self.no_of_nodes = 0
        self.no_of_turns = 0
        self.USE_PRUNING = False

    # Method of winning check function. \
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
                        return 100
                    else:
                        return -100

        # Assess horizontal win for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row][col + 1] \
                        and board[row][col] == board[row][col + 2] \
                        and board[row][col] == board[row][col + 3]:
                    if board[row][col] == self.MaxSym:
                        return 100
                    else:
                        return -100

        # Assess diagonal win (increasing) for both players
        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col + 1] \
                        and board[row][col] == board[row + 2][col + 2] \
                        and board[row][col] == board[row + 3][col + 3]:
                    if board[row][col] == self.MaxSym:
                        return 100
                    else:
                        return -100

        # Assess diagonal win (decreasing) for both players
        for row in range(self.ROWS - 3, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row - 1][col + 1] \
                        and board[row][col] == board[row - 2][col + 2] \
                        and board[row][col] == board[row - 3][col + 3]:
                    if board[row][col] == self.MaxSym:
                        return 100
                    else:
                        return -100

        # Return value of evaluation function if no win
        return self.eval(board)

    # Method of evaluation function. Returns the goodness of a state
    def eval(self, board):
        gauss_eval =[[3, 4, 5, 7, 5, 4, 3],
                     [4, 6, 8, 10, 8, 6, 4],
                     [5, 8, 11, 13, 11, 8, 5],
                     [6, 10, 13, 15, 13, 10, 6],
                     [5, 8, 11, 13, 11, 8, 5],
                     [4, 6, 8, 10, 8, 6, 4],
                     [3, 4, 5, 7, 5, 4, 3]]
        eval_score = 0
        gaussian_score = 0
        # Assess vertical 3-in-a-row for both players
        for row in range(0, self.ROWS - 2):
            for col in range(0, self.COLS):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col] \
                        and board[row][col] == board[row + 2][col]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 70
                    else:
                        eval_score = -70

        # Assess horizontal 3-in-a-row for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 2):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row][col + 1] \
                        and board[row][col] == board[row][col + 2]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 70
                    else:
                        eval_score = -70

        # Assess diagonal (increasing) 3-in-a-row for both players
        for row in range(0, self.ROWS - 2):
            for col in range(0, self.COLS - 2):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col + 1] \
                        and board[row][col] == board[row + 2][col + 2]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 60
                    else:
                        eval_score = -60

        # Assess diagonal (decreasing) 3-in-a-row for both players
        for row in range(self.ROWS - 4, self.ROWS):
            for col in range(0, self.COLS - 2):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row - 1][col + 1] \
                        and board[row][col] == board[row - 2][col + 2]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 60
                    else:
                        eval_score = -60

        # Assess vertical 2-in-a-row for both players
        for row in range(0, self.ROWS - 1):
            for col in range(0, self.COLS):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 30
                    else:
                        eval_score = -30

        # Assess horizontal 2-in-a-row for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 1):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row][col + 1]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 30
                    else:
                        eval_score = -30

        # Assess diagonal (increasing) 2-in-a-row for both players
        for row in range(0, self.ROWS - 1):
            for col in range(0, self.COLS - 1):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row + 1][col + 1]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 20
                    else:
                        eval_score = -20

        # Assess diagonal (decreasing) 2-in-a-row for both players
        for row in range(self.ROWS - 5, self.ROWS):
            for col in range(0, self.COLS - 1):
                if board[row][col] != self.EmpSym \
                        and board[row][col] == board[row - 1][col + 1]:
                    if board[row][col] == self.MaxSym:
                        eval_score = 20
                    else:
                        eval_score = -20

        # Rate board with gaussian score to give importance to center
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS):
                if board[row][col] != self.EmpSym:
                    if board[row][col] == self.MaxSym:
                        gaussian_score += gauss_eval[row][col]
                    else:
                        gaussian_score -= gauss_eval[row][col]

        return eval_score + gaussian_score

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

    # Minimax function to explore possible moves
    def minimax(self, board, depth, player):
        # Increment node counter
        self.no_of_nodes += 1
        # Look if someone player is winning
        score = self.is_winning(board)
        if score == 10 \
                or score == -10 \
                or depth > self.depth_limit \
                or time() - self.start_time > self.time_limit:
            return score

        # Run for maximizer's turn
        if player == self.MaxPlayer:
            # Gather valid moves for max player
            moves = self.move(board, self.MaxPlayer)
            best = self.MIN
            # Do every possible move and run minimax recursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = self.do_move(board, move, player)
                best = max(best, self.minimax(board, depth + 1, not player))

                # Return board to previous state
                board = self.undo_move(board, move, player)
            return best
        # Run for minimizer's move
        else:
            # Gather valid moves for min player
            moves = self.move(board, self.MinPlayer)
            best = self.MAX
            # Do every possible move and run minimax reccursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = self.do_move(board, move, player)
                best = min(best, self.minimax(board, depth + 1, not player))

                # Return board to previous state
                board = self.undo_move(board, move, player)
            return best

    #Alpha-Beta Pruning variation of minimax fuinction
    def alphabeta(self, board, depth, player, alpha, beta):
        # Increment node counter
        self.no_of_nodes += 1
        # Look if someone player is winning
        score = self.is_winning(board)

        if depth > self.depth_limit or time() - self.start_time > self.time_limit:
            return score

        # Run for maximizer's turn
        if player == self.MaxPlayer:
            best = self.MIN
            # Gather valid moves for max player
            moves = self.move(board, self.MaxPlayer)
            # Do every possible move and run minimax recursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = self.do_move(board, move, player)
                best = max(best, self.alphabeta(board, depth + 1, not player, alpha, beta))
                alpha = max(best, alpha)
                # Return board to previous state
                board = self.undo_move(board, move, player)
                if beta <= alpha:
                    break
            return best
        # Run for minimizer's move
        else:
            # Gather valid moves for min player
            moves = self.move(board, self.MinPlayer)
            best = self.MAX
            # Do every possible move and run minimax reccursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                board = self.do_move(board, move, player)
                best = min(best, self.alphabeta(board, depth + 1, not player, alpha, beta))
                beta = min(best, beta)
                # Return board to previous state
                board = self.undo_move(board, move, player)
                if beta <= alpha:
                    break
            return best

    # Runs minimax at depth 0 to return best move at present
    def find_best_move(self, board, player):
        if self.MaxPlayer == player:
            bestvalue = self.MIN
        else:
            bestvalue = self.MAX
        bestmove = [-1, -1]
        self.start_time = time()
        #print('Searching for best move')
        # Gather valid moves for player at this turn
        moves = self.move(board, player)

        for move in moves:
            board = self.do_move(board, move, player)
            if self.USE_PRUNING:
                val_of_move = self.alphabeta(board, 0, player, self.MIN, self.MAX)
            else:
                val_of_move = self.minimax(board, 0, not player)
            board = self.undo_move(board, move, player)

            # Get best move for min or max player and returns it
            if self.MaxPlayer == player:
                if val_of_move > bestvalue:
                    bestvalue = val_of_move
                    bestmove = move
            else:
                if val_of_move < bestvalue:
                    bestvalue = val_of_move
                    bestmove = move
            if time() - self.start_time > self.time_limit:
                break

        #if self.MaxPlayer == player:
            #print('Best move for Max is ' + str(move))
        #else:
            #print('Best move for Min is ' + str(move))

        return bestmove

    # Convert move from server to move format
    def convert_move(self, string):
        return [int(string[0])-1, int(string[1])-1, string[2]]

    # Convert move from move format to server format
    def send_move(self, move):
        return str(str(move[0]+1) + str(move[1]+1) + move[2] + "\n")

    def move_list(self):
        netmoves = []
        for row in [1, 2, 3, 4, 5, 6, 7]:
            for col in [1, 2, 3, 4, 5, 6, 7]:
                for char in ['N', 'S', 'W', 'E']:
                    netmoves.append(str(row)+str(col)+char)
        return netmoves

if __name__ == "__main__":
    game = game()
    game.USE_PRUNING = True
    player = game.MaxPlayer = game.MaxPlayer
    board = game.board
    score = 0

    while True:
        # Update board with best move of each player
        board = game.do_move(board, game.find_best_move(board, player), player)
        print('\n\rExplored ' + str(game.no_of_nodes) + ' nodes')
        draw_table_score(board)
        game.no_of_nodes = 0
        game.no_of_plies = []
        player = not player
        score = game.is_winning(game.board)
        if score == 100:
            print('I won')
            break
        elif score == -100:
            print('Other player won')
            break







