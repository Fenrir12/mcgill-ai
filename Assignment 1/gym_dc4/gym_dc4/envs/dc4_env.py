import gym
import time
from gym import error, spaces, utils
from DC4.DynamicConnect4 import game
from DC4.DynamicConnect4Interface import draw_table_score
import random

REWARD_INVALID_ACTION = -500.0
REWARD_INVALID_MOVE = -250.0
REWARD_VALID_MOVE = 10.0
REWARD_WIN = 500.0


class DC4Env(gym.Env):
    metadata = {'render.modes': ['ansi', 'human']}

    def __init__(self):
        self.action_space = spaces.Discrete(4)  # N, S, W, E
        self.observation_space = spaces.Box(1, 0, (7, 7))
        self.current_player = "X"
        self.board = [['_', '_', '_', '_', '_', '_', 'x4'],
                      ['x1', '_', '_', '_', '_', '_', 'o4'],
                      ['o1', '_', '_', '_', '_', '_', 'x5'],
                      ['x2', '_', '_', '_', '_', '_', 'o5'],
                      ['o2', '_', '_', '_', '_', '_', 'x6'],
                      ['x3', '_', '_', '_', '_', '_', 'o6'],
                      ['o3', '_', '_', '_', '_', '_', '_']]
        self.ROWS = 7
        self.COLS = 7
        self.EmpSym = '_'

    def create_action_vector(self):
        return {"x1": False, "x2": False,
                "x3": False, "x4": False,
                "x5": False, "x6": False,
                "o1": False, "o2": False,
                "o3": False, "o4": False,
                "o5": False, "o6": False,
                "N": False, "S": False,
                "E": False, "W": False}

    def _step(self, action):
        reward = 0.0
        if not self.validate_action(action):
            reward = REWARD_INVALID_ACTION
            self.current_player = "X" if self.current_player == "O" else "O"
            return {"board": self.board, "player": self.current_player}, True, reward, {}

        if not self.validate_move(action):
            reward = REWARD_INVALID_MOVE
            self.current_player = "X" if self.current_player == "O" else "O"
            return {"board": self.board, "player": self.current_player}, True, reward, {}

        self.update_board(action)

        if self.is_winning(self.board, self.current_player):
            return {"board": self.board, "player": self.current_player}, True, reward, {}

        self.current_player = "X" if self.current_player == "O" else "O"
        return {"board": self.board, "player": self.current_player}, False, reward, {}

    def _reset(self):
        self.current_player = "X"
        self.board = [['_', '_', '_', '_', '_', '_', 'x4'],
                      ['x1', '_', '_', '_', '_', '_', 'o4'],
                      ['o1', '_', '_', '_', '_', '_', 'x5'],
                      ['x2', '_', '_', '_', '_', '_', 'o5'],
                      ['o2', '_', '_', '_', '_', '_', 'x6'],
                      ['x3', '_', '_', '_', '_', '_', 'o6'],
                      ['o3', '_', '_', '_', '_', '_', '_']]
        return {"board": self.board, "player": self.current_player}

    def _render(self, mode='human', close=False):
        draw_table_score(self.board)

    def get_new_move(self, action):
        rowidx, colidx = self.get_peon_coords(action)
        move = self.get_selected_move(action)
        new_row, new_col = rowidx, colidx
        if move == 'N':
            new_row = rowidx - 1
        elif move == 'S':
            new_row = rowidx + 1
        elif move == 'E':
            new_col = colidx + 1
        else:
            new_col = colidx - 1
        return new_row, new_col

    def validate_move(self, action):
        new_row, new_col = self.get_new_move(action)

        # Scan center cells
        if 0 <= new_row <= 6 and 0 <= new_col <= 6:
            if self.board[new_row][new_col] == '_':
                return True

        return False

    def update_board(self, action):
        rowidx, colidx = self.get_peon_coords(action)
        new_row, new_col = self.get_new_move(action)
        self.board[rowidx][colidx] = '_'
        self.board[new_row][new_col] = self.get_selected_peon(action)

    def get_selected_move(self, action):
        keys = ["N", "S", "E", "W"]
        for key in keys:
            if action[key]:
                return key

    def get_selected_peon(self, action):
        keys = ["x1", "x2", "x3", "x4", "x5", "x6", "o1", "o2", "o3", "o4", "o5", "o6"]
        for key in keys:
            if action[key]:
                return key

    def get_peon_coords(self, action):
        for (row_idx, row) in enumerate(self.board):
            if self.get_selected_peon(action) in row:
                return row_idx, row.index(self.get_selected_peon(action))

        return -1, -1

    def validate_action(self, action):
        # All logical rules make sure that only one piece black or white has taken only one move
        if sum([action["N"], action["S"], action["E"], action["W"]]) != 1:
            return False

        if sum([action["x1"], action["x2"], action["x3"], action["x4"], action["x5"], action["x6"],
                action["o1"], action["o2"], action["o3"], action["o4"], action["o5"], action["o6"]]) != 1:
            return False

        if self.current_player == "X":
            if action["o1"] or action["o2"] or action["o3"] or action["o4"] or action["o5"] or action["o6"]:
                return False

        elif self.current_player == "O":
            if action["x1"] or action["x2"] or action["x3"] or action["x4"] or action["x5"] or action["x6"]:
                return False

        return True

    def is_winning(self, board, player):
        eval_value = 0
        # Assess vertical win for both players
        p = 'o' if player == 'O' else 'x'

        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS):
                if board[row][col] != self.EmpSym \
                        and p in board[row][col] \
                        and p in board[row + 1][col] \
                        and p in board[row + 2][col] \
                        and p in board[row + 3][col]:
                    return True

        # Assess horizontal win for both players
        for row in range(0, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and p in board[row][col] \
                        and p in board[row][col + 1] \
                        and p in board[row][col + 2] \
                        and p in board[row][col + 3]:
                    return True

        # Assess diagonal win (increasing) for both players
        for row in range(0, self.ROWS - 3):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and p in board[row][col] \
                        and p in board[row + 1][col + 1] \
                        and p in board[row + 2][col + 2] \
                        and p in board[row + 3][col + 3]:
                    return True

        # Assess diagonal win (decreasing) for both players
        for row in range(self.ROWS - 3, self.ROWS):
            for col in range(0, self.COLS - 3):
                if board[row][col] != self.EmpSym \
                        and p in board[row - 1][col + 1] \
                        and p in board[row - 2][col + 2] \
                        and p in board[row - 3][col + 3]:
                    return True

    def generate_action(self):
        action = self.create_action_vector()
        action[random.choice(list(action))] = True
        action[random.choice(list(action))] = True
        return action

