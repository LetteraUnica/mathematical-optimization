from typing import Callable

import numpy as np


class TrafficModel:
    def __init__(self,
                 traffic_over_space: Callable[[float, float], float],
                 traffic_over_time: Callable[[float], float]):
        self.traffic_over_space = traffic_over_space
        self.traffic_over_time = traffic_over_time

    def traffic_level(self, point: np.ndarray, time: float):
        traffic = 1 / (1 - min(self.traffic_over_time(time), 0.8))
        sensitivity = self.traffic_over_space(point)
        return traffic*sensitivity + 1-sensitivity
