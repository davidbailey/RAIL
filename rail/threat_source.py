"""
A class to represent Threat Sources
"""
from collections import UserDict


class ThreatSource(UserDict):  # pylint: disable=too-many-ancestors
    """
    A class to represent Threat Sources
    """

    def __init__(self, name: str) -> None:
        UserDict.__init__(self)
        self.data = {}
        self.data["name"] = name


class ThreatSources(UserDict):  # pylint: disable=too-many-ancestors
    """
    A class to hold multiple Threat Sources
    """

    def new(self, name: str) -> ThreatSource:
        """
        A method to add a new threat source to the Threat Sources class
        """
        self.data[name] = ThreatSource(name)
        return self.data[name]
