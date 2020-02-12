"""
Tests for the Likelihood class
"""
import unittest

from rail import Control, Impact, Likelihood, Risk, Risks, ThreatEvent, ThreatSources, Tree, Vulnerability

LAM = 0.5
NAME = "Test Impact"
MU = 100
SIGMA = 10

class TestRisks(unittest.TestCase):
    """
    Class to test a risk 
    """

    def setUp(self):
        self.threat_sources = ThreatSources()
        self.threat_sources.new("test")
        self.threat_event = ThreatEvent("test event", self.threat_sources["test"])
        self.system = Tree(name="test tree")
        self.system.add_child("test child")
        self.controls = [Control("test control", 100, 0.1)]
        self.vulnerability = Vulnerability(self.threat_event, self.system, self.controls)
        self.likelihood = Likelihood(LAM)
        self.impact = Impact(NAME, MU, SIGMA)
        self.risks = Risks()
        self.risks.new(self.vulnerability, self.likelihood, self.impact)

    def test_risks(self):
        """
        Test risks
        """
        pass


if __name__ == "__main__":
    unittest.main()
