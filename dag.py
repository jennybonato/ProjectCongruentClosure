
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
        f2 = self.find(n2.id)
        print("Nuovo merge", n1.id, self.nodes[f2].enemies)
        sodisfable = True
        if n1.id in self.nodes[f2].enemies:
            return False
        if n1.id != n2.id and n1.find != n2.find:
            p1 = n1.ccpar
            p2 = n2.ccpar
            self.union(n1, n2)
            for i in p1:
                for j in p2:
                    print(i, self.nodes[j].enemies)
                    print(sodisfable)
                    if self.find(i) != self.find(j) and self.congruent(self.nodes[i], self.nodes[j]):
                        if sodisfable:
                            sodisfable = self.merge(self.nodes[i], self.nodes[j])
        return sodisfable
    '''
    this function union two nodes of a dag, it puts the first node's parents in the second node's parent
    and the first node'find attribute in the second node's find attribute
    '''
    def union(self, n1, n2):
        id1 = self.find(n1.id)
        id2 = self.find(n2.id)
        self.nodes[id1].find = id2
        for par1 in self.nodes[id1].ccpar:
            self.nodes[id2].add_parent(par1)
        for ene1 in self.nodes[id1].enemies:
            self.nodes[id2].add_enemies(ene1)
        self.nodes[id1].ccpar = []
        self.nodes[id1].enemies = []

    '''
    this function stabilises if two node of a dag are in equivalence relation
    '''
    def congruent(self, n1, n2):
        ris = False
        if n1.fn == n2.fn and len(n1.args) == len(n2.args):
            for a1 in n1.args:
                for a2 in n2.args:
                    if self.nodes[a1].find == self.nodes[a2].find:
                        ris = True
                if not ris:
                    return False
        return True
