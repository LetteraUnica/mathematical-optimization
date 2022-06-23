from dataclasses import dataclass
from typing import Callable


@dataclass
class Activity:
    start: float
    end: float
    duration: Callable[[float], float]
    resources: Callable[[float], float]
    name: str = None

    def completion_time(self, start):
        return start + self.duration(start)
