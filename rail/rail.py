import copy
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
    def __init__(self, name: str, cost: float, reduction: float, implemented: bool=True) -> None:
        self.data = {}
        self.data['name'] = name
        self.data['cost'] = cost
        self.data['reduction'] = reduction
        self.data['implemented'] = implemented

    def evaluate_lognormal(self, iterations=1):
        return Control(
            name = self.data['name'],
            cost = lognorm.ppf(np.random.rand(iterations), s=np.log(self.data['cost'])),
            reduction = lognorm.ppf(np.random.rand(iterations), s=np.log(self.data['reduction'])),
            implemented = self.data['implemented']
        )


class Controls(UserDict):
    def __init__(self) -> None:
        self.data = {}

    def new(self, name: str, cost: float, reduction: float) -> Control:
        self.data[name] = Control(name, cost, reduction)
        return self.data[name]

    def costs(self):
        return np.sum(list(map(lambda x: x['cost'] if x['implemented'] is True else 0, self.data.values())))

    def costs_lognormal(self):
        return np.sum(list(map(lambda x: x.evaluate_lognormal().data['cost'] if x.data['implemented'] is True else 0, self)))



class Vulnerability(UserDict):
    def __init__(self, threat_event: ThreatEvent, system: Tree, controls: [Control] = []) -> None:
        self.data = {}
        self.data['name'] = threat_event['name'] + ' -> ' + system.path() + ' | ' + str(controls)
        self.data['threat_event'] = threat_event
        self.data['system'] = system
        self.data['controls'] = controls


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
        plt.title('%s (PDF)' % (self.data['name']))
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

    def evaluate_deterministic(self) -> float:
        reduction = np.product(list(map(lambda x: x['reduction'] if x['implemented'] is True else 1, self.data['vulnerability']['controls'])))
        return self.data['likelihood']['lam'] * self.data['impact']['mean'] * reduction

    def evaluate_lognormal(self, iterations: int = 1000) -> float:
        reduction = np.product(list(map(lambda x: x['reduction'] if x['implemented'] is True else 1, self.data['vulnerability']['controls'])))
        return lognorm.ppf(np.random.rand(iterations), s=self.data['impact']['sigma'], scale=np.exp(self.data['impact']['mu'])) * np.random.poisson(lam=self.data['likelihood']['lam'] * reduction, size=iterations)


class Risks(UserDict):
    def __init__(self) -> None:
        self.data = {}
        self.dataframe = pd.DataFrame(columns=['Threat Source', 'Threat Event', 'System', 'Controls', 'Impact', 'Impact (mean)', 'Likelihood (mean)'])
        self.cost_loss = []

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
        }, ignore_index=True)
        return self.data[name]

    def calculate_stochastic_risks(self, interations: int = 100000):
        risks_scores = np.array(list(map(lambda row: row.evaluate_lognormal(interations), self.data.values())))
        return risks_scores.sum(axis=0)

    def plot(self, axes=None):
        plt.title('expected loss')
        plt.xlabel('loss')
        plt.ylabel('probability')
        return plt.hist(self.calculate_stochastic_risks(), histtype='step', bins=10000, cumulative=-1, normed=True, axes=axes)

    def expected_loss_stochastic_mean(self, interations: int = 1000) -> float:
        return self.calculate_stochastic_risks(interations).sum() / interations

    def expected_loss_deterministic_mean(self) -> float:
        return np.array(list(map(lambda row: row.evaluate_deterministic(), self.data.values()))).sum()

    def calculate_dataframe_deterministic_mean(self):
        df = self.dataframe.copy()
        df['Risk (mean)'] = list(map(lambda x: x.evaluate_deterministic(), self.data.values()))
        return df

    def determine_optimum_controls(self, controls, controls_to_optimize, stochastic=False):
        if not controls_to_optimize:
            loss = self.expected_loss_deterministic_mean()
            if stochastic:
                cost = controls.costs_lognormal()
            else:
                cost = controls.costs()
            self.cost_loss.append({'cost': cost, 'loss': loss})
            return {'loss': loss, 'cost': cost, 'controls': copy.deepcopy(controls)}
        else:
            controls_to_optimize_new_list = list(controls_to_optimize)
            control = controls_to_optimize_new_list.pop()
            controls[control]['implemented'] = False
            control_off = self.determine_optimum_controls(controls, controls_to_optimize_new_list)
            controls[control]['implemented'] = True
            control_on = self.determine_optimum_controls(controls, controls_to_optimize_new_list)
            if control_on['loss'] + control_on['cost'] < control_off['loss'] + control_off['cost']:
                optimal_control = control_on
            else:
                optimal_control = control_off
            return optimal_control

    def set_optimum_controls(self, controls):
        optimum_controls = self.determine_optimum_controls(controls, controls)
        for control in optimum_controls['controls']:
            if optimum_controls['controls'][control]['implemented'] is True:
                controls[control]['implemented'] = True
            else:
                controls[control]['implemented'] = False
        df = pd.DataFrame(list(optimum_controls['controls'].values())).set_index('name')
        return df

    def plot_risk_cost_matrix(self, controls, axes=None):
        self.set_optimum_controls(controls)
        df = pd.DataFrame(self.cost_loss)
        plt.title('residual risk versus control cost')
        plt.ylabel('residual risk')
        plt.xlabel('control cost')
        plt.scatter(df['cost'], df['loss'], axes=axes)
        plt.scatter(controls.costs(), self.expected_loss_deterministic_mean(), color='red', axes=axes)
        axes.set_xlim(xmin=0)

    def sensitivity_test(self, controls, iterations=1000):
        results = []
        for i in range(iterations):
            results.append(self.determine_optimum_controls(controls, controls, stochastic=True)['controls'].values())
        return results
