
class Node:

    # initialization of node
    def __init__(self, id, fn, find, args):
        self.id = id
        self.fn = fn
        self.find = find
        self.ccpar = []
        self.args = args
        self.enemies = []
        self.friends = []
        self.friends.append(id)

    # add parents
    def add_parent(self, parent):
        if parent is not None and parent not in self.ccpar:
            self.ccpar.append(parent)

    # update list of forbitten nodes
    def add_enemies(self, enemy):
        self.enemies.append(enemy)

    # update list of represented nodes
    def add_friend(self, friend):
        if friend not in self.friends:
            self.friends.append(friend)
