from typing import Mapping, TypeVar
from typing import Any, Sequence, Tuple
import numpy as np

from .activity import Activity
from .time_discretizer import TimeDiscretizer


def fill_like(V: Sequence[Sequence[Any]], fill_value: Any) -> Sequence[Sequence[Any]]:
    """Returns a List of lists like V filled with fill_value"""
    return [[fill_value for _ in range(len(V[i]))] for i in range(len(V))]


def line_between_two_points(x1:np.ndarray, y1:np.ndarray, x2:np.ndarray, y2:np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Returns in order the slope and intercept of all the lines from the given points"""
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a*x1

    return a, b

def generate_V_and_q(activities: Sequence[Activity], discretizer: TimeDiscretizer) -> Tuple[Sequence[Mapping[int, float]], Sequence[Mapping[int, float]]]:
    V = []
    q = []
    for activity in activities:
        times = discretizer.discretize_activity(activity)
        V.append(dict([(i, time) for i, time in enumerate(times)]))
        q.append(dict([(i, activity.resources(time))
                for i, time in enumerate(times)]))

    return V, q