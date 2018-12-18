from parser import Parser
from dag import DAG


def import_data(name_file):
    with open(name_file) as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    return data


if __name__ == "__main__":
    # import data from file
    input = import_data("data/input1.txt")

    # initialize DAG
    d = DAG()

    # parse data and build DAG
    p = Parser(input, d)
    print(p.nodes)

    # print all node
    for i in d.nodes.keys():
        print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       find = ", d.find(i),
              "|       args = ", d.nodes[i].args, "|       par = ", d.nodes[i].ccpar,
              "|        enemies = ", d.nodes[i].enemies)

    # merge of all node that are in equivalence relation
    soddisfable = True
    for coppiaeq in p.eq:
        print("Nuova coppia", coppiaeq)
        if not d.merge(d.nodes[coppiaeq[0]], d.nodes[coppiaeq[1]]):
            soddisfable = False
    print("Soddisfacibile = ", soddisfable)

    # print results
    print('\n\n\n\n\n')
    for i in d.nodes.keys():
        print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       find = ", d.find(i),
              "|       args = ", d.nodes[i].args, "|       par = ", d.nodes[i].ccpar,
              "|        enemies = ", d.nodes[i].enemies)
