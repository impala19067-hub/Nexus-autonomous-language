"""
🌌 Sapphire Programming Language — Debian/Kali (.deb) Package Builder
Generates a native Debian/Kali Linux package: sapphire_1.0.5_all.deb
Allows installation via: sudo apt install ./sapphire_1.0.5_all.deb
"""

import os, sys, shutil, subprocess, tarfile, gzip, io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAPPHIRE_LANG_DIR = os.path.join(BASE_DIR, "sapphire_lang")
DEB_ROOT = os.path.join(BASE_DIR, "sapphire_1.0.5_all")

def create_deb_structure():
    if os.path.exists(DEB_ROOT):
        shutil.rmtree(DEB_ROOT)

    # Folders
    debian_dir = os.path.join(DEB_ROOT, "DEBIAN")
    bin_dir    = os.path.join(DEB_ROOT, "usr", "bin")
    share_dir  = os.path.join(DEB_ROOT, "usr", "share", "sapphire_lang")

    os.makedirs(debian_dir, exist_ok=True)
    os.makedirs(bin_dir,    exist_ok=True)
    os.makedirs(share_dir,  exist_ok=True)

    # 1. DEBIAN/control
    control_content = """Package: sapphire-lang
Version: 1.0.5
Section: devel
Priority: optional
Architecture: all
Maintainer: Sapphire Language Team <sapphire@local>
Depends: python3 (>= 3.8)
Description: Sapphire Programming Language
 Autonomous-first programming language for PC Automation,
 Colorless Concurrency, and Native AI Intelligence.
"""
    with open(os.path.join(debian_dir, "control"), "w", encoding="utf-8") as f:
        f.write(control_content)

    # 2. Copy source files to /usr/share/sapphire_lang
    shutil.copytree(SAPPHIRE_LANG_DIR, os.path.join(share_dir, "sapphire_lang"))
    for py_file in ["sapphire_cli.py", "sapphire_voice_tutor.py", "sapphire_tutor.py", "emerald_studio.py"]:
        src = os.path.join(BASE_DIR, py_file)
        if os.path.exists(src):
            shutil.copy(src, share_dir)

    # 3. /usr/bin/sapphire executable launcher
    sapphire_launcher = """#!/usr/bin/env bash
SAPPHIRE_SHARE="/usr/share/sapphire_lang"
PYTHON_BIN="$(which python3 || which python)"

if [ "$1" = "tutor" ]; then
    exec "${PYTHON_BIN}" "${SAPPHIRE_SHARE}/sapphire_voice_tutor.py" "$@"
elif [ "$1" = "studio" ] || [ "$1" = "ide" ]; then
    exec "${PYTHON_BIN}" "${SAPPHIRE_SHARE}/emerald_studio.py" "$@"
else
    exec "${PYTHON_BIN}" "${SAPPHIRE_SHARE}/sapphire_cli.py" "$@"
fi
"""
    launcher_path = os.path.join(bin_dir, "sapphire")
    with open(launcher_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(sapphire_launcher)
    os.chmod(launcher_path, 0o755)

    print("[OK] Package file layout created at:", DEB_ROOT)

def pack_deb():
    deb_filename = os.path.join(BASE_DIR, "sapphire_1.0.5_all.deb")
    import ar_builder
    ar_builder.build_deb(DEB_ROOT, deb_filename)

if __name__ == "__main__":
    create_deb_structure()
    pack_deb()
