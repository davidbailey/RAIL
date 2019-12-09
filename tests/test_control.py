"""
Tests for the Control and Controls classes
"""
import unittest

from rail import Control, Controls


class TestControls(unittest.TestCase):
    """
    Class to test a control
    """

    def setUp(self):
        self.controls = Controls()
        self.controls.new("test control", 100, 0.1)

    def test_controls(self):
        """
        Test controls
        """
        self.assertEqual(self.controls["test control"]["name"], "test control")
        self.assertEqual(self.controls["test control"]["cost"], 100)
        self.assertEqual(self.controls["test control"]["reduction"], 0.1)


if __name__ == "__main__":
    unittest.main()
