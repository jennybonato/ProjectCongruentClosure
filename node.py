from dag import DAG


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

    def congruent(self, n2):
        ris = False
        if self.fn == n2.fn and len(self.args) == len(n2.args):
            for a1 in self.args:
                for a2 in n2.args:
                    if a1.find == a2.find:
                        ris = True
                if not ris:
                    return False
        return True
