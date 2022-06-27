from dataclasses import dataclass
from typing import Callable, List

import numpy as np


@dataclass
class Activity:
    start: float
    end: float
    duration: Callable[[float], float]
    resources: Callable[[float], float]
    name: str = None

    def completion_time(self, start: float) -> float:
        return start + self.duration(start)

    def discretize_time(self, eps: float) -> np.ndarray:
        times = list(np.arange(self.start, self.end, eps))
        times.append(self.end)
        return times


def discretize_activity_times(activities, eps: float) -> List[List[float]]:
    return [list(a.discretize_time(eps)) for a in activities]