

class Node:

    def __init__(self, id, fn, find, args):
        self.id = id
        self.fn = fn
        self.find = find
        self.ccpar = []
        self.args = args
        self.enemies = []

    def add_enemies(self, node):
        self.enemies.append(node)

    def add_parents(self, parent):
        self.ccpar.append(parent)
