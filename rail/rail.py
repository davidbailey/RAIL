import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import lognorm
from collections import OrderedDict, UserString, UserDict
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.max_colwidth', -1)
plt.style.use('seaborn-poster')

class Tree(UserDict):
    def __init__(self, name: str, parent=None, sort: bool=True) -> None:
        self.data = {}
        self.name = name
        self.parent = parent
        self.sort = sort

    def addChild(self, name: str) -> 'Tree':
        self.data[name] = Tree(name=name, parent=self, sort=self.sort)
        if self.sort:
            self.data = OrderedDict(sorted(self.data.items(), key=lambda x: x[1].name))
        return self.data[name]

    def path(self) -> str:
        if self.parent:
            return self.parent.path() + '/' + self.name
        else:
            return '/' + self.name

    def to_print(self) -> None:
        print(self.path())
        for child in self.data.values():
            child.to_print()

    def to_latex(self) -> None:
        print('child { node{' + self.name + '}')
        for child in self.data.values():
            child.to_latex()
        print('}')

    def to_dict_list(self) -> dict:
        outdict = {}
        outdict['name'] = self.name
        outdict['children'] = []
        for child in self.data.values():
            outdict['children'].append(child.to_dict_list())
        return outdict


class ThreatSource(UserDict):
    def __init__(self, name: str) -> None:
        self.data = {}
        self.data['name'] = name


class ThreatSources(UserDict):
    def new(self, name: str) -> ThreatSource:
        self.data[name] = ThreatSource(name)
        return self.data[name]


class ThreatEvent(UserDict):
    def __init__(self, name: str, threat_source: ThreatSource) -> None:
        self.data = {}
        self.data['name'] = name
        self.data['threat_source'] = threat_source


class ThreatEvents(UserDict):
    def new(self, name: str, threat_source: ThreatSource) -> ThreatEvent:
        self.data[name] = ThreatEvent(name, threat_source)
        return self.data[name]


class Control(UserDict):
    def __init__(self, name: str, cost: float, likelihood_reduction: float) -> None:
        self.data = {}
        self.data['name'] = name
        self.data['cost'] = cost
        self.data['likelihood_reduction'] = likelihood_reduction


class Controls(UserDict):
    def __init__(self) -> None:
        self.data = {}
        self.costs = 0.0

    def new(self, name: str, cost: float, likelihood_reduction: float) -> Control:
        self.data[name] = Control(name, cost, likelihood_reduction)
        self.costs += cost
        return self.data[name]      


class Vulnerability(UserDict):
    def __init__(self, threat_event: ThreatEvent, system: Tree, controls: [Control] = []) -> None:
        self.data = {}
        self.data['name'] = threat_event['name'] + ' -> ' + system.path() + ' | ' + str(controls)
        self.data['threat_event'] = threat_event
        self.data['system'] = system
        self.data['controls'] = controls
        self.data['likelihood_reduction'] = np.product(list(map(lambda x: x['likelihood_reduction'], controls)))


class Vulnerabilities(UserDict):
    def new(self, threat_event: ThreatEvent, system: Tree, controls: [Control] = []) -> Vulnerability:
        name = threat_event['name'] + ' -> ' + system.path() + ' | ' + str(controls)
        self.data[name] = Vulnerability(threat_event, system, controls)
        return self.data[name]


class Likelihood(UserDict):
    def __init__(self, lam: float) -> None:
        if lam < 0:
            raise ValueError('Likelihood value lam must be greater than or equal to zero.')
        self.data = {}
        self.data['name'] = str(lam)
        self.data['lam'] = lam

    def plot(self, axes=None) -> tuple:
        s = np.random.poisson(self.data['lam'], 10000)
        plt.title('%s (histogram)' % (self.data['name']))
        plt.ylabel('relative frequency')
        plt.xlabel('likelihood')
        return plt.hist(s, 14, normed=True, axes=axes)


