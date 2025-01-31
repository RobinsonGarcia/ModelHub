import os
import subprocess

# Define the Python version and services
PYTHON_VERSION = "3.9.18"
PYENV_ROOT = os.path.expanduser("~/.pyenv")  # Path to Pyenv root
SERVICES = {
    "gateway": {"path": "gateway", "env": "api-hub-gateway", "dependencies": ["flask", "requests"]},
    "service1": {"path": "services/service1", "env": "api-hub-service1", "dependencies": ["flask"]},
    "service2": {"path": "services/service2", "env": "api-hub-service2", "dependencies": ["flask"]},
}

def run_command(command, env=None, cwd=None):
    """Run a shell command in the given environment and directory."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True, env=env, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Error executing: {command}\n{result.stderr}")
        exit(1)
    return result.stdout.strip()

def setup_pyenv():
    """Install Python version and create virtual environments for all services."""
    print(f"🔧 Setting up Pyenv with Python {PYTHON_VERSION}...")

    # Install Python version
    installed_versions = run_command("pyenv versions")
    if PYTHON_VERSION not in installed_versions:
        print(f"📥 Installing Python {PYTHON_VERSION} via Pyenv...")
        run_command(f"pyenv install {PYTHON_VERSION}")
    else:
        print(f"✅ Python {PYTHON_VERSION} is already installed.")

    # Create virtual environments for each service
    for service, details in SERVICES.items():
        env_name = details["env"]
        installed_envs = run_command("pyenv virtualenvs")

        if env_name not in installed_envs:
            print(f"📦 Creating virtual environment: {env_name}...")
            run_command(f"pyenv virtualenv {PYTHON_VERSION} {env_name}")
        else:
            print(f"✅ Virtual environment {env_name} already exists.")

def setup_services():
    """Configure services with their virtual environments and dependencies."""
    for service, details in SERVICES.items():
        path = details["path"]
        env_name = details["env"]
        dependencies = " ".join(details["dependencies"])

        print(f"⚙️ Setting up {service} in {path}...")

        # Ensure the service directory exists
        os.makedirs(path, exist_ok=True)

        # Write the `.python-version` file manually
        python_version_file = os.path.join(path, ".python-version")
        with open(python_version_file, "w") as f:
            f.write(env_name)

        # Get the full path to the Pyenv virtual environment Python binary
        python_bin = os.path.join(PYENV_ROOT, "versions", env_name, "bin", "python")
        pip_bin = os.path.join(PYENV_ROOT, "versions", env_name, "bin", "pip")

        # Verify we are using the correct Python binary
        print(f"🐍 Using Python binary: {python_bin}")

        # Upgrade pip inside the virtual environment
        run_command(f"{pip_bin} install --upgrade pip", cwd=path)

        # Install default dependencies
        if dependencies:
            print(f"📦 Installing default dependencies for {service}...")
            run_command(f"{pip_bin} install {dependencies}", cwd=path)

        # Install dependencies from requirements.txt if it exists
        requirements_file = os.path.join(path, "requirements.txt")
        if os.path.isfile(requirements_file):
            print(f"📜 Found `requirements.txt` for {service}. Installing dependencies...")
            run_command(f"{pip_bin} install -r requirements.txt", cwd=path)
        else:
            print(f"⚠️ No `requirements.txt` found for {service}, skipping.")

    print("🚀 Setup complete! You can now run the services.")

if __name__ == "__main__":
    setup_pyenv()
    setup_services()