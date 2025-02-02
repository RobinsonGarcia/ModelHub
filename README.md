# API Hub - Flask Microservices Framework

Welcome to **API Hub** – a Flask-based microservices framework that provides a centralized API gateway to route requests to multiple microservices. This project supports both local and Docker deployments through a unified configuration system.

---

## Project Structure

```
api-hub/
├── config.py                    # Unified configuration (loads .env)
├── docker-compose.yml           # Docker Compose configuration
├── setup_pyenv.py               # Pyenv-based setup script (auto-configured from .env & config.py)
├── start_local.py               # Script to start the gateway and all services locally
├── client/
│   ├── __init__.py
│   ├── api_client.py            # Python client to interact with the API Gateway
│   └── example_usage.py         # Example usage of the API client
├── gateway/
│   ├── app.py                   # Gateway entry point
│   └── gateway/
│       ├── __init__.py
│       ├── config.py            # Gateway configuration (imports from config.py)
│       ├── logger.py            # Logging configuration for the gateway
│       └── routes.py            # API routing logic for the gateway
└── services/
    ├── service1/
    │   ├── app.py               # Service 1 entry point
    │   └── service/
    │       ├── __init__.py
    │       ├── config.py        # Service 1 configuration (wraps config.py)
    │       ├── logger.py        # Logging configuration for service 1
    │       └── routes.py        # Service 1 request processing
    ├── service2/                # Similar structure as service1
    ├── service_template/        # Template for adding new services
    └── service5/                # **New Service as a Git Submodule Example**
        ├── submodule_name       # Git submodule containing extra functionality
        ├── app.py               # Service 5 entry point
        └── service/
            ├── __init__.py
            ├── config.py        # Service 5 configuration (wraps config.py)
            ├── logger.py        # Logging configuration for service 5
            └── routes.py        # Service 5 routes that use the submodule
```

---

## Getting Started

### Prerequisites

