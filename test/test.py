import unittest
from node import Node
from parser import Parser
from dag import DAG


class TestParser(unittest.TestCase):

    def test_parser(self):
        # test costruzione liste eq, diseq e costruttore parser
        d = DAG()
        input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
        riseq = [[hash("f(a)"), hash("a")], [hash("f(b)"), hash("c")]]
        risdiseq = [[hash("f(f(a))"), hash("b")]]
        p = Parser(input, d)
        self.assertEqual(p.eq, riseq)
        self.assertEqual(p.diseq, risdiseq)

    def test_nodetermine(self):
        # test inserimento nodi
        d = DAG()
        input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
        p = Parser(input, d)
        testnode = {hash("f(a)"): "f(a)", hash("a"): "a", hash("f(b)"): "f(b)", hash("c"): "c",
                    hash("f(f(a))"): "f(f(a))", hash("b"): "b"}
        self.assertEqual(p.nodes, testnode)

    def test_findsons(self):
        # test ricostruzione args
        args = ["f(a,b)", "b"]
        self.assertEqual(Parser.find_sons("f(f(a,b),b)", 1), args)

    def test_buildnode(self):
        # test costruzione nodi
        d = DAG()
        input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
        p = Parser(input, d)
        n1 = Node(hash("f(a)"), "f", hash("f(a)"), [hash("a")])
        n1.add_parent(hash("f(f(a))"))
        n2 = Node(hash("a"), "a", hash("a"), [])
        n2.add_parent(n1.id)
        testnode = {hash("f(a)"): n1, hash("a"): n2}
        for i in testnode.keys():
            if i not in d.nodes.keys():
                self.assertFalse(False)
            n = d.nodes[i]
            if n.id != testnode[i].id or n.fn != testnode[i].fn or n.ccpar != testnode[i].ccpar \
                    or n.find != testnode[i].find or n.args != testnode[i].args or n.enemies != testnode[i].enemies:
                self.assertFalse(False)
        self.assertTrue(True)


class TestDag(unittest.TestCase):

    def test_congruent(self):
        # test congruenza nodi
        d = DAG()
        input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
        p = Parser(input, d)
        self.assertFalse(d.congruent(d.nodes[hash("f(f(a))")], d.nodes[hash("b")]))
        d.merge(d.nodes[hash("f(a)")], d.nodes[hash("a")])
        self.assertTrue(d.congruent(d.nodes[hash("f(f(a))")], d.nodes[hash("f(a)")]))

    def test_union(self):
        # test unione dei nodi
        d = DAG()
        input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
        p = Parser(input, d)
        n1 = Node(hash("f(a)"), "f", hash("f(a)"), [hash("a")])
        n1.add_parent(hash("f(f(a))"))
        n1.add_parent(n1.id)
        n2 = Node(hash("a"), "a", hash("f(a)"), [])
        d.union(d.nodes[hash("a")], d.nodes[hash("f(a)")])
        u1 = d.nodes[hash("a")]
        u2 = d.nodes[hash("f(a)")]
        if u1.id == n2.id and u1.find == n2.find and u1.ccpar == n2.ccpar and u1.fn == n2.fn \
                and u1.enemies == u2.enemies:
            if u2.id == n1.id and u2.find == n1.find and u2.ccpar == n1.ccpar and u2.fn == n1.fn \
                    and u2.enemies == u1.enemies:
                self.assertTrue(True)

    def test_merge(self):
        # test merge dei nodi e propagazione del merge
        # self.assertTrue(self.d.merge(self.d.nodes[hash("f(a)")], self.d.nodes[hash("a")]))
        d = DAG()
        input = ["f(a) = a", "f(b) = c", "f(f(a)) != b"]
        p = Parser(input, d)
        d.nodes[hash("f(f(a))")].add_enemies((hash("a")))
        d.nodes[hash("a")].add_enemies(hash("f(f(a))"))
        self.assertFalse(d.merge(d.nodes[hash("f(a)")], d.nodes[hash("a")]))


if __name__ == "__main__":
    unittest.main()
