
class DAG:

    nodes = {}

    def __init__(self):
        self.nodes = {}

    '''
    this function return a node that are the rappre of the equivalence class which id belongs.
    '''
    def find(self, id):
        rappre = self.nodes[id]
        if rappre.id == rappre.find:
            return rappre.id
        else:
            return self.find(rappre.find)

    '''
    this function merge two nodes of a dag only if their find attribute are different 
    and the first isn't on the second's enemies list. It also returns if two nodes can be merge or not.
    '''
    def merge(self, n1, n2):
        f1 = self.find(n1.id)
        f2 = self.find(n2.id)
        satisfable = True
        # check if there aren't enemies in the equivalence class of other node
        for ene1 in self.nodes[f1].enemies:
            if ene1 in self.nodes[f2].friends:
                return False
        for ene2 in self.nodes[f2].enemies:
            if ene2 in self.nodes[f1].friends:
                return False

        if n1.id != n2.id and self.find(n1.id) != self.find(n2.id):
            p1 = n1.ccpar
            p2 = n2.ccpar
            self.union(n1, n2)
            for i in p1:
                for j in p2:
                    if satisfable:
                        if self.find(i) != self.find(j) and self.congruent(self.nodes[i], self.nodes[j]):
                            satisfable = self.merge(self.nodes[i], self.nodes[j])
        return satisfable

    '''
    this function union two nodes of a dag, it puts the first node's parents in the second node's parent
    and the first node'find attribute in the second node's find attribute
    '''
    def union(self, n1, n2):
        id1 = self.find(n1.id)
        id2 = self.find(n2.id)

        # select representative of the bigger equivalence class, if their equals chooses the second
        if len(self.nodes[id1].friends) > len(self.nodes[id2].friends):
            rappre = self.nodes[id1]
            other = self.nodes[id2]
        else:
            rappre = self.nodes[id2]
            other = self.nodes[id1]

        # union of nodes
        other.find = rappre.id
        for par in other.ccpar:
            rappre.add_parent(par)
        for ene in other.enemies:
            rappre.add_enemies(ene)
        for friend in other.friends:
            rappre.add_friend(friend)
        other.ccpar = []
        other.enemies = []
        other.friends = []

        # update find field of nodes in "other" equivalence class
        for i in self.nodes.keys():
            if i == other:
                self.nodes[i].find = rappre

    '''
    this function stabilises if two node of a dag are in equivalence relation
    '''
    def congruent(self, n1, n2):
        ris = True
        if n1.fn == n2.fn and len(n1.args) == len(n2.args):
            for a1 in n1.args:
                if ris:
                    ris = False
                    for a2 in n2.args:
                        if self.find(a1) == self.find(a2):
                            ris = True
        else:
            return False
        return ris
