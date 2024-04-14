from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ITableRow_1:
    superficie: int = field(default=None)
    poblacion : int = field(default=None)
    densidad  : int = field(default=None)

@dataclass
class ITableRow_2:
    year_2020: int
    year_2010: int
    year_2000: int
    year_1990: int
    year_1980: int
    year_1970: int
    year_1960: int
    year_1950: int
    year_1940: int
    year_1930: int
    year_1921: int  
    year_1910: int


@dataclass
class ITableRow_3:
    year_2010: int = field(default=0)
    year_2015: int = field(default=0)
    year_2020: int = field(default=0)
    year_2025: int = field(default=0)
    year_2030: int = field(default=0)

@dataclass
class ITableRow_US:
    name         : str
    official_name: str
    abbreviation : str
    density      : float
    surface      : float
    population   : int

@dataclass
class IEtimilogia_US:
    link : str = field(default="")
    text : str = field(default="")