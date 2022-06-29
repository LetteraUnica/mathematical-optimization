from dataclasses import dataclass
from typing import Mapping, Sequence

from .activity import Activity


@dataclass
class Solution:
    final_activity: int
    activities: Sequence[Activity]
    l: Sequence[Mapping[int, float]]
    p: Sequence[Mapping[int, int]]
    visited_nodes: int

    def compute_path(self):
        last = self.final_activity
        path = [last]
        for i in range(len(self.activities)-1, 0, -1):
            last = self.p[i][last]
            path.append(last)

        return path[::-1]

    def activity_durations(self):
        return [a.duration(t) for a, t in zip(self.activities, self.compute_path())]

    def activity_resouces(self):
        return [a.resources(t) for a, t in zip(self.activities, self.compute_path())]

    def total_nodes(self):
        return sum([len(l) for l in self.l])

    def summary(self):
        return sum(self.activity_durations()), sum(self.activity_resouces()), self.visited_nodes

    def __repr__(self):
        duration, resources, nodes_visited = self.summary()

        return f"""Completion time: {duration:.2f}
Resources consumed: {resources:.2f}
Nodes visited: {nodes_visited}"""
