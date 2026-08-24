#!/usr/bin/env bash
# Sapphire Programming Language - Automated Linux & macOS Installer
# Supports Kali Linux, Ubuntu, Debian, Arch, Fedora, and macOS.

echo "====================================================================="
echo "  SAPPHIRE PROGRAMMING LANGUAGE - AUTOMATED LINUX/macOS INSTALLER"
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
SAPPHIRE_SHARE="${HOME}/.sapphire_lang"

echo "[1/3] Creating Sapphire system directory at ${SAPPHIRE_SHARE}..."
mkdir -p "${SAPPHIRE_SHARE}"

echo "[2/3] Copying Sapphire runtime engine & standard libraries..."

# Copy the core sapphire_lang folder (contains lexer, parser, interpreter, stdlib)
if [ -d "${SCRIPT_DIR}/sapphire_lang" ]; then
    cp -r "${SCRIPT_DIR}/sapphire_lang" "${SAPPHIRE_SHARE}/"
    echo "      Copied sapphire_lang engine."
else
    echo "ERROR: sapphire_lang directory not found in ${SCRIPT_DIR}"
    exit 1
fi

echo "[3/3] Creating global 'sapphire' terminal executable in ${INSTALL_DIR}..."

# Write the launcher script - points directly into sapphire_lang/src/cli.py
cat > "${SAPPHIRE_SHARE}/sapphire_launcher.sh" << 'LAUNCHEREOF'
#!/usr/bin/env bash
SAPPHIRE_HOME="${HOME}/.sapphire_lang"
PYTHON_BIN="$(which python3 2>/dev/null || which python 2>/dev/null)"

if [ -z "${PYTHON_BIN}" ]; then
    echo "Error: Python 3 is required to run Sapphire on Linux/macOS."
    echo "Install it with: sudo apt install python3"
    exit 1
fi

exec "${PYTHON_BIN}" "${SAPPHIRE_HOME}/sapphire_lang/src/cli.py" "$@"
LAUNCHEREOF

chmod +x "${SAPPHIRE_SHARE}/sapphire_launcher.sh"

# Symlink into PATH
ln -sf "${SAPPHIRE_SHARE}/sapphire_launcher.sh" "${INSTALL_DIR}/sapphire"
chmod +x "${INSTALL_DIR}/sapphire"

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
echo "  SAPPHIRE LANGUAGE INSTALLATION COMPLETE!"
echo "====================================================================="
echo ""
echo "  Run these commands from any terminal:"
echo ""
echo "    sapphire info              - Language overview & version"
echo "    sapphire run <script.nx>   - Run a Sapphire script file"
echo "    sapphire repl              - Open interactive REPL shell"
echo "    sapphire eval \"<code>\"     - Evaluate inline code"
echo ""

# Run sapphire info immediately to confirm
if command -v sapphire &>/dev/null; then
    echo "--- Quick Test ---"
    sapphire info
fi
