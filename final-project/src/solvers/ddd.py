

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
