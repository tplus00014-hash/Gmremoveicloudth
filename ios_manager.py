"""
ios_manager.py
Wrapper for basic libimobiledevice commands. This module calls system binaries
(idevice_id, ideviceinfo) which must be installed separately. This code does not
bypass any Apple security measures or Activation Lock.

Supported operations:
- list_ios_devices(): calls `idevice_id -l`
- get_ios_info(udid): calls `ideviceinfo -u <udid>`

Installation (macOS/Linux/Windows): see README.IOS.md for instructions.
"""
import subprocess
import shlex


def _run(cmd, timeout=20):
    try:
        p = subprocess.run(shlex.split(cmd), capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def list_ios_devices():
    code, out, err = _run('idevice_id -l')
    if code != 0:
        return []
    return [l.strip() for l in out.splitlines() if l.strip()]


def get_ios_info(udid):
    # Returns a textual summary (first 2000 chars limited)
    code, out, err = _run(f'ideviceinfo -u {udid}')
    if code != 0:
        return f'Failed to query device {udid}: {err or out}'
    return out
