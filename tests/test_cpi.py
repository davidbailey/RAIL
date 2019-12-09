"""
Tests for the CPI class
"""
import unittest

from rail import CPI


class TestCPI(unittest.TestCase):
    """
    Class to test a CPI.
    """

    def setUp(self):
        self.cpi = CPI()

    def test_inflation(self):
        """
        Test the inflation calculation method.
        """
        self.assertEqual(self.cpi.inflation(2010, 2010), 1.0)
        self.assertEqual(self.cpi.inflation(2010, 2018), 1.1496494816926013)


if __name__ == "__main__":
    unittest.main()
