import os
import time
import signal
import subprocess
import sys
import requests
import pytest

# We'll import your APIClient to test
from client.api_client import APIClient

# Provide up to 2 minutes for environment spin-up
MAX_WAIT = 5

@pytest.fixture(params=["local", "docker"])
def environment(request):
    mode = request.param
    if mode == "local":
        print("\n=== Starting LOCAL environment... ===")
        proc = subprocess.Popen(
            [os.sys.executable, "start_local.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        wait_for_gateway(port=5001)
        yield mode
        print("\n=== Tearing down LOCAL environment... ===")
        proc.send_signal(signal.SIGINT)
        proc.wait()
    elif mode == "docker":
        print("\n=== Starting DOCKER environment... ===")
        # Using Docker Compose V2 (separate arguments)
        subprocess.run(["docker", "compose", "up", "-d", "--build"], check=True)
        wait_for_gateway(port=5001)
        yield mode
        print("\n=== Tearing down DOCKER environment... ===")
        subprocess.run(["docker", "compose", "down"], check=True)


def wait_for_gateway(port):
    """
    Repeatedly calls the gateway endpoint until a valid response is received.
    Times out after MAX_WAIT seconds if not responding.
    """
    start_time = time.time()
    while True:
        try:
            url = f"http://localhost:{port}/route/service1"
            resp = requests.post(url, json={"input": "test"}, timeout=3)
            # Only consider it ready if the response contains a "service" key
            data = resp.json()
            if "service" in data or resp.status_code in (404, 200):
                print(f"Gateway ready (response={resp.status_code})")
                return
        except requests.exceptions.RequestException:
            pass

        if time.time() - start_time > MAX_WAIT:
            raise RuntimeError(f"Gateway on port {port} not ready after {MAX_WAIT} seconds.")
        time.sleep(2)


@pytest.fixture
def client():
    """
    Return a client pointing to the gateway at localhost:5001.
    Same config in local and docker mode.
    """
    return APIClient(gateway_url="http://localhost:5001")


def test_service1(environment, client):
    """
    Test calling service1 with valid input.
    environment -> "local" or "docker"
    client -> calls http://localhost:5001
    """
    resp = client.call_service("service1", "Hello")
    # We expect {"service": "service1", "output": "HELLO"}
    assert "service" in resp, f"No 'service' key in response: {resp}"
    assert "output" in resp, f"No 'output' key in response: {resp}"
    assert resp["service"] == "service1"
    assert resp["output"] == "HELLO"


def test_service2(environment, client):
    """
    Test calling service2 with valid input.
    environment -> "local" or "docker"
    client -> calls http://localhost:5001
    """
    resp = client.call_service("service2", "World")
    # We expect {"service": "service2", "output": "WORLD"}
    assert "service" in resp, f"No 'service' key in response: {resp}"
    assert "output" in resp, f"No 'output' key in response: {resp}"
    assert resp["service"] == "service2"
    assert resp["output"] == "WORLD"


def test_unknown_service(environment, client):
    """
    Test calling an unknown service, expecting error -> 404 from gateway, 
    which your client interprets as {"error": "Service unavailable"}.
    """
    resp = client.call_service("no_such_service", "???")
    assert "error" in resp, "Expected 'error' key for unknown service"
    assert resp["error"] == "Service unavailable"