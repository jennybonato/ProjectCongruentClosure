import re
from parser import Parser


class WrapperParser:

    def __init__(self, data, dag):
        self.clauses = []
        self.dags = []
        self.parsers = []
        self.parse_operator(data)
        for set in self.clauses:
            p = Parser(set, dag)
            self.parsers.append(p)
            self.dags.append(dag)

    def ccsatisfable(self):
        satisfable_all = False
        satisfable_one = True
        for index in range(0, len(self.clauses)-1):
            d = self.dags[index]
            for coppiaeq in self.parsers[index].eq:
                if satisfable_one:
                    satisfable_one = d.merge(d.nodes[coppiaeq[0]], d.nodes[coppiaeq[1]])
            if satisfable_one:
                satisfable_all = True
        return satisfable_all

    def parse_arg(self, element, op):
        i = len(op)
        count = 0
        while True:
            if element[i] == ")":
                count -= 1
            if element[i] == "(":
                count += 1
            if count == 0 and element[i] == ",":
                return [element[len(op):i-1], element[i+1:]]
            i += 1

    def parse_operator(self, data):
        op = None
        for clause in data:
            clause = clause.strip()
            op = re.split(clause, '(')[0]
            data_build = self.parse_arg(clause, op)
            if op == "not":
                clause = self.change_sign(clause, op)
            elif op == "and":
                self.parse_and(clause, op, data_build)
                # arg = self.parse_operator(data_build)
            elif op == "or":
                self.parse_or(clause, op, data_build)
            elif op == "implies":
                clause = self.parse_implies(clause, op, data_build)
        self.clauses.append(data)

    def parse_and(self, element, data_build):
        self.clauses.remove(element)
        self.clauses.append(data_build[0])
        self.clauses.append(data_build[1])

    def parse_or(self, element, data_build, data):
        data1 = data[:]
        data2 = data[:]
        data1.remove(element)
        data2.remove(element)
        data1.append(data_build[0])
        data2.append(data_build[1])
        self.clauses.append(data1)
        self.clauses.append(data2)

    def change_sign(self, termine):
        op = re.split(termine, '(')[0]
        data_build = self.parse_arg(termine, op)
        if op == "!=":
            return "=" + termine[1:]
        elif op == "=":
            return "!=" + termine[2:]
        elif op == "and":
            arg1 = self.change_sign(data_build[0])
            arg2 = self.change_sign(data_build[1])
            return "or(" + arg1 + "," + arg2 + ")"
        elif op == "or":
            arg1 = self.change_sign(data_build[0])
            arg2 = self.change_sign(data_build[1])
            return "and(" + arg1 + "," + arg2 + ")"
        elif op == "implies":
            arg1 = self.change_sign(data_build[0])
            return "or(" + arg1 + "," + data_build[1] + ")"

    def parse_implies(self, element, data_build, data):
        data.remove(element)
        data.append("or(not(" + data_build[0] + "), " + data_build[1] + ")")
