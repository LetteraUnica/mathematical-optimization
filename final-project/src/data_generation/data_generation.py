import numpy as np


def my_tau(start):
    return np.sin(start)/2 + 2


def my_rho(start):
    return np.cos(start)/2 + 2


def gasoline_consumption(speed):
    if speed > 50:
        return 5 + 3e-4*(speed-50)**2

    return 5 + 3e-3*(speed-50)**2


def ev_consumption(speed):
    if speed > 10:
        return 5 + 2e-4*(speed-10)**2

    return 5 + 3e-2*(speed-10)**2


def traffic_over_space(point, sigma=10):
    x, y = point
    return np.exp(-((x**2 + y**2)/sigma**2))


def traffic_over_time(time, first_rush_hour: float = 480., second_rush_hour: float = 1020., sigma: float = 240.):
    """Traffic distribution over time considering two rush hours.
    The time is given in minutes since the start of day"""
    return 0.7*np.exp(-((time - first_rush_hour)/sigma)**2) + np.exp(-((time - second_rush_hour)/sigma)**2)