- **Python 3.9+** (managed with [Pyenv](https://github.com/pyenv/pyenv))
- **Docker** (for Docker mode)
- **Git** (for managing Git submodules)

### Environment Setup

Create a `.env` file in the project root with at least the following variables:

```ini
# Global settings
DATA_DIR=./data
LOG_FILE=./data/app.log

# Gateway configuration
DOCKER_MODE=false
GATEWAY_PORT=5001
GATEWAY_LOG_LEVEL=INFO

# Define the list of microservices (comma-separated)
SERVICES=service1,service2,service5

# Service-specific configuration
SERVICE1_NAME=service1
SERVICE1_PORT=5002
SERVICE1_LOG_LEVEL=INFO

SERVICE2_NAME=service2
SERVICE2_PORT=5003
SERVICE2_LOG_LEVEL=INFO

SERVICE5_NAME=service5
SERVICE5_PORT=5005
SERVICE5_LOG_LEVEL=INFO
```

---

## Running the Project

### Local Mode

1. **Set Up Virtual Environments & Install Dependencies**

   Run the setup script which creates virtual environments and installs dependencies based on your configuration:

   ```bash
   python setup_pyenv.py
   ```

2. **Start the Services Locally**

   Launch the API Hub (gateway and microservices) using:

   ```bash
   python start_local.py
   ```

   This script reads the configuration from `config.py` (overriding `DOCKER_MODE` to false), creates shared data directories, and starts each service on its configured port.

3. **Test the API**

   Use the provided client:

   ```bash
   python client/example_usage.py
   ```

   You can also use `curl` or Postman to send POST requests to endpoints like `http://localhost:5001/route/service1`.

### Docker Mode

1. **Build and Run with Docker Compose**

   Ensure your `.env` file has `DOCKER_MODE=true` (or override it) and run:

   ```bash
   docker compose up --build
   ```

2. **Access the API**

   The gateway is mapped to port 5001 on your host, and internal routing uses container hostnames.

3. **Stop the Containers**

   ```bash
   docker compose down
   ```

---

## Running Tests

Execute integration tests using Pytest from the project root:

```bash
pytest tests/test_integration.py -v
```

These tests automatically start the environment, send requests through the API client, and then tear down the environment.

---

### Adding a Service as a Git Submodule

In this scenario, you want to add a new service (**service5**) whose code is maintained as a Git submodule. The submodule is located at the root of the `service5` directory and contains extra functionality that must be called from within the service routes. **Note:** We assume you do **not** want to add or modify any files (such as an `__init__.py`) inside the submodule folder.

#### Service5 Directory Structure

After adding the submodule, your directory structure should look like this:

```
services/
└── service5/
    ├── submodule_name       # Git submodule containing extra functionality
    ├── app.py               # Service 5 entry point
    └── service/
        ├── __init__.py
        ├── config.py        # Service 5 configuration (wraps config.py)
        ├── logger.py        # Logging configuration for service 5
        └── routes.py        # Service 5 routes that call functions from the submodule
```

#### Step-by-Step Instructions

1. **Add the Git Submodule**

   In your project root, add the submodule into the `service5` directory:
   
   ```bash
   git submodule add https://github.com/username/submodule_repo.git services/service5/submodule_name
   git submodule update --init --recursive
   ```
   
   This command clones the external repository into `services/service5/submodule_name` without modifying its contents.

2. **Update the .env File**

   Add configuration for service5 in your `.env` file:
   
   ```ini
   SERVICE5_NAME=service5
   SERVICE5_PORT=5005
   SERVICE5_LOG_LEVEL=INFO
   ```
   
   Also, update the `SERVICES` variable to include the new service:
   
   ```ini
   SERVICES=service1,service2,service5
   ```

3. **Configure Service5**

   In `services/service5/service/config.py`, import the unified configuration from `config.py` and load service5-specific settings:
   
   ```python
   # services/service5/service/config.py
   from config import CONFIG

   service_cfg = CONFIG["SERVICE_CONFIG"].get("service5", {})
   SERVICE_NAME = service_cfg.get("name", "service5")
   PORT = service_cfg.get("port", 5005)  # default fallback if not set in .env
   LOG_LEVEL = service_cfg.get("log_level", "INFO")
   DATA_DIR = CONFIG["DATA_DIR"]
   ```

4. **Import the Submodule Without Modifying It**

   Since you do **not** want to add an `__init__.py` file to the submodule, you can add its path to `sys.path` in your service’s routes file. In `services/service5/service/routes.py`, do the following:
   
   ```python
   # services/service5/service/routes.py
   import sys
   import os
   from flask import Blueprint, request, jsonify
   from service.logger import logger
   from service.config import SERVICE_NAME

   # Dynamically add the submodule folder to sys.path
   # Compute the absolute path to the submodule folder
   current_dir = os.path.dirname(os.path.abspath(__file__))
   submodule_path = os.path.join(current_dir, "..", "submodule_name")
   if submodule_path not in sys.path:
       sys.path.insert(0, submodule_path)

   # Now import a function from the submodule.
   # For example, assume the submodule exposes a function called process_extra_data in extra.py.
   from extra import process_extra_data

   bp = Blueprint('service', __name__)

   @bp.route('/process', methods=['POST'])
   def process():
       try:
           data = request.json
           # Call the submodule's function to process the input.
           extra_output = process_extra_data(data.get("input", ""))
           result = {"service": SERVICE_NAME, "output": extra_output}
           logger.info(f"Processed request with submodule: {data}")
           return jsonify(result)
       except Exception as e:
           logger.error(f"Processing error: {str(e)}")
           return jsonify({"error": "Internal server error"}), 500
   ```

   **Explanation:**
   
   - The code calculates the absolute path to the submodule folder relative to the current file.
   - It then inserts that path at the beginning of `sys.path` so that Python can import the submodule even if it lacks an `__init__.py`.
   - Finally, it imports the desired function (in this example, `process_extra_data` from the module `extra` within the submodule) and uses it in the route.

5. **Run the Service**

   Run the setup and start scripts as usual:
   
   ```bash
   python setup_pyenv.py
   python start_local.py
   ```
   
   Then test with:
   
   ```bash
   python client/example_usage.py
   ```
   
   You should see that **service5** is now included and its route correctly calls the functionality from the submodule.

---

## Workflow and Best Practices

- **Unified Configuration:**  
  All settings are centralized in `config.py` and overridden via the `.env` file. To modify a service’s configuration, update the `.env` file and re-run the setup and start scripts.

- **Adding New Services:**  
  To add a new service, simply:
  1. Add its name to the `SERVICES` variable in `.env`.
  2. Provide any service‑specific configuration (like `SERVICE5_NAME`, `SERVICE5_PORT`, etc.).
  3. If the service uses a Git submodule, add the submodule (as shown above) without modifying its files.
  4. Duplicate the service template (or use the Git submodule approach) and adjust its routes, configuration, and logging as needed.

- **Importing Submodules Without Modification:**  
  By dynamically adding the submodule path to `sys.path`, you avoid having to add an `__init__.py` file to the submodule. This keeps the submodule completely untouched while still making its functions available for import.

---

## License

This project is open-source under the MIT License.

---

## Contact

For questions or contributions, please contact [Your Name](mailto:your.email@example.com) or visit [GitHub](https://github.com/YourUsername).

Happy coding!