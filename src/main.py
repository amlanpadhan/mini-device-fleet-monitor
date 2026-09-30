from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI(title="Mini Device Fleet Monitor")

devices = {}


class Device(BaseModel):
    id: str
    name: str


class Heartbeat(BaseModel):
    timestamp: datetime
    status: str


@app.post("/devices")
def register_device(device: Device):
    if device.id in devices:
        raise HTTPException(status_code=400, detail="Device already exists")

    devices[device.id] = {
        "id": device.id,
        "name": device.name,
        "last_heartbeat": None,
        "heartbeat_status": None
    }

    return devices[device.id]


@app.post("/devices/{device_id}/heartbeat")
def receive_heartbeat(device_id: str, heartbeat: Heartbeat):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")

    devices[device_id]["last_heartbeat"] = datetime.now(timezone.utc)
    devices[device_id]["heartbeat_status"] = heartbeat.status

    return {"message": "Heartbeat received"}


def get_status(device):
    if device["last_heartbeat"] is None:
        return "OFFLINE"

    elapsed = (
        datetime.now(timezone.utc) - device["last_heartbeat"]
    ).total_seconds()

    if elapsed <= 30:
        return "ONLINE"

    return "OFFLINE"


@app.get("/devices")
def list_devices():
    result = []

    for device in devices.values():
        result.append({
            "id": device["id"],
            "name": device["name"],
            "status": get_status(device),
            "last_heartbeat": device["last_heartbeat"]
        })

    return result


@app.get("/devices/{device_id}")
def get_device(device_id: str):
    if device_id not in devices:
        raise HTTPException(status_code=404, detail="Device not found")

    device = devices[device_id]

    return {
        "id": device["id"],
        "name": device["name"],
        "status": get_status(device),
        "last_heartbeat": device["last_heartbeat"]
    }


@app.get("/summary")
def get_summary():
    total = len(devices)
    online = 0

    for device in devices.values():
        if get_status(device) == "ONLINE":
            online += 1

    return {
        "total": total,
        "online": online,
        "offline": total - online
    }