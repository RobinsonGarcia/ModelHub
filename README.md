# 🚀 API Hub - Flask Microservices with Docker

## 📌 Overview
API Hub is a **Dockerized microservices framework** using **Flask** and **Nginx**. It provides a **single API gateway** to route requests to multiple Flask-based services.

- **API Gateway:** Handles routing and error management.
- **Microservices:** Each service processes requests independently.
- **Scalability:** Easily add new services with minimal changes.
- **Logging & Error Handling:** Integrated for better debugging.
- **Dockerized & Modularized:** Simple deployment with Docker Compose.

---

## 📂 Project Structure
```
api-hub/
│── docker-compose.yml       # Orchestrates all services
│── gateway/                 # API Gateway to route requests
│   ├── gateway/
│   │   ├── __init__.py
│   │   ├── config.py        # Service registry & settings
│   │   ├── routes.py        # API routing logic
│   │   ├── logger.py        # Logging configuration
│   ├── app.py               # Gateway entry point
│   ├── Dockerfile           # Gateway containerization
│   ├── requirements.txt
│── services/                # Microservices directory
│   ├── service_template/    # Template for new services
│   │   ├── service/
│   │   │   ├── __init__.py
│   │   │   ├── config.py    # Service settings
│   │   │   ├── routes.py    # Business logic
│   │   │   ├── logger.py    # Service-specific logging
│   │   ├── app.py           # Service entry point
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   ├── service1/            # Example service
│   ├── service2/
│── client/                  # Python client to interact with services
│   ├── api_client.py        # Reusable API client
│   ├── example_usage.py     # Example script using the client
│── nginx/                   # Reverse proxy settings
│   ├── nginx.conf
```

---

## ⚙️ How to Run
Ensure you have **Docker & Docker Compose** installed.

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/api-hub.git
cd api-hub
```

### 2️⃣ Build and Run Containers
```sh
docker-compose up --build
```

### 3️⃣ Test API Requests
Using `curl` or Postman:

- **Service 1**
  ```sh
  curl -X POST http://localhost/route/service1 -H "Content-Type: application/json" -d '{"input": "hello"}'
  ```

- **Service 2**
  ```sh
  curl -X POST http://localhost/route/service2 -H "Content-Type: application/json" -d '{"input": "world"}'
  ```

---

## 🆕 How to Add a New Service
1️⃣ **Copy the Template**
```sh
cp -r services/service_template services/service3
```

2️⃣ **Update `docker-compose.yml`**
Add a new service block:
```yaml
  service3:
    build: ./services/service_template
    environment:
      - SERVICE_NAME=service3
      - PORT=5003
    networks:
      - api_network
```

3️⃣ **Modify `config.py` in the New Service**
```python
SERVICE_NAME = "service3"
PORT = 5003
```

4️⃣ **Modify `routes.py` to Implement Logic**
```python
@bp.route('/process', methods=['POST'])
def process():
    data = request.json
    result = {"service": SERVICE_NAME, "output": data.get("input", "").lower()}
    return jsonify(result)
```

5️⃣ **Restart Docker Compose**
```sh
docker-compose up --build
```

🎉 **Your new service is live at:**  
```sh
curl -X POST http://localhost/route/service3 -H "Content-Type: application/json" -d '{"input": "TEST"}'
```

---

## 🖥️ Python Client
### 📌 Overview
The Python client allows you to **interact with any microservice** through the API gateway.  
It simplifies sending requests without using `curl` or Postman.

### 📂 **Client Structure**
```
client/
│── api_client.py        # Reusable Python client
│── example_usage.py     # Example script using the client
```

### 📝 **API Client**
📌 **`client/api_client.py`**
```python
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class APIClient:
    """
    A Python client to interact with API Hub's microservices.
    """
    def __init__(self, gateway_url="http://localhost:5000"):
        self.gateway_url = gateway_url
    
    def call_service(self, service_name, input_data):
        """
        Call a specific service and send data to the `/process` endpoint.

        :param service_name: Name of the service (e.g., "service1", "service2").
        :param input_data: Dictionary with the input data.
        :return: The service's response (JSON).
        """
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
📌 **`client/example_usage.py`**
```python
from api_client import APIClient

# Instantiate the client
client = APIClient()

# Call Service 1
response1 = client.call_service("service1", "Hello from client")
print("Service 1 Response:", response1)

# Call Service 2
response2 = client.call_service("service2", "Another test input")
print("Service 2 Response:", response2)
```

### 🚀 **How to Use the Client**
1️⃣ **Install Dependencies**  
If you don't have `requests`, install it:
```sh
pip install requests
```

2️⃣ **Run the API Hub**  
Start your Docker services:
```sh
docker-compose up --build
```

3️⃣ **Test the Client**
Run the example script:
```sh
python client/example_usage.py
```

📌 Expected Output:
```
INFO - Success: {'service': 'service1', 'output': 'HELLO FROM CLIENT'}
Service 1 Response: {'service': 'service1', 'output': 'HELLO FROM CLIENT'}
INFO - Success: {'service': 'service2', 'output': 'ANOTHER TEST INPUT'}
Service 2 Response: {'service': 'service2', 'output': 'ANOTHER TEST INPUT'}
```

---

## 🛠 Best Practices
✅ **Use `logging` for debugging** instead of `print()`.  
✅ **Keep microservices independent** – avoid cross-service dependencies.  
✅ **Use environment variables (`config.py`)** for easy configuration.  
✅ **Follow RESTful API design** for better scalability.  
✅ **Keep the API stateless** – store data externally if needed (e.g., databases, Redis).  
✅ **Use Nginx for rate limiting** and load balancing when scaling up.  

---

## 📜 License
This project is open-source under the **MIT License**.

---

## 📬 Contact
👨‍💻 **Author:** Robinson Garcia 
📧 **Email:** rlsgarcia@icloud.com
🔗 **GitHub:** https://github.com/RobinsonGarcia