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
    print('\n\n')

    # print all node
    for i in d.nodes.keys():
        print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       find = ", d.find(i),
              "|       args = ", d.nodes[i].args, "|       par = ", d.nodes[i].ccpar,
              "|        enemies = ", d.nodes[i].enemies)
    print('\n\n')

    # merge of all node that are in equivalence relation
    satisfable = True
    for coppiaeq in p.eq:
        if satisfable:
            satisfable = d.merge(d.nodes[coppiaeq[0]], d.nodes[coppiaeq[1]])
    print(satisfable)

    # print results
    print('\n\n')
    for i in d.nodes.keys():
        print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       find = ", d.find(i),
              "|       args = ", d.nodes[i].args, "|       par = ", d.nodes[i].ccpar,
              "|        enemies = ", d.nodes[i].enemies)
