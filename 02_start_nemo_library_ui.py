import logging
from pathlib import Path
import re
import subprocess
from threading import Thread
import time
import webview
import os
import signal
import socket

# Configure logging
LOGFILE = Path.home() / ".nemo_app" / "nemoui.log"

log_file_path = os.path.expanduser("~/nemo_ui.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler(LOGFILE, mode="a", encoding="utf-8"),  # Log to file
    ],
)


def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0


def log_stream(stream, level):
    """Log output from a stream (stdout or stderr)."""
    for line in iter(stream.readline, b""):
        logging.log(level, line.decode().strip())
    stream.close()


def get_url_from_log(stream):
    """Check if the URL is in the log stream."""
    if stream:
        port_pattern = re.compile(r"URL: http://127\.0\.0\.1:(\d+)")
        for line in iter(stream.readline, b""):
            decoded_line = line.decode().strip()
            logging.info(decoded_line)  # Log the output for debugging
            match = port_pattern.search(decoded_line)
            if match:
                return int(match.group(1))
    return None


# Start Streamlit in the background without a terminal window (Windows-specific)
streamlit_proc = subprocess.Popen(
    [
        "streamlit",
        "run",
        "03_nemo_library_ui.py",
        "--server.headless",
        "true",
        "--browser.serverAddress",
        "127.0.0.1",
        "--server.port",
        "8501",
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
)
logging.info("Streamlit process started.")  

# Start threads to log both stdout and stderr
Thread(
    target=log_stream, args=(streamlit_proc.stdout, logging.INFO), daemon=True
).start()
Thread(
    target=log_stream, args=(streamlit_proc.stderr, logging.ERROR), daemon=True
).start()

# Wait until the server is ready
logging.info("Waiting for Streamlit to start...")
streamlitport = get_url_from_log(streamlit_proc.stdout)
while not streamlit_proc.stdout and not streamlitport:
    time.sleep(0.1)
    logging.info("Waiting for Streamlit to start...")
    streamlitport = get_url_from_log(streamlit_proc.stdout)
logging.info(f"Streamlit started on port {streamlitport}")

# Wait for the port to be open
while not is_port_open('127.0.0.1', streamlitport):
    time.sleep(0.1)
    logging.info("Waiting for Streamlit Port to open...")

# Open Streamlit in a native window
webview.create_window("NEMO UI", f"http://127.0.0.1:{streamlitport}")
webview.start()

# Terminate Streamlit when the window is closed
if os.name == "nt":
    streamlit_proc.send_signal(signal.CTRL_BREAK_EVENT)
else:
    streamlit_proc.terminate()
