
class DAG:

    nodes = {}

    def __init__(self):
        self.nodes = {}

    @classmethod
    def find(cls, id):
        rappre = cls.nodes[id]
        if rappre.id == rappre.find:
            return rappre.id
        else:
            return cls.find(rappre.find)

    def is_satisfable(self, diseq):
        print("da sistemare")

    def merge(self, n1, n2):
        if n1.id != n2.id:
            p1 = n1.ccpar
            p2 = n2.ccpar
            print("n1 = ", n1.id, p1)
            print("n2 = ", n2.id, p2)
            self.union(n1, n2)
            print("n1 = ", self.id, self.find, self.ccpar)
            print("n2 = ", n2.id, n2.find, n2.ccpar)
            for i in p1:
                for j in p2:
                    print(i, j, i.congruent(j))
                    if i.find != j.find and i.congruent(j):
                        self.merge(i, j)

    def union(self, n1, n2):
        id1 = DAG.find(n1.id)
        id2 = DAG.find(n2.id)
        self.nodes[id1].find = id2
        for par1 in self.nodes[id1].ccpar:
            self.nodes[id2].add_parent(par1)
        self.nodes[n1].ccpar = []
