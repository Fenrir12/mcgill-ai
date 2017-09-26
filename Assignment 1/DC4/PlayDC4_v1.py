import sys
from telnetlib import *

from DynamicConnect4_v0 import game_v0
from DynamicConnect4_v1 import game_v1
import time

from DynamicConnect4Interface import draw_table_score


def start_auto_game(color, version):
    # Select game version
    if version == "v0":
        game = game_v0()
    elif version == "v1":
        game = game_v1()
    # Select starting player
    if color == "white":
        player = game.MaxPlayer
    elif color == "black":
        player = game.MinPlayer

    board = game.board
    game.time_limit = 9
    game.depth_limit = 2
    game.USE_PRUNING = True
    score = 0

    while True:
        # Update board with best move of each player
        best_move = game.find_best_move(board, player)
        board = game.do_move(board, best_move, player)
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


def start_server_game(host, port, game_id, color, version):
    # Setup link to game server
    netlink = Telnet()
    netlink.open(host, port, 10000)
    netlink.write(game_id + ' ' + color + "\n")
    print(netlink.read_until(b"\n"))

    # Import agent version
    if version == 'v0':
        dc4 = game_v0()
        dc4.depth_limit = 6
    elif version == 'v1':
        dc4 = game_v1()
        dc4.USE_ITERATIVE_DEEPENING = True
        dc4.depth_limit = 6

    dc4.USE_PRUNING = True
    dc4.time_limit = 9
    board = dc4.board
    player = dc4.MaxPlayer
    # Define player's color
    if color == 'white':
        isTurn = True
    elif color == "black":
        isTurn = False

    # Enter game
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

            if version == 'v0':
                score = dc4.is_winning(board)
            elif version == 'v1':
                score = dc4.is_winning(board, player)

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


if __name__ == "__main__":
    # Setup game
    while True:
        type_of_game = (raw_input("Do you want to : \n "
                                 "1 - play on the game server\n "
                                 "or \n "
                                 "2 - look at me playing with myself? \n"
                                 "Press 1 or 2\n"))
        if '1' in type_of_game :
            host = (raw_input("Enter the IP of the game server : \n"))
            port = (raw_input("Enter the port of the game server : \n"))
            game_id = (raw_input("Enter the game id : \n"))
            color = (raw_input("Enter your color : \n"))
            version = (raw_input("Enter the version of the agent you want to use (v0, v1) : \n"))
            print("Bring it on!\n\n")
            start_server_game(host, port, game_id, color, version)
            break
        elif type_of_game == "2":
            print("Wow... weird...")
            time.sleep(4)
            color = (raw_input("Enter starting color : \n"))
            version = (raw_input("Enter the version of the agent you want to use (v0, v1) : \n"))
            print("Let's look at my awesomness\n\n")
            start_auto_game(color, version)
            break
        else:
            print("Choice invalid\n\n")
