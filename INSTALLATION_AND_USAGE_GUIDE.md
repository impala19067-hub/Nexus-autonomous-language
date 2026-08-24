# 💎 Sapphire Programming Language — Complete Installation & Usage Guide

This guide explains how **anyone** can install, configure, and use the **Sapphire Programming Language** and **Emerald Developer Studio** on their computer from scratch.

---

## 📦 How Someone Installs Sapphire (3 Easy Methods)

### Method 1: Standalone Graphical Windows Installer (`Sapphire_Setup_Wizard.exe`)
No Python or third-party dependencies required!

1. Download **`Sapphire_Setup_Wizard.exe`**.
2. Double-click **`Sapphire_Setup_Wizard.exe`**.
3. The installer will automatically:
   - Copy Sapphire language engine and Emerald Developer Studio GUI (`emerald_studio.py`).
   - Register `%LOCALAPPDATA%\SapphireLang` in the system environment variable (`PATH`).
   - Create Desktop shortcuts for Emerald Developer Studio GUI.
4. Open a **new** Command Prompt or PowerShell window and test:
   ```cmd
   sapphire info
   ```

---

### Method 2: Portable Binary Execution (Zero Installation)
If someone prefers not to run installers:

1. Download **`sapphire.exe`** (standalone single-file executable binary).
2. Copy `sapphire.exe` into any project directory or place it in `C:\Windows\System32`.
3. Open terminal in that directory and run:
   ```cmd
   sapphire run my_script.nx
   ```

---

### Method 3: Source Code / Developer Installation (Cross-Platform)
If a developer wants to run Sapphire directly from Python source code:

1. Clone or copy the `sapphire_lang` repository:
   ```bash
   git clone https://github.com/sapphire-lang/sapphire.git
   cd sapphire
   ```
2. Install standard library dependencies (optional, for HTTP & system metrics):
   ```bash
   pip install requests psutil pyttsx3
   ```
3. Run the CLI engine directly:
   ```bash
   python sapphire_lang/src/cli.py run examples/01_basics.nx
   ```

---

## 🚀 How to Use Sapphire Language

Once installed, the `sapphire` command is globally available across your operating system.

### 1. Execute a Sapphire Script (`.nx`)
Create a file named `hello.nx`:
```sapphire
// hello.nx
let name = "Developer";
let info = os.system_info();

print("🚀 Hello {name}! Welcome to Sapphire.");
print("📊 Live System RAM: {info.ram_percent}%");

os.notify("Sapphire Alert", "Script executed successfully!");
```

Run it from any terminal:
```cmd
sapphire run hello.nx
```

---

### 2. Launch the Interactive REPL Shell
Type `sapphire repl` to launch an interactive terminal sandbox:
```cmd
sapphire repl
```
```text
🌌 Sapphire Language REPL 1.0.0
sapphire> let x = 50;
sapphire> let y = 100;
sapphire> print("Sum: {x + y}");
=> Sum: 150
```

---

### 3. Launch Emerald Developer Studio GUI
Type `sapphire studio` to launch Emerald Developer Studio — the graphical IDE, tool builder, and GPU dashboard:
```cmd
sapphire studio
```

---

### 4. Evaluate Inline Code Strings
Quickly evaluate an inline expression:
```cmd
sapphire eval "let info = os.system_info(); print(info.platform);"
```

---

## 📑 Core Command Reference

| Command | Description |
| :--- | :--- |
| `sapphire run <script.sp>` | Executes a `.sp` Sapphire script file. |
| `sapphire studio` | Launches Emerald Developer Studio GUI (`emerald_studio.py`). |
| `sapphire repl` | Launches the interactive REPL shell. |
| `sapphire eval "<code>"` | Evaluates an inline code string. |
| `sapphire info` | Displays version, AI LLM backends, ML engine, and capability summary. |

---

## 📁 What Files to Share/Distribute to Others

To share Sapphire with another user, zip and send them these files:
- **`install_sapphire.bat`** (Automated installer)
- **`sapphire.exe`** (Global CLI Compiler & Runtime)
- **`sapphire_voice_tutor.exe`** (Voice-Guided Interactive Tutor)
- **`Sapphire_Coding_and_Usage_Guide.pdf`** (Complete Reference Manual)
- **`Beginners_Guide_Your_First_Autonomous_AI.pdf`** (Beginner Tutorial)
