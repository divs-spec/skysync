import math, random
def allocate_tasks(drones, tasks):
    remaining = tasks.copy()
    assignments = {}
    for did, st in drones.items():
        if not remaining: break
        sx, sy, sz = st['pos']
        remaining.sort(key=lambda t: (t.get('priority',0)*-1, math.dist((sx,sy,sz), t['pos'])))
        task = remaining.pop(0)
        assignments[did] = task
    return assignments
