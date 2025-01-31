import os

SERVICES = {
    "service1": "http://service1:5001/process",
    "service2": "http://service2:5002/process",
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")