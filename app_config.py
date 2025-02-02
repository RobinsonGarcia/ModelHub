# app_config.py
import os
from dotenv import load_dotenv

# Optionally, let the admin specify a custom env file via the ENV_FILE environment variable.
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(dotenv_path=env_file)

# Base directory of the application (project root)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Global shared storage folder for the entire application.
# Convert any relative path to an absolute path.
_DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "data"))
DATA_DIR = os.path.abspath(_DATA_DIR)

# Global log file path (optional)
LOG_FILE = os.environ.get("LOG_FILE", os.path.join(DATA_DIR, "app.log"))

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