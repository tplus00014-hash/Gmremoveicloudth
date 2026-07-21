"""
adb_wrapper.py
A small wrapper that calls `adb` to list devices and perform a simple MDM removal
for Android. This wrapper uses subprocess and expects adb to be available on PATH or
bundled with the application.

Note: The simple_mdm_remove function is intentionally conservative and only demonstrates
how the GUI would call into adb-related functionality — it uninstalls packages from the
user 0 user space. Use at your own risk and always back up devices.
"""
import subprocess
import shlex


def _run(cmd, timeout=30):
    try:
        p = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def list_adb_devices():
    code, out, err = _run('adb devices')
    if code != 0:
        return []
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    devices = []
    for l in lines:
        if '\tdevice' in l:
            devices.append(l.split('\t')[0])
    return devices


def simple_mdm_remove(serial):
    # Example: uninstall a list of common MDM package names
    mdm_packages = [
        'com.knox.mdm',
        'com.mobileiron',
        'com.fiberlink',
    ]
    results = []
    for pkg in mdm_packages:
        cmd = f'adb -s {serial} shell pm uninstall --user 0 {pkg}'
        code, out, err = _run(cmd)
        if code == 0:
            results.append(f'Uninstalled {pkg}: {out or "OK"}')
        else:
            results.append(f'Failed {pkg}: {err or out}')
    return '\n'.join(results)
