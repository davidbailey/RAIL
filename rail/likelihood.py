"""
A class to represent a Likelihood
"""

from collections import UserDict

from matplotlib import pyplot as plt
import numpy as np


class Likelihood(UserDict):
    """
    A class to represent a Likelihood
    """

    def __init__(self, lam: float) -> None:
        self.data = {}
        if lam < 0:
            raise ValueError(
                "Likelihood value lam must be greater than or equal to zero."
            )
        self.data["name"] = str(lam)
        self.data["lam"] = lam

    def plot(self, axes=None) -> tuple:
        """
        A method to plot the likelihood
        """
        s = np.random.poisson(self.data["lam"], 10000)
        plt.title("%s (histogram)" % (self.data["name"]))
        plt.ylabel("relative frequency")
        plt.xlabel("likelihood")
        return plt.hist(s, 14, normed=True, axes=axes)
