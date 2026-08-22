"""
🌌 NEXUS PROGRAMMING LANGUAGE — GRAPHICAL WINDOWS SETUP WIZARD
Interactive GUI Setup Wizard for Installing Nexus Language, PATH Configuration,
Voice-Guided Tutor, PDF Documentation, and Desktop Shortcuts.
"""

import sys
import os
import shutil
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Reconfigure terminal encoding for UTF-8 compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class NexusSetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Nexus Programming Language Setup Wizard")
        self.geometry("640x480")
        self.resizable(False, False)
        self.configure(bg="#0F172A") # Dark Navy

        # Default Install Path
        default_target = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Public"), "NexusLang")
        self.install_dir = tk.StringVar(value=default_target)

        # Options
        self.opt_add_path = tk.BooleanVar(value=True)
        self.opt_tutor = tk.BooleanVar(value=True)
        self.opt_docs = tk.BooleanVar(value=True)
        self.opt_shortcuts = tk.BooleanVar(value=True)

        # Completion Actions
        self.opt_launch_tutor = tk.BooleanVar(value=True)
        self.opt_open_guide = tk.BooleanVar(value=True)

        # Styles
        self.setup_styles()

        # Frames container
        self.container = tk.Frame(self, bg="#0F172A")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        for PageClass in (WelcomePage, DirectoryPage, ProgressPage, FinishPage):
            page = PageClass(parent=self.container, controller=self)
            self.frames[PageClass] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomePage)

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TProgressbar', thickness=18, troughcolor='#1E293B', background='#2563EB')

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, 'on_show'):
            frame.on_show()

