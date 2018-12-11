

class Node:

    def __init__(self, id, fn, find, args):
        self.id = id
        self.fn = fn
        self.find = find
        self.ccpar = []
        self.args = args
        self.enemies = []

    def add_parent(self, parent):
        if parent is not None:
            self.ccpar.append(parent)

    def add_enemies(self, enemy):
        self.enemies.append(enemy)
