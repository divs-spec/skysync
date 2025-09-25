from planning.rrt import rrt
from cooperative.task_allocator import allocate_tasks
from cooperative.apf import apf_smooth
def orchestrator_tick(states):
    tasks = [{'id':'t1','pos':(25,25,8),'priority':1},
             {'id':'t2','pos':(40,10,6),'priority':2},
             {'id':'t3','pos':(10,35,6),'priority':1}]
    assignments = allocate_tasks(states, tasks)
    planned = {}
    all_pts = [s['pos'][:2] for s in states.values()] + [t['pos'][:2] for t in tasks]
    xs = [p[0] for p in all_pts]; ys = [p[1] for p in all_pts]
    xmin, xmax = min(xs)-10, max(xs)+10; ymin, ymax = min(ys)-10, max(ys)+10
    bounds2 = [(xmin,xmax),(ymin,ymax)]
    for did, task in assignments.items():
        start = states[did]['pos']; goal2 = (task['pos'][0], task['pos'][1])
        path2d = rrt((start[0], start[1]), (goal2[0], goal2[1]), bounds2, max_iter=500, step_size=2.0)
        if not path2d: wps = []
        else:
            wps = [[float(p[0]), float(p[1]), float(start[2])] for p in path2d]
            wps = apf_smooth(wps, [], iterations=5)
        planned[did] = wps
    return planned
