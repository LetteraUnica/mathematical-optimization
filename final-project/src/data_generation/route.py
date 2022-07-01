from typing import Callable

import numpy as np

from .traffic_model import TrafficModel


class Route:
    def __init__(self, traffic_model: TrafficModel,
                 energy_consumption: Callable[[float], float],
                 start: np.ndarray, end: np.ndarray,
                 base_speed: float = 50, time_steps: int = 100):
        self.traffic_model = traffic_model
        self.energy_consumption = energy_consumption
        self.start = start
        self.time_steps = time_steps
        self.base_speed = base_speed

        self.dx = (end - start) / time_steps
        self.dx_norm = np.linalg.norm(self.dx)

    def travel_time(self, start_time, time_steps=100):
        point = self.start
        time = start_time
        for _ in range(time_steps):
            traffic_level = self.traffic_model.traffic_level(point, time)
            speed = self.base_speed/traffic_level
            time += self.dx_norm/speed
            point += self.dx

        return (time - start_time)*60

    def resources_consumed(self, start_time, time_steps=100):
        point = self.start
        time, resources = start_time, 0
        for _ in range(time_steps):
            traffic_level = self.traffic_model.traffic_level(point, time)
            speed = self.base_speed/traffic_level
            time += self.dx_norm/speed
            resources += self.dx_norm / 100 * self.energy_consumption(speed)
            point += self.dx

        return resources
