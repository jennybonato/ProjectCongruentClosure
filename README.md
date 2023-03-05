# ProjectCongruentClosure
An app that given a set of clauses return if it's satisfable or not.

The goal of this project is to implement the congruence closure algorithm of first-order logic without quantifiers. This algorithm builds a directed acyclic graph in which a node is a constant or a function symbol and an edge represents the "be argument" relation of the parent node. Every node is unique so exists some node with multiple parents.

To use this program is required to edit a file in put it in the `data` folder. The file have to contain a raw for every equivalence or disequivalence of function symbols or constants. It is possible to introduce predicates different than equality but they will be interpreted as symbol function.

To exec the program run: `python3 cc.py <input_file>`

### Project structure
The project was implemented in python3 and it contains the `data` folder for inputs, the `doc` folder for the documentation that is in `LaTeX`, the `test` folder for the unit test and the `main` folder with the program.

The main bricks of the program are:
- *Node* contains: 
    - the hash of his value
    - eventually his own function symbol
    - the hash of the rapresentative node of the equivalence class which this node belongs
    - the list of his parents
    - the list of his arguments
    - the list of his enemies
    - in the rapresentative node there is also a `friends` list containing all the nodes in the equivalence class that he represents
- *DAG* represents the graph so it contains the nodes, the edges and some functions to operate on the graph such as: merge, union, congruent and find
-  *Parser* contains:
    - the nodes object which it associates the hash of the value to the value
    - the edges lists `eq` and `diseq` in which can be found the couples of nodes that are in a equivalence or disequivalence relation
    - a function that given a list of strings (the raws of the file) it populates the edges lists and the nodes object
    - a function that given the `nodes` object build the node and its arguments node
    - a function that given a `node` returns the list of his arguments
    - a function that given the `diseq` list populates the `enemies` list wich contains the couples of nodes that can not be in the same equivalence class

<!-- ### Significant implementation decisions and heuristics -->
