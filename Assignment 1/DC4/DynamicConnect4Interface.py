#!/usr/bin/python


def draw_table_score(board):
    print("   1 2 3 4 5 6 7    ")
    print("1  %s,%s,%s,%s,%s,%s,%s" % (
    board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], board[0][6]))
    print("2  %s,%s,%s,%s,%s,%s,%s" % (
    board[1][0], board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], board[1][6]))
    print("3  %s,%s,%s,%s,%s,%s,%s" % (
    board[2][0], board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], board[2][6]))
    print("4  %s,%s,%s,%s,%s,%s,%s" % (
    board[3][0], board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], board[3][6]))
    print("5  %s,%s,%s,%s,%s,%s,%s" % (
    board[4][0], board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], board[4][6]))
    print("6  %s,%s,%s,%s,%s,%s,%s" % (
    board[5][0], board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], board[5][6]))
    print("7  %s,%s,%s,%s,%s,%s,%s" % (
    board[6][0], board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], board[6][6]))


def write_2_file(board, no_of_nodes, depth, filename):
    with open(filename + ".txt", "a") as myfile:
        myfile.write("Expanded " + str(no_of_nodes) + " nodes")
        myfile.write("\n\n\n   1 2 3 4 5 6 7    \n")
        myfile.write("1  %s ,%s ,%s ,%s ,%s ,%s ,%s\n" % (
            board[0][0], board[0][1], board[0][2], board[0][3], board[0][4], board[0][5], board[0][6]))
        myfile.write("2  %s, %s, %s, %s, %s, %s, %s\n" % (
            board[1][0], board[1][1], board[1][2], board[1][3], board[1][4], board[1][5], board[1][6]))
        myfile.write("3  %s,%s,%s,%s,%s,%s,%s\n" % (
            board[2][0], board[2][1], board[2][2], board[2][3], board[2][4], board[2][5], board[2][6]))
        myfile.write("4  %s,%s,%s,%s,%s,%s,%s\n" % (
            board[3][0], board[3][1], board[3][2], board[3][3], board[3][4], board[3][5], board[3][6]))
        myfile.write("5  %s,%s,%s,%s,%s,%s,%s\n" % (
            board[4][0], board[4][1], board[4][2], board[4][3], board[4][4], board[4][5], board[4][6]))
        myfile.write("6  %s,%s,%s,%s,%s,%s,%s\n" % (
            board[5][0], board[5][1], board[5][2], board[5][3], board[5][4], board[5][5], board[5][6]))
        myfile.write("7  %s,%s,%s,%s,%s,%s,%s\n" % (
            board[6][0], board[6][1], board[6][2], board[6][3], board[6][4], board[6][5], board[6][6]))


if __name__ == "__main__":
    gauss_eval = [[3, 4, 5, 7, 5, 4, 3],
              [4, 6, 8, 10, 8, 6, 4],
              [5, 8, 11, 13, 11, 8, 5],
              [6, 10, 13, 15, 13, 10, 6],
              [5, 8, 11, 13, 11, 8, 5],
              [4, 6, 8, 10, 8, 6, 4],
              [3, 4, 5, 7, 5, 4, 3]]
    draw_table_score(gauss_eval)
    write_2_file(gauss_eval, 20, 4, 'gauss_board')
