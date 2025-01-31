import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class APIClient:
    """
    A Python client to interact with API Hub's microservices via the Gateway.
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