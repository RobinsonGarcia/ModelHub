import os
import subprocess
from config import CONFIG

# Define the Python version and Pyenv root.
PYTHON_VERSION = "3.9.18"
PYENV_ROOT = os.path.expanduser("~/.pyenv")  # Path to Pyenv root

def get_service_setup_config():
    """
    Build the services-to-setup dictionary from the unified configuration and environment.
    
    This function uses CONFIG["SERVICES_LIST"] from config.py to determine the microservices,
    and it adds a special entry for the gateway.
    
    For each service, it uses:
      - path: For the gateway, "gateway"; for others, "services/<service>"
      - env: from ENV variable (e.g. GATEWAY_ENV or SERVICE1_ENV) or default to "api-hub-<service>"
      - dependencies: from an environment variable (e.g. GATEWAY_DEPENDENCIES or SERVICE1_DEPENDENCIES)
        or defaults (gateway: "flask requests", others: "flask").
    """
    services = {}
    
    # Gateway configuration:
    gateway_env = os.environ.get("GATEWAY_ENV", "api-hub-gateway")
    gateway_deps = os.environ.get("GATEWAY_DEPENDENCIES", "flask requests")
    services["gateway"] = {
        "path": "gateway",
        "env": gateway_env,
        "dependencies": gateway_deps.split(),
    }
    
    # Microservices configuration:
    for service in CONFIG["SERVICES_LIST"]:
        # Use environment variables if available; otherwise, default.
        env_name = os.environ.get(f"{service.upper()}_ENV", f"api-hub-{service}")
        deps = os.environ.get(f"{service.upper()}_DEPENDENCIES", "flask")
        services[service] = {
            "path": f"services/{service}",
            "env": env_name,
            "dependencies": deps.split(),
        }
    return services

# Build the services dictionary dynamically.
SERVICES = get_service_setup_config()

def run_command(command, env=None, cwd=None):
    """Run a shell command in the given environment and directory."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True, env=env, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Error executing: {command}\n{result.stderr}")
        exit(1)
    return result.stdout.strip()

def setup_pyenv():
    """Install the specified Python version and create virtual environments for all services."""
    print(f"🔧 Setting up Pyenv with Python {PYTHON_VERSION}...")
    
    # Check installed Python versions
    installed_versions = run_command("pyenv versions")
    if PYTHON_VERSION not in installed_versions:
        print(f"📥 Installing Python {PYTHON_VERSION} via Pyenv...")
        run_command(f"pyenv install {PYTHON_VERSION}")
    else:
        print(f"✅ Python {PYTHON_VERSION} is already installed.")
    
    # Create virtual environments for each service.
    for service, details in SERVICES.items():
        env_name = details["env"]
        installed_envs = run_command("pyenv virtualenvs")
        if env_name not in installed_envs:
            print(f"📦 Creating virtual environment: {env_name} for {service}...")
            run_command(f"pyenv virtualenv {PYTHON_VERSION} {env_name}")
        else:
            print(f"✅ Virtual environment {env_name} already exists for {service}.")

def setup_services():
    """Install dependencies and prepare each service’s directory with its virtual environment."""
    for service, details in SERVICES.items():
        path = details["path"]
        env_name = details["env"]
        dependencies = " ".join(details["dependencies"])
        
        print(f"⚙️ Setting up {service} in {path}...")
        
        # Ensure the service directory exists.
        os.makedirs(path, exist_ok=True)
        
        # Write the .python-version file to associate the service with its virtualenv.
        python_version_file = os.path.join(path, ".python-version")
        with open(python_version_file, "w") as f:
            f.write(env_name)
        
        # Determine the Python and pip binaries.
        python_bin = os.path.join(PYENV_ROOT, "versions", env_name, "bin", "python")
        pip_bin = os.path.join(PYENV_ROOT, "versions", env_name, "bin", "pip")
        
        print(f"🐍 Using Python binary: {python_bin} for {service}")
        
        # Upgrade pip in the virtual environment.
        run_command(f"{pip_bin} install --upgrade pip", cwd=path)
        
        # Install default dependencies (if any).
        if dependencies:
            print(f"📦 Installing default dependencies for {service}: {dependencies}")
            run_command(f"{pip_bin} install {dependencies}", cwd=path)
        
        # If a requirements.txt file exists, install those dependencies.
        requirements_file = os.path.join(path, "requirements.txt")
        if os.path.isfile(requirements_file):
            print(f"📜 Found requirements.txt for {service}. Installing dependencies...")
            run_command(f"{pip_bin} install -r requirements.txt", cwd=path)
        else:
            print(f"⚠️ No requirements.txt found for {service}, skipping.")
    
    print("🚀 Setup complete! You can now run the services.")

if __name__ == "__main__":
    setup_pyenv()
    setup_services()