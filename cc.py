from node import Node
import re
from dag import DAG

def import_data(nameFile):
    with open(nameFile) as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    return data


def parse_data(data):
    diseq = []
    eq = []
    for element in data:
        if "!=" in element:
            list_node = re.split('!=', element)
            diseq.append(list_node)
        elif "=" in element:
            list_node = re.split('=', element)
            eq.append(list_node)

    return eq, diseq


if __name__ == "__main__":
    input = import_data("data/input1.txt")
    parsed = parse_data(input)
    #d = DAG()
    #d.build_dag(parsed)
    #print(parsed)

    print(DAG.find_sons("f(f(a,b),f(b))"))