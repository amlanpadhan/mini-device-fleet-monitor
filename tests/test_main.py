from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

from src.main import app, devices


client = TestClient(app)


def setup_function():
    devices.clear()


def test_register_device():
    response = client.post(
        "/devices",
        json={
            "id": "device-01",
            "name": "Lab Device 01"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == "device-01"


def test_heartbeat():
    client.post(
        "/devices",
        json={
            "id": "device-01",
            "name": "Lab Device 01"
        }
    )

    response = client.post(
        "/devices/device-01/heartbeat",
        json={
            "timestamp": "2026-09-30T10:30:00Z",
            "status": "OK"
        }
    )

    assert response.status_code == 200


def test_device_online_after_heartbeat():
    client.post(
        "/devices",
        json={
            "id": "device-01",
            "name": "Lab Device 01"
        }
    )

    client.post(
        "/devices/device-01/heartbeat",
        json={
            "timestamp": "2026-09-30T10:30:00Z",
            "status": "OK"
        }
    )

    response = client.get("/devices/device-01")

    assert response.status_code == 200
    assert response.json()["status"] == "ONLINE"


def test_device_offline_after_30_seconds():
    client.post(
        "/devices",
        json={
            "id": "device-01",
            "name": "Lab Device 01"
        }
    )

    devices["device-01"]["last_heartbeat"] = (
        datetime.now(timezone.utc) - timedelta(seconds=31)
    )

    response = client.get("/devices/device-01")

    assert response.status_code == 200
    assert response.json()["status"] == "OFFLINE"


def test_summary():
    client.post(
        "/devices",
        json={
            "id": "device-01",
            "name": "Lab Device 01"
        }
    )

    client.post(
        "/devices",
        json={
            "id": "device-02",
            "name": "Lab Device 02"
        }
    )

    client.post(
        "/devices/device-01/heartbeat",
        json={
            "timestamp": "2026-09-30T10:30:00Z",
            "status": "OK"
        }
    )

    response = client.get("/summary")

    assert response.status_code == 200
    assert response.json()["total"] == 2
    assert response.json()["online"] == 1
    assert response.json()["offline"] == 1