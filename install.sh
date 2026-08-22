#!/usr/bin/env bash
# 🌌 Nexus Programming Language — Automated Linux & macOS Installer
# Supports Kali Linux, Ubuntu, Debian, Arch, Fedora, and macOS.

set -e

echo "====================================================================="
echo "  🌌 NEXUS PROGRAMMING LANGUAGE — AUTOMATED LINUX/macOS INSTALLER"
echo "====================================================================="
echo ""

# Determine OS
OS_TYPE="$(uname -s)"
echo "Detected Operating System: ${OS_TYPE}"

# Target install directory
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
    NEED_SUDO=""
else
    INSTALL_DIR="${HOME}/.local/bin"
    NEED_SUDO=""
    mkdir -p "${INSTALL_DIR}"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEXUS_SHARE="${HOME}/.nexus_lang"

echo "[1/3] Creating Nexus system directory at ${NEXUS_SHARE}..."
mkdir -p "${NEXUS_SHARE}"

echo "[2/3] Copying Nexus runtime engine & standard libraries..."
cp -r "${SCRIPT_DIR}/nexus_lang" "${NEXUS_SHARE}/"
cp "${SCRIPT_DIR}/nexus_cli.py" "${NEXUS_SHARE}/"
if [ -f "${SCRIPT_DIR}/nexus_voice_tutor.py" ]; then
    cp "${SCRIPT_DIR}/nexus_voice_tutor.py" "${NEXUS_SHARE}/"
fi
if [ -f "${SCRIPT_DIR}/nexus_tutor.py" ]; then
    cp "${SCRIPT_DIR}/nexus_tutor.py" "${NEXUS_SHARE}/"
fi

echo "[3/3] Creating global 'nexus' terminal executable in ${INSTALL_DIR}..."

cat << 'EOF' > "${NEXUS_SHARE}/nexus_launcher.sh"
#!/usr/bin/env bash
NEXUS_HOME="${HOME}/.nexus_lang"
PYTHON_BIN="$(which python3 || which python)"

if [ -z "${PYTHON_BIN}" ]; then
    echo "❌ Error: Python 3 is required to run Nexus on Linux/macOS."
    exit 1
fi

if [ "$1" = "tutor" ]; then
    "${PYTHON_BIN}" "${NEXUS_HOME}/nexus_voice_tutor.py" "$@"
else
    "${PYTHON_BIN}" "${NEXUS_HOME}/nexus_cli.py" "$@"
fi
EOF

chmod +x "${NEXUS_SHARE}/nexus_launcher.sh"
ln -sf "${NEXUS_SHARE}/nexus_launcher.sh" "${INSTALL_DIR}/nexus"

# Verify PATH for ~/.local/bin
if [ "${INSTALL_DIR}" = "${HOME}/.local/bin" ]; then
    if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
        SHELL_RC="${HOME}/.bashrc"
        if [ -f "${HOME}/.zshrc" ]; then
            SHELL_RC="${HOME}/.zshrc"
        fi
        echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${SHELL_RC}"
        echo "ℹ️ Added ~/.local/bin to your PATH in ${SHELL_RC}"
    fi
fi

echo ""
echo "====================================================================="
echo "  🎉 NEXUS LANGUAGE INSTALLATION COMPLETE!"
echo "====================================================================="
echo ""
echo " You can now open any terminal on Linux/macOS and type:"
echo ""
echo "    nexus info           - Display language overview & version"
echo "    nexus run bot.nx     - Run a Nexus script file"
echo "    nexus repl           - Open interactive REPL shell"
echo "    nexus tutor          - Launch Interactive Tutor"
echo ""
