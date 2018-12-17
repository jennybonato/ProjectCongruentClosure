

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

    def union(self, n2):
        n2.find = self.find
        for par1 in self.ccpar:
            n2.add_parent(par1)
        self.ccpar = []
        return self, n2

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

    def merge(self, n2):
        if self.id != n2.id:
            p1 = self.ccpar
            p2 = n2.ccpar
            print("n1 = ", self.id, p1)
            print("n2 = ", n2.id, p2)
            self.union(self.find(self.id), self.find(n2.id))
            print("n1 = ", self.id, self.find, self.ccpar)
            print("n2 = ", n2.id, n2.find, n2.ccpar)
            for i in p1:
                for j in p2:
                    print(i, j, i.congruent(j))
                    if i.find != j.find and i.congruent(j):
                        i.merge(j)
