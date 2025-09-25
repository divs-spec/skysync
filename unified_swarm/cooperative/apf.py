import math
def apf_smooth(path, obstacles, attract_k=1.0, repel_k=100.0, d0=5.0, iterations=10):
    pts = [list(p) for p in path]
    for _ in range(iterations):
        new_pts = []
        for i,p in enumerate(pts):
            fx=fy=fz=0.0
            gx,gy,gz = pts[-1]
            fx += attract_k * (gx - p[0]); fy += attract_k * (gy - p[1]); fz += attract_k * (gz - p[2])
            for ox,oy,oz,r in obstacles:
                d = math.dist(p, (ox,oy,oz))
                if d < d0 and d>0:
                    mag = repel_k * (1.0/d - 1.0/d0) / (d*d)
                    fx += mag * (p[0]-ox); fy += mag * (p[1]-oy); fz += mag * (p[2]-oz)
            step = 0.1
            new_pts.append([p[0] + step*fx, p[1] + step*fy, p[2] + step*fz])
        pts = new_pts
    return pts
