import os

# Determine if we're in Docker mode.
DOCKER_MODE = os.getenv("DOCKER_MODE", "false").lower() == "true"
GATEWAY_PORT = int(os.getenv("GATEWAY_PORT", "5001"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_DIR = os.getenv("DATA_DIR", "/app/data")  # or some default

# Get the list of service names from the environment.
services_list = os.getenv("SERVICES", "service1,service2").split(',')
# Clean up whitespace and filter out empty names.
services_list = [s.strip() for s in services_list if s.strip()]

# Build a configuration dictionary: For each service, look up its port.
service_config = {}
for service in services_list:
    # Expect the port to be defined as SERVICE1_PORT, SERVICE2_PORT, etc.
    port = int(os.getenv(f"{service.upper()}_PORT", "5000"))
    service_config[service] = port

# Build the SERVICES dictionary based on the mode.
if DOCKER_MODE:
    SERVICES = {name: f"http://{name}:{port}/process" for name, port in service_config.items()}
else:
    SERVICES = {name: f"http://localhost:{port}/process" for name, port in service_config.items()}

# For debugging purposes:
print("Gateway SERVICES configuration:", SERVICES)