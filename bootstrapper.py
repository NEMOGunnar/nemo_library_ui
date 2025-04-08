import os
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path
import logging
import shutil  # Add this import for recursive directory removal
import hashlib  # Add this import for hashing
import requests  # Add this import for GitHub API requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration
PYTHON_VERSION = "3.13.2"
PYTHON_ZIP_NAME = f"python-{PYTHON_VERSION}-embed-amd64.zip"
PYTHON_ZIP_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/{PYTHON_ZIP_NAME}"

APP_DIR = Path.home() / ".nemo_app"
PYTHON_DIR = APP_DIR / "python"
PYTHON_ZIP_PATH = APP_DIR / PYTHON_ZIP_NAME
PYTHON_EXE = PYTHON_DIR / "python.exe"

# Your main Streamlit app file (must exist or be downloaded separately)
MAIN_APP_FILE = "nemo_library_ui.py"

# Python packages to install
REQUIRED_PACKAGES = [
    "streamlit",
    "nemo-library"
]

# GitHub repository details
GITHUB_REPO = "H3rm1nat0r/nemo_library"
GITHUB_FILE_PATH = "nemo_library_ui.py"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/commits?path={GITHUB_FILE_PATH}"

def download_python():
    """Downloads the embeddable Python ZIP from python.org."""
    logging.info(f"Downloading Python {PYTHON_VERSION}...")
    urllib.request.urlretrieve(PYTHON_ZIP_URL, PYTHON_ZIP_PATH)
    logging.info("Download completed.")

def extract_python():
    """Extracts the downloaded Python ZIP into the target directory."""
    logging.info("Extracting Python...")
    with zipfile.ZipFile(PYTHON_ZIP_PATH, 'r') as zip_ref:
        zip_ref.extractall(PYTHON_DIR)
    logging.info("Extraction complete.")

def check_python_version():
    """Checks if the existing Python version matches the required version."""
    if PYTHON_EXE.exists():
        result = subprocess.run([PYTHON_EXE, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            installed_version = result.stdout.strip().split()[-1]
            if installed_version == PYTHON_VERSION:
                logging.info(f"Python version {installed_version} is already installed.")
                return True
            else:
                logging.warning(f"Python version mismatch: found {installed_version}, expected {PYTHON_VERSION}.")
    return False

def ensure_python_env():
    """Ensures that Python is downloaded, extracted, and matches the required version."""
    if not check_python_version():
        if PYTHON_DIR.exists():
            logging.info(f"Removing old Python environment at {PYTHON_DIR}...")
            shutil.rmtree(PYTHON_DIR)  # Use shutil.rmtree to remove non-empty directories
            logging.info("Old Python environment removed.")
        os.makedirs(APP_DIR, exist_ok=True)
        download_python()
        extract_python()
        enable_site_packages()

def check_pip_version():
    """Checks if pip is installed and up-to-date."""
    try:
        result = subprocess.run([PYTHON_EXE, "-m", "pip", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logging.info(f"Pip is already installed: {result.stdout.strip()}")
            return True
    except Exception as e:
        logging.warning(f"Failed to check pip version: {e}")
    return False

def install_pip():
    """Downloads and installs pip using get-pip.py if not already installed."""
    if not check_pip_version():
        logging.info("Pip not found or outdated. Installing pip...")
        get_pip_path = APP_DIR / "get-pip.py"
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
        subprocess.run([PYTHON_EXE, str(get_pip_path)], check=True)
        logging.info("Pip installation completed.")

def enable_site_packages():
    """Enables site packages by editing python*._pth."""
    for file in PYTHON_DIR.glob("python*._pth"):
        lines = file.read_text().splitlines()
        lines = [l if l.strip() != "#import site" else "import site" for l in lines]
        if "import site" not in lines:
            lines.append("import site")
        file.write_text("\n".join(lines))

def install_requirements():
    """Installs required packages using pip."""
    logging.info("Installing required packages...")
    subprocess.run(
        [PYTHON_EXE, "-m", "pip", "install", "--upgrade", "pip", "--no-warn-script-location", "--no-warn-conflicts"],
        check=True,
        env={**os.environ, "PYTHONWARNINGS": "ignore"}  # Suppress warnings
    )
    subprocess.run(
        [PYTHON_EXE, "-m", "pip", "install", "--no-warn-script-location", "--no-warn-conflicts", *REQUIRED_PACKAGES],
        check=True,
        env={**os.environ, "PYTHONWARNINGS": "ignore"}  # Suppress warnings
    )

def get_latest_commit_hash():
    """Fetches the latest commit hash for the file from GitHub."""
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()
        commits = response.json()
        if commits:
            return commits[0]["sha"]
    except Exception as e:
        logging.warning(f"Failed to fetch latest commit hash: {e}")
    return None

def get_local_file_hash(file_path):
    """Calculates the SHA-1 hash of the local file."""
    if file_path.exists():
        sha1 = hashlib.sha1()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha1.update(chunk)
        return sha1.hexdigest()
    return None

def ensure_correct_app_version():
    """Ensures the local app file matches the latest version on GitHub."""
    app_path = APP_DIR / MAIN_APP_FILE
    latest_commit_hash = get_latest_commit_hash()
    local_file_hash = get_local_file_hash(app_path)

    if latest_commit_hash and latest_commit_hash == local_file_hash:
        logging.info("App file is up-to-date.")
    else:
        logging.info("App file is outdated or missing. Downloading the latest version...")
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/{GITHUB_FILE_PATH}"
        urllib.request.urlretrieve(url, app_path)
        logging.info("App file updated.")

def run_app():
    """Launches the Streamlit application."""
    logging.info("Launching Streamlit app...")
    subprocess.run([
        str(PYTHON_EXE),
        "-m", "streamlit",
        "run",
        MAIN_APP_FILE
    ], cwd=APP_DIR)

def main():
    logging.info("Bootstrapping Nemo Application...")
    ensure_python_env()
    install_pip()
    install_requirements()
    ensure_correct_app_version()  # Replace the previous app download logic
    run_app()

if __name__ == "__main__":
    main()