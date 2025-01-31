from api_client import APIClient

# Instantiate the client
client = APIClient()

# Call Service 1
response1 = client.call_service("service1", "Hello from client")
print("Service 1 Response:", response1)

# Call Service 2
response2 = client.call_service("service2", "Another test input")
print("Service 2 Response:", response2)