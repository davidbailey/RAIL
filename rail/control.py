"""
A class to represent Controls
"""

from collections import UserDict

import numpy as np
from scipy.stats import lognorm


class Control(UserDict):
    """
    A class to represent Controls
    """

    def __init__(
        self, name: str, cost: float, reduction: float, implemented: bool = True
    ) -> None:
        self.data = {}
        self.data["name"] = name
        self.data["cost"] = cost
        self.data["reduction"] = reduction
        self.data["implemented"] = implemented

    def evaluate_lognormal(self, iterations=1):
        return Control(
            name=self.data["name"],
            cost=lognorm.ppf(np.random.rand(iterations), s=np.log(self.data["cost"])),
            reduction=lognorm.ppf(
                np.random.rand(iterations), s=np.log(self.data["reduction"])
            ),
            implemented=self.data["implemented"],
        )


class Controls(UserDict):
    """
    A class to hold multiple Controls
    """

    def __init__(self) -> None:
        self.data = {}

    def new(self, name: str, cost: float, reduction: float) -> Control:
        """
        A method to add a new controls to the Controls class
        """
        self.data[name] = Control(name, cost, reduction)
        return self.data[name]

    def costs(self):
        """
        A method to compute the deterministic costs of implemented controls in a Controls class
        """
        return np.sum(
            list(
                map(
                    lambda x: x["cost"] if x["implemented"] is True else 0,
                    self.data.values(),
                )
            )
        )

    def costs_lognormal(self):
        """
        A method to compute the stochastic costs of implemented controls in a Controls class
        """
        return np.sum(
            list(
                map(
                    lambda x: x.evaluate_lognormal().data["cost"]
                    if x.data["implemented"] is True
                    else 0,
                    self,
                )
            )
        )
