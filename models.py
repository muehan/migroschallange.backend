
from dataclasses import dataclass, field
from typing import List

@dataclass
class rating:
    total: int
    average: float
    count: int

@dataclass
class basket:
    id: int
    date: str
    rating_co2: rating
    rating_animal_welfare: rating

@dataclass
class sustainability:
    total_co2: int
    total_animal_welfare: int

@dataclass
class customer:
    id: int
    baskets: List[basket]
    sustainability: sustainability = field(init=False)
