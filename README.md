# 🌌 Nexus Programming Language

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Platform: Windows | Linux | macOS](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-0078D6.svg)
![Release: v1.0.0](https://img.shields.io/badge/Release-v1.0.0-green.svg)

**Nexus** is a cross-platform, autonomous-first programming language engineered for **PC Automation**, **Native AI Intelligence**, and **Colorless Parallel Concurrency**. Supports **Windows**, **Linux (Kali, Ubuntu, Debian, Arch)**, and **macOS**.

---

## ✨ Key Features

- 🤖 **Native AI Primitives**: Built-in `ai.prompt("...")` construct directly in the syntax.
- 🖥️ **PC Automation**: System telemetry (`os.system_info()`), desktop notifications (`os.notify()`), and clipboard access (`os.clip_write()`).
- ⚡ **Colorless Concurrency**: Execute concurrent tasks with simple `parallel { ... }` blocks.
- ⏱️ **Persistent Schedulers**: Native background task scheduling via `scheduler.interval()`.
- 🔊 **Voice & Interactive Tutor**: Included interactive tutor (`nexus_voice_tutor.exe` / `nexus tutor`) that teaches Nexus step-by-step.
- 🌐 **Cross-Platform**: Natively runs on Windows, Kali Linux, Ubuntu, Debian, Arch, and macOS.

---

## 🚀 Installation Guide

### 🪟 Windows Setup
Download **[Nexus_Setup_Wizard.exe](https://github.com/impala19067-hub/Nexus-autonomous-language/releases)** from the Latest Release and double-click to install.

### 🐧 Linux (Kali, Ubuntu, Debian, Arch) & 🍎 macOS Setup

#### Method A: 1-Line Instant Installer (Recommended)
Run this single command in your Linux / Kali / macOS terminal:

```bash
curl -sSL https://raw.githubusercontent.com/impala19067-hub/Nexus-autonomous-language/main/install.sh | bash
```

#### Method B: Native Kali / Debian Package (`.deb`)
Download `nexus_1.0.0_all.deb` from Releases and install via `apt`:

```bash
sudo apt install ./nexus_1.0.0_all.deb
```

---

## 💻 Terminal Command Usage

Once installed, open any terminal on Windows, Linux, or macOS and type:

```cmd
# 1. Display Nexus information
nexus info

# 2. Run a Nexus script file
nexus run my_bot.nx

# 3. Launch Interactive REPL Shell
nexus repl

# 4. Launch Interactive Tutor
nexus tutor
```

---

## 💻 Code Example: 5-Line Autonomous AI Bot

```nexus
// my_first_bot.nx
fn main() {
    let stats = os.system_info();
    let opinion = ai.prompt("System RAM is at {stats.ram_percent}%. Is this healthy?");
    
    print("🤖 AI Evaluation: {opinion}");
    os.notify("Nexus Bot Alert", opinion);
}

main();
```

---

## 📚 Documentation & Manuals

- [📘 Nexus Coding & Usage Guide (PDF)](Nexus_Coding_and_Usage_Guide.pdf)
- [🤖 Building Advanced Autonomous AI (PDF)](Building_Advanced_Autonomous_AI.pdf)
- [📊 Autonomy & Performance Benchmarks (PDF)](Nexus_Autonomy_and_Performance_Benchmarks.pdf)
- [🎓 Beginner's Guide: Your First Autonomous AI (PDF)](Beginners_Guide_Your_First_Autonomous_AI.pdf)

---

## 📄 License
Released under the MIT License.
