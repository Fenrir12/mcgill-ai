#!/usr/bin/python

from time import time
import copy
import numpy as np
from DynamicConnect4Interface import draw_table_score


# Alpha Beta Pruning with Iterative Deepening
class game_v1():
    def __init__(self):
        self.ROWS = 7
        self.COLS = 7
        self.MaxSym = 'O'
        self.MinSym = 'X'
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
        self.reached_depth = 0
        self.time_limit = 9
        self.start_time = time()
        self.MIN = -1000000
        self.MAX = 1000000
        self.no_of_nodes = 0
        self.no_of_turns = 0
        self.USE_PRUNING = False
        self.USE_ITERATIVE_DEEPENING = False
        self.eval_time = []

    # Method of winning check function. \
    # Returns 1000 for winning Maximizer and -1000 for winning Minimizer
    def is_winning(self, board, player):
        eval_value = 0
        if player == self.MaxPlayer:
            color = 'O'
        else:
            color = 'X'
        # Assess vertical win for both players
        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS):
                if board[row][col] == color \
                        and board[row][col] == board[row + 1][col] \
                        and board[row][col] == board[row + 2][col] \
                        and board[row][col] == board[row + 3][col]:
                    return 1000

        # Assess horizontal win for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] == color \
                        and board[row][col] == board[row][col + 1] \
                        and board[row][col] == board[row][col + 2] \
                        and board[row][col] == board[row][col + 3]:
                    return 1000

        # Assess diagonal win (increasing) for both players
        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS - 3):
                if board[row][col] == color \
                        and board[row][col] == board[row + 1][col + 1] \
                        and board[row][col] == board[row + 2][col + 2] \
                        and board[row][col] == board[row + 3][col + 3]:
                    return 1000

        # Assess diagonal win (decreasing) for both players
        for row in range(self.ROWS - 3, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] == color \
                        and board[row][col] == board[row - 1][col + 1] \
                        and board[row][col] == board[row - 2][col + 2] \
                        and board[row][col] == board[row - 3][col + 3]:
                    return 1000

        # Return value of evaluation function if no win
        return self.eval(board, color)

    # Method of evaluation function. Returns the goodness of a state
    def eval(self, board, color):
        start_time = time()
        gauss_eval = [[3, 4, 5, 7, 5, 4, 3],
                      [4, 6, 8, 10, 8, 6, 4],
                      [5, 8, 11, 13, 11, 8, 5],
                      [6, 10, 13, 15, 13, 10, 6],
                      [5, 8, 11, 13, 11, 8, 5],
                      [4, 6, 8, 10, 8, 6, 4],
                      [3, 4, 5, 7, 5, 4, 3]]
        node = copy.deepcopy(board)
        eval_score = 0
        gaussian_score = 0
        # Assess vertical 3-in-a-row for both players
        for row in range(0, self.ROWS - 2):
            for col in range(0, self.COLS):
                if node[row][col] == color\
                        and node[row][col] == node[row + 1][col] \
                        and node[row][col] == node[row + 2][col]:
                    eval_score = max(eval_score, 70)
                    node[row][col] = self.EmpSym
                    node[row + 1][col] = self.EmpSym
                    node[row + 2][col] = self.EmpSym
        # Assess horizontal 3-in-a-row for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 2):
                if node[row][col] == color \
                        and node[row][col] == node[row][col + 1] \
                        and node[row][col] == node[row][col + 2]:
                    eval_score = max(eval_score, 70)
                    node[row][col] = self.EmpSym
                    node[row][col + 1] = self.EmpSym
                    node[row][col + 2] = self.EmpSym
        # Assess diagonal (increasing) 3-in-a-row for both players
        for row in range(0, self.ROWS - 2):
            for col in range(0, self.COLS - 2):
                if node[row][col] == color \
                        and node[row][col] == node[row + 1][col + 1] \
                        and node[row][col] == node[row + 2][col + 2]:
                    eval_score = max(eval_score, 70)
                    node[row][col] = self.EmpSym
                    node[row + 1][col + 1] = self.EmpSym
                    node[row + 2][col + 2] = self.EmpSym

        # Assess diagonal (decreasing) 3-in-a-row for both players
        for row in range(self.ROWS - 4, self.ROWS):
            for col in range(0, self.COLS - 2):
                if node[row][col] == color \
                        and node[row][col] == node[row - 1][col + 1] \
                        and node[row][col] == node[row - 2][col + 2]:
                    eval_score = max(eval_score, 70)
                    node[row][col] = self.EmpSym
                    node[row - 1][col + 1] = self.EmpSym
                    node[row - 2][col + 2] = self.EmpSym

        # Assess vertical 2-in-a-row for both players
        for row in range(0, self.ROWS - 1):
            for col in range(0, self.COLS):
                if node[row][col] == color \
                        and node[row][col] == node[row + 1][col]:
                    eval_score = max(eval_score, 30)
                    node[row][col] = self.EmpSym
                    node[row + 1][col] = self.EmpSym

        # Assess horizontal 2-in-a-row for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 1):
                if node[row][col] == color \
                        and node[row][col] == node[row][col + 1]:
                    eval_score = max(eval_score, 30)
                    node[row][col] = self.EmpSym
                    node[row][col + 1] = self.EmpSym

        # Assess diagonal (increasing) 2-in-a-row for both players
        for row in range(0, self.ROWS - 1):
            for col in range(0, self.COLS - 1):
                if node[row][col] == color \
                        and node[row][col] == node[row + 1][col + 1]:
                    eval_score = max(eval_score, 30)
                    node[row][col] = self.EmpSym
                    node[row + 1][col + 1] = self.EmpSym

        # Assess diagonal (decreasing) 2-in-a-row for both players
        for row in range(self.ROWS - 5, self.ROWS):
            for col in range(0, self.COLS - 1):
                if node[row][col] == color \
                        and node[row][col] == node[row - 1][col + 1]:
                    eval_score = max(eval_score, 30)
                    node[row][col] = self.EmpSym
                    node[row - 1][col + 1] = self.EmpSym

        # Rate board with gaussian score to give importance to center
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS):
                if node[row][col] == color:
                    gaussian_score += gauss_eval[row][col]

        self.eval_time.append(time() - start_time)
        return eval_score + gaussian_score


    # Method that adds complexity to evaluation function
    def eval_addon(self, board, color):
        pass

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


    def minimax_ab(self, board, depth, player, alpha, beta):
        # Increment node counter
        self.no_of_nodes += 1
        node = list(board)
        # Look if someone player is winning
        score = self.is_winning(node, self.MaxPlayer) - self.is_winning(node, self.MinPlayer)

        if depth >= self.depth_limit or time() - self.start_time > self.time_limit:
            return score

        # Run for maximizer's turn
        if player == self.MaxPlayer:
            best = self.MIN
            # Gather valid moves for max player
            moves = self.move(node, self.MaxPlayer)
            # Do every possible move and run minimax recursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                node = self.do_move(node, move, player)
                best = max(best, self.minimax_ab(node, depth + 1, not player, alpha, beta))
                alpha = max(best, alpha)
                # Return board to previous state
                node = self.undo_move(node, move, player)
                if beta <= alpha:
                    break
            return best
        # Run for minimizer's move
        else:
            # Gather valid moves for min player
            moves = self.move(node, self.MinPlayer)
            best = self.MAX
            # Do every possible move and run minimax reccursively for each possible state at different depths
            for move in moves:
                # Do the move and go into minimax for next depth
                node = self.do_move(node, move, player)
                best = min(best, self.minimax_ab(node, depth + 1, not player, alpha, beta))
                beta = min(best, beta)
                # Return board to previous state
                node = self.undo_move(node, move, player)
                if beta <= alpha:
                    break
            return best


    # Negamax function to explore possible moves
    def negamax(self, board, depth, player):
        # Increment node counter
        self.no_of_nodes += 1

        # Look if someone player is winning
        score = self.is_winning(board, not player)
        if depth >= self.depth_limit or time() - self.start_time > self.time_limit:
            return score * -1

        best = self.MIN

        # Gather valid moves for player
        moves = self.move(board, player)
        # Do every possible move and run minimax recursively for each possible state at different depths
        for move in moves:
            # Do the move and go into another minimax for next depth
            node = self.do_move(board, move, player)
            val = -self.negamax(node, depth + 1, not player)
            best = max(best, val)
            # Return board to previous state
            node = self.undo_move(node, move, player)
        return best


    # Negamax with alpha-beta Pruning
    def negamax_ab(self, node, depth, player, alpha, beta):
        # Increment node counter node is scored
        self.no_of_nodes += 1
        # Look if someone player is winning
        score = self.is_winning(node, not player)
        if depth >= self.depth_limit \
                or time() - self.start_time > self.time_limit \
                or score == 100:
            # Set object's depth limit to reached depth if time limit is reached
            # No change if depth limit was reached
            return score
        bestvalue = self.MIN
        # Run for player's turn
        # Gather valid moves for player
        moves = self.move(node, player)
        # Do every possible move and run minimax recursively for each possible state at different depths
        for move in moves:
            # Do the move and go into another minimax for next depth
            node = self.do_move(node, move, player)
            score = -self.negamax_ab(node, depth + 1, not player, -beta, -alpha)
            bestvalue = max(score, bestvalue)
            alpha = max(score, alpha)
            # Return board to previous state
            node = self.undo_move(node, move, player)
            if beta <= alpha:
                break
        return bestvalue


    # Alpha-Beta Pruning variation of minimax function with Negascout.
    # Needs good ordering of moves to achieve better performances
    def negascout(self, node, depth, player, alpha, beta):
        # Increment node counter
        self.no_of_nodes += 1
        # Look if someone player is winning
        score = self.is_winning(node, player)
        if depth >= self.depth_limit \
                or time() - self.start_time > self.time_limit \
                or score == 100:
            if player == self.MaxPlayer:
                return score
            else:
                return -score

        # Run for player's turn
        score = self.MIN
        # Gather valid moves for player
        moves = self.move(node, player)
        # Do every possible move and run minimax recursively for each possible state at different depths
        for move in moves:
            # Do the move and go into another minimax for next depth
            node = self.do_move(node, move, player)
            if move == moves[0]:
                score = -self.negascout(node, depth + 1, not player, -alpha - 1, -alpha)
                if alpha < score < beta:
                    score = -self.negascout(node, depth + 1, not player, -beta, -score)
            else:
                score = -self.negascout(node, depth + 1, not player, -beta, -alpha)
            alpha = max(score, alpha)
            # Return board to previous state
            node = self.undo_move(node, move, player)
            if beta <= alpha:
                break
        return alpha


    # Runs minimax at depth 0 to return best move at present
    def find_best_move(self, board, player):
        # Set depth limit to 1 if using incrementing search, we will
        # then perform a depth-first search with incrementing depth
        # Else we use the specified depth cutoff of the object's parameter
        if self.USE_ITERATIVE_DEEPENING:
            self.depth_limit = 1

        if self.MaxPlayer == player:
            bestvalue = self.MIN
            id_best_value = self.MIN
        else:
            bestvalue = self.MAX
            id_best_value = self.MAX
        bestmove = [-1, -1]
        id_best_move = [-1, -1]
        self.start_time = time()

        root_node = list(board)
        # Gather valid moves for player at this turn
        moves = self.move(root_node, player)

        # Repeat fin best move with alpha beta at incrementing levels of depth
        while True:
            # First moves at depth 1
            for move in moves:

                root_node = self.do_move(root_node, move, player)
                if self.USE_PRUNING:
                    val_of_move = self.minimax_ab(root_node, 1, not player, self.MIN, self.MAX)
                else:
                    val_of_move = -self.negamax(root_node, 1, not player)
                root_node = self.undo_move(root_node, move, player)

                # Get best move for min or max player and returns it at this depth level search
                if player:
                    if val_of_move > bestvalue:
                        bestvalue = val_of_move
                        bestmove = move
                else:
                    if val_of_move < bestvalue:
                        bestvalue = val_of_move
                        bestmove = move
                if time() - self.start_time > self.time_limit:
                    break
            print(bestvalue)
            # Update best move if search at deeper level has better result
            if self.MaxPlayer == player:
                if bestvalue > id_best_value:
                    id_best_value = bestvalue
                    id_best_move = bestmove
            else:
                if bestvalue < id_best_value:
                    id_best_value = bestvalue
                    id_best_move = bestmove

            print("Explored " + str(self.no_of_nodes) + ' nodes at depth ' + str(self.depth_limit) + ' in ' + str(
                time() - self.start_time) + ' s.')
            if self.USE_ITERATIVE_DEEPENING:
                if time() - self.start_time > self.time_limit:
                    break
                # Go for a deeper search level if time permits it
                self.no_of_nodes = 0
                self.depth_limit += 1
            else:
                break
        return id_best_move


    # Convert move from server to move format
    def convert_move(self, string):
        return [int(string[0]) - 1, int(string[1]) - 1, string[2]]


    # Convert move from move format to server format
    def send_move(self, move):
        return str(str(move[0] + 1) + str(move[1] + 1) + move[2] + "\n")


    def move_list(self):
        netmoves = []
        for row in [1, 2, 3, 4, 5, 6, 7]:
            for col in [1, 2, 3, 4, 5, 6, 7]:
                for char in ['N', 'S', 'W', 'E']:
                    netmoves.append(str(row) + str(col) + char)
        return netmoves


if __name__ == "__main__":
    game = game_v1()
    game.time_limit = 10
    game.depth_limit = 10
    player = game.MaxPlayer
    board = game.board
    game.USE_PRUNING = True
    game.USE_ITERATIVE_DEEPENING = False
    score = 0

    while True:
        # Update board with best move of each player
        best_move = game.find_best_move(board, player)
        board = game.do_move(board, best_move, player)
        draw_table_score(board)
        print(
        "mean evaluation time is " + str(np.mean(game.eval_time)) + ' seconds for ' + str(game.no_of_nodes) + ' nodes')
        game.no_of_nodes = 0
        game.no_of_plies = []
        game.eval_time = []
        score = game.is_winning(game.board, player)
        if score == 1000:
            print('I won')
            break
        elif score == -1000:
            print('Other player won')
            break
        player = not player
