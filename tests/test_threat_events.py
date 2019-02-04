"""
Tests for the ThreatEvent and ThreatEvents classes
"""
import unittest

from rail import ThreatSources, ThreatEvents

class TestThreatEvents(unittest.TestCase):
    """
    Class to test a threat event
    """
    def setUp(self):
        self.threat_sources = ThreatSources()
        self.threat_sources.new('test')
        self.threat_events = ThreatEvents()
        self.threat_events.new('test event', self.threat_sources['test'])

    def test_threat_sources(self):
        """
        Test threat sources
        """
        self.assertEqual(self.threat_events['test event']['name'], 'test event')
        self.assertEqual(self.threat_events['test event']['threat_source'], self.threat_sources['test'])


if __name__ == '__main__':
    unittest.main()
