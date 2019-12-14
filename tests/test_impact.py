"""
Tests for the Impact class
"""
import unittest

import numpy as np

from rail import Impact

NAME = "Test Impact"
MU = 100
SIGMA = 10


class TestImpact(unittest.TestCase):
    """
    Class to test an impact
    """

    def setUp(self):
        self.impact = Impact(NAME, MU, SIGMA)

    def test_impact(self):
        """
        Test a impact
        """
        self.assertEqual(self.impact["name"], NAME)
        self.assertEqual(self.impact["mu"], MU)
        self.assertEqual(self.impact["sigma"], SIGMA)
        self.assertEqual(self.impact["mean"], np.exp(MU + SIGMA ** 2 / 2))
        self.assertEqual(self.impact["median"], np.exp(MU))


if __name__ == "__main__":
    unittest.main()
