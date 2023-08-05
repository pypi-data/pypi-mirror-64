import unittest
from netaddr import IPNetwork
from networksearch.networksearch import NetworkTree
class TestNetworkSearch(unittest.TestCase):

    def test_overlaps(self):
        tree = NetworkTree()
        tree.add("9.0.0.0-10.0.0.2")
        tree.add("192.168.0.1")
        tree.add("192.168.0.0/24")
        tree.add("192.168.0.0/22")
        tree.add("192.168.0.0/23")

        self.assertTrue(tree.overlaps("192.168.0.2"))

    def test_remove_duplicate(self):
        tree = NetworkTree()
        tree.add("9.0.0.0-10.0.0.2")
        tree.add("192.168.0.1")
        tree.add("192.168.0.0/24")
        tree.add("192.168.0.0/22")
        tree.add("192.168.0.0/23")

        expected = [
            IPNetwork("9.0.0.0/8"),
            IPNetwork("10.0.0.0/31"),
            IPNetwork("10.0.0.2/32"),
            IPNetwork("192.168.0.0/22")
        ]
        tree_list = list(tree.runTree())

        self.assertListEqual(tree_list, expected)

if __name__ == '__main__':
    unittest.main()