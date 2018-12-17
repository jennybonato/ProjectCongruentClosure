from node import Node
import re


class Parser:

    def __init__(self):
        self.nodes = {}

    def division_eq(self, data):
        diseq = []
        eq = []
        for element in data:
            if "!=" in element:
                coppia = re.split('!=', element)
                self.nodes[hash(coppia[0].strip())] = coppia[0].strip()
                self.nodes[hash(coppia[1].strip())] = coppia[1].strip()
                coppia[0] = hash(coppia[0].strip())
                coppia[1] = hash(coppia[1].strip())
                diseq.append(coppia)
            elif "=" in element:
                coppia = re.split('=', element)
                self.nodes[hash(coppia[0].strip())] = coppia[0].strip()
                self.nodes[hash(coppia[1].strip())] = coppia[1].strip()
                coppia[0] = hash(coppia[0].strip())
                coppia[1] = hash(coppia[1].strip())
                eq.append(coppia)
        return eq, diseq

    def parse_data(self, d):
        for coppia in list[0]:
            for element in coppia:
                self.build_node(element.strip(), None, d)
        for coppia in list[1]:
            for element in coppia:
                self.build_node(element.strip(), None, d)
            n1 = d.find_node(hash(coppia[0].strip()))
            n2 = d.find_node(hash(coppia[1].strip()))
            d.nodes[n1].add_enemies(d.nodes[n2].id)
            d.nodes[n2].add_enemies(d.nodes[n1].id)

    @staticmethod
    def find_sons(termine, lenfn):
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

    def build_node(self, termine, parent, d):
        id = hash(termine)
        args = []
        fn = termine
        neq = d.find_node(id)
        if neq >= 0:
            (d.nodes[neq]).add_parent(parent)
        else:
            if "(" in termine:
                fn = termine.split("(")[0]
                sons = self.find_sons(termine, len(fn))
                for s in sons:
                    self.build_node(s, id, d)
                    args.append(hash(s))
            n = Node(id, fn, id, args)
            n.add_parent(parent)
            d.nodes.append(n)
