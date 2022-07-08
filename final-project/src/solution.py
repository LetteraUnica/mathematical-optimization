from dataclasses import dataclass
from typing import Mapping, Sequence, Set, Tuple

from regex import F

from .activity import Activity


class Solution:
    def __init__(self,
                 final_activity: int,
                 activities: Sequence[Activity],
                 V: Sequence[Mapping[int, float]],
                 l: Sequence[Mapping[int, float]],
                 p: Sequence[Mapping[int, int]],
                 visited: Sequence[Set[int]]):
        self.activities = activities
        self.V = V
        self.l = l
        self.n_total_nodes = sum([len(v) for v in V])
        self.n_visited_nodes = sum([len(v) for v in visited])
        self.path = self.init_path(final_activity, p)

    def init_path(self, final_activity_time: int, p: Sequence[Mapping[int, int]]) -> Sequence[int]:
        last = final_activity_time
        path = [last]
        for i in range(len(self.activities)-1, 0, -1):
            last = p[i][last]
            path.append(last)

        return path[::-1]

    def activity_durations(self) -> Sequence[float]:
        return [a.duration(v[t]) for a, t, v in zip(self.activities, self.path, self.V)]

    def activity_resouce_consumption(self) -> Sequence[float]:
        return [a.resources(v[t]) for a, t, v in zip(self.activities, self.path, self.V)]

    def completion_time(self) -> float:
        return self.activities[-1].completion_time(self.V[-1][self.path[-1]])

    def resources_consumed(self) -> float:
        return sum(self.activity_resouce_consumption())

    def n_replenishments(self) -> int:
        return len([li for p, li in zip(self.path, self.l) if li[p] < 1e-8]) - 1

    def __repr__(self) -> str:
        duration, resources = self.completion_time(), self.resources_consumed()
        nodes_visited, n_replenishments = self.n_visited_nodes, self.n_replenishments()

        return f"""Completion time: {duration:.2f}
Resources consumed: {resources:.2f}
Nodes visited: {nodes_visited}
Number of replenishments: {n_replenishments}"""
