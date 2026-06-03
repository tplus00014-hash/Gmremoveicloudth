import subprocess
import platform
import sys
from pathlib import Path


class ADBManager:
    """Manage ADB commands for Samsung devices"""
    
    def __init__(self):
        self.adb_command = self.get_adb_path()
        self.platform = platform.system()
    
    def get_adb_path(self):
        """Get the path to ADB executable"""
        # Try to find adb in PATH
        try:
            result = subprocess.run(
                ["where" if platform.system() == "Windows" else "which", "adb"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Default locations
        if platform.system() == "Windows":
            possible_paths = [
                Path(r"C:\Android\platform-tools\adb.exe"),
                Path(r"C:\Users") / Path.home().name / r"AppData\Local\Android\Sdk\platform-tools\adb.exe",
            ]
        else:
            possible_paths = [
                Path.home() / "Android/Sdk/platform-tools/adb",
                Path("/usr/bin/adb"),
                Path("/usr/local/bin/adb"),
            ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return "adb"  # Hope it's in PATH
    
    def run_command(self, cmd):
        """Run a shell command and return output"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=False
            )
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    def check_devices(self):
        """List connected ADB devices"""
        cmd = [self.adb_command, "devices"]
        return self.run_command(cmd)
    
    def reboot_device(self, mode="recovery"):
        """
        Reboot device to specified mode
        mode: 'recovery', 'download', 'bootloader', or 'system'
        """
        if mode == "download":
            # Samsung Download mode
            cmd = [self.adb_command, "reboot", "download"]
        elif mode == "bootloader":
            cmd = [self.adb_command, "reboot", "bootloader"]
        else:
            # Default recovery
            cmd = [self.adb_command, "reboot", "recovery"]
        
        result = self.run_command(cmd)
        return f"Rebooting to {mode}...\n{result}"
    
    def remove_mdm_simple(self):
        """
        Simple MDM removal: Uninstall common MDM packages
        """
        mdm_packages = [
            "com.samsung.knox.keasecurefolderapp",
            "com.samsung.android.knox.kgclient",
            "com.samsung.android.fmm",
            "com.sec.enterprise.mdm.manager",
            "com.samsung.android.mdm",
            "com.ssi.mdm",
            "com.mobileiron.client",
            "com.fiberlink.maas360",
            "com.air.mobileiron",
        ]
        
        output = "Starting Simple MDM Removal...\n"
        output += "=" * 50 + "\n"
        
        for package in mdm_packages:
            output += f"\nChecking: {package}\n"
            cmd = [self.adb_command, "shell", "pm", "uninstall", "--user", "0", package]
            result = self.run_command(cmd)
            output += result + "\n"
        
        output += "=" * 50 + "\n"
        output += "Simple MDM removal process completed!\n"
        return output
    
    def remove_mdm_advanced(self):
        """
        Advanced MDM removal: Reset device policies and admin privileges
        """
        output = "Starting Advanced MDM Removal...\n"
        output += "=" * 50 + "\n"
        
        # Step 1: Clear device admin
        output += "\n[Step 1] Clearing Device Admin...\n"
        cmd = [
            self.adb_command, "shell", "dpm", "remove-active-admin",
            "com.sec.enterprise.mdm.manager/.PushReceiver"
        ]
        result = self.run_command(cmd)
        output += result + "\n"
        
        # Step 2: Reset device policies
        output += "\n[Step 2] Resetting Device Policies...\n"
        cmd = [self.adb_command, "shell", "settings", "delete", "secure", "device_policy_manager"]
        result = self.run_command(cmd)
        output += result + "\n"
        
        # Step 3: Clear package installer cache
        output += "\n[Step 3] Clearing Package Installer Cache...\n"
        cmd = [
            self.adb_command, "shell", "pm", "clear",
            "com.android.packageinstaller"
        ]
        result = self.run_command(cmd)
        output += result + "\n"
        
        # Step 4: Disable Knox Guard
        output += "\n[Step 4] Disabling Knox Guard...\n"
        cmd = [
            self.adb_command, "shell", "pm", "uninstall", "--user", "0",
            "com.samsung.android.fmm"
        ]
        result = self.run_command(cmd)
        output += result + "\n"
        
        # Step 5: Reset default launcher
        output += "\n[Step 5] Resetting Launcher Settings...\n"
        cmd = [
            self.adb_command, "shell", "settings", "put", "secure",
            "launcher_permissions_changed", "1"
        ]
        result = self.run_command(cmd)
        output += result + "\n"
        
        # Step 6: Uninstall MDM packages
        output += "\n[Step 6] Uninstalling MDM Packages...\n"
        mdm_packages = [
            "com.sec.enterprise.mdm.manager",
            "com.samsung.android.mdm",
            "com.samsung.android.knox.kgclient",
        ]
        
        for package in mdm_packages:
            cmd = [self.adb_command, "shell", "pm", "uninstall", "--user", "0", package]
            result = self.run_command(cmd)
            output += f"{package}: {result}\n"
        
        output += "=" * 50 + "\n"
        output += "Advanced MDM removal process completed!\n"
        output += "Note: Device may need to be rebooted for changes to take effect.\n"
        
        return output
    
    def push_file(self, local_path, device_path):
        """Push a file to the device"""
        cmd = [self.adb_command, "push", local_path, device_path]
        return self.run_command(cmd)
    
    def pull_file(self, device_path, local_path):
        """Pull a file from the device"""
        cmd = [self.adb_command, "pull", device_path, local_path]
        return self.run_command(cmd)
    
    def shell_command(self, command):
        """Execute a shell command on the device"""
        cmd = [self.adb_command, "shell", command]
        return self.run_command(cmd)
