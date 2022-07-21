import time

import numpy as np

from .utils import generate_V_and_q
from .activity import Activity

import pylab as pl


def resources(start_time: float) -> float:
    return np.sin(start_time) + 2


def duration(start_time: float) -> float:
    return np.cos(start_time) + 2


def mock_problem(n_activities, discretizer):
    # Generate activities
    activities = [Activity(2*i, 4*(i+4), duration, resources, lambda x: 1)
                  for i in range(n_activities)]

    # Fill times
    V, q = generate_V_and_q(activities, discretizer)

    return activities, V, q


def my_timeit(f, args, repeat=3):
    times = []
    for _ in range(repeat):
        start = time.time()
        sol = f(*args)
        times.append(time.time() - start)

    return np.mean(times), np.std(times)


def plot_times(x, mus, stds, names):
    for mu, std, name in zip(mus, stds, names):
        pl.errorbar(x, mu, std, label=name)
    pl.legend()
