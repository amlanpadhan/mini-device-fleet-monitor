import requests
import time
import sys
from datetime import datetime, timezone


BASE_URL = "http://127.0.0.1:8000"

devices = [
    ("device-01", "Lab Device 01"),
    ("device-02", "Lab Device 02"),
    ("device-03", "Lab Device 03"),
    ("device-04", "Lab Device 04"),
    ("device-05", "Lab Device 05")
]


def register_devices():
    for device_id, name in devices:
        response = requests.post(
            f"{BASE_URL}/devices",
            json={
                "id": device_id,
                "name": name
            }
        )

        if response.status_code == 200:
            print(f"{device_id} registered")
        else:
            print(f"{device_id}: {response.json()['detail']}")


def send_heartbeats():
    stopped_device = None

    if len(sys.argv) > 1:
        stopped_device = sys.argv[1]

    while True:
        for device_id, _ in devices:

            if device_id == stopped_device:
                continue

            requests.post(
                f"{BASE_URL}/devices/{device_id}/heartbeat",
                json={
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "status": "OK"
                }
            )

            print(f"{device_id} -> heartbeat")

        print()
        time.sleep(5)


register_devices()
send_heartbeats()