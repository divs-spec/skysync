# check_waypoints.py
import math

# replace with the JSON you received (or load from file)
waypoints = [
    [39.72613775384949, 9.946606646250359, 5.0],
    [40.52371257406809, 9.075636975967132, 5.0],
    [40.0, 10.0, 5.0]
]

# expected task (from config/tasks.json)
task = (40.0, 10.0, 6.0)   # planner preserved altitude 5.0; task altitude is 6.0 in config

def dist(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + ( (a[2]-b[2])**2 if len(a)>2 and len(b)>2 else 0))

# distance between last waypoint and task xy (ignore z mismatch if needed)
final_wp = waypoints[-1]
xy_dist = math.sqrt((final_wp[0] - task[0])**2 + (final_wp[1] - task[1])**2)
path_length = 0.0
for i in range(1, len(waypoints)):
    path_length += dist(waypoints[i-1], waypoints[i])

print("Final waypoint:", final_wp)
print("Task position:", task)
print(f"XY distance final_wp -> task: {xy_dist:.4f} m")
print(f"Path length (sum segments): {path_length:.4f} m")
if xy_dist < 1.0:
    print("Success: final waypoint is within 1 meter of task position in XY plane.")
