import random
import sys
import time
from telnetlib import *

from DynamicConnect4_v0 import game

if __name__ == "__main__":
    # Setup game
    host = sys.argv[1]
    port = sys.argv[2]
    game_id = sys.argv[3]
    color = sys.argv[4]
    dc4 = game()
    dc4.USE_PRUNING = True
    dc4.time_limit = 9
    dc4.depth_limit = 4
    board = dc4.board
    player = dc4.MaxPlayer

    netmoves = []
    for row in [1, 2, 3, 4, 5, 6, 7]:
        for col in [1, 2, 3, 4, 5, 6, 7]:
            for char in ['N', 'S', 'W', 'E']:
                netmoves.append(str(row) + str(col) + char)

    # Setup link to game server
    netlink = Telnet()
    netlink.open(host, port, 10000)
    print(netlink.read_eager())
    netlink.write((game_id + ' ' + color + "\n"))
    print(netlink.read_eager())
    while True:
        netlink.write((random.choice(netmoves)+"\n"))
        print(netlink.read_eager())
        time.sleep(5)