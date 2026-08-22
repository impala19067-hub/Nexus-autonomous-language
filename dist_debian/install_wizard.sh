#!/usr/bin/env bash
# 🌌 Launch Nexus Setup Wizard GUI on Debian / Kali Linux
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$(which python3 || which python)"

if [ -z "${PYTHON_BIN}" ]; then
    echo "❌ Python 3 is required to run the Graphical Setup Wizard."
    exit 1
fi

"${PYTHON_BIN}" "${SCRIPT_DIR}/nexus_setup_wizard_linux.py" "$@"
