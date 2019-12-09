"""
A class to represent an Impact
"""

from collections import UserDict

from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import lognorm


class Impact(UserDict):
    """
    A class to represent an Impact
    """

    def __init__(self, name: str, mu: float, sigma: float) -> None:
        if mu < 0:
            raise ValueError("Impact value mu must be greater than or equal to 0.")
        if sigma < 0:
            raise ValueError("Impact value s must be greater than or equal to 0.")
        self.data = {}
        self.data["name"] = name
        self.data["mean"] = np.exp(mu + sigma ** 2 / 2)
        self.data["median"] = np.exp(mu)
        self.data["mu"] = mu
        self.data["sigma"] = sigma

    def from_lower_90_upper_90(name: str, lower_90: float, upper_90: float):
        """
        A method to create an impact from the lower 90th and upper 90th percentiles
        """
        if lower_90 < 0:
            raise ValueError(
                "Impact value lower_90 must be greater than or equal to 0."
            )
        if upper_90 < 0:
            raise ValueError(
                "Impact value upper_90 must be greater than or equal to 0."
            )
        if lower_90 >= upper_90:
            raise ValueError(
                "Impact value upper_90 must be greater than value lower_90."
            )
        sigma = (np.log(upper_90) - np.log(lower_90)) / 3.29
        mu = (np.log(lower_90) + np.log(upper_90)) / 2
        return Impact(name, mu, sigma)

    def plot(self, num=1000, axes=None) -> list:
        """
        A method to plot the impact
        """
        x = np.linspace(
            lognorm.ppf(0.001, s=self.data["sigma"], scale=np.exp(self.data["mu"])),
            lognorm.ppf(0.999, s=self.data["sigma"], scale=np.exp(self.data["mu"])),
            num,
        )
        plt.title("%s (PDF)" % (self.data["name"]))
        plt.ylabel("relative likelihood")
        plt.xlabel("impact")
        return plt.plot(
            x,
            lognorm.pdf(x, s=self.data["sigma"], scale=np.exp(self.data["mu"])),
            axes=axes,
        )
