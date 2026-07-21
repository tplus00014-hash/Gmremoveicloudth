# iOS Support Notes (branch: feature/full-refactor-ui-ios-support)

This document explains how to enable the iOS-related features in the application.

1) What this provides
- Ability to list connected iOS devices (using idevice_id)
- Ability to query device information (using ideviceinfo)
- These operations require libimobiledevice binaries installed on the host.
- This does NOT provide any method to bypass Activation Lock or remove iCloud locks.

2) Installing libimobiledevice

macOS (recommended for iOS advanced tooling):
- Install Homebrew if you don't have it: https://brew.sh/
- Then: brew install libimobiledevice

Ubuntu / Debian:
- sudo apt update
- sudo apt install -y libimobiledevice6 libimobiledevice-utils

Windows:
- libimobiledevice can be built from source or you can use prebuilt binaries from
  third-party distributions. Windows support is more complex and may require adding
  the tools to PATH. Search for "libimobiledevice windows binaries" and follow
  a trusted guide.

3) Usage from the GUI
- Open the application and click "Refresh iOS". If no devices appear, ensure libimobiledevice
  is installed and the device is trusted on the host.

4) Legal and safety note
- This project provides management and diagnostic tooling for devices you own or manage.
- Do not attempt to bypass vendor security measures (Activation Lock, Find My, etc.).
- The authors do not endorse illegal or unauthorized use.
