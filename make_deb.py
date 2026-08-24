"""
🌌 Nexus Programming Language — Debian/Kali (.deb) Package Builder
Generates a native Debian/Kali Linux package: nexus_1.0.0_all.deb
Allows installation via: sudo apt install ./nexus_1.0.0_all.deb
"""

import os, sys, shutil, subprocess, tarfile, gzip, io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NEXUS_LANG_DIR = os.path.join(BASE_DIR, "nexus_lang")
DEB_ROOT = os.path.join(BASE_DIR, "nexus_1.0.0_all")

def create_deb_structure():
    if os.path.exists(DEB_ROOT):
        shutil.rmtree(DEB_ROOT)

    # Folders
    debian_dir = os.path.join(DEB_ROOT, "DEBIAN")
    bin_dir    = os.path.join(DEB_ROOT, "usr", "bin")
    share_dir  = os.path.join(DEB_ROOT, "usr", "share", "nexus_lang")

    os.makedirs(debian_dir, exist_ok=True)
    os.makedirs(bin_dir,    exist_ok=True)
    os.makedirs(share_dir,  exist_ok=True)

    # 1. DEBIAN/control
    control_content = """Package: nexus-lang
Version: 1.0.0
Section: devel
Priority: optional
Architecture: all
Maintainer: Nexus Language Team <nexus@local>
Depends: python3 (>= 3.8)
Description: Nexus Programming Language
 Autonomous-first programming language for PC Automation,
 Colorless Concurrency, and Native AI Intelligence.
"""
    with open(os.path.join(debian_dir, "control"), "w", encoding="utf-8") as f:
        f.write(control_content)

    # 2. Copy source files to /usr/share/nexus_lang
    shutil.copytree(NEXUS_LANG_DIR, os.path.join(share_dir, "nexus_lang"))
    for py_file in ["nexus_cli.py", "nexus_voice_tutor.py", "nexus_tutor.py", "nexus_studio.py"]:
        src = os.path.join(BASE_DIR, py_file)
        if os.path.exists(src):
            shutil.copy(src, share_dir)

    # 3. /usr/bin/nexus executable launcher
    nexus_launcher = """#!/usr/bin/env bash
NEXUS_SHARE="/usr/share/nexus_lang"
PYTHON_BIN="$(which python3 || which python)"

if [ "$1" = "tutor" ]; then
    exec "${PYTHON_BIN}" "${NEXUS_SHARE}/nexus_voice_tutor.py" "$@"
elif [ "$1" = "studio" ] || [ "$1" = "ide" ]; then
    exec "${PYTHON_BIN}" "${NEXUS_SHARE}/nexus_studio.py" "$@"
else
    exec "${PYTHON_BIN}" "${NEXUS_SHARE}/nexus_cli.py" "$@"
fi
"""
    launcher_path = os.path.join(bin_dir, "nexus")
    with open(launcher_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(nexus_launcher)
    os.chmod(launcher_path, 0o755)

    print("[OK] Package file layout created at:", DEB_ROOT)

def pack_deb():
    deb_filename = os.path.join(BASE_DIR, "nexus_1.0.0_all.deb")
    import ar_builder
    ar_builder.build_deb(DEB_ROOT, deb_filename)

if __name__ == "__main__":
    create_deb_structure()
    pack_deb()
