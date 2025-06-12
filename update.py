import subprocess
import sys
import os
import zipfile
import tempfile
import shutil
import urllib.request

def update_nemo_library():
    print("📦 Updating nemo-library from PyPI...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "nemo-library"])

def update_ui_from_github():
    zip_url = "https://github.com/NEMOGunnar/nemo_library_ui/archive/refs/heads/main.zip"
    print(f"🌐 Downloading UI from GitHub...")
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "ui.zip")
        urllib.request.urlretrieve(zip_url, zip_path)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        base_folder = os.path.join(tmpdir, "nemo_library_ui-main")

        for folder in ["templates", "static"]:
            src = os.path.join(base_folder, folder)
            dst = os.path.join(os.getcwd(), folder)
            if os.path.isdir(src):
                print(f"🔁 Updating {folder}/...")
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            else:
                print(f"⚠️ {folder}/ not found in archive.")

        # Optional: ui.py ersetzen (nur wenn du willst)
        src_ui = os.path.join(base_folder, "ui.py")
        dst_ui = os.path.join(os.getcwd(), "ui.py")
        if os.path.isfile(src_ui):
            print("📄 Updating ui.py...")
            shutil.copy2(src_ui, dst_ui)