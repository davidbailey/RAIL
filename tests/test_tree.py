"""
Tests for the Tree class
"""
import unittest
from unittest import mock

from rail import Tree

class TestTree(unittest.TestCase):
    """
    Class to test a Tree.
    """
    def setUp(self):
        self.tree = Tree(name='test tree')
        self.tree.add_child('test child')

    def test_tree(self):
        """
        Test the attributes of a Tree.
        """
        self.assertEqual(self.tree.name, 'test tree')
        self.assertEqual(self.tree.parent, None)
        self.assertEqual(self.tree['test child'].name, 'test child')
        self.assertEqual(self.tree['test child'].parent, self.tree)

    def test_path(self):
        """
        Test the path method of a Tree.
        """
        self.assertEqual(self.tree['test child'].path(), '/test tree/test child')

    def test_print(self):
        """
        Test the to_print method of a Tree.
        """
        with mock.patch('builtins.print') as mock_print:
            self.assertEqual(self.tree['test child'].to_print(), None)
            mock_print.assert_called_once_with('/test tree/test child')
            mock_print.reset_mock()
            self.assertEqual(self.tree.to_print(), None)
            mock_print.assert_called()
            mock_print.assert_has_calls([
                mock.call('/test tree'),
                mock.call('/test tree/test child')
            ])

    def test_to_latex(self):
        """
        Test the to_latex method of a Tree.
        """
        with mock.patch('builtins.print') as mock_print:
            self.assertEqual(self.tree.to_latex(), None)
            mock_print.assert_called()
            mock_print.assert_has_calls([
                mock.call('child { node{test tree}'),
                mock.call('child { node{test child}'),
                mock.call('}'),
                mock.call('}')
            ])

    def test_to_dict_list(self):
        """
        Test the to_dict_list method of a Tree.
        """
        self.assertEqual(
            self.tree.to_dict_list(),
            {'name': 'test tree', 'children': [{'name': 'test child', 'children': []}]}
        )

if __name__ == '__main__':
    unittest.main()
