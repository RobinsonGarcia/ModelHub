import subprocess
import time
import sys
import os
import signal

SERVICES = [
    {
        "name": "gateway",
        "path": "gateway",
        "port": 5001,
        "env_vars": {
            "GATEWAY_PORT": "5001",  # Force gateway to 5001
            "DOCKER_MODE": "false",  # Local
        },
    },
    {
        "name": "service1",
        "path": "services/service1",
        "port": 5002,
        "env_vars": {
            "SERVICE_NAME": "service1",
            "PORT": "5002",
        },
    },
    {
        "name": "service2",
        "path": "services/service2",
        "port": 5003,
        "env_vars": {
            "SERVICE_NAME": "service2",
            "PORT": "5003",
        },
    },
]

processes = []

def start_service(service):
    env = os.environ.copy()
    for k, v in service["env_vars"].items():
        env[k] = v

    print(f"🚀 Starting {service['name']} on port {service['port']} (local)...")
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=service["path"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    processes.append(proc)
    time.sleep(2)  # give time to start

def stop_services(signal_received, frame):
    print("\n⛔ Stopping all services...")
    for proc in processes:
        proc.terminate()
    sys.exit(0)

if __name__ == "__main__":
    print("🚀 Starting API Hub Locally...\n")

    for svc in SERVICES:
        start_service(svc)

    signal.signal(signal.SIGINT, stop_services)
    print("\n✅ All services are running locally. Press CTRL+C to stop.")
    while True:
        time.sleep(1)