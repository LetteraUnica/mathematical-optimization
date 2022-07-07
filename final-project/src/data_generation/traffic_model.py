from typing import Callable

import numpy as np

def traffic_over_space(point, sigma=10):
    x, y = point
    return np.exp(-((x**2 + y**2)/sigma**2))


def traffic_over_time(time, first_rush_hour: float = 480., second_rush_hour: float = 1020., sigma: float = 240.):
    """Traffic distribution over time considering two rush hours.
    The time is given in minutes since the start of day"""
    return 0.7*np.exp(-((time - first_rush_hour)/sigma)**2) + np.exp(-((time - second_rush_hour)/sigma)**2)


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
