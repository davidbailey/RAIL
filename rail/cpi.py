"""
A class to retrieve United States CPI data and calculate inflation
"""
import pandas as pd


class CPI:
    """
    A class to retrieve United States CPI data and calculate inflation
    """

    def __init__(self) -> None:
        url = "https://download.bls.gov/pub/time.series/cu/cu.data.0.Current"
        self.cpi = pd.read_csv(url, sep="\t", skipinitialspace=True)
        self.cpi.columns = [c.replace(" ", "") for c in self.cpi.columns]

    def inflation(self, from_year: int, to_year: int) -> float:
        """
        A method to retrieve United States CPI data and calculate inflation
        """
        cpi_from = self.cpi[
            (self.cpi["series_id"] == "CUUS0000SA0      ")
            & (self.cpi["year"] == from_year)
            & (self.cpi["period"] == "S01")
        ]["value"]
        cpi_to = self.cpi[
            (self.cpi["series_id"] == "CUUS0000SA0      ")
            & (self.cpi["year"] == to_year)
            & (self.cpi["period"] == "S01")
        ]["value"]
        return cpi_to.values[0] / cpi_from.values[0]
