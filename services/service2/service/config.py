import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "service2")
PORT = int(os.getenv("PORT", 5003))  # Defaults to 5003
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")