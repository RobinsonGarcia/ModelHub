# services/service1/service/config.py
from config import CONFIG

# Look up configuration for service1 (use a default if not defined)
service_cfg = CONFIG["SERVICE_CONFIG"].get("service1", {})
SERVICE_NAME = service_cfg.get("name", "service1")
PORT = service_cfg.get("port", 5002)  # default fallback if not set in .env
LOG_LEVEL = service_cfg.get("log_level", "INFO")

# Use the global DATA_DIR from config
DATA_DIR = CONFIG["DATA_DIR"]