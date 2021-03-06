from dataclasses import dataclass
from typing import Callable


@dataclass
class Activity:
    start: float
    end: float
    duration: Callable[[float], float]
    resources: Callable[[float], float]
    replenishment_duration: Callable[[float], float]
    name: str = None

    def completion_time(self, start_time: float) -> float:
        """Returns the completion time of the activity when starting at start_time
        """
        return start_time + self.duration(start_time)
