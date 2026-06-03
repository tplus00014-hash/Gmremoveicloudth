import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import subprocess
import sys
from adb_manager import ADBManager


class ADBManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Samsung ADB Manager - Remove iCloud/MDM")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        self.adb_manager = ADBManager()
        
        # Color scheme
        self.bg_color = "#f0f0f0"
        self.button_color = "#4CAF50"
        self.button_hover = "#45a049"
        self.warning_color = "#ff9800"
        self.danger_color = "#f44336"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the GUI components"""
        
        # Header frame
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Samsung ADB Manager",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        header_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Remove iCloud/MDM - Simple & Advanced Methods",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack(pady=5)
        
        # Status indicator frame
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="● Disconnected",
            font=("Arial", 10),
            fg="#e74c3c",
            bg=self.bg_color
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Row 1: Device Check
        row1_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        row1_frame.pack(fill=tk.X, pady=5)
        
        self.check_devices_btn = self.create_button(
            row1_frame,
            "📱 Check Devices (adb devices)",
            self.check_devices,
            self.button_color
        )
        self.check_devices_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 2: Reboot options
        row2_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        row2_frame.pack(fill=tk.X, pady=5)
        
        self.reboot_recovery_btn = self.create_button(
            row2_frame,
            "🔄 Reboot to Recovery",
            lambda: self.reboot_device("recovery"),
            self.warning_color
        )
        self.reboot_recovery_btn.pack(side=tk.LEFT, padx=5)
        
        self.reboot_download_btn = self.create_button(
            row2_frame,
            "📥 Reboot to Download Mode",
            lambda: self.reboot_device("download"),
            self.warning_color
        )
        self.reboot_download_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 3: MDM Removal - Simple Method
        row3_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        row3_frame.pack(fill=tk.X, pady=5)
        
        mdm_label = tk.Label(
            row3_frame,
            text="Remove MDM - Simple Method:",
            font=("Arial", 9, "bold"),
            bg=self.bg_color
        )
        mdm_label.pack(side=tk.LEFT, padx=5)
        
        self.remove_mdm_simple_btn = self.create_button(
            row3_frame,
            "🗑️ Remove MDM (Simple)",
            self.remove_mdm_simple,
            self.danger_color
        )
        self.remove_mdm_simple_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 4: MDM Removal - Advanced Method
        row4_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        row4_frame.pack(fill=tk.X, pady=5)
        
        adv_label = tk.Label(
            row4_frame,
            text="Remove MDM - Advanced Method:",
            font=("Arial", 9, "bold"),
            bg=self.bg_color
        )
        adv_label.pack(side=tk.LEFT, padx=5)
        
        self.remove_mdm_advanced_btn = self.create_button(
            row4_frame,
            "⚙️ Remove MDM (Advanced)",
            self.remove_mdm_advanced,
            self.danger_color
        )
        self.remove_mdm_advanced_btn.pack(side=tk.LEFT, padx=5)
        
        # Row 5: Additional options
        row5_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        row5_frame.pack(fill=tk.X, pady=5)
        
        self.clear_log_btn = self.create_button(
            row5_frame,
            "🗑️ Clear Log",
            self.clear_log,
            "#95a5a6"
        )
        self.clear_log_btn.pack(side=tk.LEFT, padx=5)
        
        # Log display area
        log_label = tk.Label(
            main_frame,
            text="Command Log & Status:",
            font=("Arial", 10, "bold"),
            bg=self.bg_color
        )
        log_label.pack(anchor=tk.W, pady=(15, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            height=15,
            width=80,
            font=("Courier", 9),
            bg="#2c3e50",
            fg="#ecf0f1",
            insertbackground="white"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        self.log_message("=== Samsung ADB Manager Started ===")
        self.log_message("Ready to connect with your Samsung device")
    
    def create_button(self, parent, text, command, color):
        """Create a styled button"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 9, "bold"),
            bg=color,
            fg="white",
            padx=10,
            pady=8,
            cursor="hand2",
            relief=tk.RAISED,
            bd=2
        )
        return btn
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def clear_log(self):
        """Clear the log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("=== Log Cleared ===")
    
    def update_status(self, connected, device_name=""):
        """Update connection status"""
        if connected:
            self.status_label.config(
                text=f"● Connected to: {device_name}",
                fg="#27ae60"
            )
        else:
            self.status_label.config(
                text="● Disconnected",
                fg="#e74c3c"
            )
    
    def check_devices(self):
        """Check connected devices"""
        def run():
            self.log_message("\n--- Checking for connected devices ---")
            result = self.adb_manager.check_devices()
            self.log_message(result)
            
            if "device" in result and result.count("\n") > 1:
                devices = [line.strip() for line in result.split("\n") if "device" in line and not line.startswith("List")]
                if devices:
                    device_name = devices[0].split("\t")[0] if devices else "Unknown"
                    self.update_status(True, device_name)
            else:
                self.update_status(False)
        
        threading.Thread(target=run, daemon=True).start()
    
    def reboot_device(self, mode):
        """Reboot device to specified mode"""
        def run():
            mode_display = "Recovery" if mode == "recovery" else "Download"
            self.log_message(f"\n--- Rebooting to {mode_display} Mode ---")
            result = self.adb_manager.reboot_device(mode)
            self.log_message(result)
        
        threading.Thread(target=run, daemon=True).start()
    
    def remove_mdm_simple(self):
        """Remove MDM - Simple method"""
        confirm = messagebox.askyesno(
            "Confirm",
            "Remove MDM packages? (Simple Method)\n\nThis will uninstall MDM applications."
        )
        
        if confirm:
            def run():
                self.log_message("\n--- Remove MDM (Simple Method) ---")
                result = self.adb_manager.remove_mdm_simple()
                self.log_message(result)
            
            threading.Thread(target=run, daemon=True).start()
    
    def remove_mdm_advanced(self):
        """Remove MDM - Advanced method"""
        confirm = messagebox.askyesno(
            "Confirm",
            "Remove MDM? (Advanced Method)\n\nThis will reset device policies and admin privileges."
        )
        
        if confirm:
            def run():
                self.log_message("\n--- Remove MDM (Advanced Method) ---")
                result = self.adb_manager.remove_mdm_advanced()
                self.log_message(result)
            
            threading.Thread(target=run, daemon=True).start()


def main():
    root = tk.Tk()
    app = ADBManagerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
