# start_local.py
import subprocess
import time
import sys
import os
import signal
from typing import List, Dict
from config import CONFIG, DATA_DIR, ensure_data_dirs

def build_gateway_dict() -> Dict[str, any]:
    """Return gateway configuration for local startup."""
    return {
        "name": "gateway",
        "path": "gateway",
        "port": CONFIG["GATEWAY_PORT"],
        "env_vars": {
            "GATEWAY_PORT": str(CONFIG["GATEWAY_PORT"]),
            "DOCKER_MODE": "false",  # For local mode, force false.
        },
    }

def build_service_dict(service: str) -> Dict[str, any]:
    """Return microservice configuration for local startup."""
    cfg = CONFIG["SERVICE_CONFIG"].get(service, {})
    return {
        "name": service,
        "path": f"services/{service}",
        "port": cfg.get("port", 5000),
        "env_vars": {
            f"{service.upper()}_NAME": cfg.get("name", service),
            f"{service.upper()}_PORT": str(cfg.get("port", 5000)),
        },
    }

def load_services_from_config() -> List[Dict[str, any]]:
    """Build a list of service dictionaries for startup: gateway then microservices."""
    services = [build_gateway_dict()]
    for service in CONFIG["SERVICES_LIST"]:
        services.append(build_service_dict(service))
    return services

def start_service(service: Dict[str, any]) -> subprocess.Popen:
    """Start a service subprocess."""
    env = os.environ.copy()
    env.update(service["env_vars"])
    env["DATA_DIR"] = DATA_DIR
    env["DOCKER_MODE"] = "false"  # Force local mode
    # Add project root to PYTHONPATH so that "from config import CONFIG" works.
    env["PYTHONPATH"] = CONFIG["BASE_DIR"]
    print(f"🚀 Starting {service['name']} on port {service['port']} (local)...")
    proc = subprocess.Popen(
        [sys.executable, "app.py"],
        cwd=service["path"],
        env=env,
        stdout=None,   # let output go to the console
        stderr=None,
        text=True,
    )
    time.sleep(2)  # Give the process time to start up
    return proc

def stop_services(*args) -> None:
    print("\n⛔ Stopping all services...")
    for p in processes:
        p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    print("🚀 Starting API Hub Locally...\n")
    SERVICES = load_services_from_config()
    # Ensure data directories exist for each service
    ensure_data_dirs([s["name"] for s in SERVICES])
    
    processes = []
    for svc in SERVICES:
        proc = start_service(svc)
        processes.append(proc)
    
    signal.signal(signal.SIGINT, stop_services)
    print("\n✅ All services are running locally. Press CTRL+C to stop.")
    while True:
        time.sleep(1)