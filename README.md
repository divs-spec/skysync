# skysync

**skysyncswarm**— a hybrid Python/MATLAB swarm orchestration stack that turns drone telemetry into coordinated multi-UAV missions using RRT* planning, cooperative tasking, and real-time command delivery.

***skysyncswarm*** is an integrated, research-minded prototype that fuses three core capabilities required for practical multi-UAV systems:

Real-time telemetry & command exchange (Flask-based server & client),

Trajectory planning (RRT prototype in Python + MATLAB RRTstar.m reference),

Cooperative multiagent behavior (greedy task allocation + APF smoothing inspired by cooperative-attack research).

It translates streaming telemetry into task assignment and collision-aware waypoint sequences in seconds. The codebase targets reproducible hackathon demos, research validation, and clear migration paths to SITL or field deployments.

----

**🏷️ Problem Statement**

Traditional drone control is single-agent and limited:

Managing multiple drones manually is inefficient.

Lack of interoperability between existing swarm simulators, libraries, and AI models.

No unified platform for simulation → planning → networking → execution.

SkySyncSwarm solves this by providing a plug-and-play ecosystem where swarm behaviors, communication protocols, and mission execution can be developed, tested, and scaled seamlessly.

---

***skysyncswarm*** is a modular swarm orchestration stack that converts real-time drone telemetry into coordinated multi-UAV missions using RRT-style path planning and cooperative allocation. It merges a Flask telemetry hub, a Python RRT planner (plus MATLAB RRTstar.m as a canonical reference), and cooperative guidance ideas (virtual guidance + APF smoothing) into one reproducible demo-ready repository.

----

**Repository Structure**

```
/comm
  server.py            # Flask server (endpoints: /update_state, /get_waypoints, /status)
  client.py            # Example drone client
/planning
  rrt.py               # Python RRT (prototype)
  RRTstar.m            # MATLAB RRT* reference
/cooperative
  task_allocator.py    # Greedy nearest/priority assignment
  apf.py               # Artificial Potential Field smoother
/control
  controller.py        # orchestrator_tick(states) -> planned waypoints
/config
  drones.json
  tasks.json
README.md
requirements.txt

```
---

**Prerequisites & installation**

Python 3.8+

(Optional) MATLAB + MATLAB Engine for Python if you want to call RRTstar.m directly.

Recommended packages (install via pip):

```
pip install -r requirements.txt
# requirements.txt contains:
# flask
# numpy
# scipy
# scikit-learn
# requests

```
---

**Quickstart — run the demo (Windows / Linux)**

Recommended: run from project root (the folder that contains comm/, control/, etc.)

***Linux / macOS***

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m comm.server            # run server
# in other terminals:
python comm/client.py --id drone1
python comm/client.py --id drone2
```

***Windows PowerShell***

```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m comm.server
# in other PS windows:
python comm/client.py --id drone1
python comm/client.py --id drone2
```

Notes:

If you run python comm/server.py directly and see ModuleNotFoundError: No module named 'control', either run from project root with python -m comm.server, or use the patched comm/server.py which inserts project root into sys.path.

---

**Concrete outputs (from your run) — verbatim**

***GET /status returned:***
```
{
  "drone_count": 1,
  "drones": [
    "drone1"
  ]
}
```

***GET /get_waypoints?id=drone1 returned:***
```
{
  "waypoints": [
    [39.72613775384949, 9.946606646250359, 5.0],
    [40.52371257406809, 9.075636975967132, 5.0],
    [40.0, 10.0, 5.0]
  ]
}
```
---

**Architecture & module descriptions (technical)**

* comm/server.py
  
  * Flask endpoints: ```/update_state```, ```/get_waypoints```, ```/status```.
  * Maintains in-memory ```DRONE_STATE``` mapping: ```id -> {pos, battery, last_seen}.```
  * On get_waypoints, snapshots states and calls ```control.controller.orchestrator_tick(states).```

* control/controller.py
  * orchestrator_tick(states):
    * Reads tasks (from config or dynamic source).
    * Calls cooperative.task_allocator.allocate_tasks (greedy nearest + priority).
    * For each assignment, calls planning.rrt.rrt to compute a path (2D/3D compact RRT).
    * Applies cooperative.apf.apf_smooth to refine path.
    * Returns dict[drone_id] -> waypoints.

* planning/rrt.py
  * Lightweight RRT implementation; parameterizable max_iter, step_size.
  * Currently basic collision checks are optional — obstacles support can be added.

* cooperative/task_allocator.py
  * Greedy assignment sorted by (priority desc, distance asc).

* cooperative/apf.py
  * Artificial Potential Field smoother used to nudge discrete waypoints to smoother, safer paths.

---

**MATLAB integration & migration path**

* ```planning/RRTstar.m``` is included as the canonical MATLAB research implementation.

* Two integration strategies:
  * Quick: call RRTstar.m via the MATLAB Engine for Python (matlab.engine).

  * Production: port RRTstar.m to Python/NumPy (or use OMPL bindings) for runtime performance and to remove MATLAB dependency.

---

**Deployment considerations (SITL → real drones)**

* Coordinate transforms: convert local ENU meters → GPS (lat/lon/alt) for MAVLink missions. Consider using geographic libraries (pyproj, geodetic utils).

* Autopilot integration: implement control/drone_interface.py using DroneKit/MAVSDK to upload mission waypoints, or convert list to MAVLink mission items.

* Message bus: for larger swarms, prefer MQTT or ROS2 DDS for multicast instead of HTTP polling.

* Safety: implement geofencing, RTL, battery thresholds, and heartbeat/failsafe logic.

---

**🎯 Use Cases**

- Defense & Surveillance → Multi-drone patrols with adaptive formations.

- Disaster Response → Swarm search-and-rescue in dynamic terrains.

- Agriculture → Coordinated crop monitoring & spraying.

- Research & Academia → Unified platform for swarm robotics studies.

---

**🔑 Unique Selling Points (USP)**

- Unified Framework → Combines simulation, AI, and autonomy in one repo.

- Hackathon-Ready → Ready-to-demo missions with visualizations.

- Scalable & Modular → Extend with new AI models or swarm algorithms.

- Real-World Applications → Built with real defense and disaster scenarios in mind.

---

**Tech stack**

Python 3, Flask (comms), NumPy/SciPy, scikit-learn (if KMeans used), matplotlib for plotting.

Optional: MATLAB + MATLAB Engine, ROS/ROS2, DroneKit/MAVSDK, Gazebo/SITL.

---

**Contributors**
Divyani Singh

---

**Contact**
email id - divyanisingh210221101@gmail.com
