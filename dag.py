
class DAG:

    nodes = {}

    def __init__(self):
        self.nodes = {}

    @classmethod
    def find_node(cls, id):
        for n in cls.nodes:
            if n.id == id:
                return DAG.nodes.index(n)
        return -1

    @classmethod
    def find(cls, id):
        for i in cls.nodes:
            if i.id == id:
                if i.id == i.find:
                    print("ramo if ", i.id, i.find)
                    return i.id
                else:
                    print("ramo else ", i.id, i.find)
                    return cls.find(i.find)

    def is_satisfable(self, diseq):
        for coppia in diseq:
            e1 = hash(coppia[0].strip())
            e2 = hash(coppia[1].strip())
            if self.find(e1) == self.find(e2):
                return False
        return True
