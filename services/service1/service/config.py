import os

SERVICE_NAME = os.getenv("SERVICE1_NAME", "service1")
PORT = int(os.getenv("SERVICE1_PORT", 5002))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Shared storage folder available to the service
DATA_DIR = os.getenv("DATA_DIR", "/app/data")