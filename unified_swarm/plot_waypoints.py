# plot_waypoints.py
import matplotlib.pyplot as plt

waypoints = [
    [39.72613775384949, 9.946606646250359, 5.0],
    [40.52371257406809, 9.075636975967132, 5.0],
    [40.0, 10.0, 5.0]
]
xs = [p[0] for p in waypoints]
ys = [p[1] for p in waypoints]

plt.figure(figsize=(6,6))
plt.plot(xs, ys, '-o', label='planned path')
plt.scatter([40.0],[10.0], c='red', marker='x', label='task goal (40,10)')
plt.title('Waypoints (top-down)')
plt.xlabel('X'); plt.ylabel('Y')
plt.legend(); plt.grid()
plt.axis('equal')
plt.show()
