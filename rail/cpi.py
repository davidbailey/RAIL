import pandas as pd


class CPI(object):
    """A class to retrieve United States CPI data and calculate inflation"""

    def __init__(self) -> None:
        self.cpi = pd.read_csv('https://download.bls.gov/pub/time.series/cu/cu.data.0.Current', sep='\t')

    def inflation(self, from_year: int, to_year: int) -> float:
        cpi_from = self.cpi[(self.cpi['series_id'] == 'CUUS0000SA0      ') & (self.cpi['year'] == from_year) & (self.cpi['period'] == 'S01')]['value']
        cpi_to = self.cpi[(self.cpi['series_id'] == 'CUUS0000SA0      ') & (self.cpi['year'] == to_year) & (self.cpi['period'] == 'S01')]['value']
        return cpi_to.values[0] / cpi_from.values[0]
