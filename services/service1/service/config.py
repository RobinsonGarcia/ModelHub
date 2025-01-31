import os

SERVICE_NAME = os.getenv("SERVICE_NAME", "service1")
PORT = int(os.getenv("PORT", 5002))  # Defaults to 5002
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")