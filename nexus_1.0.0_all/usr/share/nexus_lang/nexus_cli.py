"""
🌌 NEXUS PROGRAMMING LANGUAGE — GLOBAL CLI LAUNCHER
Usage:
  nexus run <script.nx>    Execute a Nexus script file
  nexus repl               Launch Interactive REPL shell
  nexus eval "<code>"      Evaluate inline Nexus code string
  nexus tutor              Launch Voice-Guided Interactive Tutor
  nexus studio             Launch Nexus Studio (VSCode-Inspired IDE)
  nexus ide                Alias for 'nexus studio'
  nexus info               Show language architecture info & version
"""

import sys
import os
import subprocess

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NEXUS_DIR = os.path.join(BASE_DIR, "nexus_lang")

for p in [BASE_DIR, NEXUS_DIR]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

# Pre-import stdlib dependencies for PyInstaller static bundling
try:
    import requests
except ImportError:
    requests = None
try:
    import psutil
except ImportError:
    psutil = None
import urllib.request
import json
import ctypes
import platform

from src.cli import main as cli_main

def launch_app(exe_name, py_name):
    """Helper to launch a companion app by exe or py fallback."""
    exe_path = os.path.join(BASE_DIR, exe_name)
    py_path  = os.path.join(BASE_DIR, py_name)
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path], cwd=BASE_DIR)
    elif os.path.exists(py_path):
        subprocess.Popen([sys.executable, py_path], cwd=BASE_DIR)
    else:
        print(f"❌ Module not found: {exe_name} / {py_name}")

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == "tutor":
        launch_app("nexus_voice_tutor.exe", "nexus_voice_tutor.py")

    elif cmd in ("studio", "ide"):
        launch_app("Nexus_Studio.exe", "nexus_studio.py")

    elif cmd == "info":
        print("🌌 Nexus Language v1.0.0 (Automation Era)")
        print("Executables:")
        print("  nexus run <file.nx>   — Execute a Nexus script")
        print("  nexus repl            — Interactive REPL shell")
        print("  nexus studio          — Launch Nexus Studio (VSCode IDE)")
        print("  nexus tutor           — Launch Voice-Guided Interactive Tutor")
        print("  nexus eval \"<code>\"  — Evaluate inline code string")

    else:
        cli_main()

if __name__ == "__main__":
    main()
