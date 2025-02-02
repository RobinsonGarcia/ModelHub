# config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env (or a file specified by ENV_FILE)
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=env_file)

# -------------------------
# Global Paths and Logging
# -------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Convert any relative DATA_DIR value to an absolute path.
_data_dir = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
DATA_DIR = os.path.abspath(_data_dir)

LOG_FILE = os.environ.get("LOG_FILE", os.path.join(DATA_DIR, "app.log"))

# -------------------------
# Mode & Gateway Settings
# -------------------------
DOCKER_MODE = os.environ.get("DOCKER_MODE", "false").lower() == "true"

GATEWAY_PORT = int(os.environ.get("GATEWAY_PORT", "5001"))
GATEWAY_LOG_LEVEL = os.environ.get("GATEWAY_LOG_LEVEL", "INFO")

# -------------------------
# Service Configurations
# -------------------------
SERVICES_ENV = os.environ.get("SERVICES", "service1,service2")
SERVICES_LIST = [s.strip() for s in SERVICES_ENV.split(",") if s.strip()]

SERVICE_CONFIG = {}
for service in SERVICES_LIST:
    key = service.upper()  # e.g., "SERVICE1"
    SERVICE_CONFIG[service] = {
        "name": os.environ.get(f"{key}_NAME", service),
        "port": int(os.environ.get(f"{key}_PORT", "5000")),
        "log_level": os.environ.get(f"{key}_LOG_LEVEL", "INFO"),
    }

if DOCKER_MODE:
    GATEWAY_SERVICES = {
        service: f"http://{service}:{cfg['port']}/process" 
        for service, cfg in SERVICE_CONFIG.items()
    }
else:
    GATEWAY_SERVICES = {
        service: f"http://localhost:{cfg['port']}/process" 
        for service, cfg in SERVICE_CONFIG.items()
    }

# -------------------------
# Utility: Ensure Data Directories Exist
# -------------------------
def ensure_data_dirs(service_names):
    """
    Ensure that the global shared data directory exists,
    along with subdirectories for each service (including the gateway).
    
    :param service_names: A list of service names (e.g., ["gateway", "service1", "service2"])
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for name in service_names:
        service_dir = os.path.join(DATA_DIR, name)
        if not os.path.exists(service_dir):
            os.makedirs(service_dir)

# -------------------------
# Expose configuration
# -------------------------
CONFIG = {
    "BASE_DIR": BASE_DIR,
    "DATA_DIR": DATA_DIR,
    "LOG_FILE": LOG_FILE,
    "DOCKER_MODE": DOCKER_MODE,
    "GATEWAY_PORT": GATEWAY_PORT,
    "GATEWAY_LOG_LEVEL": GATEWAY_LOG_LEVEL,
    "SERVICES_LIST": SERVICES_LIST,
    "SERVICE_CONFIG": SERVICE_CONFIG,
    "GATEWAY_SERVICES": GATEWAY_SERVICES,
}