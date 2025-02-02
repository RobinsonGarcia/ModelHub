import os

SERVICE_NAME = os.getenv("SERVICE2_NAME", "service2")
PORT = int(os.getenv("SERVICE2_PORT", 5003))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Shared storage folder available to the service
DATA_DIR = os.getenv("DATA_DIR", "/app/data")