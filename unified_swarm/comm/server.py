import logging
werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.ERROR)   # change to WARNING or INFO as desired

# Fixes import path when running this script directly.
# Recommended: run from project root with `python -m comm.server`
import os, sys
# Ensure project root (parent of comm/) is on sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify
from threading import Lock
from control.controller import orchestrator_tick
import time, threading

app = Flask(__name__)

from flask import jsonify

@app.route('/')
def index():
    return jsonify({'status': 'unified_swarm_server', 'version': '0.1'})

@app.route('/favicon.ico')
def favicon():
    # 204 No Content avoids sending a file and prevents 404s in logs
    return '', 204

DRONE_STATE = {}
STATE_LOCK = Lock()

@app.route('/update_state', methods=['POST'])
def update_state():
    data = request.get_json()
    if not data or 'id' not in data or 'pos' not in data:
        return jsonify({'error': 'invalid payload'}), 400
    drone_id = data['id']
    pos = data['pos']
    battery = data.get('battery', None)
    with STATE_LOCK:
        DRONE_STATE[drone_id] = {'pos': tuple(pos), 'battery': battery, 'last_seen': time.time()}
    return jsonify({'status': 'ok'})

@app.route('/get_waypoints', methods=['GET'])
def get_waypoints():
    drone_id = request.args.get('id')
    if not drone_id:
        return jsonify({'error': 'id required'}), 400
    with STATE_LOCK:
        states = {k:v.copy() for k,v in DRONE_STATE.items()}
    if drone_id not in states:
        return jsonify({'error': 'unknown drone id'}), 404
    # Call orchestrator to compute waypoints for all drones (non-blocking snapshot)
    planned = orchestrator_tick(states)
    return jsonify({'waypoints': planned.get(drone_id, [])})

@app.route('/status', methods=['GET'])
def status():
    with STATE_LOCK:
        return jsonify({'drone_count': len(DRONE_STATE), 'drones': list(DRONE_STATE.keys())})

if __name__ == '__main__':
    # Start background thread that periodically runs controller orchestration (optional)
    def bg_loop():
        while True:
            time.sleep(1.0)
    t = threading.Thread(target=bg_loop, daemon=True)
    t.start()
    # If you prefer using module mode (recommended), run: python -m comm.server
    app.run(host='0.0.0.0', port=5000, debug=True)
