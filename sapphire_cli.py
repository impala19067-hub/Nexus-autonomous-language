"""
🌌 SAPPHIRE PROGRAMMING LANGUAGE — GLOBAL CLI LAUNCHER
Usage:
  sapphire run <script.sp>    Execute a Sapphire script file
  sapphire repl               Launch Interactive REPL shell
  sapphire eval "<code>"      Evaluate inline Sapphire code string
  sapphire tutor              Launch Voice-Guided Interactive Tutor
  sapphire studio             Launch Emerald Developer Studio (VSCode-Inspired IDE)
  sapphire ide                Alias for 'sapphire studio'
  sapphire info               Show language architecture info & version
"""

import sys
import os
import subprocess

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAPPHIRE_DIR = os.path.join(BASE_DIR, "sapphire_lang")

for p in [BASE_DIR, SAPPHIRE_DIR]:
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
        launch_app("sapphire_voice_tutor.exe", "sapphire_voice_tutor.py")

    elif cmd in ("studio", "ide"):
        launch_app("Emerald_Studio.exe", "emerald_studio.py")

    elif cmd == "info":
        print("🌌 Sapphire Language v1.0.0 (Automation Era)")
        print("Executables:")
        print("  sapphire run <file.sp>   — Execute a Sapphire script")
        print("  sapphire repl            — Interactive REPL shell")
        print("  sapphire studio          — Launch Emerald Developer Studio (VSCode IDE)")
        print("  sapphire tutor           — Launch Voice-Guided Interactive Tutor")
        print("  sapphire eval \"<code>\"  — Evaluate inline code string")

    else:
        cli_main()

if __name__ == "__main__":
    main()
