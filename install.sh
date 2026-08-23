#!/usr/bin/env bash
# Nexus Programming Language - Automated Linux & macOS Installer
# Supports Kali Linux, Ubuntu, Debian, Arch, Fedora, and macOS.

echo "====================================================================="
echo "  NEXUS PROGRAMMING LANGUAGE - AUTOMATED LINUX/macOS INSTALLER"
echo "====================================================================="
echo ""

# Determine OS
OS_TYPE="$(uname -s)"
echo "Detected Operating System: ${OS_TYPE}"

# Install directory
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="${HOME}/.local/bin"
    mkdir -p "${INSTALL_DIR}"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEXUS_SHARE="${HOME}/.nexus_lang"

echo "[1/3] Creating Nexus system directory at ${NEXUS_SHARE}..."
mkdir -p "${NEXUS_SHARE}"

echo "[2/3] Copying Nexus runtime engine & standard libraries..."

# Copy the core nexus_lang folder (contains lexer, parser, interpreter, stdlib)
if [ -d "${SCRIPT_DIR}/nexus_lang" ]; then
    cp -r "${SCRIPT_DIR}/nexus_lang" "${NEXUS_SHARE}/"
    echo "      Copied nexus_lang engine."
else
    echo "ERROR: nexus_lang directory not found in ${SCRIPT_DIR}"
    exit 1
fi

echo "[3/3] Creating global 'nexus' terminal executable in ${INSTALL_DIR}..."

# Write the launcher script - points directly into nexus_lang/src/cli.py
cat > "${NEXUS_SHARE}/nexus_launcher.sh" << 'LAUNCHEREOF'
#!/usr/bin/env bash
NEXUS_HOME="${HOME}/.nexus_lang"
PYTHON_BIN="$(which python3 2>/dev/null || which python 2>/dev/null)"

if [ -z "${PYTHON_BIN}" ]; then
    echo "Error: Python 3 is required to run Nexus on Linux/macOS."
    echo "Install it with: sudo apt install python3"
    exit 1
fi

exec "${PYTHON_BIN}" "${NEXUS_HOME}/nexus_lang/src/cli.py" "$@"
LAUNCHEREOF

chmod +x "${NEXUS_SHARE}/nexus_launcher.sh"

# Symlink into PATH
ln -sf "${NEXUS_SHARE}/nexus_launcher.sh" "${INSTALL_DIR}/nexus"
chmod +x "${INSTALL_DIR}/nexus"

# Add ~/.local/bin to PATH if needed
if [ "${INSTALL_DIR}" = "${HOME}/.local/bin" ]; then
    if [[ ":$PATH:" != *":${HOME}/.local/bin:"* ]]; then
        SHELL_RC="${HOME}/.bashrc"
        if [ -f "${HOME}/.zshrc" ]; then
            SHELL_RC="${HOME}/.zshrc"
        fi
        echo 'export PATH="${HOME}/.local/bin:${PATH}"' >> "${SHELL_RC}"
        echo "      Added ~/.local/bin to PATH in ${SHELL_RC}"
        export PATH="${HOME}/.local/bin:${PATH}"
    fi
fi

echo ""
echo "====================================================================="
echo "  NEXUS LANGUAGE INSTALLATION COMPLETE!"
echo "====================================================================="
echo ""
echo "  Run these commands from any terminal:"
echo ""
echo "    nexus info              - Language overview & version"
echo "    nexus run <script.nx>   - Run a Nexus script file"
echo "    nexus repl              - Open interactive REPL shell"
echo "    nexus eval \"<code>\"     - Evaluate inline code"
echo ""

# Run nexus info immediately to confirm
if command -v nexus &>/dev/null; then
    echo "--- Quick Test ---"
    nexus info
fi
