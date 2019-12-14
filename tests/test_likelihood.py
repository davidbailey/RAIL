"""
Tests for the Likelihood class
"""
import unittest

from rail import Likelihood

LAM = 0.5

class TestLikelihood(unittest.TestCase):
    """
    Class to test a likelihood
    """

    def setUp(self):
        self.likelihood = Likelihood(LAM)

    def test_likelihood(self):
        """
        Test a likelihood
        """
        self.assertEqual(self.likelihood["name"], str(LAM))
        self.assertEqual(self.likelihood["lam"], LAM)


if __name__ == "__main__":
    unittest.main()
