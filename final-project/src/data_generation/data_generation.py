from typing import Callable, Tuple
import numpy as np


def my_tau(start: float) -> float:
    return np.sin(start)/2 + 2


def my_rho(start: float) -> float:
    return np.cos(start)/2 + 2


def satisfies_fifo_property(f: Callable[[float], float], interval: Tuple[int], n_samples: int = 1000):
    """Raises an exception if the given function does not satisfy the FIFO property.
    FIFO property: a+f(a) <= b+f(b) if a <= b

    Args:
        f (Callable[[float], float]): function
        interval (Tuple[int]): interval where to check for the FIFO property
        n_samples (int, optional): Samples to use for the checking. Defaults to 1000.
    """
    t = np.linspace(interval[0], interval[1], n_samples)
    for i in range(len(t)-1):
        if t[i] + f(t[i]) > t[i+1] + f(t[i+1]):
            raise Exception("f does not satisfies_fifo_property at t: ", t[i])
