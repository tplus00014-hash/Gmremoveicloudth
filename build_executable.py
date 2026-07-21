# build_executable.py
import os
import sys
import subprocess
import urllib.request
import zipfile

PLATTOOLS_ZIP_URL = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
PLATTOOLS_DIR = "platform-tools"
ENTRY_SCRIPT = "ui_app.py"  # Entry point for the GUI


def download_platform_tools():
    if os.path.isdir(PLATTOOLS_DIR) and os.path.exists(os.path.join(PLATTOOLS_DIR, "adb.exe")):
        print("platform-tools found, skipping download.")
        return
    print("Downloading platform-tools...")
    zip_path = "platform-tools.zip"
    urllib.request.urlretrieve(PLATTOOLS_ZIP_URL, zip_path)
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall('.')
    if os.path.exists(zip_path):
        os.remove(zip_path)
    print("platform-tools ready.")


def ensure_pyinstaller():
    try:
        import PyInstaller  # noqa: F401
        return
    except Exception:
        print("Installing pyinstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def build_exe():
    # Prepare --add-data args for PyInstaller on Windows (use ; as separator)
    add_data_args = []
    if os.path.isdir(PLATTOOLS_DIR):
        add_data_args += ["--add-data", f"{PLATTOOLS_DIR};{PLATTOOLS_DIR}"]
    # Include README.IOS.md as reference
    if os.path.exists("README.IOS.md"):
        add_data_args += ["--add-data", "README.IOS.md;."]

    cmd = [sys.executable, "-m", "PyInstaller",
           "--noconfirm", "--onefile", "--windowed"] + add_data_args + [ENTRY_SCRIPT]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)


if __name__ == "__main__":
    if os.name != "nt":
        print("Warning: This build script is targeted for Windows hosts. You can still run it on other OS but the bundled platform-tools will be Windows build.")
    download_platform_tools()
    ensure_pyinstaller()
    build_exe()
    print("Build finished. Check the dist\\ folder for the .exe file.")
