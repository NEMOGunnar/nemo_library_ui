import os
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import logging
import shutil  # Add this import for recursive directory removal
import requests  # Add this import for GitHub API requests

# Configure logging
current_script_name = Path(
    __file__
).stem  # Get the current script name without extension
LOGFILE = Path.home() / ".nemo_app" / "logs" / f"{current_script_name}.log"

# Ensure the directory for the log file exists
LOGFILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(LOGFILE, mode="a", encoding="utf-8"),  # Log to file
    ],
)

# Configuration
PYTHON_VERSION = "3.13.2"
PYTHON_ZIP_NAME = f"python-{PYTHON_VERSION}-embed-amd64.zip"
PYTHON_ZIP_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/{PYTHON_ZIP_NAME}"

APP_DIR = Path.home() / ".nemo_app"
PYTHON_DIR = APP_DIR / "python"
PYTHON_ZIP_PATH = APP_DIR / PYTHON_ZIP_NAME
PYTHON_EXE = PYTHON_DIR / "python.exe"

# GitHub repository details
GITHUB_REPO = "NEMOGunnar/nemo_library_ui"


def ensure_python():
    """Ensures that Python is downloaded, extracted, and matches the required version."""

    def check_python_version():
        """Checks if the existing Python version matches the required version."""
        if PYTHON_EXE.exists():
            result = subprocess.run(
                [PYTHON_EXE, "--version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                installed_version = result.stdout.strip().split()[-1]
                if installed_version == PYTHON_VERSION:
                    logging.info(
                        f"Python version {installed_version} is already installed."
                    )
                    return True
                else:
                    logging.warning(
                        f"Python version mismatch: found {installed_version}, expected {PYTHON_VERSION}."
                    )
        return False

    def download_python():
        """Downloads the embeddable Python ZIP from python.org."""
        logging.info(f"Downloading Python {PYTHON_VERSION}...")
        urllib.request.urlretrieve(PYTHON_ZIP_URL, PYTHON_ZIP_PATH)
        logging.info("Download completed.")

    def extract_python():
        """Extracts the downloaded Python ZIP into the target directory."""
        logging.info("Extracting Python...")
        with zipfile.ZipFile(PYTHON_ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(PYTHON_DIR)
        logging.info("Extraction complete.")

    def enable_site_packages():
        """Enables site packages by editing python*._pth."""
        for file in PYTHON_DIR.glob("python*._pth"):
            lines = file.read_text().splitlines()
            lines = [l if l.strip() != "#import site" else "import site" for l in lines]
            if "import site" not in lines:
                lines.append("import site")
            file.write_text("\n".join(lines))

    if not check_python_version():
        if PYTHON_DIR.exists():
            logging.info(f"Removing old Python environment at {PYTHON_DIR}...")
            shutil.rmtree(
                PYTHON_DIR
            )  # Use shutil.rmtree to remove non-empty directories
            logging.info("Old Python environment removed.")
        os.makedirs(APP_DIR, exist_ok=True)
        download_python()
        extract_python()
        enable_site_packages()


def ensure_pip():
    """Downloads and installs pip using get-pip.py if not already installed."""

    def check_pip_version():
        """Checks if pip is installed and up-to-date."""
        try:
            result = subprocess.run(
                [PYTHON_EXE, "-m", "pip", "--version"], capture_output=True, text=True
            )
            if result.returncode == 0:
                logging.info(f"Pip is already installed: {result.stdout.strip()}")
                return True
        except Exception as e:
            logging.warning(f"Failed to check pip version: {e}")
        return False

    if not check_pip_version():
        logging.info("Pip not found or outdated. Installing pip...")
        get_pip_path = APP_DIR / "get-pip.py"
        urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", get_pip_path)
        subprocess.run(
            [PYTHON_EXE, str(get_pip_path), "--no-warn-script-location"], check=True
        )
        logging.info("Pip installation completed.")


def ensure_requirements():
    """Installs required packages using pip."""
    logging.info("Installing required packages...")
    subprocess.run(
        [
            PYTHON_EXE,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
            "--no-warn-script-location",
            "--no-warn-conflicts",
        ],
        check=True,
        env={**os.environ, "PYTHONWARNINGS": "ignore"},  # Suppress warnings
    )
    subprocess.run(
        [
            PYTHON_EXE,
            "-m",
            "pip",
            "install",
            "--no-warn-script-location",
            "--no-warn-conflicts",
            "--upgrade",
            "-r",
            str(APP_DIR / "requirements.txt"),
        ],
        check=True,
        env={**os.environ, "PYTHONWARNINGS": "ignore"},  # Suppress warnings
    )


def ensure_correct_file_version(filepath: str):
    """Ensures the local app file matches the latest version on GitHub."""

    def get_remote_file_content():
        """Fetches the content of the file from GitHub."""
        try:
            url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/{filepath}"
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.warning(f"Failed to fetch remote file content: {e}")
        return None

    def get_local_file_content():
        """Reads the content of the local file."""
        if local_path.exists():
            with open(local_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    local_path = APP_DIR / filepath
    remote_content = get_remote_file_content()
    local_content = get_local_file_content()

    if remote_content is not None and remote_content == local_content:
        logging.info(f"file {filepath} is up-to-date.")
    else:
        logging.info(
            f"file {filepath} is outdated or missing. Downloading the latest version..."
        )
        url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/master/{filepath}"
        logging.info(f"Downloading from {url}...")
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(remote_content)
        logging.info(f"file  {filepath} updated.")


def run_app():
    """Launches the Streamlit application."""
    logging.info("Launching NEMO UI app...")
    subprocess.Popen(
        [str(PYTHON_EXE), "02_start_nemo_library_ui.py"],
        cwd=APP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )


def main():
    logging.info("Bootstrapping Nemo Application...")
    ensure_python()
    ensure_pip()
    ensure_correct_file_version("requirements.txt")
    ensure_requirements()
    ensure_correct_file_version("02_start_nemo_library_ui.py")
    ensure_correct_file_version("03_nemo_library_ui.py")
    run_app()


if __name__ == "__main__":
    main()
