from typing import Mapping, Sequence, Tuple

from ..activity import Activity
from ..solution import Solution
from ..time_discretizer import TimeDiscretizer
from .ten import TEN_solve


def DDD_initialize(activities: Sequence[Activity],
                   discretizer: TimeDiscretizer) -> Tuple[Sequence[Mapping[int, float]], Sequence[Mapping[int, float]]]:
    V = [dict() for _ in activities]
    q = [dict() for _ in activities]
    for i in range(len(activities)-1, -1, -1):
        activity = activities[i]
        end = discretizer.activity_to_index(activity, activity.end)
        V, q = DDD_addRecursive(V, activities, q, i,
                                end, discretizer)
        start = discretizer.activity_to_index(activity, activity.start)
        V, q = DDD_addRecursive(V, activities, q, i,
                                start, discretizer)

    return V, q


def DDD_addRecursive(V: Sequence[Mapping[int, float]],
                     activities: Sequence[Activity],
                     q: Sequence[Mapping[int, float]],
                     i: int, t: int,
                     discretizer: TimeDiscretizer) -> Tuple[Sequence[Mapping[int, float]], Sequence[Mapping[int, float]]]:
    if t in V[i]:
        return V, q

    activity = activities[i]
    eps = discretizer.eps
    time = discretizer.activity_to_time(activity, t)
    V[i][t] = time

    if t == discretizer.activity_to_index(activity, activity.end):
        q[i][t] = activity.resources(time)
    else:  # Minimum at lines 14-16
        min_q = activity.resources(time)
        t_bar = t + 1
        while t_bar not in V[i]:
            resources = activity.resources(
                discretizer.activity_to_time(activity, t_bar))
            if min_q > resources:
                min_q = resources
            t_bar += 1
        q[i][t] = min_q

        if time > activity.start:  # Minimum at lines 17-19
            t_bar = t - 1
            min_q = activity.resources(
                discretizer.activity_to_time(activity, t_bar))
            while t_bar not in V[i]:
                t_bar -= 1
                resources = activity.resources(
                    discretizer.activity_to_time(activity, t_bar))
                if min_q > resources:
                    min_q = resources
            q[i][t_bar] = min_q

    if i == len(activities)-1:
        return V, q

    else:
        next_t = discretizer.activity_to_index(
            activities[i+1], activity.completion_time(time)+eps/2)
        return DDD_addRecursive(V, activities, q, i+1, next_t, discretizer)


def DDD_solve(activities: Sequence[Activity],
              Q: float,
              discretizer: TimeDiscretizer) -> Solution:
    V, q = DDD_initialize(activities, discretizer)

    while True:
        solution = TEN_solve(V, activities, q, Q)
        if solution is None:
            return None

        path = solution.path
        node = None
        for i, t in enumerate(path):
            time = discretizer.activity_to_time(activities[i], t)
            if t in V[i] and activities[i].resources(time) > q[i][t]:
                node = (i, t)
                break

        if node is not None:
            i, t_i = node
            activity = activities[i]
            t = min([t for t in V[i] if t > t_i])
            while True:
                t = (t_i + t) // 2 + (t_i + t) % 2
                if min([activity.resources(discretizer.activity_to_time(activity, t_bar))
                        for t_bar in range(t_i, t)]) > q[i][t_i]:
                    break

            V, q = DDD_addRecursive(V, activities, q, i, t, discretizer)
        else:
            return solution
