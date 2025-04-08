import logging
import subprocess
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

# Start Streamlit in the background without a terminal window (Windows-specific)
streamlit_proc = subprocess.Popen(
    ["streamlit", "run", "nemo_library_ui.py", "--server.headless", "true", "--browser.serverAddress", "127.0.0.1"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
)

# Wait until the server is ready
while not is_port_open('127.0.0.1', 8501):
    time.sleep(0.1)
    logging.info("Waiting for Streamlit to start...")

# Open Streamlit in a native window
webview.create_window("NEMO UI", "http://localhost:8501")
webview.start()

# Terminate Streamlit when the window is closed
if os.name == 'nt':
    streamlit_proc.send_signal(signal.CTRL_BREAK_EVENT)
else:
    streamlit_proc.terminate()