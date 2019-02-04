"""
Tests for the ThreatSource and ThreatSources classes
"""
import unittest

from rail import ThreatSources

class TestThreatSource(unittest.TestCase):
    """
    Class to test a threat source
    """
    def setUp(self):
        self.threat_sources = ThreatSources()
        self.threat_sources.new('test')

    def test_threat_sources(self):
        """
        Test threat sources
        """
        self.assertEqual(self.threat_sources['test']['name'], 'test')


if __name__ == '__main__':
    unittest.main()
