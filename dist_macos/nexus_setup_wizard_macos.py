"""
╔══════════════════════════════════════════════════════════════════════╗
║  🌌 NEXUS PROGRAMMING LANGUAGE — macOS SETUP WIZARD                  ║
╚══════════════════════════════════════════════════════════════════════╝
Graphical Setup Wizard for macOS (Apple Silicon M1/M2/M3 & Intel Mac).
"""

import sys, os, shutil, subprocess, threading, time
import tkinter as tk
from tkinter import ttk, messagebox

# ─── PATHS ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(BASE_DIR)

C = {
    'bg':        '#1E1E1E',
    'surface':   '#252526',
    'elevated':  '#2D2D2D',
    'cyan':      '#00D4FF',
    'green':     '#30D158',
    'purple':    '#BF5AF2',
    'text':      '#FFFFFF',
    'text2':     '#8E8E93',
    'border':    '#383838',
}

class MacOSSetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ Nexus Language Setup Wizard — macOS Edition")
        self.geometry("700x500")
        self.resizable(False, False)
        self.configure(bg=C['bg'])

        self.opt_cli    = tk.BooleanVar(value=True)
        self.opt_studio = tk.BooleanVar(value=True)
        self.opt_tutor  = tk.BooleanVar(value=True)
        self.opt_path   = tk.BooleanVar(value=True)

        self.install_dir = os.path.expanduser("~/.local/bin")
        self.nexus_share = os.path.expanduser("~/.nexus_lang")

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

        hdr = tk.Frame(self, bg=C['surface'], height=80)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['cyan'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  🍎 NEXUS FOR macOS", bg=C['surface'], fg=C['cyan'], font=("System", 16, "bold")).pack(anchor="w", padx=10, pady=(15,0))
        tk.Label(hdr, text="  Graphical Setup Wizard for Apple Silicon & Intel Mac", bg=C['surface'], fg=C['text2'], font=("System", 10)).pack(anchor="w", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        info = ("Welcome to the Nexus Programming Language Installer for macOS.\n\n"
                "This installer will configure:\n"
                "  • Nexus Global Terminal Compiler ('nexus')\n"
                "  • Nexus Studio IDE (Dark Theme)\n"
                "  • Voice-Guided Interactive Tutor with macOS Speech Engine\n"
                "  • Registration in your macOS zsh/bash PATH environment\n\n"
                "Click 'Continue' to begin setup.")
        tk.Label(body, text=info, bg=C['bg'], fg=C['text'], font=("System", 11), justify="left", wraplength=640).pack(anchor="w")

        ftr = tk.Frame(self, bg=C['surface'], height=50)
        ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
        btn_next = tk.Button(ftr, text="Continue  ❯", bg=C['cyan'], fg='#000000', font=("System", 10, "bold"), padx=20, pady=5, relief="flat", cursor="hand2", command=lambda: controller.show_frame("OptionsPage"))
        btn_next.pack(side="right", padx=16, pady=8)

class OptionsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=C['bg'])
        self.controller = controller

        hdr = tk.Frame(self, bg=C['surface'], height=60)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['cyan'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  Select Installation Options", bg=C['surface'], fg=C['cyan'], font=("System", 14, "bold")).pack(side="left", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        def cb(txt, var):
            c = tk.Checkbutton(body, text=f"  {txt}", variable=var, bg=C['bg'], fg=C['text'], selectcolor=C['surface'], activebackground=C['bg'], activeforeground=C['cyan'], font=("System", 11))
            c.pack(anchor="w", pady=6)

        cb("Install Nexus Global CLI Engine (nexus command)", controller.opt_cli)
        cb("Install Nexus Studio IDE (nexus studio)", controller.opt_studio)
        cb("Install Voice-Guided Interactive Tutor (nexus tutor)", controller.opt_tutor)
        cb("Add ~/.local/bin to macOS terminal PATH (~/.zshrc)", controller.opt_path)

        ftr = tk.Frame(self, bg=C['surface'], height=50)
        ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
        btn_next = tk.Button(ftr, text="Install Now  🚀", bg=C['green'], fg='#000000', font=("System", 10, "bold"), padx=20, pady=5, relief="flat", cursor="hand2", command=self.start_install)
        btn_next.pack(side="right", padx=16, pady=8)
        btn_back = tk.Button(ftr, text="❮  Back", bg=C['elevated'], fg=C['text'], font=("System", 10), padx=14, pady=5, relief="flat", cursor="hand2", command=lambda: controller.show_frame("WelcomePage"))
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
        tk.Label(hdr, text="  Installing Nexus on macOS...", bg=C['surface'], fg=C['green'], font=("System", 14, "bold")).pack(side="left", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        self.lbl_status = tk.Label(body, text="Preparing installation...", bg=C['bg'], fg=C['cyan'], font=("System", 10))
        self.lbl_status.pack(anchor="w", pady=(10,4))

        self.pbar = ttk.Progressbar(body, length=640, mode="determinate")
        self.pbar.pack(fill="x", pady=10)

        self.log_text = tk.Text(body, bg='#040410', fg=C['green'], font=("Menlo", 10), height=12, state="disabled")
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
        steps = 4
        cur = 0

        # Step 1
        self.lbl_status.config(text="Creating macOS system directory (~/.nexus_lang)...")
        os.makedirs(ctrl.nexus_share, exist_ok=True)
        os.makedirs(ctrl.install_dir, exist_ok=True)
        self.log("Created ~/.nexus_lang and ~/.local/bin")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 2
        self.lbl_status.config(text="Copying runtime modules...")
        src_nexus_lang = os.path.join(PARENT_DIR, "nexus_lang")
        if os.path.exists(src_nexus_lang):
            dest_lang = os.path.join(ctrl.nexus_share, "nexus_lang")
            if os.path.exists(dest_lang): shutil.rmtree(dest_lang)
            shutil.copytree(src_nexus_lang, dest_lang)
            self.log("Copied nexus_lang standard library")

        for f in ["nexus_cli.py", "nexus_studio.py", "nexus_voice_tutor.py", "nexus_tutor.py"]:
            sp = os.path.join(PARENT_DIR, f)
            if os.path.exists(sp):
                shutil.copy(sp, ctrl.nexus_share)
                self.log(f"Copied {f}")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 3
        self.lbl_status.config(text="Creating global 'nexus' launcher...")
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
        self.log(f"Created macOS launcher: {launcher_path}")
        cur += 1; self.pbar.config(value=(cur/steps)*100); time.sleep(0.3)

        # Step 4: PATH update in .zshrc
        if ctrl.opt_path.get():
            zshrc = os.path.expanduser("~/.zshrc")
            export_line = 'export PATH="$HOME/.local/bin:$PATH"'
            already = False
            if os.path.exists(zshrc):
                with open(zshrc, "r") as zf:
                    if export_line in zf.read(): already = True
            if not already:
                with open(zshrc, "a") as zf:
                    zf.write(f"\n# Nexus Language PATH\n{export_line}\n")
                self.log("Added ~/.local/bin to ~/.zshrc")
        cur += 1; self.pbar.config(value=100); time.sleep(0.5)

        self.lbl_status.config(text="macOS Installation Complete!")
        self.log("✅ Nexus Language installed on macOS!")

        self.after(0, lambda: ctrl.show_frame("FinishPage"))

class FinishPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=C['bg'])
        self.controller = controller

        hdr = tk.Frame(self, bg=C['surface'], height=80)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['green'], width=4).pack(side="left", fill="y")
        tk.Label(hdr, text="  🎉 macOS INSTALLATION COMPLETE", bg=C['surface'], fg=C['green'], font=("System", 16, "bold")).pack(anchor="w", padx=10, pady=(15,0))
        tk.Label(hdr, text="  Nexus Language is ready to run on your Mac!", bg=C['surface'], fg=C['text2'], font=("System", 10)).pack(anchor="w", padx=10)

        body = tk.Frame(self, bg=C['bg'])
        body.pack(fill="both", expand=True, padx=24, pady=20)

        tk.Label(body, text="Open Terminal app and test these commands:", bg=C['bg'], fg=C['text'], font=("System", 11, "bold")).pack(anchor="w", pady=(0,10))

        cmds = [
            ("nexus studio",  "Launch Nexus Studio IDE"),
            ("nexus tutor",   "Launch Voice Tutor"),
            ("nexus repl",    "Open REPL sandbox"),
            ("nexus run <file.nx>", "Run script file"),
        ]
        for cmd, desc in cmds:
            row = tk.Frame(body, bg=C['surface'])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"  {cmd:<22}", bg=C['surface'], fg=C['green'], font=("Menlo", 10, "bold")).pack(side="left", pady=6)
            tk.Label(row, text=f"  {desc}", bg=C['surface'], fg=C['text2'], font=("System", 9)).pack(side="left")

        ftr = tk.Frame(self, bg=C['surface'], height=50)
        ftr.pack(fill="x", side="bottom"); ftr.pack_propagate(False)
        btn_close = tk.Button(ftr, text="Finish & Exit", bg=C['cyan'], fg='#000000', font=("System", 10, "bold"), padx=20, pady=5, relief="flat", cursor="hand2", command=self.close)
        btn_close.pack(side="right", padx=16, pady=8)

    def close(self):
        self.controller.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = MacOSSetupWizard()
    app.mainloop()
