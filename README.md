# Samsung ADB Manager - Remove iCloud/MDM

🚀 A user-friendly Windows GUI application to manage Samsung devices via ADB and remove MDM/iCloud restrictions.

**Now available as standalone .exe with bundled ADB!** No installation required! ⭐

## Features

✅ **Device Management**
- Check connected devices (adb devices)
- Reboot to Recovery mode
- Reboot to Download mode

🗑️ **MDM Removal - Two Methods**
1. **Simple Method**: Uninstall common MDM packages
   - Samsung Knox
   - MobileIron
   - Fiberlink
   - And more...

2. **Advanced Method**: Deep cleanup
   - Clear device admin privileges
   - Reset device policies
   - Disable Knox Guard
   - Clear package installer cache
   - Reset launcher settings

📋 **Real-time Logging**
- View all command outputs in real-time
- Clear log history
- Status indicator for device connection

## Quick Start (Executable Version)

### Option A: Download Ready-Made .exe
Simply download `Gmremoveicloudth.exe` and run it!
- ✅ No Python installation needed
- ✅ No ADB setup required
- ✅ All bundled and ready to use

### Option B: Build .exe Yourself

**Requirements:**
- Windows OS
- Python 3.6+
- Internet connection (to download ADB)

**Steps:**

1. **Clone Repository**
```bash
git clone https://github.com/gmmblspprt-ai/Gmremoveicloudth.git
cd Gmremoveicloudth
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Build Executable**
```bash
python build_executable.py
```

The script will:
- ✓ Download Android SDK Platform Tools
- ✓ Extract ADB tools
- ✓ Install PyInstaller
- ✓ Build standalone .exe with bundled ADB

4. **Find Your .exe**
```
Gmremoveicloudth/
└── dist/
    └── Gmremoveicloudth.exe  ← Ready to use!
```

5. **Distribute**
- Copy `dist/Gmremoveicloudth.exe` to any Windows PC
- Run directly - no setup needed!

---

## Usage (All Versions)

### 1. Enable USB Debugging on Samsung
- Go to **Settings > About Phone**
- Tap "Build Number" 7 times to enable Developer Mode
- Go back to **Settings > Developer Options**
- Enable **USB Debugging**
- Connect device via USB cable

### 2. Run the Application
- **Script version**: `python main.py`
- **Executable version**: Double-click `Gmremoveicloudth.exe`

### 3. Use the GUI
1. **📱 Check Devices** - Verify device is connected
2. **🗑️ Remove MDM (Simple)** - For basic MDM apps (try this first)
3. **⚙️ Remove MDM (Advanced)** - For stubborn MDM (deep cleanup)
4. **🔄 Reboot to Recovery/Download** - Reboot device to special modes
5. **📋 View Logs** - See real-time command output

---

## Troubleshooting

### Device not found?
```bash
# Enable wireless debugging
adb connect <device-ip>:5555

# Or try resetting ADB
adb kill-server
adb start-server
```

### Permission denied?
- Confirm USB Debugging is enabled on device
- Disconnect and reconnect USB cable
- Try different USB port
- Try different USB cable

### MDM still locked after Simple method?
- Try **Advanced Method** for deeper cleanup
- Reboot device after removal
- Some devices require factory reset

### Build errors?
- Ensure internet connection (to download ADB)
- Ensure Python 3.6+ is installed
- Try: `pip install --upgrade pyinstaller`

---

## File Structure

```
Gmremoveicloudth/
├── main.py                 # GUI application
├── adb_manager.py          # ADB commands handler
├── adb_bundler.py          # Bundled ADB manager
├── build_executable.py     # Build script for .exe
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
│
└── dist/                   # Generated after building
    └── Gmremoveicloudth.exe   # Standalone executable
```

---

## Important Notes

⚠️ **WARNING**
- Always backup your device before using this tool
- MDM removal may void warranty
- Some features require specific device conditions
- Use at your own risk

📌 **Tips**
- Keep USB connection stable during operations
- Don't disconnect device during command execution
- Reboot device after successful MDM removal
- Some changes require device restart to take effect

---

## Command Reference (For Manual Use)

```bash
# List connected devices
adb devices

# Reboot to recovery
adb reboot recovery

# Reboot to download mode (Samsung)
adb reboot download

# Check installed MDM packages
adb shell pm list packages | grep mdm

# Uninstall specific package
adb shell pm uninstall --user 0 com.package.name

# Clear device admin
adb shell dpm remove-active-admin com.package/.Admin

# Get device info
adb shell getprop ro.build.version.release
```

---

## Version History

### Version 2.0 (Current - Executable Release)
- ✅ Standalone .exe with bundled ADB
- ✅ No installation required
- ✅ Automatic platform-tools download
- ✅ Enhanced error handling
- ✅ Ready for distribution

### Version 1.0 (Script Release)
- ✅ GUI interface with tkinter
- ✅ Check connected devices
- ✅ Reboot functions
- ✅ Simple & Advanced MDM removal
- ✅ Real-time log display

---

## License

This project is provided as-is for educational and personal use.

---

## Support

For issues:
1. Check Troubleshooting section
2. Verify USB Debugging is enabled
3. Ensure device is properly connected
4. Check GitHub Issues for known problems

---

**Made with ❤️ for Samsung users**

Last Updated: June 2024

---

### Quick Links
- 🔗 [GitHub Repository](https://github.com/gmmblspprt-ai/Gmremoveicloudth)
- 📥 [Download Latest Release](https://github.com/gmmblspprt-ai/Gmremoveicloudth/releases)
- 🐛 [Report Issues](https://github.com/gmmblspprt-ai/Gmremoveicloudth/issues)
