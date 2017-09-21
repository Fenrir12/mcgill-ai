import sys
from telnetlib import *

from DynamicConnect4 import game

from DynamicConnect4Interface import draw_table_score

if __name__ == "__main__":
    # Setup game
    host = sys.argv[1]
    port = sys.argv[2]
    game_id = sys.argv[3]
    color = sys.argv[4]
    dc4 = game()
    dc4.USE_PRUNING = (sys.argv[5].lower() == 'true')
    dc4.time_limit = 9
    dc4.depth_limit = int(sys.argv[6])
    board = dc4.board

    # Setup link to game server
    netlink = Telnet()
    netlink.open(host, port, 10000)
    netlink.write(game_id + ' ' + color + "\n")
    print(netlink.read_until(b"\n"))
    if color == 'white':
        player = dc4.MinPlayer
        isTurn = True
    else:
        player = dc4.MaxPlayer
        isTurn = False
    while True:
        if isTurn:
            dc4.no_of_turns += 1
            print("----------------------")
            print("My turn (" + str(dc4.no_of_turns) + ")\n")
            best_move = dc4.find_best_move(board, player)
            board = dc4.do_move(board, best_move, player)
            netlink.write(dc4.send_move(best_move))
            print(netlink.read_until(b"\n"))
            draw_table_score(board)
            print("----------------------")
            score = dc4.is_winning(board)

            if player == dc4.MinPlayer:
                if score == 100:
                    print('Other player won')
                    break
                elif score == -100:
                    print('I won in ' + str(dc4.no_of_turns))
                    break
            else:
                if score == 100:
                    print('I won in ' + str(dc4.no_of_turns))
                    break
                elif score == -100:
                    print('Other player won')
                    break
            dc4.no_of_nodes = 0
            isTurn = False
        else:
            print("----------------------")
            print("Other turn\n")
            string = netlink.read_until(b"\n")
            print(string)
            board = dc4.do_move(board, dc4.convert_move(string), not player)
            draw_table_score(board)
            print("----------------------")
            isTurn = True
