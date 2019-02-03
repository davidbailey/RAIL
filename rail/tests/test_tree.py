import unittest

from rail import Tree

class TestTree(unittest.TestCase):
    def setUp(self):
        self.tree = Tree(name='test tree')
        self.tree.addChild('test child')

    def test_tree(self):
        self.assertEqual(self.tree.name, 'test tree')
        self.assertEqual(self.tree.parent, None)
        self.assertEqual(self.tree['test child'].name, 'test child')
        self.assertEqual(self.tree['test child'].parent, self.tree)

    def test_path(self):
        self.assertEqual(self.tree['test child'].path(), '/test tree/test child')

    def test_to_dict_list(self):
        self.assertEqual(self.tree.to_dict_list(), {'name': 'test tree', 'children': [{'name': 'test child', 'children': []}]})

if __name__ == '__main__':
    unittest.main()

