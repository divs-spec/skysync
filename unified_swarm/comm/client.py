import requests, time, argparse, random
SERVER = 'http://127.0.0.1:5000'
def run_drone(drone_id):
    x = random.uniform(0, 5); y = random.uniform(0, 5); z = 5.0
    battery = 100.0
    for step in range(200):
        payload = {'id': drone_id, 'pos': [x, y, z], 'battery': battery}
        try:
            requests.post(SERVER + '/update_state', json=payload, timeout=1.0)
        except Exception as e:
            print('telemetry error', e)
        try:
            r = requests.get(SERVER + '/get_waypoints', params={'id': drone_id}, timeout=2.0)
            if r.ok:
                data = r.json(); wps = data.get('waypoints', [])
                if wps:
                    tx, ty, tz = wps[0]
                    dx = tx - x; dy = ty - y
                    dist = (dx*dx + dy*dy)**0.5
                    if dist > 0.01:
                        step_move = 0.5
                        x += step_move * dx/dist
                        y += step_move * dy/dist
            else:
                print('get_waypoints failed', r.status_code, r.text)
        except Exception as e:
            print('waypoint request error', e)
        battery -= random.uniform(0.05, 0.5)
        time.sleep(0.5)
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--id', required=True); args = ap.parse_args()
    run_drone(args.id)
