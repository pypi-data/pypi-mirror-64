import covid.data.cia_factbook
from . import data
from .types import cached


class Region:
    """
    Generic demographic and epidemiologic information about region.
    """
    population_size = cached(lambda _: _.age_distribution.sum() * 1000)

    def __init__(self, name, year=2020):
        self.name = name
        self.age_distribution = covid.data.cia_factbook.age_distribution(name, year)
        self.age_coarse = covid.data.cia_factbook.age_distribution(name, year, coarse=True)

    def __str__(self):
        return self.name

    def _repr_html_(self):
        return self.name

    def report(self):
        return f"""Region {self.name} 
"""