# Base Frame for Wizard Pages
class WizardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

    def create_header(self, title_text, subtitle_text):
        header_frame = tk.Frame(self, bg="#1E293B", height=70)
        header_frame.pack(fill="x", side="top")
        
        lbl_title = tk.Label(header_frame, text=title_text, font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#1E293B")
        lbl_title.pack(anchor="w", padx=20, pady=(10, 2))
        
        lbl_sub = tk.Label(header_frame, text=subtitle_text, font=("Helvetica", 9), fg="#94A3B8", bg="#1E293B")
        lbl_sub.pack(anchor="w", padx=20, pady=(0, 10))

        sep = tk.Frame(self, bg="#2563EB", height=3)
        sep.pack(fill="x")

# Page 1: Welcome Page
class WelcomePage(WizardPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header(
            "🌌 Welcome to Nexus Language Setup Wizard",
            "Installs Nexus Language Core CLI, Voice Tutor, and PDF Documentation on your PC"
        )

        content = tk.Frame(self, bg="#0F172A", padx=25, pady=20)
        content.pack(fill="both", expand=True)

        txt_info = (
            "Nexus is an autonomous-first programming language designed specifically for:\n\n"
            "• PC System Automation & Native Telemetry\n"
            "• Built-in AI Intelligence Primitives (`ai.prompt`)\n"
            "• Colorless Concurrency (`parallel { ... }` blocks)\n"
            "• Zero-Dependency Standalone Runtime\n\n"
            "This setup wizard will guide you through installing the Nexus language compiler, "
            "registering global PATH commands, installing the Voice-Guided Tutor, and setting up "
            "PDF developer manuals."
        )

        lbl_desc = tk.Label(content, text=txt_info, font=("Helvetica", 10), fg="#E2E8F0", bg="#0F172A", justify="left", wraplength=570)
        lbl_desc.pack(anchor="w", pady=10)

        # Footer Navigation
        footer = tk.Frame(self, bg="#1E293B", height=50)
        footer.pack(fill="x", side="bottom")

        btn_next = tk.Button(footer, text="Next >", font=("Helvetica", 10, "bold"), bg="#2563EB", fg="#FFFFFF", relief="flat", padx=15, pady=5, command=lambda: controller.show_frame(DirectoryPage))
        btn_next.pack(side="right", padx=20, pady=10)

        btn_cancel = tk.Button(footer, text="Cancel", font=("Helvetica", 10), bg="#334155", fg="#FFFFFF", relief="flat", padx=15, pady=5, command=controller.quit)
        btn_cancel.pack(side="right", padx=10, pady=10)

# Page 2: Options & Directory Page
class DirectoryPage(WizardPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header(
            "Select Destination & Components",
            "Choose installation folder and optional features to configure"
        )

        content = tk.Frame(self, bg="#0F172A", padx=25, pady=15)
        content.pack(fill="both", expand=True)

        # Directory Selector
        lbl_dir = tk.Label(content, text="Destination Folder:", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#0F172A")
        lbl_dir.pack(anchor="w", pady=(0, 5))

        dir_frame = tk.Frame(content, bg="#0F172A")
        dir_frame.pack(fill="x", pady=(0, 15))

        ent_dir = tk.Entry(dir_frame, textvariable=controller.install_dir, font=("Helvetica", 9), bg="#1E293B", fg="#FFFFFF", insertbackground="#FFFFFF", relief="solid", bd=1)
        ent_dir.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 10))

        btn_browse = tk.Button(dir_frame, text="Browse...", font=("Helvetica", 9), bg="#334155", fg="#FFFFFF", relief="flat", padx=10, command=self.browse_folder)
        btn_browse.pack(side="right")

        # Component Checkboxes
        lbl_comp = tk.Label(content, text="Select Components to Install:", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#0F172A")
        lbl_comp.pack(anchor="w", pady=(5, 5))

        chk_path = tk.Checkbutton(content, text="Add Nexus to System PATH (Global 'nexus' command)", variable=controller.opt_add_path, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#FFFFFF")
        chk_path.pack(anchor="w", pady=2)

        chk_tutor = tk.Checkbutton(content, text="Install Voice-Guided Interactive Tutor (`nexus_voice_tutor.exe`)", variable=controller.opt_tutor, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#FFFFFF")
        chk_tutor.pack(anchor="w", pady=2)

        self.opt_studio = tk.BooleanVar(value=True)
        chk_studio = tk.Checkbutton(content, text="Install Nexus Studio IDE (`Nexus_Studio.exe`) — VSCode-Inspired IDE", variable=self.opt_studio, font=("Helvetica", 9), fg="#38BDF8", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#FFFFFF")
        chk_studio.pack(anchor="w", pady=2)
        # Store reference on controller for install step
        controller.opt_studio = self.opt_studio

        chk_docs = tk.Checkbutton(content, text="Install PDF Developer Manuals & Benchmarks (4 PDF Files)", variable=controller.opt_docs, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#FFFFFF")
        chk_docs.pack(anchor="w", pady=2)

        chk_shortcuts = tk.Checkbutton(content, text="Create Desktop & Start Menu Shortcuts", variable=controller.opt_shortcuts, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#FFFFFF")
        chk_shortcuts.pack(anchor="w", pady=2)

        # Footer Navigation
        footer = tk.Frame(self, bg="#1E293B", height=50)
        footer.pack(fill="x", side="bottom")

        btn_install = tk.Button(footer, text="Install Now", font=("Helvetica", 10, "bold"), bg="#2563EB", fg="#FFFFFF", relief="flat", padx=15, pady=5, command=self.start_install)
        btn_install.pack(side="right", padx=20, pady=10)

        btn_back = tk.Button(footer, text="< Back", font=("Helvetica", 10), bg="#334155", fg="#FFFFFF", relief="flat", padx=15, pady=5, command=lambda: controller.show_frame(WelcomePage))
        btn_back.pack(side="right", padx=5, pady=10)

    def browse_folder(self):
        chosen = filedialog.askdirectory(initialdir=self.controller.install_dir.get())
        if chosen:
            self.controller.install_dir.set(chosen)

    def start_install(self):
        self.controller.show_frame(ProgressPage)

# Page 3: Installation Progress Page
class ProgressPage(WizardPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header(
            "Installing Nexus Language...",
            "Please wait while files and settings are being configured"
        )

        content = tk.Frame(self, bg="#0F172A", padx=25, pady=40)
        content.pack(fill="both", expand=True)

        self.lbl_status = tk.Label(content, text="Preparing installation...", font=("Helvetica", 10), fg="#E2E8F0", bg="#0F172A")
        self.lbl_status.pack(anchor="w", pady=(0, 10))

        self.progress = ttk.Progressbar(content, orient="horizontal", mode="determinate", style="TProgressbar")
        self.progress.pack(fill="x", pady=10)

        self.lbl_detail = tk.Label(content, text="", font=("Helvetica", 9), fg="#94A3B8", bg="#0F172A")
        self.lbl_detail.pack(anchor="w", pady=5)

    def on_show(self):
        threading.Thread(target=self.run_installation, daemon=True).start()

    def run_installation(self):
        target = self.controller.install_dir.get()
        os.makedirs(target, exist_ok=True)

        steps = [
            ("Copying Nexus Core CLI Binary (nexus.exe)...", 20),
            ("Copying Voice Tutor Binary (nexus_voice_tutor.exe)...", 35),
            ("Copying Nexus Studio IDE (Nexus_Studio.exe)...", 50),
            ("Copying PDF Documentation Manuals...", 60),
            ("Configuring Windows PATH Environment...", 80),
            ("Generating Desktop & Start Menu Shortcuts...", 100)
        ]

        # 1. Copy Files
        self.update_status("Copying Nexus Executables...", 15, "Target: " + target)
        for fname in ["nexus.exe", "nexus_voice_tutor.exe", "nexus_tutor.exe", "nexus_cli.py", "nexus_voice_tutor.py", "nexus_tutor.py", "nexus_tutor.bat", "nexus_voice_tutor.bat"]:
            src_path = os.path.join(BASE_DIR, fname)
            if os.path.exists(src_path):
                shutil.copy2(src_path, os.path.join(target, fname))

        # Copy Nexus Studio if selected
        if getattr(self.controller, 'opt_studio', None) and self.controller.opt_studio.get():
            self.update_status("Copying Nexus Studio IDE...", 40, "Installing Nexus_Studio.exe")
            for fname in ["Nexus_Studio.exe", "nexus_studio.py"]:
                src_path = os.path.join(BASE_DIR, fname)
                if os.path.exists(src_path):
                    shutil.copy2(src_path, os.path.join(target, fname))

        # Copy Docs
        self.update_status("Copying PDF Developer Manuals...", 55, "Copying PDF documentation")
        for pdf_file in ["Nexus_Coding_and_Usage_Guide.pdf", "Building_Advanced_Autonomous_AI.pdf", "Nexus_Autonomy_and_Performance_Benchmarks.pdf", "Beginners_Guide_Your_First_Autonomous_AI.pdf", "INSTALLATION_AND_USAGE_GUIDE.md"]:
            src_path = os.path.join(BASE_DIR, pdf_file)
            if os.path.exists(src_path):
                shutil.copy2(src_path, os.path.join(target, pdf_file))

        # Copy stdlib folder
        src_nexus_lang = os.path.join(BASE_DIR, "nexus_lang")
        if os.path.exists(src_nexus_lang):
            dst_nexus_lang = os.path.join(target, "nexus_lang")
            if os.path.exists(dst_nexus_lang):
                shutil.rmtree(dst_nexus_lang, ignore_errors=True)
            shutil.copytree(src_nexus_lang, dst_nexus_lang)

        # 2. Configure PATH
        if self.controller.opt_add_path.get():
            self.update_status("Registering Nexus in System PATH...", 70, "Executing PowerShell PATH script")
            try:
                ps_cmd = f"$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($oldPath -notlike '*{target}*') {{ [Environment]::SetEnvironmentVariable('Path', $oldPath + ';{target}', 'User') }}"
                subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
            except Exception:
                pass

        # 3. Create Shortcuts
        if self.controller.opt_shortcuts.get():
            self.update_status("Creating Shortcuts...", 90, "Writing Desktop shortcuts")
            try:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                tutor_exe = os.path.join(target, "nexus_voice_tutor.exe")
                if os.path.exists(tutor_exe) and os.path.exists(desktop):
                    ps_shortcut = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{os.path.join(desktop, 'Nexus Voice Tutor.lnk')}'); $s.TargetPath='{tutor_exe}'; $s.WorkingDirectory='{target}'; $s.Save()"
                    subprocess.run(["powershell", "-Command", ps_shortcut], capture_output=True)
                studio_exe = os.path.join(target, "Nexus_Studio.exe")
                if os.path.exists(studio_exe) and os.path.exists(desktop):
                    ps_shortcut2 = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{os.path.join(desktop, 'Nexus Studio.lnk')}'); $s.TargetPath='{studio_exe}'; $s.WorkingDirectory='{target}'; $s.Save()"
                    subprocess.run(["powershell", "-Command", ps_shortcut2], capture_output=True)
            except Exception:
                pass

        self.update_status("Installation Completed Successfully!", 100, "All items configured.")
        time.sleep(0.5)
        self.controller.after(0, lambda: self.controller.show_frame(FinishPage))

    def update_status(self, text, val, detail=""):
        self.controller.after(0, lambda: self.lbl_status.config(text=text))
        self.controller.after(0, lambda: self.progress.config(value=val))
        self.controller.after(0, lambda: self.lbl_detail.config(text=detail))

# Page 4: Finish Page
class FinishPage(WizardPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_header(
            "🎉 Nexus Setup Wizard Completed!",
            "Nexus Programming Language has been successfully installed on your PC"
        )

        content = tk.Frame(self, bg="#0F172A", padx=25, pady=20)
        content.pack(fill="both", expand=True)

        lbl_congrats = tk.Label(
            content,
            text="Nexus core compiler, Nexus Studio IDE, voice tutor, and developer manuals are ready to use.",
            font=("Helvetica", 10), fg="#E2E8F0", bg="#0F172A"
        )
        lbl_congrats.pack(anchor="w", pady=(0, 15))

        # Checkboxes for launch actions
        self.opt_launch_studio = tk.BooleanVar(value=True)
        chk_studio = tk.Checkbutton(
            content, text="🖥️  Launch Nexus Studio IDE Now  (VSCode-Inspired IDE)",
            variable=self.opt_launch_studio, font=("Helvetica", 10, "bold"),
            fg="#38BDF8", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#38BDF8"
        )
        chk_studio.pack(anchor="w", pady=5)

        chk_launch = tk.Checkbutton(
            content, text="Launch Voice-Guided Interactive Tutor Now",
            variable=controller.opt_launch_tutor, font=("Helvetica", 10, "bold"),
            fg="#38BDF8", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#38BDF8"
        )
        chk_launch.pack(anchor="w", pady=5)

        chk_pdf = tk.Checkbutton(
            content, text="Open Beginner's Autonomous AI PDF Guide",
            variable=controller.opt_open_guide, font=("Helvetica", 9),
            fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A", activeforeground="#FFFFFF"
        )
        chk_pdf.pack(anchor="w", pady=5)

        lbl_path_note = tk.Label(
            content,
            text="Note: Open any new Command Prompt and type 'nexus info', 'nexus studio', or 'nexus run file.nx'.",
            font=("Helvetica", 9, "italic"), fg="#94A3B8", bg="#0F172A"
        )
        lbl_path_note.pack(anchor="w", pady=(20, 0))

        # Footer Navigation
        footer = tk.Frame(self, bg="#1E293B", height=50)
        footer.pack(fill="x", side="bottom")

        btn_finish = tk.Button(footer, text="Finish", font=("Helvetica", 10, "bold"), bg="#2563EB", fg="#FFFFFF", relief="flat", padx=20, pady=5, command=self.finish_action)
        btn_finish.pack(side="right", padx=20, pady=10)

    def finish_action(self):
        target = self.controller.install_dir.get()
        if self.opt_launch_studio.get():
            studio_exe = os.path.join(target, "Nexus_Studio.exe")
            if os.path.exists(studio_exe):
                subprocess.Popen([studio_exe], cwd=target)

        if self.controller.opt_launch_tutor.get():
            tutor_exe = os.path.join(target, "nexus_voice_tutor.exe")
            if os.path.exists(tutor_exe):
                subprocess.Popen([tutor_exe], cwd=target)

        if self.controller.opt_open_guide.get():
            pdf_path = os.path.join(target, "Beginners_Guide_Your_First_Autonomous_AI.pdf")
            if os.path.exists(pdf_path):
                os.startfile(pdf_path)

        self.controller.quit()

if __name__ == "__main__":
    app = NexusSetupWizard()
    app.mainloop()
