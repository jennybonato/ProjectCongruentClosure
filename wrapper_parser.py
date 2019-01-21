import re
from parser import Parser


class WrapperParser:

    def __init__(self, data, d):
        self.datas = []
        self.dags = []
        self.parsers = []
        self.parse_operator(data)

    def ccsatisfable(self, d):
        satisfable_all = False
        for set in self.datas:
            p = Parser(set, d)
            satisfable_one = True
            for coppiaeq in p.eq:
                if satisfable_one:
                    satisfable_one = d.merge(d.nodes[coppiaeq[0]], d.nodes[coppiaeq[1]])
            if satisfable_one:
                satisfable_all = True
            self.parsers.append(p)
            self.dags.append(d)
        return satisfable_all

    def parse_operator(self, data):
        op = None
        for element in data:
            count = 0
            data_build = []
            for i in element:
                if i == ")":
                    count -= 1
                if i == "(":
                    count += 1
                if count == 0:
                    j = element.index(i) + 1
                    op = (re.split('\(', element[j:])[0]).strip()
                    data_build.append(element[0:j - 1])
                    i = j + len(op) - 1
                    data_build.append(element[i:])
                    break
            self.parse_division(element, data_build, op, data)

    def parse_division(self, element, data_build, op, data):
        if op == "and":
            self.parse_and(element, data_build)
        elif op == "or":
            self.parse_or(element, data_build, data)
        elif op == "implies":
            self.parse_implies(data_build)

    def parse_and(self, element, data):
        self.data.remove(element)
        self.data.append(data[0])
        self.data.append(data[1])

    def parse_or(self, element, data_build, data):
        data1 = data
        data1.remove(element)
        data1.append(data_build[0])
        data2 = data
        data2.remove(element)
        data2.append(data_build[1])
        self.datas.append(data1)
        self.datas.append(data2)

    def parse_implies(self, element, data_build):
        self.data.remove(element)
        self.data.append("not(" + data_build[0] + ") or " + data_build[1])
