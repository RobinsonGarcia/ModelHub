# 🚀 API Hub - Flask Microservices

## 📌 Overview
API Hub is a **Flask-based microservices framework** providing:
- **API Gateway** for centralized routing and error handling
- **Multiple Microservices** (service1, service2, etc.) each listening on dedicated ports
- **Flexible Deployment**: Run locally on your machine or with Docker
- **Logging & Error Handling** built in for better debugging
- **Modular, Easy to Extend** architecture with a service template

---

## 📂 Project Structure
```
api-hub/
├── docker-compose.yml          # Orchestrates services in Docker
├── start_local.py              # Launches gateway + services locally
├── gateway/
│   ├── gateway/
│   │   ├── __init__.py
│   │   ├── config.py           # Service registry & settings
│   │   ├── routes.py           # API routing logic
│   │   └── logger.py           # Logging configuration
│   ├── app.py                  # Gateway entry point
│   ├── Dockerfile
│   └── requirements.txt
├── services/
│   ├── service_template/       # Template for new services
│   │   ├── service/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── routes.py
│   │   │   └── logger.py
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── service1/
│   │   ├── service/
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── service2/
│       ├── service/
│       ├── app.py
│       ├── Dockerfile
│       └── requirements.txt
├── client/                     # Python client to interact with the gateway
│   ├── api_client.py
│   └── example_usage.py
├── tests/
│   ├── __init__.py
│   └── test_integration.py     # Pytest suite (runs local & docker tests)
└── setup_pyenv.py              # Pyenv-based setup script (optional)
```

---

## ⚙️ Running the API Hub

### 1️⃣ Local Mode
1. **Install dependencies** (Flask, requests, etc.). For example:
   ```sh
   pip install flask requests flask-cors
   ```
2. **Start all services** (gateway + microservices):
   ```sh
   python start_local.py
   ```
