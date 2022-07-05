import heapq
import sys
from typing import Literal, Mapping, Sequence


from ..activity import Activity
from ..solution import Solution


def init_l(V: Sequence[Mapping[int, float]]) -> Sequence[Mapping[int, float]]:
    """Initializes the labels, 0 for the first activity vertexes and np.inf otherwise"""
    l = [dict([(t, 0) for t in V[0].keys()])]
    for i in range(1, len(V)):
        l.append(dict([(t, sys.float_info.max) for t in V[i].keys()]))
    return l


def init_p(V: Sequence[Mapping[int, float]]) -> Sequence[Mapping[int, float]]:
    """Initializes the predecessor structure to None"""
    return [dict([(t, None) for t in v.keys()]) for v in V]


def min_time_per_activity(V: Sequence[Mapping[int, float]],
                          activities: Sequence[Activity]) -> Sequence[float]:
    """Returns a list with the minimum possible time to do each activity"""
    return [min([a.duration(time) for time in v.values()]) for a, v in zip(activities, V)]


def A_star_bound(V: Sequence[Mapping[int, float]],
                 activities: Sequence[Activity],
                 min_taus: Sequence[float],
                 i: int, t: int) -> float:
    """Lower bound on the total completion time when doing activity i at time t"""
    return activities[i].completion_time(V[i][t]) + sum(min_taus[i+1:])


def TEN_solve(V: Sequence[Mapping[int, float]],
              activities: Sequence[Activity],
              q: Sequence[Mapping[int, float]],
              Q: float) -> Solution:
    """Solves the TDASP in a Time Expanded Network, implements Algorithm 1 of the paper
    https://www.sciencedirect.com/science/article/pii/S0377221721009838?

    Given n=number of activities and m=activity discred
    This implementation uses a MinHeap to keep the vertexes sorted and achieves a
    time complexity of O(n*m^2), less than the one cited in the paper O(n^2*m^2)

    Note: In this code t does not stand for time, but stands for the index of V which then gives the time
        Ex. V[i][t] -> Actual time in seconds for activity i at index t
    This choice preserves motonicity and was made to avoid equality comparisons between floats. 
    """
    l = init_l(V)
    p = init_p(V)
    min_taus = min_time_per_activity(V, activities)
    visited = [set() for _ in V]
    to_visit = [(A_star_bound(V, activities, min_taus, 0, t), 0, t)
                for t in V[0].keys() if q[0][t] <= Q]
    heapq.heapify(to_visit)

    while len(to_visit) > 0:
        _, i, t = heapq.heappop(to_visit)
        visited[i].add(t)
        if i == len(activities)-1:
            return Solution(t, activities, V, p, visited)

        completion_time = activities[i].completion_time(V[i][t])
        for t_next in V[i+1].keys():
            if t_next in visited[i+1]:
                continue
            if completion_time > V[i+1][t_next]:
                continue

            # If the resouce consumption goes below Q we insert the vertex in the heap
            new_consumption = l[i][t] + q[i][t]
            if l[i+1][t_next] + q[i+1][t_next] > Q and new_consumption + q[i+1][t_next] <= Q:
                heapq.heappush(to_visit,
                               (A_star_bound(V, activities, min_taus, i+1, t_next), i+1, t_next))

            if new_consumption < l[i+1][t_next]:
                l[i+1][t_next] = new_consumption
                p[i+1][t_next] = t

    return None
