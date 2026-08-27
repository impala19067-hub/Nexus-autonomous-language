"""Sapphire v1.0.5 Windows installer."""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

VERSION = "1.0.5"
ROOT = os.path.dirname(os.path.abspath(__file__))
PALETTE = {
    "canvas": "#F4FBF7", "surface": "#FFFFFF", "header": "#073B2A",
    "ink": "#123B27", "muted": "#557A64", "line": "#C8E3D1",
    "mint": "#42D98A", "mint_dark": "#087F4E", "soft": "#E6F5EC",
}
FILES = [
    "sapphire.exe", "sapphire_cli.exe", "emerald.exe", "Emerald_Studio.exe",
    "Sapphire_Compiler.exe", "Sapphire_Runtime.exe", "Sapphire_Icon.ico",
    "Emerald_Icon.ico", "sapphire_voice_tutor.exe", "sapphire_tutor.exe",
    "uninstall.exe", "uninstall_sapphire.exe", "emerald_studio.py",
    "sapphire_cli.py", "sapphire_compiler.py", "sapphire_voice_tutor.py",
    "sapphire_tutor.py", "uninstall_sapphire.py", "install_sapphire.bat",
    "README.md", "INSTALLATION_AND_USAGE_GUIDE.md", "INDUSTRIAL_READINESS.md",
    "release_manifest.json", "Sapphire_Coding_and_Usage_Guide.pdf",
    "Building_Advanced_Autonomous_AI.pdf", "Sapphire_Autonomy_and_Performance_Benchmarks.pdf",
    "Beginners_Guide_Your_First_Autonomous_AI.pdf",
    "Sapphire_Language_Specification_and_Automation_Manual.pdf",
    "Sapphire_Capabilities_and_Transparency_Manual.pdf",
]


def source_path(name: str):
    candidates = []
    if getattr(sys, "frozen", False):
        candidates.extend([os.path.join(getattr(sys, "_MEIPASS", ""), name), os.path.join(os.path.dirname(sys.executable), name)])
    candidates.extend([os.path.join(ROOT, name), os.path.join(os.getcwd(), name)])
    return next((path for path in candidates if os.path.exists(path)), None)


def shell_folder(name: str, fallback: str) -> str:
    if os.name == "nt":
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", f"[Environment]::GetFolderPath('{name}')"], capture_output=True, text=True, check=True)
            return result.stdout.strip() or fallback
        except (OSError, subprocess.CalledProcessError):
            pass
    return fallback


class Wizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"Sapphire Setup  /  v{VERSION}")
        self.geometry("900x650")
        self.minsize(780, 570)
        self.configure(bg=PALETTE["canvas"])
        self.target = tk.StringVar(value=os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "SapphireLang"))
        self.add_path = tk.BooleanVar(value=True)
        self.add_shortcuts = tk.BooleanVar(value=True)
        self.install_docs = tk.BooleanVar(value=True)
        self.launch_studio = tk.BooleanVar(value=True)
        self.page = 0
        self._header()
        self._content()
        self._footer()
        self.show_page(0)

    def _header(self):
        header = tk.Frame(self, bg=PALETTE["header"], height=100)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="◆", font=("Segoe UI Symbol", 36, "bold"), fg=PALETTE["mint"], bg=PALETTE["header"]).pack(side="left", padx=(30, 14))
        title = tk.Frame(header, bg=PALETTE["header"])
        title.pack(side="left", pady=19)
        tk.Label(title, text="SAPPHIRE", font=("Segoe UI", 22, "bold"), fg="#F4FFF8", bg=PALETTE["header"]).pack(anchor="w")
        tk.Label(title, text="WINDOWS DEVELOPMENT RUNTIME", font=("Segoe UI", 9, "bold"), fg="#A9EBC5", bg=PALETTE["header"]).pack(anchor="w")
        tk.Label(header, text=f"v{VERSION}", font=("Segoe UI", 11, "bold"), fg=PALETTE["mint"], bg=PALETTE["header"]).pack(side="right", padx=30)

    def _content(self):
        self.content = tk.Frame(self, bg=PALETTE["canvas"])
        self.content.pack(fill="both", expand=True, padx=44, pady=28)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)
        self.step_label = tk.Label(self.content, font=("Segoe UI", 9, "bold"), fg=PALETTE["mint_dark"], bg=PALETTE["canvas"])
        self.step_label.grid(row=0, column=0, sticky="w", pady=(0, 12))
        self.stage = tk.Frame(self.content, bg=PALETTE["canvas"])
        self.stage.grid(row=1, column=0, sticky="nsew")

    def _footer(self):
        footer = tk.Frame(self, bg=PALETTE["soft"], height=72)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        self.back = tk.Button(footer, text="Back", font=("Segoe UI", 10), fg=PALETTE["ink"], bg=PALETTE["line"], bd=0, padx=22, pady=9, command=self.back_page)
        self.back.pack(side="left", padx=34, pady=15)
        self.next = tk.Button(footer, text="Continue", font=("Segoe UI", 10, "bold"), fg="#042615", bg=PALETTE["mint"], activebackground="#7AF2B4", bd=0, padx=28, pady=9, command=self.next_page)
        self.next.pack(side="right", padx=34, pady=15)

    def clear_stage(self):
        for widget in self.stage.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=10, color=None, bold=False):
        return tk.Label(parent, text=text, font=("Segoe UI", size, "bold" if bold else "normal"), fg=color or PALETTE["ink"], bg=PALETTE["canvas"])

    def show_page(self, page):
        self.page = page
        self.clear_stage()
        self.step_label.config(text=f"STEP {page + 1} OF 3   /   {'WELCOME' if page == 0 else 'INSTALL LOCATION' if page == 1 else 'READY TO INSTALL'}")
        if page == 0:
            self.label(self.stage, "Build your Sapphire workspace", 24, PALETTE["mint_dark"], True).pack(anchor="w", pady=(0, 5))
            self.label(self.stage, "A clean local runtime for scripts, AI integrations, ML experiments, and Emerald Studio.", 11, PALETTE["muted"]).pack(anchor="w", pady=(0, 22))
            card = tk.Frame(self.stage, bg=PALETTE["surface"], highlightbackground=PALETTE["line"], highlightthickness=1)
            card.pack(fill="x", pady=5)
            self.label(card, "Included in this installation", 12, PALETTE["mint_dark"], True).pack(anchor="w", padx=22, pady=(18, 10))
            for item in ("Sapphire interpreter, CLI, and .sp file association", "Emerald Studio and compiler tools", "Optional PyTorch/CUDA-compatible ML integration", "Current manuals, examples, benchmarks, and transparency notes"):
                tk.Label(card, text=f"◆  {item}", font=("Segoe UI", 10), fg=PALETTE["ink"], bg=PALETTE["surface"]).pack(anchor="w", padx=22, pady=4)
            tk.Label(card, text="The installer does not install Python, PyTorch, NVIDIA drivers, or AI credentials.", font=("Segoe UI", 9, "italic"), fg=PALETTE["muted"], bg=PALETTE["surface"]).pack(anchor="w", padx=22, pady=(14, 18))
        elif page == 1:
            self.label(self.stage, "Choose an installation location", 22, PALETTE["mint_dark"], True).pack(anchor="w", pady=(0, 5))
            self.label(self.stage, "The runtime and tools will be copied here.", 11, PALETTE["muted"]).pack(anchor="w", pady=(0, 20))
            card = tk.Frame(self.stage, bg=PALETTE["surface"], highlightbackground=PALETTE["line"], highlightthickness=1)
            card.pack(fill="x", pady=5)
            self.label(card, "INSTALL LOCATION", 9, PALETTE["muted"], True).pack(anchor="w", padx=22, pady=(20, 6))
            row = tk.Frame(card, bg=PALETTE["surface"])
            row.pack(fill="x", padx=22, pady=(0, 20))
            tk.Entry(row, textvariable=self.target, font=("Consolas", 10), fg=PALETTE["ink"], bg="#FFFFFF", relief="solid", bd=1).pack(side="left", fill="x", expand=True, ipady=8)
            tk.Button(row, text="Browse", font=("Segoe UI", 9, "bold"), fg="#042615", bg=PALETTE["mint"], bd=0, padx=15, pady=8, command=self.browse).pack(side="right", padx=(10, 0))
            for text, variable in (("Add Sapphire to User PATH", self.add_path), ("Create Desktop and Start Menu shortcuts", self.add_shortcuts), ("Install current manuals", self.install_docs)):
                tk.Checkbutton(card, text=text, variable=variable, font=("Segoe UI", 10), fg=PALETTE["ink"], bg=PALETTE["surface"], selectcolor=PALETTE["soft"], activebackground=PALETTE["surface"]).pack(anchor="w", padx=22, pady=3)
        else:
            self.label(self.stage, "Ready to install Sapphire", 22, PALETTE["mint_dark"], True).pack(anchor="w", pady=(0, 5))
            self.label(self.stage, "Review the destination, then select Install Sapphire.", 11, PALETTE["muted"]).pack(anchor="w", pady=(0, 20))
            card = tk.Frame(self.stage, bg=PALETTE["surface"], highlightbackground=PALETTE["line"], highlightthickness=1)
            card.pack(fill="x", pady=5)
            tk.Label(card, text="DESTINATION", font=("Segoe UI", 9, "bold"), fg=PALETTE["muted"], bg=PALETTE["surface"]).pack(anchor="w", padx=22, pady=(20, 3))
            tk.Label(card, textvariable=self.target, font=("Consolas", 11), fg=PALETTE["ink"], bg=PALETTE["surface"]).pack(anchor="w", padx=22, pady=(0, 18))
            tk.Label(card, text="INSTALLATION PLAN", font=("Segoe UI", 9, "bold"), fg=PALETTE["muted"], bg=PALETTE["surface"]).pack(anchor="w", padx=22, pady=(0, 5))
            tk.Label(card, text="Runtime  ·  Emerald Studio  ·  CLI  ·  Documentation  ·  File association  ·  Shortcuts", font=("Segoe UI", 10), fg=PALETTE["ink"], bg=PALETTE["surface"]).pack(anchor="w", padx=22, pady=(0, 20))
        self.back.config(state="normal" if page else "disabled")
        self.next.config(text="Install Sapphire" if page == 2 else "Continue", command=self.install if page == 2 else self.next_page)

    def browse(self):
        chosen = filedialog.askdirectory(initialdir=self.target.get())
        if chosen:
            self.target.set(chosen)

    def next_page(self):
        if self.page < 2:
            self.show_page(self.page + 1)

    def back_page(self):
        if self.page > 0:
            self.show_page(self.page - 1)

    def log(self, text):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)

    def install(self):
        self.clear_stage()
        self.step_label.config(text="INSTALLING   /   PLEASE WAIT")
        self.back.config(state="disabled")
        self.next.config(state="disabled", text="Installing...")
        self.log_box = tk.Text(self.stage, font=("Consolas", 9), fg=PALETTE["mint_dark"], bg="#FFFFFF", relief="solid", bd=1)
        self.log_box.pack(fill="both", expand=True)
        threading.Thread(target=self._install_worker, daemon=True).start()

    def _install_worker(self):
        target = os.path.abspath(self.target.get())
        try:
            os.makedirs(target, exist_ok=True)
            for name in FILES:
                source = source_path(name)
                if source:
                    destination = os.path.join(target, name)
                    if os.path.isdir(source):
                        shutil.copytree(source, destination, dirs_exist_ok=True)
                    else:
                        shutil.copy2(source, destination)
                    self.after(0, self.log, f"Installed  {name}")
            language = source_path("sapphire_lang")
            if language:
                shutil.copytree(language, os.path.join(target, "sapphire_lang"), dirs_exist_ok=True)
                self.after(0, self.log, "Installed  sapphire_lang runtime")
            for directory in ("apps", "benchmarks"):
                source_directory = source_path(directory)
                if source_directory and os.path.isdir(source_directory):
                    shutil.copytree(source_directory, os.path.join(target, directory), dirs_exist_ok=True)
                    self.after(0, self.log, f"Installed  {directory} assets")
            compiler = os.path.join(target, "Sapphire_Compiler.exe")
            icon = os.path.join(target, "Sapphire_Icon.ico")
            if os.path.exists(compiler):
                command = (
                    "$k='HKCU:\\Software\\Classes\\SapphireScript'; New-Item $k -Force | Out-Null; "
                    f"New-Item ($k+'\\DefaultIcon') -Force | Out-Null; Set-ItemProperty ($k+'\\DefaultIcon') -Name '(default)' -Value '{icon}'; "
                    "New-Item ($k+'\\shell\\open\\command') -Force | Out-Null; "
                    f"Set-ItemProperty ($k+'\\shell\\open\\command') -Name '(default)' -Value '\"{compiler}\" \"%1\"'; "
                    "New-Item 'HKCU:\\Software\\Classes\\.sp' -Force | Out-Null; Set-ItemProperty 'HKCU:\\Software\\Classes\\.sp' -Name '(default)' -Value 'SapphireScript'"
                )
                subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True)
                self.after(0, self.log, "Registered .sp file association")
            if self.add_path.get():
                command = f"$p=[Environment]::GetEnvironmentVariable('Path','User'); if($p -notlike '*{target}*'){{[Environment]::SetEnvironmentVariable('Path',$p+';{target}','User')}}"
                subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True)
                self.after(0, self.log, "Updated   User PATH")
            if self.add_shortcuts.get():
                self._shortcuts(target)
            self.after(0, self._complete)
        except Exception as error:
            self.after(0, self._failed, str(error))

    def _shortcuts(self, target):
        desktop = shell_folder("Desktop", os.path.join(os.path.expanduser("~"), "Desktop"))
        start = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "Microsoft", "Windows", "Start Menu", "Programs", "Sapphire")
        os.makedirs(desktop, exist_ok=True)
        os.makedirs(start, exist_ok=True)
        ps = "New-Object -ComObject WScript.Shell"
        for folder in (desktop, start):
            path = os.path.join(folder, "Emerald Developer Studio.lnk").replace("'", "''")
            exe = os.path.join(target, "Emerald_Studio.exe").replace("'", "''")
            command = f"$w={ps}; $s=$w.CreateShortcut('{path}'); $s.TargetPath='{exe}'; $s.WorkingDirectory='{target.replace(chr(39), chr(39)*2)}'; $s.IconLocation='{os.path.join(target, 'Emerald_Icon.ico').replace(chr(39), chr(39)*2)}'; $s.Save()"
            result = subprocess.run(["powershell", "-NoProfile", "-Command", command], capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stderr.strip() or "Shortcut creation failed")
        self.after(0, self.log, "Created   Desktop and Start Menu shortcuts")

    def _complete(self):
        self.step_label.config(text="COMPLETE   /   SAPPHIRE IS READY")
        self.log("\nInstallation completed successfully.")
        self.next.config(state="normal", text="Finish", command=self.destroy)
        self.back.config(state="disabled")

    def _failed(self, error):
        self.log(f"\nInstallation failed: {error}")
        self.next.config(state="normal", text="Close", command=self.destroy)


if __name__ == "__main__":
    Wizard().mainloop()
