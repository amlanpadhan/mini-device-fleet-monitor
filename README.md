# Mini Device Fleet Monitor

A small Python application that monitors a fleet of simulated devices.

Each device can be registered with the application and can periodically send
a heartbeat. The application keeps track of the latest heartbeat and
automatically determines whether a device is ONLINE or OFFLINE.

## Features

- Register a device
- Receive device heartbeats
- List all registered devices
- View details of a single device
- View fleet summary
- Automatically mark devices OFFLINE after 30 seconds without a heartbeat
- Simulate 5 devices sending heartbeats
- Automated tests

## Technology

- Python
- FastAPI
- Uvicorn
- pytest
- Requests

## Project Structure

```text
Mini Fleet Device Monitor/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   └── test_main.py
│
└── simulator/
    └── simulator.py

## Prerequisites

Python 3
pip
Installation

Clone the repository and open a terminal in the project directory.

Create a virtual environment:

python -m venv venv

Activate it on Windows PowerShell:

.\venv\Scripts\Activate.ps1

Install the required packages:

pip install -r requirements.txt
Running the Application

Start the FastAPI server:

uvicorn src.main:app --reload

The application will be available at:

http://127.0.0.1:8000

Interactive API documentation is available at:

http://127.0.0.1:8000/docs
Running the Simulator

Open another terminal and activate the virtual environment.

Run:

python simulator/simulator.py

The simulator registers five devices and sends a heartbeat from each device
every 5 seconds.

To simulate a stopped device, for example device-03, run:

python simulator/simulator.py device-03

That device will not send heartbeats and will become OFFLINE after more than
30 seconds.

Running Tests

Run:

python -m pytest

The tests cover:

Device registration
Heartbeat handling
ONLINE status
OFFLINE status after 30 seconds
Fleet summary
API Endpoints
Register a Device
POST /devices

Request:

{
  "id": "device-01",
  "name": "Lab Device 01"
}
Send a Heartbeat
POST /devices/{id}/heartbeat

Request:

{
  "timestamp": "2026-09-30T10:30:00Z",
  "status": "OK"
}
List Devices
GET /devices

Example response:

[
  {
    "id": "device-01",
    "name": "Lab Device 01",
    "status": "ONLINE",
    "last_heartbeat": "2026-09-30T10:30:00Z"
  }
]
Get Device Details
GET /devices/{id}
Get Fleet Summary
GET /summary

Example response:

{
  "total": 5,
  "online": 5,
  "offline": 0
}
Device Status

A device is considered:

ONLINE when its latest heartbeat was received within the last 30 seconds.
OFFLINE when more than 30 seconds have passed since its latest heartbeat.

The status is calculated when the device information is requested. No
background process is required.

Assumptions
Device IDs are unique.
Devices must be registered before sending heartbeats.
The application uses the server's heartbeat reception time to determine
device status.
Device information is stored in memory.
Restarting the application clears all registered devices.
Known Limitations
Data is not persistent and is lost when the application stops.
There is no authentication or authorization.
The application is intended for a small simulated fleet.
The simulator runs locally.
What I Would Improve With One Additional Day

With more time, I would consider:

Adding persistent storage such as SQLite or PostgreSQL.
Adding better input validation.
Adding structured logging.
Adding more test cases for invalid requests and concurrent heartbeats.
Adding configuration through environment variables.
AI Usage

I used ChatGPT as an AI coding assistant during development.

It was used for:

Discussing the project structure and implementation approach.
Generating an initial version of the API and test code.
Troubleshooting setup and dependency issues.

I reviewed and tested the generated code and kept the implementation
simple to match the requirements.

One improvement made during development was testing the 30-second timeout
without making the test wait for 30 seconds. The test directly uses an older
heartbeat time so that the test remains fast and deterministic.

I personally verified that the application runs locally, the simulator
sends heartbeats, a stopped device becomes OFFLINE after the timeout, and
the automated tests pass.

