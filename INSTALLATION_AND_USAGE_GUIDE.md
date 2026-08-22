# 🌌 Nexus Programming Language — Complete Installation & Usage Guide

This guide explains how **anyone** can install, configure, and use the **Nexus Programming Language** on their computer from scratch.

---

## 📦 How Someone Installs Nexus (3 Easy Methods)

### Method 1: Standalone One-Click Windows Installer (Recommended for Beginners)
No Python or third-party dependencies required!

1. Download or receive the Nexus distribution folder (containing `install_nexus.bat`, `nexus.exe`, and `nexus_voice_tutor.exe`).
2. Double-click **`install_nexus.bat`**.
3. The installer will automatically:
   - Copy `nexus.exe` and `nexus_voice_tutor.exe` to `%LOCALAPPDATA%\NexusLang`.
   - Register `%LOCALAPPDATA%\NexusLang` in the system environment variable (`PATH`).
4. Open a **new** Command Prompt or PowerShell window and test:
   ```cmd
   nexus info
   ```

---

### Method 2: Portable Binary Execution (Zero Installation)
If someone prefers not to run installers:

1. Download **`nexus.exe`** (standalone single-file executable binary).
2. Copy `nexus.exe` into any project directory or place it in `C:\Windows\System32`.
3. Open terminal in that directory and run:
   ```cmd
   nexus run my_script.nx
   ```

---

### Method 3: Source Code / Developer Installation (Cross-Platform)
If a developer wants to run Nexus directly from Python source code:

1. Clone or copy the `nexus_lang` repository:
   ```bash
   git clone https://github.com/nexus-lang/nexus.git
   cd nexus
   ```
2. Install standard library dependencies (optional, for HTTP & system metrics):
   ```bash
   pip install requests psutil pyttsx3
   ```
3. Run the CLI engine directly:
   ```bash
   python nexus_lang/src/cli.py run examples/01_basics.nx
   ```

---

## 🚀 How to Use Nexus Language

Once installed, the `nexus` command is globally available across your operating system.

### 1. Execute a Nexus Script (`.nx`)
Create a file named `hello.nx`:
```nexus
// hello.nx
let name = "Developer";
let info = os.system_info();

print("🚀 Hello {name}! Welcome to Nexus.");
print("📊 Live System RAM: {info.ram_percent}%");

os.notify("Nexus Alert", "Script executed successfully!");
```

Run it from any terminal:
```cmd
nexus run hello.nx
```

---

### 2. Launch the Interactive REPL Shell
Type `nexus repl` to launch an interactive terminal sandbox:
```cmd
nexus repl
```
```text
🌌 Nexus Language REPL 1.0.0
nexus> let x = 50;
nexus> let y = 100;
nexus> print("Sum: {x + y}");
=> Sum: 150
```

---

### 3. Launch the Voice-Guided Interactive Tutor
Type `nexus tutor` to launch the interactive voice tutor with audio speech narration and step-by-step guidance:
```cmd
nexus tutor
```

---

### 4. Evaluate Inline Code Strings
Quickly evaluate an inline expression:
```cmd
nexus eval "let info = os.system_info(); print(info.platform);"
```

---

## 📑 Core Command Reference

| Command | Description |
| :--- | :--- |
| `nexus run <script.nx>` | Executes a `.nx` script file. |
| `nexus repl` | Launches the interactive REPL shell. |
| `nexus eval "<code>"` | Evaluates an inline code string. |
| `nexus tutor` | Launches the Voice-Guided Interactive Tutor (`nexus_voice_tutor.exe`). |
| `nexus info` | Displays version and capability summary. |

---

## 📁 What Files to Share/Distribute to Others

To share Nexus with another user, zip and send them these files:
- **`install_nexus.bat`** (Automated installer)
- **`nexus.exe`** (Global CLI Compiler & Runtime)
- **`nexus_voice_tutor.exe`** (Voice-Guided Interactive Tutor)
- **`Nexus_Coding_and_Usage_Guide.pdf`** (Complete Reference Manual)
- **`Beginners_Guide_Your_First_Autonomous_AI.pdf`** (Beginner Tutorial)
