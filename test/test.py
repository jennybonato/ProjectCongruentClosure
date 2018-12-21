import unittest
from node import Node
from parser import Parser
from dag import  DAG


class TestSodisfableProcedure(unittest.TestCase):

    d = DAG()
    input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
    riseq = [[hash("f(a)"), hash("a")], [hash("f(b)"), hash("c")]]
    risdiseq = [[hash("f(f(a))"), hash("b")]]
    p = Parser(input, d)

    def test_parser(self):
        # test costruzione liste eq, diseq
        self.assertEqual(self.p.eq, self.riseq)
        self.assertEqual(self.p.diseq, self.risdiseq)

    def test_nodetermine(self):
        # test inserimento nodi
        testnode = {hash("f(a)"): "f(a)", hash("a"): "a", hash("f(b)"): "f(b)", hash("c"): "c",
                    hash("f(f(a))"): "f(f(a))", hash("b"): "b"}
        self.assertEqual(self.p.nodes, testnode)

    def test_findsons(self):
        # test ricostruzione args
        args = ["f(a)", "g(h(b,c,d))"]
        self.assertEqual(Parser.find_sons("f(f(a), g(h(b,c,d)))", 1), args)

    def test_buildnode(self):
        # test costruzione nodi
        n1 = Node(hash("f(a)"), "f", hash("f(a)"), [hash("a")])
        n1.add_parent(hash("f(f(a))"))
        n2 = Node(hash("a"), "a", hash("a"), [])
        n2.add_parent(n1.id)
        testnode = {hash("f(a)"): n1, hash("a"): n2}
        for i in testnode.keys():
            if i not in self.d.nodes.keys():
                self.assertFalse(False)
            n = self.d.nodes[i]
            if n.id != testnode[i].id or n.fn != testnode[i].fn or n.ccpar != testnode[i].ccpar \
                    or n.find != testnode[i].find or n.args != testnode[i].args or n.enemies != testnode[i].enemies:
                self.assertFalse(False)
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()

