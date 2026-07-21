"""
UI skeleton using PySide6. This file provides a minimal GUI that lists Android and iOS devices
and offers action buttons. It is a safe, non-destructive interface and calls into
adb_wrapper.py and ios_manager.py for device operations.

Run: python ui_app.py

Dependencies: PySide6
"""
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QListWidget, QTextEdit, QLabel)
from PySide6.QtCore import Qt, Slot
import threading
import subprocess
import sys

from adb_wrapper import list_adb_devices, simple_mdm_remove
from ios_manager import list_ios_devices, get_ios_info


def run_in_thread(fn, *args, callback=None):
    def wrapper():
        result = fn(*args)
        if callback:
            callback(result)
    t = threading.Thread(target=wrapper, daemon=True)
    t.start()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gmremoveicloudth - Device Manager (Preview)")
        self.setMinimumSize(800, 500)

        layout = QVBoxLayout()

        # Device lists
        lists_layout = QHBoxLayout()

        # Android
        android_layout = QVBoxLayout()
        android_label = QLabel("Android Devices")
        self.android_list = QListWidget()
        btn_refresh_android = QPushButton("Refresh Android")
        btn_refresh_android.clicked.connect(self.refresh_android)
        android_layout.addWidget(android_label)
        android_layout.addWidget(self.android_list)
        android_layout.addWidget(btn_refresh_android)

        # iOS
        ios_layout = QVBoxLayout()
        ios_label = QLabel("iOS Devices")
        self.ios_list = QListWidget()
        btn_refresh_ios = QPushButton("Refresh iOS")
        btn_refresh_ios.clicked.connect(self.refresh_ios)
        ios_layout.addWidget(ios_label)
        ios_layout.addWidget(self.ios_list)
        ios_layout.addWidget(btn_refresh_ios)

        lists_layout.addLayout(android_layout)
        lists_layout.addLayout(ios_layout)

        layout.addLayout(lists_layout)

        # Action buttons
        actions_layout = QHBoxLayout()
        btn_simple_mdm = QPushButton("Simple MDM (Android)")
        btn_simple_mdm.clicked.connect(self.simple_mdm)
        btn_ios_info = QPushButton("Get iOS Info")
        btn_ios_info.clicked.connect(self.ios_info)
        actions_layout.addWidget(btn_simple_mdm)
        actions_layout.addWidget(btn_ios_info)

        layout.addLayout(actions_layout)

        # Log view
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

        # Initial refresh
        self.refresh_android()
        self.refresh_ios()

    def append_log(self, text: str):
        self.log.append(text)

    def refresh_android(self):
        self.append_log("Refreshing Android devices...")
        run_in_thread(list_adb_devices, callback=self._on_android_listed)

    def _on_android_listed(self, devices):
        self.android_list.clear()
        if not devices:
            self.append_log("No Android devices found")
            return
        for d in devices:
            self.android_list.addItem(d)
        self.append_log(f"Found {len(devices)} Android device(s)")

    def refresh_ios(self):
        self.append_log("Refreshing iOS devices...")
        run_in_thread(list_ios_devices, callback=self._on_ios_listed)

    def _on_ios_listed(self, devices):
        self.ios_list.clear()
        if not devices:
            self.append_log("No iOS devices found or libimobiledevice not installed")
            return
        for d in devices:
            self.ios_list.addItem(d)
        self.append_log(f"Found {len(devices)} iOS device(s)")

    def simple_mdm(self):
        item = self.android_list.currentItem()
        if not item:
            self.append_log("Select an Android device first")
            return
        serial = item.text()
        self.append_log(f"Running simple MDM removal on {serial} (this may be destructive).")
        run_in_thread(simple_mdm_remove, serial, callback=lambda r: self.append_log(r))

    def ios_info(self):
        item = self.ios_list.currentItem()
        if not item:
            self.append_log("Select an iOS device first")
            return
        udid = item.text()
        self.append_log(f"Fetching iOS info for {udid}...")
        run_in_thread(get_ios_info, udid, callback=lambda r: self.append_log(r))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
