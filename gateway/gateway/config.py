import os

# If DOCKER_MODE is true, route calls to Docker hostnames
DOCKER_MODE = os.getenv("DOCKER_MODE", "false").lower() == "true"

if DOCKER_MODE:
    SERVICES = {
        "service1": "http://service1:5002/process",
        "service2": "http://service2:5003/process",
    }
else:
    # Local
    SERVICES = {
        "service1": "http://localhost:5002/process",
        "service2": "http://localhost:5003/process",
    }

# Gateway port (default 5001) - override with GATEWAY_PORT env if needed
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", 5001))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")