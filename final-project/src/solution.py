from dataclasses import dataclass
from typing import Mapping, Sequence, Set

from .activity import Activity


class Solution:
    def __init__(self,
                 final_activity: int,
                 activities: Sequence[Activity],
                 V: Sequence[Mapping[int, float]],
                 p: Sequence[Mapping[int, int]],
                 visited: Sequence[Set[int]],
                 ):
        self.activities = activities
        self.V = V
        self.n_total_nodes = sum([len(v) for v in V])
        self.n_visited_nodes = sum([len(v) for v in visited])
        self.path = self.init_path(final_activity, p)

    def init_path(self, final_activity, p):
        last = final_activity
        path = [last]
        for i in range(len(self.activities)-1, 0, -1):
            last = p[i][last]
            path.append(last)

        return path[::-1]

    def activity_durations(self):
        return [a.duration(v[t]) for a, t, v in zip(self.activities, self.path, self.V)]

    def activity_resouce_consumption(self):
        return [a.resources(v[t]) for a, t, v in zip(self.activities, self.path, self.V)]

    def completion_time(self):
        return self.activities[-1].completion_time(self.V[-1][self.path[-1]])

    def resources_consumed(self):
        return sum(self.activity_resouce_consumption())

    def summary(self):
        return self.completion_time(), self.resources_consumed(), self.n_visited_nodes

    def __repr__(self):
        duration, resources, nodes_visited = self.summary()

        return f"""Completion time: {duration:.2f}
Resources consumed: {resources:.2f}
Nodes visited: {nodes_visited}"""
