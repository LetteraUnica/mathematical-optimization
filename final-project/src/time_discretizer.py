from typing import Sequence
import numpy as np
from .activity import Activity
from .utils import clamp


class TimeDiscretizer:
    def __init__(self, eps: float):
        self.eps = eps

    def discretize_time(self, start: float, end: float) -> Sequence[float]:
        """Discretizes the time with a granularity of eps

        Returns:
            Sequence[float]: list of discretized times [start, start+eps, start+2*eps, ..., end]
        """
        times = list(np.arange(start, end, self.eps))
        times.append(end)
        return times

    def discretize_activity(self, activity: Activity) -> Sequence[float]:
        """Discretizes an activity time with a granularity of eps

        Returns:
            Sequence[float]: list of discretized times [start, start+eps, start+2*eps, ..., end]
        """
        return self.discretize_time(activity.start, activity.end)

    def discretize_all_activities(self, activities: Sequence[Activity]) -> Sequence[Sequence[float]]:
        """Discretizes all activities with a granularity of eps"""
        return [self.discretize_activity(activity) for activity in activities]

    def index_to_time(self, start: float, end: float, index: int) -> float:
        """Given an index, start and end time, returns the discretized time
        the index points to, equivalent to discretize_time(start, end)[index] but much faster
        """
        time = start + self.eps*index
        return clamp(time, start, end)

    def time_to_index(self, start: float, end: float, time: float) -> int:
        """Given a time, start and end, returns the index
        such that time = index_to_time(start, end, index)
        """
        n_steps = int((end - start) / self.eps) + 2
        n_steps -= 1 if end % self.eps == 0 else 0
        return clamp(int((time - start + self.eps/2) / self.eps), 0, n_steps-1)

    def activity_to_time(self, activity: Activity, index: int) -> float:
        """Given an index and an activity, returns the activity time
        the index points to
        """
        return self.index_to_time(activity.start, activity.end, index)

    def activity_to_index(self, activity: Activity, time: float) -> int:
        """Given a time and an activity, returns the nearest index
        that time refers to
        """
        return self.time_to_index(activity.start, activity.end, time)
