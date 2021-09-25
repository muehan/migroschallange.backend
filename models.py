
from dataclasses import dataclass, field
from typing import List


@dataclass
class basket:
    id: int
    date: str
    total_co2: int
    total_animal_wellfare: int
    avaragescore_co2: float
    avaragescore_animal_wellfare: float

@dataclass
class sustainability:
    total_co2: int
    total_animal_wellfare: int

@dataclass
class customer:
    id: int
    baskets: List[basket]
    sustainability: sustainability = field(init=False)
