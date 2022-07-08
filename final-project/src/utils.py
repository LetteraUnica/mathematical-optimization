from typing import TypeVar
from typing import Any, Callable, List, Tuple
import numpy as np


def fill_like(V: List[List[Any]], fill_value: Any) -> List[List[Any]]:
    """Returns a List of lists like V filled with fill_value"""
    return [[fill_value for _ in range(len(V[i]))] for i in range(len(V))]


T = TypeVar('T')
def clamp(x: T, low: T, high: T) -> T:
    return max(low, min(x, high))


def line_between_two_points(x1:np.ndarray, y1:np.ndarray, x2:np.ndarray, y2:np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Returns in order the slope and intercept of all the lines from the given points"""
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a*x1

    return a, b
