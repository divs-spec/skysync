import random, math
class Node:
    def __init__(self, point, parent=None):
        self.point = point
        self.parent = parent
def dist(a,b):
    return math.sqrt(sum((a[i]-b[i])**2 for i in range(len(a))))
def rrt(start, goal, bounds, obstacles=None, max_iter=1000, step_size=1.0):
    dims = len(start)
    def sample():
        return tuple(random.uniform(bounds[i][0], bounds[i][1]) for i in range(dims))
    tree = [Node(tuple(start))]
    for i in range(max_iter):
        s = sample() if random.random() > 0.1 else tuple(goal)
        nearest = min(tree, key=lambda n: dist(n.point, s))
        vec = tuple(s[j]-nearest.point[j] for j in range(dims))
        d = dist(nearest.point, s)
        if d==0: continue
        new = tuple(nearest.point[j] + vec[j]/d * min(step_size, d) for j in range(dims))
        node = Node(new, nearest)
        tree.append(node)
        if dist(new, goal) <= step_size:
            path = [goal]
            cur = node
            while cur:
                path.append(cur.point)
                cur = cur.parent
            path.reverse()
            return path
    return []
