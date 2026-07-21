"""
adb_wrapper.py
A small wrapper that calls `adb` to list devices and perform a simple MDM removal
for Android. This wrapper uses subprocess and expects adb to be available on PATH or
bundled with the application (platform-tools folder).

The wrapper now resolves the adb executable path by checking, in order:
 - bundled platform-tools inside the frozen executable (sys._MEIPASS)
 - a platform-tools folder next to this script (./platform-tools/adb or adb.exe)
 - the system PATH (shutil.which)

Use get_adb_path() to get the resolved adb binary. Commands are executed with the
absolute adb path where possible to ensure the bundled adb is used when present.

Note: Keep conservative behavior — always check devices and warn users before
running destructive operations.
"""
import os
import sys
import shutil
import subprocess
from typing import List, Tuple


def get_adb_path() -> str:
    """Return the path to adb executable.

    Resolution order:
    1. If frozen (PyInstaller), look under sys._MEIPASS/platform-tools/adb(.exe)
    2. Look for ./platform-tools/adb(.exe) next to this script
    3. Use shutil.which('adb' or 'adb.exe') to find adb in PATH
    4. Return the adb executable name as last resort
    """
    adb_name = 'adb.exe' if os.name == 'nt' else 'adb'

    # 1) When frozen by PyInstaller, data is in sys._MEIPASS
    bundle_base = None
    if getattr(sys, 'frozen', False):
        bundle_base = getattr(sys, '_MEIPASS', None)
        if bundle_base:
            candidate = os.path.join(bundle_base, 'platform-tools', adb_name)
            if os.path.exists(candidate):
                return candidate

    # 2) Check local project platform-tools (next to this file)
    this_dir = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(this_dir, 'platform-tools', adb_name)
    if os.path.exists(candidate):
        return candidate

    # 3) Check PATH
    which = shutil.which(adb_name)
    if which:
        return which

    # 4) Fallback to generic name (may rely on PATH at runtime)
    return adb_name


def _run(cmd: List[str], timeout: int = 30) -> Tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def list_adb_devices() -> List[str]:
    adb = get_adb_path()
    code, out, err = _run([adb, 'devices'])
    if code != 0:
        return []
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    devices = []
    for l in lines:
        if '\tdevice' in l:
            devices.append(l.split('\t')[0])
    return devices


def simple_mdm_remove(serial: str) -> str:
    # Example: uninstall a list of common MDM package names (conservative)
    mdm_packages = [
        'com.knox.mdm',
        'com.mobileiron',
        'com.fiberlink',
    ]
    adb = get_adb_path()
    results = []
    for pkg in mdm_packages:
        cmd = [adb, '-s', serial, 'shell', 'pm', 'uninstall', '--user', '0', pkg]
        code, out, err = _run(cmd)
        if code == 0:
            results.append(f'Uninstalled {pkg}: {out or "OK"}')
        else:
            results.append(f'Failed {pkg}: {err or out}')
    return '\n'.join(results)
