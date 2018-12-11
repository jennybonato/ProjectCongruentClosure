from node import Node


class DAG:
    nodes = []

    @classmethod
    def find_sons(cls, termine, lenfn):
        i = lenfn + 1
        sons = []
        index_son = i
        par = 0
        while i < len(termine):
            if termine[i] == '(':
                par = 1
            elif termine[i] == ')' and par == 1:
                par = 0
            elif (termine[i] == ',' and par == 0) or (termine[i] == ')' and par == 0):
                sons.append(termine[index_son:i])
                index_son = i + 1
            i = i + 1
        return sons

    @classmethod
    def find_node(cls, id):
        for n in DAG.nodes:
            if n.id == id:
                return n
        return None

    @classmethod
    def build_node(cls, termine, parent):
        id = hash(termine)
        sons = []
        args = []
        fn = termine
        neq = DAG.find_node(id)
        if neq is not None:
            neq.add_parent(parent)
        else:
            if "(" in termine:
                fn = termine.split("(")[0]
                sons = DAG.find_sons(termine, len(fn))
                for s in sons:
                    DAG.build_node(s, id)
                    args.append(hash(s))
            n = Node(id, fn, id, args)
            n.add_parent(parent)
            DAG.nodes.append(n)

    @classmethod
    def build_dag(cls, list):
        dag = []
        # eq
        for coppia in list[0]:
            for element in coppia:
                DAG.build_node(element.strip(), None)
        for coppia in list[1]:
            for element in coppia:
                DAG.build_node(element.strip(), None)
#            DAG.find_node(hash(coppia[0])).add_enemies(n2)
 #           DAG.find_node(hash(coppia[1])).add_enemies(n1)
