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
        with self.assertRaises(ValueError):
            Likelihood(-1)
        self.assertEqual(self.likelihood["name"], str(LAM))
        self.assertEqual(self.likelihood["lam"], LAM)
        self.assertIsNotNone(self.likelihood.plot())


if __name__ == "__main__":
    unittest.main()
