"""
💎 SAPPHIRE PROGRAMMING LANGUAGE — GRAPHICAL WINDOWS SETUP WIZARD
Interactive GUI Setup Wizard for Installing Sapphire Language, Emerald Developer Studio,
Polymorphic Compiler Studio, PATH Configuration, GPU/ML Stack, PDF Documentation,
Uninstaller, and Desktop Shortcuts.
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

def find_source_item(name: str):
    """Finds an asset file/directory across PyInstaller temp bundles, exe directory, and workspace."""
    candidates = []
    # 1. PyInstaller _MEIPASS temp extraction folder
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        candidates.append(os.path.join(sys._MEIPASS, name))
        candidates.append(os.path.join(sys._MEIPASS, "docs", name))
    
    # 2. Directory where the setup wizard .exe is running from
    if getattr(sys, 'frozen', False) and sys.executable:
        exe_dir = os.path.dirname(sys.executable)
        candidates.append(os.path.join(exe_dir, name))
        candidates.append(os.path.join(exe_dir, "docs", name))

    # 3. Source script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(script_dir, name))
    candidates.append(os.path.join(script_dir, "docs", name))

    # 4. Current working directory
    candidates.append(os.path.join(os.getcwd(), name))
    candidates.append(os.path.join(os.getcwd(), "docs", name))

    for p in candidates:
        if os.path.exists(p):
            return p
    return None

class SapphireSetupWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💎 Sapphire Programming Language & Emerald Studio Setup Wizard")
        self.geometry("700x580")
        self.minsize(680, 540)
        self.resizable(True, True)
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

        # 1. BOTTOM BAR (Packed first so it is ALWAYS anchored and visible)
        btm = tk.Frame(self, bg="#0A0F1D", height=60)
        btm.pack(fill="x", side="bottom")

        sep = tk.Frame(btm, bg="#334155", height=1)
        sep.pack(fill="x", side="top")

        btn_inner = tk.Frame(btm, bg="#0A0F1D")
        btn_inner.pack(fill="x", padx=30, pady=12)

        btn_next = tk.Button(
            btn_inner, text="Next >", font=("Helvetica", 10, "bold"),
            fg="#FFFFFF", bg="#2563EB", activebackground="#1D4ED8", activeforeground="#FFFFFF",
            bd=0, padx=24, pady=7, cursor="hand2", command=lambda: controller.show_frame(DirectoryPage)
        )
        btn_next.pack(side="right")

        btn_cancel = tk.Button(
            btn_inner, text="Cancel", font=("Helvetica", 10),
            fg="#94A3B8", bg="#1E293B", activebackground="#334155", activeforeground="#FFFFFF",
            bd=0, padx=16, pady=7, cursor="hand2", command=controller.quit
        )
        btn_cancel.pack(side="right", padx=10)

        # 2. MAIN CONTENT (Scrollable/Padded)
        content = tk.Frame(self, bg="#0F172A")
        content.pack(fill="both", expand=True, padx=30, pady=(20, 10))

        # Title
        lbl_title = tk.Label(content, text="💎 Sapphire Programming Language v1.0.0", font=("Helvetica", 15, "bold"), fg="#38BDF8", bg="#0F172A")
        lbl_title.pack(anchor="w", pady=(0, 2))

        lbl_sub = tk.Label(content, text="Autonomous AI/ML Programming Language, Emerald Studio & Polymorphic Compiler", font=("Helvetica", 10), fg="#10B981", bg="#0F172A")
        lbl_sub.pack(anchor="w", pady=(0, 10))

        # Description
        desc_text = (
            "Welcome to the official Windows Setup Wizard for Sapphire.\n\n"
            "This installer will configure:\n"
            "  • Sapphire Core Language Engine (.sp scripts & REPL)\n"
            "  • Emerald Developer Studio GUI (IDE, Tool Builder & Hardware Dashboard)\n"
            "  • Sapphire Polymorphic Compiler & JIT Studio (AST, IR, Bytecode, EXE bundler)\n"
            "  • Sapphire Deep Learning & Tensor Stack (ml, autograd, GPU/TPU)\n"
            "  • Sapphire Agent Architecture (memory, planning, tools, autonomy)\n"
            "  • Interactive Voice-Guided Tutor with Q&A Mode\n"
            "  • Sapphire Uninstaller (uninstall.exe)\n"
            "  • System PATH Environment Registration & PDF Documentation Suite"
        )
        lbl_desc = tk.Label(content, text=desc_text, font=("Helvetica", 9), fg="#CBD5E1", bg="#1E293B", justify="left", anchor="nw", padx=14, pady=8, relief="solid", bd=1)
        lbl_desc.pack(fill="x", pady=(0, 10))

        # Options Checkboxes
        opts_frame = tk.Frame(content, bg="#0F172A")
        opts_frame.pack(fill="x")

        chk_path = tk.Checkbutton(opts_frame, text="Register Sapphire in System PATH", variable=controller.opt_add_path, font=("Helvetica", 10), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_path.pack(anchor="w", pady=1)

        chk_studio = tk.Checkbutton(opts_frame, text="Install Emerald Developer Studio & Compiler Binaries", variable=controller.opt_studio, font=("Helvetica", 10), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_studio.pack(anchor="w", pady=1)

        chk_docs = tk.Checkbutton(opts_frame, text="Include Full 5-Manual PDF Documentation Suite", variable=controller.opt_docs, font=("Helvetica", 10), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_docs.pack(anchor="w", pady=1)

        chk_short = tk.Checkbutton(opts_frame, text="Create Desktop & Start Menu Shortcuts", variable=controller.opt_shortcuts, font=("Helvetica", 10), fg="#F8FAFC", bg="#0F172A", selectcolor="#1E293B", activebackground="#0F172A")
        chk_short.pack(anchor="w", pady=1)


class DirectoryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        # 1. BOTTOM BAR
        btm = tk.Frame(self, bg="#0A0F1D", height=60)
        btm.pack(fill="x", side="bottom")

        sep = tk.Frame(btm, bg="#334155", height=1)
        sep.pack(fill="x", side="top")

        btn_inner = tk.Frame(btm, bg="#0A0F1D")
        btn_inner.pack(fill="x", padx=30, pady=12)

        btn_next = tk.Button(
            btn_inner, text="Install Now", font=("Helvetica", 10, "bold"),
            fg="#FFFFFF", bg="#16A34A", activebackground="#15803D", activeforeground="#FFFFFF",
            bd=0, padx=22, pady=7, cursor="hand2", command=lambda: controller.show_frame(ProgressPage)
        )
        btn_next.pack(side="right")

        btn_back = tk.Button(
            btn_inner, text="< Back", font=("Helvetica", 10),
            fg="#E2E8F0", bg="#334155", activebackground="#475569", activeforeground="#FFFFFF",
            bd=0, padx=16, pady=7, cursor="hand2", command=lambda: controller.show_frame(WelcomePage)
        )
        btn_back.pack(side="right", padx=10)

        # 2. MAIN CONTENT
        content = tk.Frame(self, bg="#0F172A")
        content.pack(fill="both", expand=True, padx=30, pady=(20, 10))

        lbl_title = tk.Label(content, text="Select Destination Folder", font=("Helvetica", 14, "bold"), fg="#38BDF8", bg="#0F172A")
        lbl_title.pack(anchor="w", pady=(0, 5))

        lbl_sub = tk.Label(content, text="Choose where Sapphire Language, Tools, and Studio will be installed.", font=("Helvetica", 9), fg="#94A3B8", bg="#0F172A")
        lbl_sub.pack(anchor="w", pady=(0, 20))

        box_frame = tk.Frame(content, bg="#1E293B", padx=15, pady=15, relief="solid", bd=1)
        box_frame.pack(fill="x", pady=10)

        lbl_dir = tk.Label(box_frame, text="Install Location:", font=("Helvetica", 10, "bold"), fg="#E2E8F0", bg="#1E293B")
        lbl_dir.pack(anchor="w", pady=(0, 5))

        entry_frame = tk.Frame(box_frame, bg="#1E293B")
        entry_frame.pack(fill="x")

        ent_path = tk.Entry(entry_frame, textvariable=controller.install_dir, font=("Consolas", 10), bg="#0F172A", fg="#F8FAFC", bd=1)
        ent_path.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse = tk.Button(entry_frame, text="Browse...", font=("Helvetica", 9), fg="#FFFFFF", bg="#334155", activebackground="#475569", activeforeground="#FFFFFF", bd=0, padx=12, pady=4, cursor="hand2", command=self.browse)
        btn_browse.pack(side="right")

    def browse(self):
        target = filedialog.askdirectory(initialdir=self.controller.install_dir.get())
        if target:
            self.controller.install_dir.set(target)


class ProgressPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        content = tk.Frame(self, bg="#0F172A")
        content.pack(fill="both", expand=True, padx=30, pady=(25, 15))

        lbl_title = tk.Label(content, text="Installing Sapphire...", font=("Helvetica", 14, "bold"), fg="#38BDF8", bg="#0F172A")
        lbl_title.pack(anchor="w", pady=(0, 5))

        self.lbl_status = tk.Label(content, text="Preparing installation...", font=("Helvetica", 10), fg="#94A3B8", bg="#0F172A")
        self.lbl_status.pack(anchor="w", pady=(0, 15))

        self.progress = ttk.Progressbar(content, orient="horizontal", mode="determinate", length=620)
        self.progress.pack(fill="x", pady=5)

        self.log_box = tk.Text(content, font=("Consolas", 9), bg="#1E293B", fg="#38BDF8", bd=1, height=14)
        self.log_box.pack(fill="both", expand=True, pady=(10, 0))

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

        # 1. Copy All Executables, Scripts, and Tools
        self.update_status("Unpacking Sapphire Binaries & Tools...", 15, f"Destination: {target}")
        
        all_binaries = [
            "sapphire.exe",
            "emerald.exe",
            "Emerald_Studio.exe",
            "Sapphire_Compiler.exe",
            "compiler.exe",
            "sapphire_voice_tutor.exe",
            "sapphire_tutor.exe",
            "uninstall_sapphire.exe",
            "uninstall.exe",
            "emerald_studio.py",
            "sapphire_studio.py",
            "sapphire_compiler.py",
            "sapphire_cli.py",
            "sapphire_voice_tutor.py",
            "sapphire_tutor.py",
            "uninstall_sapphire.py",
            "install_sapphire.bat",
        ]

        for fname in all_binaries:
            src = find_source_item(fname)
            if src and os.path.exists(src):
                shutil.copy2(src, os.path.join(target, fname))
                self.log_box.insert(tk.END, f"  ✅ Unpacked: {fname}\n")
                self.log_box.see(tk.END)
            else:
                self.log_box.insert(tk.END, f"  ⚠️ Skipped: {fname} (not found in bundle)\n")

        # 2. Copy All 5 PDF Manuals & Markdown Guides
        self.update_status("Unpacking PDF Developer Documentation...", 45, "Copying PDF documentation suite")
        all_docs = [
            "Sapphire_Coding_and_Usage_Guide.pdf",
            "Building_Advanced_Autonomous_AI.pdf",
            "Sapphire_Autonomy_and_Performance_Benchmarks.pdf",
            "Beginners_Guide_Your_First_Autonomous_AI.pdf",
            "Sapphire_Language_Specification_and_Automation_Manual.pdf",
            "INSTALLATION_AND_USAGE_GUIDE.md",
            "README.md",
        ]
        for doc_name in all_docs:
            src = find_source_item(doc_name)
            if src and os.path.exists(src):
                shutil.copy2(src, os.path.join(target, doc_name))
                self.log_box.insert(tk.END, f"  📄 Document: {doc_name}\n")
                self.log_box.see(tk.END)

        # 3. Copy sapphire_lang Core Engine
        src_lang = find_source_item("sapphire_lang")
        if src_lang and os.path.exists(src_lang):
            dst_lang = os.path.join(target, "sapphire_lang")
            if os.path.exists(dst_lang):
                shutil.rmtree(dst_lang, ignore_errors=True)
            shutil.copytree(src_lang, dst_lang)
            self.log_box.insert(tk.END, "  📦 Unpacked: sapphire_lang ML, Agent & Stdlib Engine\n")

        # 4. Configure PATH
        if self.controller.opt_add_path.get():
            self.update_status("Registering Sapphire in System PATH...", 70, "Executing PowerShell PATH registration")
            try:
                ps_cmd = f"$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); if ($oldPath -notlike '*{target}*') {{ [Environment]::SetEnvironmentVariable('Path', $oldPath + ';{target}', 'User') }}"
                subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
                self.log_box.insert(tk.END, "  ⚡ PATH updated: Added Sapphire to User PATH\n")
            except Exception as e:
                self.log_box.insert(tk.END, f"  PATH error: {e}\n")

        # 5. Create Desktop & Start Menu Shortcuts
        if self.controller.opt_shortcuts.get():
            self.update_status("Creating Desktop Shortcuts...", 90, "Generating Desktop shortcuts")
            try:
                desktop = os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Public"), "Desktop")
                
                def create_vbs_shortcut(shortcut_name, target_exe_name, fallback_script):
                    target_exe = os.path.join(target, target_exe_name)
                    script_file = os.path.join(target, fallback_script)
                    
                    if os.path.exists(target_exe):
                        t_path = target_exe
                        args = ""
                    elif os.path.exists(script_file):
                        t_path = "python.exe"
                        args = f'"{script_file}"'
                    else:
                        return

                    vbs_cmd = f'''
                    $ws = New-Object -ComObject WScript.Shell
                    $s = $ws.CreateShortcut("{desktop}\\{shortcut_name}.lnk")
                    $s.TargetPath = "{t_path}"
                    $s.Arguments = '{args}'
                    $s.WorkingDirectory = "{target}"
                    $s.Save()
                    '''
                    subprocess.run(["powershell", "-NoProfile", "-Command", vbs_cmd], capture_output=True)
                    self.log_box.insert(tk.END, f"  🔗 Shortcut: {shortcut_name}\n")

                create_vbs_shortcut("Emerald Developer Studio", "Emerald_Studio.exe", "emerald_studio.py")
                create_vbs_shortcut("Sapphire Compiler Studio", "Sapphire_Compiler.exe", "sapphire_compiler.py")
                create_vbs_shortcut("Sapphire Language Tutor", "sapphire_voice_tutor.exe", "sapphire_voice_tutor.py")
                create_vbs_shortcut("Uninstall Sapphire", "uninstall.exe", "uninstall_sapphire.py")

            except Exception as e:
                self.log_box.insert(tk.END, f"  Shortcut notice: {e}\n")

        self.update_status("Installation Complete!", 100, "✨ All Sapphire components unpacked and installed successfully.")
        time.sleep(0.8)
        self.controller.show_frame(FinishPage)


class FinishPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#0F172A")
        self.controller = controller

        # 1. BOTTOM BAR
        btm = tk.Frame(self, bg="#0A0F1D", height=60)
        btm.pack(fill="x", side="bottom")

        sep = tk.Frame(btm, bg="#334155", height=1)
        sep.pack(fill="x", side="top")

        btn_inner = tk.Frame(btm, bg="#0A0F1D")
        btn_inner.pack(fill="x", padx=30, pady=12)

        btn_finish = tk.Button(
            btn_inner, text="Finish", font=("Helvetica", 10, "bold"),
            fg="#FFFFFF", bg="#2563EB", activebackground="#1D4ED8", activeforeground="#FFFFFF",
            bd=0, padx=28, pady=7, cursor="hand2", command=self.finish
        )
        btn_finish.pack(side="right")

        # 2. MAIN CONTENT
        content = tk.Frame(self, bg="#0F172A")
        content.pack(fill="both", expand=True, padx=30, pady=(25, 10))

        lbl_title = tk.Label(content, text="🎉 Sapphire Installation Complete!", font=("Helvetica", 16, "bold"), fg="#10B981", bg="#0F172A")
        lbl_title.pack(anchor="w", pady=(0, 5))

        lbl_sub = tk.Label(content, text="Sapphire Language, Emerald Studio, and Compiler are ready to use.", font=("Helvetica", 10), fg="#CBD5E1", bg="#0F172A")
        lbl_sub.pack(anchor="w", pady=(0, 20))

        box_frame = tk.Frame(content, bg="#1E293B", padx=15, pady=15, relief="solid", bd=1)
        box_frame.pack(fill="x", pady=10)

        chk_launch = tk.Checkbutton(box_frame, text="Launch Emerald Developer Studio GUI Now", variable=controller.opt_launch_studio, font=("Helvetica", 10, "bold"), fg="#38BDF8", bg="#1E293B", selectcolor="#0F172A", activebackground="#1E293B")
        chk_launch.pack(anchor="w", pady=4)

        chk_guide = tk.Checkbutton(box_frame, text="Open Sapphire Documentation & AI Manual", variable=controller.opt_open_guide, font=("Helvetica", 10), fg="#F8FAFC", bg="#1E293B", selectcolor="#0F172A", activebackground="#1E293B")
        chk_guide.pack(anchor="w", pady=4)

        lbl_cmd = tk.Label(box_frame, text="\nTerminal Commands: 'sapphire run file.sp' | 'sapphire compiler' | 'sapphire studio' | 'sapphire tutor'", font=("Consolas", 9), fg="#94A3B8", bg="#1E293B")
        lbl_cmd.pack(anchor="w")

    def finish(self):
        target = self.controller.install_dir.get()
        
        if self.controller.opt_launch_studio.get():
            studio_exe = os.path.join(target, "Emerald_Studio.exe")
            studio_py = os.path.join(target, "emerald_studio.py")
            if os.path.exists(studio_exe):
                subprocess.Popen([studio_exe], cwd=target)
            elif os.path.exists(studio_py):
                subprocess.Popen([sys.executable, studio_py], cwd=target)

        if self.controller.opt_open_guide.get():
            pdf_path = os.path.join(target, "Beginners_Guide_Your_First_Autonomous_AI.pdf")
            if os.path.exists(pdf_path):
                os.startfile(pdf_path)

        self.controller.quit()

if __name__ == "__main__":
    app = SapphireSetupWizard()
    app.mainloop()
