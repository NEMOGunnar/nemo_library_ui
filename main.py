import subprocess
import sys
import webbrowser
import time
import socket
import threading
import os
from datetime import datetime, timezone
from urllib.request import urlopen
from urllib.error import URLError

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

# === Import version info ===
try:
    from nemo_library import NemoLibrary
    version = NemoLibrary.__version__
except Exception:
    version = "Unknown"
    import traceback
    traceback.print_exc()

# === Heartbeat monitor (thread-safe) ===
class HeartbeatMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self._last_ping = datetime.now(timezone.utc)

    def ping(self):
        with self._lock:
            self._last_ping = datetime.now(timezone.utc)

    def too_old(self, max_age_seconds: int) -> bool:
        with self._lock:
            elapsed = (datetime.now(timezone.utc) - self._last_ping).total_seconds()
            return elapsed > max_age_seconds

monitor = HeartbeatMonitor()

# === FastAPI setup ===
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "version": version})

@app.get("/heartbeat")
def heartbeat():
    monitor.ping()
    return {"status": "ok"}

# === Server management helpers ===
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def wait_for_server(url: str, timeout: float = 10.0):
    start_time = time.time()
    while True:
        try:
            urlopen(url)
            return True
        except URLError:
            if time.time() - start_time > timeout:
                print(f"⚠️ Server did not start within {timeout} seconds.")
                return False
            time.sleep(0.3)

def run_server(port: int):
    uvicorn.run(app=app, host="127.0.0.1", port=port, reload=False)
    
def monitor_heartbeat(timeout_seconds=15):
    while True:
        time.sleep(timeout_seconds)
        if monitor.too_old(timeout_seconds):
            print("💀 No heartbeat detected, shutting down...")
            os._exit(0)

# === Main execution ===
if __name__ == "__main__":
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"

    threading.Thread(target=run_server, args=(port,), daemon=True).start()
    threading.Thread(target=monitor_heartbeat, daemon=True).start()

    if wait_for_server(url):
        webbrowser.open(url)

    while True:
        time.sleep(1)