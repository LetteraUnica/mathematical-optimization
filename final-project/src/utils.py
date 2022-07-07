from typing import TypeVar
from typing import Any, Callable, List, Tuple
import numpy as np


def fill_like(V: List[List[Any]], fill_value: Any) -> List[List[Any]]:
    """Returns a List of lists like V filled with fill_value"""
    return [[fill_value for _ in range(len(V[i]))] for i in range(len(V))]


T = TypeVar('T')
def clamp(x: T, low: T, high: T) -> T:
    return max(low, min(x, high))