class Impact(UserDict):
    def __init__(self, name: str, mu: float, sigma: float) -> None:
        if mu < 0:
            raise ValueError('Impact value mu must be greater than or equal to 0.')
        if sigma < 0:
            raise ValueError('Impact value s must be greater than or equal to 0.')
        self.data = {}
        self.data['name'] = name
        self.data['mean'] = np.exp(mu + sigma**2 / 2)
        self.data['median'] = np.exp(mu)
        self.data['mu'] = mu
        self.data['sigma'] = sigma

    def from_lower_90_upper_90(name: str, lower_90: float, upper_90: float):
        if lower_90 < 0:
            raise ValueError('Impact value lower_90 must be greater than or equal to 0.')
        if upper_90 < 0:
            raise ValueError('Impact value upper_90 must be greater than or equal to 0.')
        if lower_90 >= upper_90:
            raise ValueError('Impact value upper_90 must be greater than value lower_90.')
        sigma = (np.log(upper_90) - np.log(lower_90)) / 3.29
        mu = (np.log(lower_90) + np.log(upper_90)) / 2
        return Impact(name, mu, sigma)

    def plot(self, num=1000, axes=None) -> list:
        x = np.linspace(
            lognorm.ppf(0.001, s=self.data['sigma'], scale=np.exp(self.data['mu'])),
            lognorm.ppf(0.999, s=self.data['sigma'], scale=np.exp(self.data['mu'])),
            num
        )
        plt.title('%s (probability density function)' % (self.data['name']))
        plt.ylabel('relative likelihood')
        plt.xlabel('impact')
        return plt.plot(x, lognorm.pdf(x, s=self.data['sigma'], scale=np.exp(self.data['mu'])), axes=axes)


class Risk(UserDict):
    def __init__(self, vulnerability: Vulnerability, likelihood: Likelihood, impact: Impact) -> None:
        self.data = {}
        self.data['name'] = vulnerability['name'] + ' -> ' + likelihood['name'] + ' -> ' + impact['name']
        self.data['vulnerability'] = vulnerability
        self.data['likelihood'] = likelihood
        self.data['impact'] = impact
        self.data['mean'] = impact['mean'] * likelihood['lam'] * vulnerability['likelihood_reduction']

    def evaluate_lognormal(self, iterations: int = 1000) -> float:
        return lognorm.ppf(np.random.rand(iterations), s=self.data['impact']['sigma'], scale=np.exp(self.data['impact']['mu'])) * np.random.poisson(lam=self.data['likelihood']['lam'] * self.data['vulnerability']['likelihood_reduction'], size=iterations)


class Risks(UserDict):
    def __init__(self) -> None:
        self.data = {}
        self.dataframe = pd.DataFrame(columns=['Threat Source', 'Threat Event', 'System', 'Controls', 'Impact', 'Impact (mean)', 'Likelihood (mean)', 'Expected Loss (mean)'])

    def new(self, vulnerability: Vulnerability, likelihood: Likelihood, impact: Impact) -> Risk:
        name = vulnerability['name'] + ' -> ' + likelihood['name'] + ' -> ' + impact['name']
        self.data[name] = Risk(vulnerability, likelihood, impact)
        self.dataframe = self.dataframe.append({
            'Threat Source': vulnerability['threat_event']['threat_source']['name'],
            'Threat Event': vulnerability['threat_event']['name'],
            'System': vulnerability['system'].path(),
            'Controls': list(map(lambda x: x['name'], vulnerability['controls'])),
            'Impact': impact['name'],
            'Impact (mean)': impact['mean'],
            'Likelihood (mean)': likelihood['lam'],
            'Expected Loss (mean)': impact['mean'] * likelihood['lam'] * vulnerability['likelihood_reduction'],
        }, ignore_index=True)
        return self.data[name]

    def calculate_stochastic_risks(self, interations: int = 100000):
        risks_scores = np.array(list(map(lambda row: row.evaluate_lognormal(interations), self.data.values())))
        return risks_scores.sum(axis=0)

    def plot(self, range=(0, 1000000)):
        plt.title('expected loss')
        plt.xlabel('loss')
        plt.ylabel('probability')
        return plt.hist(self.calculate_stochastic_risks(), histtype='stepfilled', bins=100, cumulative=-1, normed=True, range=range)

    def expected_loss_stochastic_mean(self, interations: int = 1000) -> float:
        return self.calculate_stochastic_risks(interations).sum() / interations

    def expected_loss_deterministic_mean(self) -> float:
        return self.dataframe['Expected Loss (mean)'].sum()
