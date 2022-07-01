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

    def travel_time_function(self, start: np.ndarray, end: np.ndarray, time_steps=100):
        point = start
        direction = (end - start) / time_steps

        def time_and_resources_consumed(start_time: float):
            time = start_time
            for _ in range(time_steps):
                traffic_level = self.traffic_level(point, time)
                time += traffic_level
                resources += fuel_consumption_function(traffic_level)
                point += direction

            return time - start_time, resources

        return time_and_resources_consumed
