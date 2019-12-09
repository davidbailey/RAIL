"""
A class to represent Threat Events
"""
from collections import UserDict

from .threat_source import ThreatSource


class ThreatEvent(UserDict):  # pylint: disable=too-many-ancestors
    """
    A class to represent Threat Events
    """

    def __init__(self, name: str, threat_source: ThreatSource) -> None:
        UserDict.__init__(self)
        self.data = {}
        self.data["name"] = name
        self.data["threat_source"] = threat_source


class ThreatEvents(UserDict):  # pylint: disable=too-many-ancestors
    """
    A class to hold multiple Threat Events
    """

    def new(self, name: str, threat_source: ThreatSource) -> ThreatEvent:
        """
        A method to add a new threat event to the Threat Events class
        """
        self.data[name] = ThreatEvent(name, threat_source)
        return self.data[name]
