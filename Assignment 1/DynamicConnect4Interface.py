#!/usr/bin/python


def draw_table_score(board):

    print("\n\n           ------------------------------------")
    print("\n\n        BLACK X ============== O WHITE ")
    print("\n\n           ------------------------------------")
    print("1           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], board[0][6]))
    print("2           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[1][0], board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], board[1][6]))
    print("3           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[2][0], board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], board[2][6]))
    print("4           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[3][0], board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], board[3][6]))
    print("5           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[4][0], board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], board[4][6]))
    print("6           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[5][0], board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], board[5][6]))
    print("7           [%s] [%s] [%s] [%s] [%s] [%s] [%s] "%(board[6][0], board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], board[6][6]))
    print("           ------------------------------------")
    print("            1   2   3   4   5   6   7    \n\n")

if __name__ == "__main__":
    board = [['_', '_', '_', '_', '_', '_', 'X'],
             ['X', '_', '_', '_', '_', '_', 'O'],
             ['O', '_', '_', '_', '_', '_', 'X'],
             ['X', '_', '_', '_', '_', '_', 'O'],
             ['O', '_', '_', '_', '_', '_', 'X'],
             ['X', '_', '_', '_', '_', '_', 'O'],
             ['O', '_', '_', '_', '_', '_', '_']]
    draw_table_score(board)
