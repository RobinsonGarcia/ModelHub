# start_local.py
import subprocess
import time
import sys
import os
import signal
from typing import List, Dict
from dotenv import load_dotenv
from app_config import DATA_DIR, ensure_data_dirs

# 1) Load our .env environment variables
load_dotenv()

def build_gateway_dict() -> Dict[str, any]:
    """Build a config dict for the gateway from environment vars."""
    gateway_port = int(os.getenv("GATEWAY_PORT", "5001"))
    return {
        "name": "gateway",
        "path": "gateway",
        "port": gateway_port,
        "env_vars": {
            "GATEWAY_PORT": str(gateway_port),
            "DOCKER_MODE": os.getenv("DOCKER_MODE", "false"),
            # You could also pass LOG_LEVEL here if you want:
            # "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        },
    }

def build_service_dict(service_name: str) -> Dict[str, any]:
    """Build a config dict for each microservice from environment vars."""
    uppercase = service_name.upper()       # e.g. "SERVICE1"
    service_port = int(os.getenv(f"{uppercase}_PORT", "5000"))
    service_name_env = os.getenv(f"{uppercase}_NAME", service_name)
    return {
        "name": service_name,
        "path": f"services/{service_name}",  # default path
        "port": service_port,
        "env_vars": {
            f"{uppercase}_NAME": service_name_env,    # e.g. SERVICE1_NAME=service1
            f"{uppercase}_PORT": str(service_port),   # e.g. SERVICE1_PORT=5002
            # You could also pass LOG_LEVEL if needed
            # "LOG_LEVEL": os.getenv("LOG_LEVEL", "INFO"),
        },
    }

def load_services_from_env() -> List[Dict[str, any]]:
    """Read the SERVICES list from .env and build config for each microservice + gateway."""
    services_env = os.getenv("SERVICES", "")  # e.g. "service1,service2"
    service_names = [s.strip() for s in services_env.split(",") if s.strip()]

    # Start with the gateway
    all_services = [build_gateway_dict()]

    # Then add each microservice
    for svc_name in service_names:
        svc_dict = build_service_dict(svc_name)
        all_services.append(svc_dict)

    return all_services


def start_service(service: Dict[str, any]) -> subprocess.Popen:
    """Start an individual service as a subprocess."""
    env = os.environ.copy()
    env.update(service["env_vars"])           # merge in the special env vars
    env["DATA_DIR"] = DATA_DIR               # always pass the shared data dir
    print(f"🚀 Starting {service['name']} on port {service['port']} (local)...")

    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=service["path"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(2)  # short delay to give it time to bind the port
    return proc


def stop_services(*args) -> None:
    """Stops all running services gracefully."""
    print("\n⛔ Stopping all services...")
    for p in processes:
        p.terminate()
    sys.exit(0)


if __name__ == "__main__":
    print("🚀 Starting API Hub Locally...\n")

    # 2) Build the list of services dynamically from .env
    SERVICES = load_services_from_env()
    # E.g. SERVICES = [
    #   {
    #     "name": "gateway",
    #     "path": "gateway",
    #     "port": 5001,
    #     "env_vars": {...},
    #   },
    #   {
    #     "name": "service1",
    #     "path": "services/service1",
    #     "port": 5002,
    #     "env_vars": {...},
    #   },
    #   ...
    # ]

    # 3) Ensure data directories exist for each
    ensure_data_dirs([s["name"] for s in SERVICES])

    processes = []
    for svc in SERVICES:
        proc = start_service(svc)
        processes.append(proc)

    # 4) Listen for CTRL+C to shut down gracefully
    signal.signal(signal.SIGINT, stop_services)
    print("\n✅ All services are running locally. Press CTRL+C to stop.")

    # 5) Keep the main thread alive
    while True:
        time.sleep(1)