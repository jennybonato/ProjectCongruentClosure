import re
from parser import Parser
from dag import DAG


def import_data(nameFile):
    with open(nameFile) as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    return data


if __name__ == "__main__":
    input = import_data("data/input1.txt")
    d = DAG()
    p = Parser()
    parsed = p.division_eq(input)
    print(parsed)
    print(p.nodes)
    # print("a =", DAG.nodes[DAG.find(hash("a"))].fn, hash("a"))
    '''
    print("     id                 fn   find               args        ccpar       enemies")
    for n1 in d.nodes:
        print("n = ", n1.id, n1.fn, n1.find, n1.args, n1.ccpar, n1.enemies)
    print('\n\n\n\n')
    for coppiaeq in parsed[0]:
        n3 = d.find_node(hash(coppiaeq[0].strip()))
        n3.merge(hash(coppiaeq[1].strip()))
    print("Soddisfacibile = ", d.is_satisfable(parsed[1]))

    print("     id                 fn   find               args        ccpar       enemies")
    for n1 in d.nodes:
        print("n = ", n1.id, n1.fn, n1.find, n1.args, n1.ccpar, n1.enemies)

    print('\n\n\n\n\n')
    n = d.nodes[DAG.find_node(hash("a"))]
    print(n.id, n.find)
    print(DAG.find(n))
    
    for i in DAG.nodes:
        print("id = ", i.id)
        print("fn = ", i.fn)
        print("find = ", i.find)
        print("ccpar = ", i.ccpar)
        print("args = ", i.args)
        print("enemies = ", i.enemies)
    '''
