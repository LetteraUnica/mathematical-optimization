import heapq
from math import ceil
from typing import List, Set, Tuple

import numpy as np

from .utils import fill_like

from .activity import Activity


def init_l(V: List[List[float]]) -> List[List[float]]:
    """Initializes the labels, 0 for the first activity vertexes and np.inf otherwise"""
    l = [[0 for _ in range(len(V[0]))]]
    for i in range(1, len(V)):
        l.append([np.inf for _ in range(len(V[i]))])

    return l


def min_time_per_activity(V: List[List[float]], activities: List[Activity]) -> List[float]:
    """Returns a list with the minimum possible time to do each activity"""
    return [min(activities[i].duration(V[i])) for i in range(len(V))]


def A_star_bound(V: List[List[float]], activities: List[Activity], min_taus: List[float], i: int, t: int):
    """Lower bound on the total completion time when doing activity i at time t"""
    return activities[i].completion_time(V[i][t]) + sum(min_taus[i+1:])


def TEN_solve(V: List[List[float]], activities: List[Activity], q: List[List[float]], Q: float):
    """Solves the TDASP in a Time Expanded Network, implements Algorithm 1 of the paper
    https://www.sciencedirect.com/science/article/pii/S0377221721009838?

    This implementation uses a MinHeap to keep the vertexes sorted and achieves a
    time complexity of O(n*m^2), less than the one cited in the paper O(n^2*m^2)

    Note: In this code t does not stand for time, but stands for the index of V which then gives the time
        Ex. V[i][t] -> Actual time in seconds for activity i at index t
    This choice preserves motonicity and was made to avoid equality comparisons between floats. 
    """
    l = init_l(V)
    p = fill_like(V, None)
    min_taus = min_time_per_activity(V, activities)
    visited = set()
    to_visit = [(A_star_bound(V, activities, min_taus, 0, t), 0, t)
                for t in range(len(V[0])) if q[0][t] <= Q]
    heapq.heapify(to_visit)

    while len(to_visit) > 0:
        _, i, t = heapq.heappop(to_visit)
        visited.add((i, t))
        if i == len(activities)-1:
            print("Solved!")
            break

        completion_time = activities[i].completion_time(V[i][t])
        for t_next in range(len(V[i+1])):
            if (i+1, t_next) in visited:
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
                p[i+1][t_next] = (i, t)

    return (i, t), l, p


def DDD_initialize(activities: List[Activity], q: List[List[float]]):
    V = set()
    for i, activity in enumerate(activities):
        V, q = DDD_addRecursive(V, q, (i, activity.start))
        V, q = DDD_addRecursive(V, q, (i, activity.end))

    return V, q


def time_to_index(i: int, t: float) -> int:
    pass


def DDD_addRecursive(V: Set[Tuple[int, float]],
                     q: List[List[float]],
                     activities: List[Activity],
                     i: int, t: float, eps: float):

    #t = time_to_index(i, t)
    activity = activities[i
                          ]
    if (i, t) in V:
        return V, q

    V.add((i, t))
    if t == activity.end:
        q[i][t] = activity.resources(t)
    else:
        min_q = activity.resources(t)
        t_bar = t+eps
        while (i, t_bar) not in V:
            if min_q < activity.resources(t_bar):
                min_q = activity.resources(t_bar)
            t_bar += eps

        if t > activity.start:
            t_bar = t-eps
            min_q = activity.resources(t_bar)
            while (i, t_bar) not in V:
                if min_q < activity.resources(t_bar):
                    min_q = activity.resources(t_bar)
                t_bar -= eps

    if i == len(activities)-1:
        return V, q

    else:
        return DDD_addRecursive(V, q, activities, i+1,
                                max(activities[i+1].end, eps*ceil(activities[i].completion_time(t)/eps)))


def DDD_solve(V: List[List[float]], activities: List[Activity], q: List[List[float]], Q: float):
    V, q = DDD_initialize()

    while True:
        path = TEN_solve(V, activities, q, Q)
        if path[-1][1] == np.inf:
            break

        available_nodes = [(i, t) for i, t in path if (i, t) in V and activities[i].resources(t) > q[i, t]]
        if len(available_nodes)>0:
            i, t_i = available_nodes[0]
            t = min([t for t in V[i] if t > t_i])
            while True:
                t = eps*ceil((t_i + t) / eps)
                if min([activities[i].resources(t_i+i*eps) for i in range(0, t-eps, eps)]) <= q[i, t]:
                    break 
            
            V, q = DDD_addRecursive(V, q, activities, i, t, eps)

        if activities[i].resources(t_i) != q[i, t_i]:
            break
    
    return path
