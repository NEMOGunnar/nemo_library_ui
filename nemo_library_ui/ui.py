import os
import time
import socket
import threading
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
import importlib.resources

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from nemo_library import NemoLibrary
import nemo_library_ui  # needed for static/templates resolution

version = NemoLibrary.__version__

# === Heartbeat monitor ===
class HeartbeatMonitor:
    def __init__(self):
        self._lock = threading.Lock()
        self._last_ping = datetime.now(timezone.utc)

    def ping(self):
        with self._lock:
            self._last_ping = datetime.now(timezone.utc)

    def too_old(self, max_age_seconds: int) -> bool:
        with self._lock:
            return (datetime.now(timezone.utc) - self._last_ping).total_seconds() > max_age_seconds

monitor = HeartbeatMonitor()

# === Paths to static/templates inside installed package ===
package_dir = Path(nemo_library_ui.__file__).parent
static_dir = package_dir / "static"
templates_dir = package_dir / "templates"

# === FastAPI setup ===
app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "version": version})

@app.get("/heartbeat")
def heartbeat():
    monitor.ping()
    return {"status": "ok"}

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]

def wait_for_server(url: str, timeout: float = 10.0):
    import urllib.request
    import urllib.error
    start = time.time()
    while True:
        try:
            urllib.request.urlopen(url)
            return True
        except urllib.error.URLError:
            if time.time() - start > timeout:
                return False
            time.sleep(0.3)

def monitor_heartbeat(timeout=15):
    while True:
        time.sleep(timeout)
        if monitor.too_old(timeout):
            print("No heartbeat received – shutting down.")
            os._exit(0)

def start_ui(open_browser=True):
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"

    threading.Thread(target=monitor_heartbeat, daemon=True).start()
    threading.Thread(target=lambda: uvicorn.run(app=app, host="127.0.0.1", port=port), daemon=True).start()

    if wait_for_server(url):
        if open_browser:
            webbrowser.open(url)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    start_ui()