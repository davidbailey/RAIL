"""
Tests for the Likelihood class
"""
import unittest

from rail import Likelihood

class TestLikelihood(unittest.TestCase):
    """
    Class to test a likelihood
    """
    def setUp(self):
        self.likelihood = Likelihood(.5)

    def test_likelihood(self):
        """
        Test a likelihood
        """
        self.assertEqual(self.likelihood['name'], '0.5')
        self.assertEqual(self.likelihood['lam'], .5)


if __name__ == '__main__':
    unittest.main()
