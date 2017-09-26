import random

class TransTable:
    def __init__(self):
        self.table_white = random.sample(range(0, 2**16-1), 49*6)
        self.table_black = self.table_white = random.sample(range(0, 2**16-1), 49*6)
        self.num_of_hash_white = 0
        self.num_of_hash_black = 0

    def lookup(self):
        pass

    def store(self, node, depth, score):
        new_hash = self.table[self.num_of_hash]
        self.num_of_hash += 1