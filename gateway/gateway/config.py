# gateway/gateway/config.py
from config import CONFIG

DOCKER_MODE = CONFIG["DOCKER_MODE"]
GATEWAY_PORT = CONFIG["GATEWAY_PORT"]
LOG_LEVEL = CONFIG["GATEWAY_LOG_LEVEL"]
DATA_DIR = CONFIG["DATA_DIR"]
SERVICES = CONFIG["GATEWAY_SERVICES"]

print("Gateway SERVICES configuration:", SERVICES)