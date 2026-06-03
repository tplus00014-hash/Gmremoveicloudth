import os
import sys
import subprocess
from pathlib import Path
import shutil
import zipfile
import urllib.request


class ADBBundler:
    """Handle bundled ADB management"""
    
    def __init__(self):
        self.base_path = self.get_base_path()
        self.adb_dir = self.base_path / "adb_tools"
        self.adb_exe = self.adb_dir / "adb.exe"
    
    def get_base_path(self):
        """Get the base path for the application"""
        if getattr(sys, 'frozen', False):
            # Running as compiled .exe
            return Path(sys.executable).parent
        else:
            # Running as script
            return Path(__file__).parent
    
    def ensure_adb_exists(self):
        """Ensure ADB is available"""
        if self.adb_exe.exists():
            return str(self.adb_exe)
        
        # If not frozen, try to find system ADB
        if not getattr(sys, 'frozen', False):
            try:
                result = subprocess.run(
                    ["where", "adb"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
        
        raise FileNotFoundError(
            "ADB not found! Please ensure ADB tools are properly bundled."
        )
    
    def get_adb_path(self):
        """Get ADB executable path"""
        return str(self.ensure_adb_exists())
