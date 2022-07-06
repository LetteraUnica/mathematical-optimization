import heapq
import math
from typing import Mapping, Sequence


from ..activity import Activity
from ..solution import Solution

from .ten import *
from .ddd import *


def TEN_delta(V: Sequence[Mapping[int, float]],
              activities: Sequence[Activity],
              q: Sequence[Mapping[int, float]],
              Q: float,
              discretizer: TimeDiscretizer) -> Solution:
    """Solves the TDASPR in a Time Expanded Network, implements Algorithm 4 of the paper
    https://www.sciencedirect.com/science/article/pii/S0377221721009838?

    This implementation uses a MinHeap to keep the vertexes sorted and achieves a
    time complexity of O(n*m^2), less than the one cited in the paper O(n^2*m^2)
    Given n=number of activities and m=number of time discretization steps.

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
            return Solution(t, activities, V, l, p, visited)

        completion_time = activities[i].completion_time(V[i][t])
        t_star = completion_time + \
            activities[i].replenishment_duration(q[i][t] + l[i][t])
        t_star = discretizer.activity_to_index(
            activities[i+1], t_star+discretizer.eps/2)
        if t_star <= discretizer.activity_to_index(activities[i+1], activities[i+1].end):
            V, q = DDD_addRecursive(V, activities, q, i+1, t_star, discretizer)
            

        for t_next in V[i+1].keys():
            if t_next in visited[i+1]:
                continue
            if completion_time > V[i+1][t_next]:
                continue
            if V[i+1][t_next] >= V[i+1][t_star]:
                continue

            # If the resouce consumption goes below Q we insert the vertex in the heap
            new_consumption = l[i][t] + q[i][t]
            if l[i+1][t_next] + q[i+1][t_next] > Q and new_consumption + q[i+1][t_next] <= Q:
                heapq.heappush(to_visit,
                               (A_star_bound(V, activities, min_taus, i+1, t_next), i+1, t_next))

            if new_consumption < l[i+1][t_next]:
                l[i+1][t_next] = new_consumption
                p[i+1][t_next] = t

        for t_next in V[i+1].keys():
            if t_next in visited[i+1]:
                continue
            if V[i+1][t_next] < V[i+1][t_star]:
                continue

            # Replenish the resource
            new_consumption = 0
            if l[i+1][t_next] + q[i+1][t_next] > Q and q[i+1][t_next] <= Q:
                heapq.heappush(to_visit,
                               (A_star_bound(V, activities, min_taus, i+1, t_next), i+1, t_next))

            l[i+1][t_next] = 0
            p[i+1][t_next] = t

    return None