3. **Gateway** will run at [http://localhost:5001](http://localhost:5001)  
   - `service1` → [http://localhost:5002](http://localhost:5002)  
   - `service2` → [http://localhost:5003](http://localhost:5003)

### 2️⃣ Docker Mode
1. **Build & Run** everything:
   ```sh
   docker compose up --build
   ```
2. **Gateway** mapped to [http://localhost:5001](http://localhost:5001)  
   - `service1` runs in Docker at `service1:5002`  
   - `service2` runs in Docker at `service2:5003`

### 3️⃣ Testing the Gateway
Either in **local** or **docker** mode, you can test with `curl` or Postman:

- **service1**:
  ```sh
  curl -X POST http://localhost:5001/route/service1 -H "Content-Type: application/json" -d '{"input": "hello"}'
  ```
- **service2**:
  ```sh
  curl -X POST http://localhost:5001/route/service2 -H "Content-Type: application/json" -d '{"input": "world"}'
  ```

---

## 🛠 Adding a New Service
1. **Copy the Template**
   ```sh
   cp -r services/service_template services/service3
   ```
2. **Adjust the Port & Name**
   - In `services/service3/service/config.py`:
     ```python
     SERVICE_NAME = "service3"
     PORT = 5004  # for example
     ```
3. **Docker Setup** (if you want to run it in Docker). Add a block in `docker-compose.yml`:
   ```yaml
   service3:
     build: ./services/service3
     environment:
       - SERVICE_NAME=service3
       - PORT=5004
   ```
4. **Local Setup**  
   If running locally, ensure `start_local.py` starts it:
   ```python
   {
     "name": "service3",
     "path": "services/service3",
     "port": 5004,
     "env_vars": {
       "SERVICE_NAME": "service3",
       "PORT": "5004"
     }
   },
   ```
5. **Restart** (local or Docker). Your new service is now available at:
   ```sh
   # local
   curl -X POST http://localhost:5001/route/service3 -H "Content-Type: application/json" -d '{"input":"TEST"}'
   # docker
   curl -X POST http://localhost:5001/route/service3 -H "Content-Type: application/json" -d '{"input":"TEST"}'
   ```

## Global Configuration & Shared Storage

The API Hub now uses a centralized configuration file (`app_config.py`) to:
- Set up global parameters (such as the shared data directory and logging settings).
- Create a global storage folder (by default, `./data` on the host) and subdirectories for each service.
- Pass these configuration values to all services and the gateway.

### How It Works

- **Local Mode:**  
  The `start_local.py` script imports `app_config.py` and calls `ensure_data_dirs()` to create the shared data folder and subfolders for each service (e.g., `data/gateway`, `data/service1`, etc.). The `DATA_DIR` environment variable is then passed to all services.

- **Docker Mode:**  
  The Docker Compose file maps a host folder (`./data`) as a shared volume to `/app/data` in all containers. Each container uses the `DATA_DIR` environment variable (set to `/app/data`) to access this shared storage.

- **Logging:**  
  You can configure logging to write to files within the shared storage folder by setting the `LOG_FILE` (or using the provided defaults). This allows you to centralize log output for easier monitoring.
  
---

## 🖥️ Python Client

### 📌 Overview
A lightweight Python client makes it easy to call any service via the gateway. By default, it points to `http://localhost:5001`.

### 📂 **Client Structure**
```
client/
├── __init__.py
├── api_client.py
└── example_usage.py
```

### 📝 **API Client**

```python
import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class APIClient:
    """
    A Python client to interact with the API Hub's microservices.
    """
    def __init__(self, gateway_url="http://localhost:5001"):
        self.gateway_url = gateway_url

    def call_service(self, service_name, input_data):
        url = f"{self.gateway_url}/route/{service_name}"
        try:
            response = requests.post(url, json={"input": input_data}, timeout=5)
            response.raise_for_status()
            logger.info(f"Success: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to {service_name}: {e}")
            return {"error": "Service unavailable"}
```

### 🎯 **Example Usage**
```python
# client/example_usage.py
from api_client import APIClient

client = APIClient()  # => http://localhost:5001 by default

res1 = client.call_service("service1", "Hello from client")
print("Service 1 Response:", res1)

res2 = client.call_service("service2", "Another test")
print("Service 2 Response:", res2)
```
**Run**:
```sh
python client/example_usage.py
```
---

## 🧪 Running Integration Tests
We use **pytest** to automatically test **both local & Docker** environments in one sweep:

1. **Install pytest**:
   ```sh
   pip install pytest
   ```
2. **From the project root**, run:
   ```sh
   pytest tests/test_integration.py -v
   ```
3. **What happens**:
   - Pytest starts the **local** environment (`python start_local.py`)  
   - Runs test calls to the gateway  
   - Tears it down  
   - Then spins up **Docker** (`docker compose up -d`)  
   - Runs the same calls  
   - Finally `docker compose down`

You’ll see output like:
```
test_integration.py::test_service1[local] PASSED
test_integration.py::test_service2[local] PASSED
test_integration.py::test_unknown_service[local] PASSED
test_integration.py::test_service1[docker] PASSED
test_integration.py::test_service2[docker] PASSED
test_integration.py::test_unknown_service[docker] PASSED
```

---

## 🛠 Best Practices
- **Use logging** (`logger`) for debugging instead of prints.
- **Avoid cross-service dependencies**; keep each microservice standalone.
- **Use environment variables** to configure ports and modes (`DOCKER_MODE=true`).
- **Stateless Services**: persist data externally if needed.
- **Use Nginx** (or any reverse proxy) for load balancing or rate limiting at scale.
- **Add more tests** in `tests/` to cover edge cases, performance, or new microservices.

---

## 📜 License
This project is open-source under the **MIT License**.

---

## 📬 Contact
- **Author:** Robinson Garcia  
- **Email:** rlsgarcia@icloud.com  
- **GitHub:** [RobinsonGarcia](https://github.com/RobinsonGarcia)
~~~markdown