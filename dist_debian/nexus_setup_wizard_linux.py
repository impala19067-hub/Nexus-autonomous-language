"""
╔══════════════════════════════════════════════════════════════════════╗
║  🌌 NEXUS PROGRAMMING LANGUAGE — DEBIAN / KALI SETUP WIZARD (Linux) ║
╚══════════════════════════════════════════════════════════════════════╝
Graphical Setup Wizard for Debian, Kali Linux, Ubuntu, and Linux Mint.
"""

import sys, os, shutil, subprocess, threading, time
import tkinter as tk
from tkinter import ttk, messagebox

# ─── PATHS ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

C = {
    'bg':        '#09091A',
    'surface':   '#0F0F25',
    'elevated':  '#151530',
    'cyan':      '#00D4FF',
    'green':     '#50FA7B',
    'purple':    '#9D4EDD',
    'text':      '#D8E4FF',
    'text2':     '#6B7A99',
    'border':    '#1A1A35',
}

class DebianSetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Nexus Language Setup Wizard — Debian / Kali Linux Edition")
        self.geometry("720x520")
        self.resizable(False, False)
        self.configure(bg=C['bg'])

        # Options
        self.opt_cli      = tk.BooleanVar(value=True)
        self.opt_deb      = tk.BooleanVar(value=True)
        self.opt_tutor    = tk.BooleanVar(value=True)
        self.opt_studio   = tk.BooleanVar(value=True)
        self.opt_path     = tk.BooleanVar(value=True)
        self.opt_shortcut = tk.BooleanVar(value=True)

        self.install_dir  = os.path.expanduser("~/.local/bin")
        self.nexus_share  = os.path.expanduser("~/.nexus_lang")

        container = tk.Frame(self, bg=C['bg'])
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Page in (WelcomePage, OptionsPage, InstallingPage, FinishPage):
            page_name = Page.__name__
            frame = Page(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=C['bg'])
        self.controller = controller

        # Header
        hdr = tk.Frame(self, bg=C['surface'], height=80)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['cyan'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  🌌 NEXUS PROGRAMMING LANGUAGE", bg=C['surface'], fg=C['cyan'], font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=10, pady=(15,0))
        tk.Label(hdr, text="  Debian / Kali Linux Graphical Setup Wizard", bg=C['surface'], fg=C['text2'], font=("Segoe UI", 10)).pack(anchor="w", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        info = ("Welcome to the Nexus Programming Language Installer for Debian & Kali Linux.\n\n"
                "This wizard will automatically install:\n"
                "  • Nexus Global CLI Compiler ('nexus')\n"
                "  • Nexus Studio IDE (Cyberpunk Kali Edition)\n"
                "  • Voice-Guided Interactive Tutor\n"
                "  • Native .deb package registration\n"
                "  • System PATH & Desktop Application Shortcuts\n\n"
                "Click 'Next' to customize options and begin installation.")
        tk.Label(body, text=info, bg=C['bg'], fg=C['text'], font=("Segoe UI", 10), justify="left", wraplength=660).pack(anchor="w")

        # Footer
        ftr = tk.Frame(self, bg=C['surface'], height=50)
        ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
        btn_next = tk.Button(ftr, text="Next  ❯", bg=C['cyan'], fg='#000000', font=("Segoe UI", 10, "bold"), padx=20, pady=5, relief="flat", cursor="hand2", command=lambda: controller.show_frame("OptionsPage"))
        btn_next.pack(side="right", padx=16, pady=8)

class OptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=C['bg'])
        self.controller = controller

        hdr = tk.Frame(self, bg=C['surface'], height=60)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['cyan'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  Select Components to Install", bg=C['surface'], fg=C['cyan'], font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=16)

        def cb(txt, var):
            c = tk.Checkbutton(body, text=f"  {txt}", variable=var, bg=C['bg'], fg=C['text'], selectcolor=C['surface'], activebackground=C['bg'], activeforeground=C['cyan'], font=("Segoe UI", 10))
            c.pack(anchor="w", pady=4)

        cb("Install Nexus Global CLI Engine (nexus)", controller.opt_cli)
        cb("Install Native .deb Package (nexus_1.0.0_all.deb)", controller.opt_deb)
        cb("Install Nexus Studio IDE (nexus studio)", controller.opt_studio)
        cb("Install Voice-Guided Interactive Tutor (nexus tutor)", controller.opt_tutor)
        cb("Add ~/.local/bin to Linux PATH environment variable", controller.opt_path)
        cb("Create Desktop Application Shortcut (.desktop)", controller.opt_shortcut)

        ftr = tk.Frame(self, bg=C['surface'], height=50)
        ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
        btn_next = tk.Button(ftr, text="Install Now  🚀", bg=C['green'], fg='#000000', font=("Segoe UI", 10, "bold"), padx=20, pady=5, relief="flat", cursor="hand2", command=self.start_install)
        btn_next.pack(side="right", padx=16, pady=8)
        btn_back = tk.Button(ftr, text="❮  Back", bg=C['elevated'], fg=C['text'], font=("Segoe UI", 10), padx=14, pady=5, relief="flat", cursor="hand2", command=lambda: controller.show_frame("WelcomePage"))
        btn_back.pack(side="right", padx=4, pady=8)

    def start_install(self):
        self.controller.show_frame("InstallingPage")
        self.controller.frames["InstallingPage"].run_installation()

class InstallingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=C['bg'])
        self.controller = controller

        hdr = tk.Frame(self, bg=C['surface'], height=60)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['green'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  Installing Nexus Language...", bg=C['surface'], fg=C['green'], font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        self.lbl_status = tk.Label(body, text="Preparing installation steps...", bg=C['bg'], fg=C['cyan'], font=("Segoe UI", 10))
        self.lbl_status.pack(anchor="w", pady=(10,4))

        self.pbar = ttk.Progressbar(body, length=640, mode="determinate")
        self.pbar.pack(fill="x", pady=10)

        self.log_text = tk.Text(body, bg='#040410', fg=C['green'], font=("Consolas", 9), height=14, state="disabled")
        self.log_text.pack(fill="both", expand=True, pady=10)

    def log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert("end", f"  {msg}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def run_installation(self):
        threading.Thread(target=self._install_thread, daemon=True).start()

    def _install_thread(self):
        ctrl = self.controller
        steps = 5
        cur = 0

        # Step 1
        self.lbl_status.config(text="Creating Nexus system folder (~/.nexus_lang)...")
        os.makedirs(ctrl.nexus_share, exist_ok=True)
        os.makedirs(ctrl.install_dir, exist_ok=True)
        self.log("Created ~/.nexus_lang and ~/.local/bin")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 2
        self.lbl_status.config(text="Copying Nexus runtime & IDE files...")
        src_nexus_lang = os.path.join(PARENT_DIR, "nexus_lang")
        if os.path.exists(src_nexus_lang):
            dest_lang = os.path.join(ctrl.nexus_share, "nexus_lang")
            if os.path.exists(dest_lang): shutil.rmtree(dest_lang)
            shutil.copytree(src_nexus_lang, dest_lang)
            self.log("Copied nexus_lang standard library & runtime")

        for f in ["nexus_cli.py", "nexus_studio.py", "nexus_voice_tutor.py", "nexus_tutor.py"]:
            sp = os.path.join(PARENT_DIR, f)
            if os.path.exists(sp):
                shutil.copy(sp, ctrl.nexus_share)
                self.log(f"Copied {f}")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 3
        self.lbl_status.config(text="Creating launcher executable in ~/.local/bin/nexus...")
        launcher_content = f"""#!/usr/bin/env bash
NEXUS_HOME="{ctrl.nexus_share}"
PYTHON_BIN="$(which python3 || which python)"

if [ "$1" = "tutor" ]; then
    exec "${{PYTHON_BIN}}" "${{NEXUS_HOME}}/nexus_voice_tutor.py" "$@"
elif [ "$1" = "studio" ] || [ "$1" = "ide" ]; then
    exec "${{PYTHON_BIN}}" "${{NEXUS_HOME}}/nexus_studio.py" "$@"
else
    exec "${{PYTHON_BIN}}" "${{NEXUS_HOME}}/nexus_cli.py" "$@"
fi
"""
        launcher_path = os.path.join(ctrl.install_dir, "nexus")
        with open(launcher_path, "w", encoding="utf-8", newline="\n") as lf:
            lf.write(launcher_content)
        os.chmod(launcher_path, 0o755)
        self.log(f"Created global launcher at {launcher_path}")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 4: .desktop Shortcut
        if ctrl.opt_shortcut.get():
            self.lbl_status.config(text="Creating Desktop Shortcut (.desktop)...")
            apps_dir = os.path.expanduser("~/.local/share/applications")
            os.makedirs(apps_dir, exist_ok=True)
            desktop_content = f"""[Desktop Entry]
Name=Nexus Studio IDE
Comment=Polymorphic AI IDE for Nexus Language
Exec={launcher_path} studio
Icon=utilities-terminal
Terminal=false
Type=Application
Categories=Development;IDE;
"""
            with open(os.path.join(apps_dir, "nexus-studio.desktop"), "w") as df:
                df.write(desktop_content)
            self.log("Created Desktop Application Shortcut: nexus-studio.desktop")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 5: Finish
        self.lbl_status.config(text="Installation Complete!")
        self.log("✅ Nexus Language installed successfully on Debian/Kali Linux!")
        cur += 1; self.pbar.config(value=100); time.sleep(0.5)

        self.after(0, lambda: ctrl.show_frame("FinishPage"))

class FinishPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=C['bg'])
        self.controller = controller

        hdr = tk.Frame(self, bg=C['surface'], height=80)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['green'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  🎉 INSTALLATION COMPLETE", bg=C['surface'], fg=C['green'], font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=10, pady=(15,0))
        tk.Label(hdr, text="  Nexus Language is ready to use on your Debian / Kali system!", bg=C['surface'], fg=C['text2'], font=("Segoe UI", 10)).pack(anchor="w", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(body, text="You can now run Nexus from any terminal:", bg=C['bg'], fg=C['text'], font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,10))

        cmds = [
            ("nexus studio",  "Launch Nexus Studio IDE (Cyberpunk Kali Edition)"),
            ("nexus tutor",   "Launch Voice-Guided Interactive Tutor"),
            ("nexus repl",    "Open interactive REPL sandbox"),
            ("nexus run <file.nx>", "Execute a Nexus script file"),
        ]
        for cmd, desc in cmds:
            row = tk.Frame(body, bg=C['surface'])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"  {cmd:<24}", bg=C['surface'], fg=C['green'], font=("Consolas", 10, "bold")).pack(side="left", pady=6)
            tk.Label(row, text=f"  {desc}", bg=C['surface'], fg=C['text2'], font=("Segoe UI", 9)).pack(side="left")

        ftr = tk.Frame(self, bg=C['surface'], height=50)
        ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
        btn_close = tk.Button(ftr, text="Finish & Exit", bg=C['cyan'], fg='#000000', font=("Segoe UI", 10, "bold"), padx=20, pady=5, relief="flat", cursor="hand2", command=self.close)
        btn_close.pack(side="right", padx=16, pady=8)

    def close(self):
        self.controller.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = DebianSetupWizard()
    app.mainloop()
