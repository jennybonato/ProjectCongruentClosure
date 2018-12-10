import re
from node import Node

class DAG:

    def __init__(self):
        self.nodes = []

    @staticmethod
    def find_sons(termine):
        i = len(termine.split("(")[0])+1
        print("fn = ", i)
        sons = []
        count = 0
        index_son = i
        par = 0
        while i < len(termine):
            print(termine[i])
            if termine[i] == '(':
                par = 1
            elif termine[i] == ')' and par ==1:
                par = 0
            elif (termine[i] == ',' and par ==0) or (termine[i] == ')' and par == 0):
                sons.append(termine[index_son:i])
                index_son = i+1
            i = i+1
        print("sons = ", sons)
        return sons


    @staticmethod
    def build_node(termine, parent):
        id = hash(termine)
        if "(" not in termine:
            n = Node(id, termine, id, [])
        else:
            fn = termine.split("(")[0]
            sons = DAG.find_sons(termine)
        return n

    def build_dag(self, list):
        dag = []
        #eq
        for coppia in list[0]:
            for element in coppia:
                self.nodes.append(self.build_node(element.strip()))
