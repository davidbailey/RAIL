import copy
from collections import OrderedDict, UserString, UserDict

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import lognorm

from .control import Control, Controls
from .likelihood import Likelihood
from .impact import Impact
from .vulnerability import Vulnerability, Vulnerabilities

pd.set_option("display.float_format", lambda x: "%.2f" % x)
pd.set_option("display.max_colwidth", -1)
plt.style.use("seaborn-poster")


class Risk(UserDict):
    def __init__(
        self, vulnerability: Vulnerability, likelihood: Likelihood, impact: Impact
    ) -> None:
        self.data = {}
        self.data["name"] = (
            vulnerability["name"]
            + " -> "
            + likelihood["name"]
            + " -> "
            + impact["name"]
        )
        self.data["vulnerability"] = vulnerability
        self.data["likelihood"] = likelihood
        self.data["impact"] = impact

    def evaluate_deterministic(self) -> float:
        reduction = np.product(
            list(
                map(
                    lambda x: x["reduction"] if x["implemented"] is True else 1,
                    self.data["vulnerability"]["controls"],
                )
            )
        )
        return self.data["likelihood"]["lam"] * self.data["impact"]["mean"] * reduction

    def evaluate_lognormal(self, iterations: int = 1000) -> float:
        reduction = np.product(
            list(
                map(
                    lambda x: x["reduction"] if x["implemented"] is True else 1,
                    self.data["vulnerability"]["controls"],
                )
            )
        )
        return lognorm.ppf(
            np.random.rand(iterations),
            s=self.data["impact"]["sigma"],
            scale=np.exp(self.data["impact"]["mu"]),
        ) * np.random.poisson(
            lam=self.data["likelihood"]["lam"] * reduction, size=iterations
        )


class Risks(UserDict):
    def __init__(self) -> None:
        self.data = {}
        self.dataframe = pd.DataFrame(
            columns=[
                "Threat Source",
                "Threat Event",
                "System",
                "Controls",
                "Impact",
                "Impact (mean)",
                "Likelihood (mean)",
            ]
        )
        self.cost_loss = []

    def new(
        self, vulnerability: Vulnerability, likelihood: Likelihood, impact: Impact
    ) -> Risk:
        name = (
            vulnerability["name"]
            + " -> "
            + likelihood["name"]
            + " -> "
            + impact["name"]
        )
        self.data[name] = Risk(vulnerability, likelihood, impact)
        self.dataframe = self.dataframe.append(
            {
                "Threat Source": vulnerability["threat_event"]["threat_source"]["name"],
                "Threat Event": vulnerability["threat_event"]["name"],
                "System": vulnerability["system"].path(),
                "Controls": list(map(lambda x: x["name"], vulnerability["controls"])),
                "Impact": impact["name"],
                "Impact (mean)": impact["mean"],
                "Likelihood (mean)": likelihood["lam"],
            },
            ignore_index=True,
        )
        return self.data[name]

    def calculate_stochastic_risks(self, interations: int = 100000):
        risks_scores = np.array(
            list(
                map(lambda row: row.evaluate_lognormal(interations), self.data.values())
            )
        )
        return risks_scores.sum(axis=0)

    def plot(self, axes=None):
        plt.title("expected loss")
        plt.xlabel("loss")
        plt.ylabel("probability")
        return plt.hist(
            self.calculate_stochastic_risks(),
            histtype="step",
            bins=10000,
            cumulative=-1,
            normed=True,
            axes=axes,
        )

    def expected_loss_stochastic_mean(self, interations: int = 1000) -> float:
        return self.calculate_stochastic_risks(interations).sum() / interations

    def expected_loss_deterministic_mean(self) -> float:
        return np.array(
            list(map(lambda row: row.evaluate_deterministic(), self.data.values()))
        ).sum()

    def calculate_dataframe_deterministic_mean(self):
        df = self.dataframe.copy()
        df["Risk (mean)"] = list(
            map(lambda x: x.evaluate_deterministic(), self.data.values())
        )
        return df

    def determine_optimum_controls(
        self, controls, controls_to_optimize, stochastic=False
    ):
        if not controls_to_optimize:
            loss = self.expected_loss_deterministic_mean()
            if stochastic:
                cost = controls.costs_lognormal()
            else:
                cost = controls.costs()
            self.cost_loss.append({"cost": cost, "loss": loss})
            return {"loss": loss, "cost": cost, "controls": copy.deepcopy(controls)}
        else:
            controls_to_optimize_new_list = list(controls_to_optimize)
            control = controls_to_optimize_new_list.pop()
            controls[control]["implemented"] = False
            control_off = self.determine_optimum_controls(
                controls, controls_to_optimize_new_list
            )
            controls[control]["implemented"] = True
            control_on = self.determine_optimum_controls(
                controls, controls_to_optimize_new_list
            )
            if (
                control_on["loss"] + control_on["cost"]
                < control_off["loss"] + control_off["cost"]
            ):
                optimal_control = control_on
            else:
                optimal_control = control_off
            return optimal_control

    def set_optimum_controls(self, controls):
        optimum_controls = self.determine_optimum_controls(controls, controls)
        for control in optimum_controls["controls"]:
            if optimum_controls["controls"][control]["implemented"] is True:
                controls[control]["implemented"] = True
            else:
                controls[control]["implemented"] = False
        df = pd.DataFrame(list(optimum_controls["controls"].values())).set_index("name")
        return df

    def plot_risk_cost_matrix(self, controls, axes=None):
        self.set_optimum_controls(controls)
        df = pd.DataFrame(self.cost_loss)
        plt.title("residual risk versus control cost")
        plt.ylabel("residual risk")
        plt.xlabel("control cost")
        plt.scatter(df["cost"], df["loss"], axes=axes)
        plt.scatter(
            controls.costs(),
            self.expected_loss_deterministic_mean(),
            color="red",
            axes=axes,
        )
        axes.set_xlim(xmin=0)

    def sensitivity_test(self, controls, iterations=1000):
        results = []
        for i in range(iterations):
            results.append(
                self.determine_optimum_controls(controls, controls, stochastic=True)[
                    "controls"
                ].values()
            )
        return results
