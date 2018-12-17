import re
from parser import Parser
from dag import DAG


def import_data(name_file):
    with open(name_file) as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    return data


if __name__ == "__main__":
    input = import_data("data/input1.txt")
    d = DAG()
    p = Parser(input, d)
    print(p.nodes)

    for i in d.nodes.keys():
        print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       args = ",
              d.nodes[i].args, "|       par = ", d.nodes[i].ccpar, "|        enemies = ", d.nodes[i].enemies)

    for coppiaeq in p.eq:
        d.merge(d.nodes[coppiaeq[0]], d.nodes[coppiaeq[1]])
    print("Soddisfacibile = ", d.is_satisfable(p.diseq))

    print('\n\n\n\n\n')
    for i in d.nodes.keys():
        print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       args = ",
              d.nodes[i].args, "|       par = ", d.nodes[i].ccpar, "|        enemies = ", d.nodes[i].enemies)
