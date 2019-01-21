from node import Node
import re


class Parser:

    def __init__(self, data, d):
        self.nodes = {}
        self.diseq = []
        self.eq = []
        self.parse_data(data, d, False)

    def add_node(self, termine):
        termine = termine.strip()
        self.nodes[hash(termine)] = termine
        son = self.find_sons(termine)
        for i in son:
            self.add_node(i)

    def division_eq(self, data, f):
        for element in data:
            if "!=" in element:
                coppia = re.split('!=', element)
                self.add_node(coppia[0])
                self.add_node(coppia[1])
                coppia[0] = hash(coppia[0].strip())
                coppia[1] = hash(coppia[1].strip())
                self.diseq.append(coppia)
            elif "=" in element:
                coppia = re.split('=', element)
                self.add_node(coppia[0])
                self.add_node(coppia[1])
                coppia[0] = hash(coppia[0].strip())
                coppia[1] = hash(coppia[1].strip())
                self.eq.append(coppia)

    def parse_data(self, data, d, f):
        self.division_eq(data, f)

        # build all nodes
        for element in self.nodes.keys():
            self.build_node(element, None, d)

        # add enemeis
        for coppia in self.diseq:
            d.nodes[coppia[0]].add_enemies(coppia[1])
            d.nodes[coppia[1]].add_enemies(coppia[0])

    @staticmethod
    def find_sons(termine):
        lenfn = len(termine.split("(")[0])
        i = lenfn + 1
        sons = []
        index_son = i
        par = 0
        while i < len(termine):
            if termine[i] == '(':
                par = par + 1
            elif termine[i] == ')' and par > 0:
                par = par - 1
            elif (termine[i] == ',' and par == 0) or (termine[i] == ')' and par == 0):
                if termine[index_son:i] != "":
                    sons.append(termine[index_son:i].strip())
                    index_son = i + 1
            i = i + 1
        return sons

    def build_node(self, element, parent, d):
        args = []
        if element in d.nodes.keys():
            (d.nodes[element]).add_parent(parent)
        else:
            fn = self.nodes[element]
            if "(" in fn:
                fn = self.nodes[element].split("(")[0]
                sons = self.find_sons(self.nodes[element])
                for s in sons:
                    self.build_node(hash(s), element, d)
                    args.append(hash(s))
            n = Node(element, fn, element, args)
            n.add_parent(parent)
            d.nodes[element] = n
