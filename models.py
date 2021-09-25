
from dataclasses import dataclass

@dataclass
class customer:
    id: int

@dataclass
class basket:
    id: int
    customer_id: int
    score: int
