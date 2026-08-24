"""
💎 SAPPHIRE PROGRAMMING LANGUAGE — GRAPHICAL WINDOWS SETUP WIZARD
Interactive GUI Setup Wizard for Installing Sapphire Language, Emerald Developer Studio,
PATH Configuration, GPU/ML Stack, PDF Documentation, and Desktop Shortcuts.
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

class SapphireSetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💎 Sapphire Programming Language & Emerald Studio Setup Wizard")
        self.geometry("660x500")
        self.resizable(False, False)
        self.configure(bg="#0F172A") # Dark Navy

        # Default Install Path
        default_target = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Public"), "SapphireLang")
        self.install_dir = tk.StringVar(value=default_target)

        # Options
        self.opt_add_path = tk.BooleanVar(value=True)
        self.opt_studio = tk.BooleanVar(value=True)
        self.opt_docs = tk.BooleanVar(value=True)
        self.opt_shortcuts = tk.BooleanVar(value=True)

        # Completion Actions
        self.opt_launch_studio = tk.BooleanVar(value=True)
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
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#0F172A")
        self.style.configure("Header.TLabel", font=("Helvetica", 16, "bold"), foreground="#38BDF8", background="#0F172A")
        self.style.configure("SubHeader.TLabel", font=("Helvetica", 10), foreground="#94A3B8", background="#0F172A")
        self.style.configure("TCheckbutton", font=("Helvetica", 10), foreground="#E2E8F0", background="#0F172A")

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()


class WelcomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        # Title
        lbl_title = tk.Label(self, text="💎 Sapphire Programming Language v1.0.0", font=("Helvetica", 15, "bold"), fg="#38BDF8", bg="#0F172A")
        lbl_title.pack(anchor="w", padx=30, pady=(25, 5))

        lbl_sub = tk.Label(self, text="Autonomous AI/ML Programming Language & Emerald Developer Studio", font=("Helvetica", 10), fg="#10B981", bg="#0F172A")
        lbl_sub.pack(anchor="w", padx=30, pady=(0, 15))

        # Description
        desc_text = (
            "Welcome to the official Windows Setup Wizard for Sapphire.\n\n"
            "This installer will configure:\n"
            "  • Sapphire Core Language Engine (.sp scripts & REPL)\n"
            "  • Emerald Developer Studio GUI (IDE, Tool Builder & Hardware Dashboard)\n"
            "  • Sapphire Deep Learning & Tensor Stack (ml, autograd, GPU/TPU)\n"
            "  • Sapphire Agent Architecture (memory, planning, tools, autonomy)\n"
            "  • System PATH Environment Registration & PDF Documentation"
        )
        lbl_desc = tk.Label(self, text=desc_text, font=("Helvetica", 9), fg="#CBD5E1", bg="#1E293B", justify="left", anchor="nw", padx=15, pady=12, relief="solid", bd=1)
        lbl_desc.pack(fill="x", padx=30, pady=5)

        # Options Checkboxes
        opts_frame = tk.Frame(self, bg="#0F172A")
        opts_frame.pack(fill="x", padx=30, pady=10)

        chk_path = tk.Checkbutton(opts_frame, text="Register Sapphire in System PATH", variable=controller.opt_add_path, font=("Helvetica", 9.5), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_path.pack(anchor="w", pady=2)

        chk_studio = tk.Checkbutton(opts_frame, text="Install Emerald Developer Studio GUI (emerald_studio.py)", variable=controller.opt_studio, font=("Helvetica", 9.5), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_studio.pack(anchor="w", pady=2)

        chk_docs = tk.Checkbutton(opts_frame, text="Include PDF Developer & AI Manuals", variable=controller.opt_docs, font=("Helvetica", 9.5), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_docs.pack(anchor="w", pady=2)

        chk_short = tk.Checkbutton(opts_frame, text="Create Desktop & Start Menu Shortcuts", variable=controller.opt_shortcuts, font=("Helvetica", 9.5), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_short.pack(anchor="w", pady=2)

        # Bottom Bar
        btm = tk.Frame(self, bg="#0F172A")
        btm.pack(fill="x", side="bottom", padx=30, pady=20)

        btn_next = tk.Button(btm, text="Next >", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#2563EB", activebackground="#1D4ED8", activeforeground="#FFFFFF", bd=0, padx=20, pady=6, command=lambda: controller.show_frame(DirectoryPage))
        btn_next.pack(side="right")


class DirectoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        lbl_title = tk.Label(self, text="Select Destination Folder", font=("Helvetica", 14, "bold"), fg="#38BDF8", bg="#0F172A")
        lbl_title.pack(anchor="w", padx=30, pady=(25, 5))

        lbl_sub = tk.Label(self, text="Choose where Sapphire Language and Emerald Studio will be installed.", font=("Helvetica", 9), fg="#94A3B8", bg="#0F172A")
        lbl_sub.pack(anchor="w", padx=30, pady=(0, 20))

        # Folder Selection
        box_frame = tk.Frame(self, bg="#1E293B", padx=15, pady=15)
        box_frame.pack(fill="x", padx=30, pady=10)

        lbl_dir = tk.Label(box_frame, text="Install Location:", font=("Helvetica", 9.5, "bold"), fg="#E2E8F0", bg="#1E293B")
        lbl_dir.pack(anchor="w", pady=(0, 5))

        entry_frame = tk.Frame(box_frame, bg="#1E293B")
        entry_frame.pack(fill="x")

        ent_path = tk.Entry(entry_frame, textvariable=controller.install_dir, font=("Consolas", 10), bg="#0F172A", fg="#F8FAFC", bd=1)
        ent_path.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse = tk.Button(entry_frame, text="Browse...", font=("Helvetica", 9), fg="#FFFFFF", bg="#334155", activebackground="#475569", activeforeground="#FFFFFF", bd=0, padx=12, pady=4, command=self.browse)
        btn_browse.pack(side="right")

        # Bottom Bar
        btm = tk.Frame(self, bg="#0F172A")
        btm.pack(fill="x", side="bottom", padx=30, pady=20)

        btn_next = tk.Button(btm, text="Install Now", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#16A34A", activebackground="#15803D", activeforeground="#FFFFFF", bd=0, padx=20, pady=6, command=lambda: controller.show_frame(ProgressPage))
        btn_next.pack(side="right")

        btn_back = tk.Button(btm, text="< Back", font=("Helvetica", 10), fg="#E2E8F0", bg="#334155", activebackground="#475569", activeforeground="#FFFFFF", bd=0, padx=15, pady=6, command=lambda: controller.show_frame(WelcomePage))
        btn_back.pack(side="right", padx=10)

    def browse(self):
        target = filedialog.askdirectory(initialdir=self.controller.install_dir.get())
        if target:
            self.controller.install_dir.set(target)


class ProgressPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        lbl_title = tk.Label(self, text="Installing Sapphire...", font=("Helvetica", 14, "bold"), fg="#38BDF8", bg="#0F172A")
        lbl_title.pack(anchor="w", padx=30, pady=(30, 5))

        self.lbl_status = tk.Label(self, text="Preparing installation...", font=("Helvetica", 9.5), fg="#94A3B8", bg="#0F172A")
        self.lbl_status.pack(anchor="w", padx=30, pady=(0, 15))

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", mode="determinate", length=580)
        self.progress.pack(padx=30, pady=10)

        # Log output
        self.log_box = tk.Text(self, font=("Consolas", 8.5), bg="#1E293B", fg="#38BDF8", bd=1, height=12)
        self.log_box.pack(fill="x", padx=30, pady=15)

    def on_show(self):
        threading.Thread(target=self.do_install, daemon=True).start()

    def update_status(self, text, val, log=None):
        self.lbl_status.config(text=text)
        self.progress["value"] = val
        if log:
            self.log_box.insert(tk.END, log + "\n")
            self.log_box.see(tk.END)
        self.update_idletasks()

    def do_install(self):
        target = self.controller.install_dir.get()
        os.makedirs(target, exist_ok=True)

        # 1. Copy Files
        self.update_status("Copying Sapphire Core & Studio Files...", 15, "Target: " + target)
        for fname in ["sapphire.exe", "nexus.exe", "emerald_studio.py", "sapphire_studio.py", "nexus_cli.py", "nexus_voice_tutor.exe", "nexus_tutor.exe", "nexus_voice_tutor.py", "nexus_tutor.py"]:
            src_path = os.path.join(BASE_DIR, fname)
            if os.path.exists(src_path):
                shutil.copy2(src_path, os.path.join(target, fname))

        # Copy Docs
        self.update_status("Copying PDF Developer Manuals...", 45, "Copying PDF documentation")
        for pdf_file in ["Nexus_Coding_and_Usage_Guide.pdf", "Building_Advanced_Autonomous_AI.pdf", "Nexus_Autonomy_and_Performance_Benchmarks.pdf", "Beginners_Guide_Your_First_Autonomous_AI.pdf", "INSTALLATION_AND_USAGE_GUIDE.md"]:
            src_path = os.path.join(BASE_DIR, pdf_file)
            if not os.path.exists(src_path):
                src_path = os.path.join(BASE_DIR, "docs", pdf_file)
            if os.path.exists(src_path):
                shutil.copy2(src_path, os.path.join(target, pdf_file))

        # Copy stdlib folder
        src_nexus_lang = os.path.join(BASE_DIR, "nexus_lang")
        if os.path.exists(src_nexus_lang):
            dst_nexus_lang = os.path.join(target, "nexus_lang")
            if os.path.exists(dst_nexus_lang):
                shutil.rmtree(dst_nexus_lang, ignore_errors=True)
            shutil.copytree(src_nexus_lang, dst_nexus_lang)
            self.log_box.insert(tk.END, "Copied Sapphire ML, Agent, and Stdlib engine.\n")

        # 2. Configure PATH
        if self.controller.opt_add_path.get():
            self.update_status("Registering Sapphire in System PATH...", 70, "Executing PowerShell PATH script")
            try:
                ps_cmd = f"$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($oldPath -notlike '*{target}*') {{ [Environment]::SetEnvironmentVariable('Path', $oldPath + ';{target}', 'User') }}"
                subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
                self.log_box.insert(tk.END, "PATH variable updated.\n")
            except Exception as e:
                self.log_box.insert(tk.END, f"PATH error: {e}\n")

        # 3. Create Shortcuts
        if self.controller.opt_shortcuts.get():
            self.update_status("Creating Desktop Shortcuts...", 90, "Generating Shortcuts")
            try:
                desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
                studio_script = os.path.join(target, "emerald_studio.py")
                
                # PowerShell VBS shortcut helper
                vbs_cmd = f'''
                $ws = New-Object -ComObject WScript.Shell
                $s = $ws.CreateShortcut("{desktop}\\Emerald Developer Studio.lnk")
                $s.TargetPath = "python.exe"
                $s.Arguments = '"{studio_script}"'
                $s.WorkingDirectory = "{target}"
                $s.Save()
                '''
                subprocess.run(["powershell", "-Command", vbs_cmd], capture_output=True)
                self.log_box.insert(tk.END, "Desktop shortcuts generated.\n")
            except Exception as e:
                self.log_box.insert(tk.END, f"Shortcut notice: {e}\n")

        self.update_status("Installation Complete!", 100, "Installation finished successfully.")
        time.sleep(0.5)
        self.controller.show_frame(FinishPage)


class FinishPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        lbl_title = tk.Label(self, text="🎉 Sapphire Installation Complete!", font=("Helvetica", 16, "bold"), fg="#10B981", bg="#0F172A")
        lbl_title.pack(anchor="w", padx=30, pady=(35, 5))

        lbl_sub = tk.Label(self, text="Sapphire Language & Emerald Developer Studio are ready to use.", font=("Helvetica", 10), fg="#CBD5E1", bg="#0F172A")
        lbl_sub.pack(anchor="w", padx=30, pady=(0, 20))

        box_frame = tk.Frame(self, bg="#1E293B", padx=15, pady=15)
        box_frame.pack(fill="x", padx=30, pady=10)

        chk_launch = tk.Checkbutton(box_frame, text="Launch Emerald Developer Studio GUI Now", variable=controller.opt_launch_studio, font=("Helvetica", 10, "bold"), fg="#38BDF8", bg="#1E293B", selectcolor="#0F172A", activebackground="#1E293B")
        chk_launch.pack(anchor="w", pady=4)

        chk_guide = tk.Checkbutton(box_frame, text="Open Sapphire Documentation & AI Manual", variable=controller.opt_open_guide, font=("Helvetica", 9.5), fg="#F8FAFC", bg="#1E293B", selectcolor="#0F172A", activebackground="#1E293B")
        chk_guide.pack(anchor="w", pady=4)

        # Command Reference summary
        lbl_cmd = tk.Label(box_frame, text="\nTerminal Commands: 'sapphire run script.sp' | 'sapphire studio' | 'sapphire info'", font=("Consolas", 8.5), fg="#94A3B8", bg="#1E293B")
        lbl_cmd.pack(anchor="w")

        # Bottom Bar
        btm = tk.Frame(self, bg="#0F172A")
        btm.pack(fill="x", side="bottom", padx=30, pady=20)

        btn_finish = tk.Button(btm, text="Finish", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#2563EB", activebackground="#1D4ED8", activeforeground="#FFFFFF", bd=0, padx=25, pady=6, command=self.finish)
        btn_finish.pack(side="right")

    def finish(self):
        target = self.controller.install_dir.get()
        
        if self.controller.opt_launch_studio.get():
            studio_py = os.path.join(target, "emerald_studio.py")
            if os.path.exists(studio_py):
                subprocess.Popen([sys.executable, studio_py], cwd=target)

        if self.controller.opt_open_guide.get():
            pdf_path = os.path.join(target, "Beginners_Guide_Your_First_Autonomous_AI.pdf")
            if os.path.exists(pdf_path):
                os.startfile(pdf_path)

        self.controller.quit()

if __name__ == "__main__":
    app = SapphireSetupWizard()
    app.mainloop()
