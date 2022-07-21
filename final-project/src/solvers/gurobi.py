from typing import Mapping, Sequence
import gurobipy as gb
import numpy as np

from ..utils import line_between_two_points

from ..time_discretizer import TimeDiscretizer

from ..activity import Activity


def gurobi_solve(activities: Sequence[Activity],
                 Q: float,
                 discretizer: TimeDiscretizer,
                 replenishments: bool = False,
                 replenishment_duration: int = 1,
                 verbose: bool = False):

    ## Model & Variable initialization
    tdaspr = gb.Model()
    if not verbose:
        tdaspr.setParam('OutputFlag', 0)
    tdaspr.modelSense = gb.GRB.MINIMIZE
    n_activities = len(activities)
    M = Q*n_activities*10  # A big enough number

    x = []
    for activity in activities:
        n_times = discretizer.activity_to_index(activity, activity.end)
        x.append(tdaspr.addMVar((n_times), vtype=gb.GRB.BINARY))

    t = []
    for activity in activities:
        n_times = discretizer.activity_to_index(activity, activity.end)
        t.append(tdaspr.addMVar((n_times), vtype=gb.GRB.CONTINUOUS))

    y = tdaspr.addMVar((n_activities), vtype=gb.GRB.BINARY)  # Replenishments
    
    ## Constraints
    # 12a
    _ = [tdaspr.addConstr(gb.quicksum(xi) == 1) for xi in x]

    # 12b
    for i, activity in enumerate(activities):
        e = np.array(discretizer.discretize_activity(activity)[:-1])
        l = e+discretizer.eps
        for s in range(x[i].shape[0]):
            tdaspr.addConstr(e[s]*x[i][s] <= t[i][s])
            tdaspr.addConstr(t[i][s] <= l[s]*x[i][s])

    # 12c
    t_i = [gb.quicksum(ti) for ti in t]

    # 12d
    d_i = []
    for i, activity in enumerate(activities):
        times = np.array(discretizer.discretize_activity(activity))
        taus = np.array([activity.duration(time) for time in times])
        a, b = line_between_two_points(
            times[:-1], taus[:-1], times[1:], taus[1:])

        d_i.append(gb.quicksum([a[s]*t[i][s] + b[s]*x[i][s]
                   for s in range(len(a))]))

    # 12e
    _ = [tdaspr.addConstr(t_i[i] + d_i[i] + replenishment_duration *
                          y[i] <= t_i[i+1]) for i in range(n_activities-1)]

    # 13d
    q_i = []
    for i, activity in enumerate(activities):
        times = np.array(discretizer.discretize_activity(activity))
        rhos = np.array([activity.resources(i) for i in times])
        a, b = line_between_two_points(
            times[:-1], rhos[:-1], times[1:], rhos[1:])

        q_i.append(gb.quicksum([a[s]*t[i][s] + b[s]*x[i][s]
                   for s in range(len(a))]))

    # 13e
    for i in range(n_activities):
        for j in range(i, n_activities):
            tdaspr.addConstr(gb.quicksum(
                q_i[i:j+1]) <= Q + M*gb.quicksum(y[i:j]))

    _ = tdaspr.addConstr(gb.quicksum(q_i) <= Q)

    ## Remove replenishments
    if not replenishments:
        for yi in y:
            tdaspr.addConstr(yi == 0)

    ## Solve
    _ = tdaspr.setObjective(d_i[-1] + t_i[-1])

    tdaspr.optimize()

    return tdaspr
