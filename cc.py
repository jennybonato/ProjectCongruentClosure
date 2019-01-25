from parser import Parser
from dag import DAG
import time
import sys


def import_data(name_file):
    with open(name_file) as f:
        data = [line.rstrip('\n') for line in f.readlines()]
    return data


if __name__ == "__main__":
    runtime = []
    # import data from file
    start = time.clock()
    if len(sys.argv) < 2:
        print("Input non valido è necessario inserire un file di input. \n Riprova con \t \"python3 cc.py <file>\"")
    else:
        file = "data/" + sys.argv[1]
        input = import_data(file)
        # initialize DAG
        d = DAG()
        p = Parser(input, d)

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

        if satisfable:
            # print results
            print('\n\n')
            for i in d.nodes.keys():
                print("id =", d.nodes[i].id, "|     fn = ", d.nodes[i].fn, "|       find = ", d.find(i),
                      "|       args = ", d.nodes[i].args, "|       par = ", d.nodes[i].ccpar,
                      "|        enemies = ", d.nodes[i].enemies)

        end = time.clock()
        print('\n\n')
        print("Run in :", end-start)
        print("-"*180)
