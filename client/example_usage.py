from api_client import APIClient

client = APIClient()  # -> calls http://localhost:5001 by default

# Call Service 1
response1 = client.call_service("service1", "Hello from client")
print("Service 1 Response:", response1)

# Call Service 2
response2 = client.call_service("service2", "Another test input")
print("Service 2 Response:", response2)

# Call Service 3
response3 = client.call_service("service3", "Another Another test input")
print("Service 2 Response:", response3)