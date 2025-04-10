import logging
import subprocess
from threading import Thread
import time
import webview
import os
import signal
import socket

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def is_port_open(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def log_stream(stream, level):
    """Log output from a stream (stdout or stderr)."""
    for line in iter(stream.readline, b''):
        logging.log(level, line.decode().strip())
    stream.close()

# Start Streamlit in the background without a terminal window (Windows-specific)
streamlit_proc = subprocess.Popen(
    ["streamlit", "run", "nemo_library_ui.py", "--server.headless", "true", "--browser.serverAddress", "127.0.0.1","--server.port", "8501"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
     creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
)

# Start threads to log both stdout and stderr
Thread(target=log_stream, args=(streamlit_proc.stdout, logging.INFO), daemon=True).start()
Thread(target=log_stream, args=(streamlit_proc.stderr, logging.ERROR), daemon=True).start()

# Wait until the server is ready
logging.info("Waiting for Streamlit to start...")
while not is_port_open('127.0.0.1', 8501):
    time.sleep(0.1)
    logging.info("Waiting for Streamlit to start...")

# Open Streamlit in a native window
webview.create_window("NEMO UI", "http://127.0.0.1:8501")
webview.start()

# Terminate Streamlit when the window is closed
if os.name == 'nt':
    streamlit_proc.send_signal(signal.CTRL_BREAK_EVENT)
else:
    streamlit_proc.terminate()