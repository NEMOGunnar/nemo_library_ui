import subprocess
import sys
import os

# 1. Ensure virtualenv or conda is activated (optional if you pre-bundle Python)
# 2. Install required packages
subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "nemo-library", "fastapi", "uvicorn", "jinja2"])

# 3. Start the UI
import ui
ui.start_ui()