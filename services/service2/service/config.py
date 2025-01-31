import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "default_service")
PORT = int(os.getenv("PORT", 5001))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")