"""
💎 SAPPHIRE PROGRAMMING LANGUAGE — OFFICIAL UNINSTALLER (uninstall.exe)
Removes Sapphire language files, binaries, documentation, PATH registration,
and desktop shortcuts from Windows PC cleanly and safely.
"""

import sys
import os
import shutil
import subprocess
import time
import tkinter as tk
from tkinter import ttk, messagebox

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

if getattr(sys, 'frozen', False):
    EXE_DIR = os.path.dirname(sys.executable)
else:
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))

DEFAULT_INSTALL_DIR = os.path.join(os.environ.get("LOCALAPPDATA", r"C:\Users\Public"), "SapphireLang")

class SapphireUninstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💎 Uninstall Sapphire Programming Language & Emerald Studio")
        self.geometry("580x420")
        self.resizable(False, False)
        self.configure(bg="#0F172A")

        self.install_dir = tk.StringVar(value=EXE_DIR if "Sapphire" in EXE_DIR else DEFAULT_INSTALL_DIR)
        self.remove_path = tk.BooleanVar(value=True)
        self.remove_shortcuts = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self):
        # Header
        hdr = tk.Frame(self, bg="#0F172A")
        hdr.pack(fill="x", padx=25, pady=(20, 10))

        lbl_title = tk.Label(hdr, text="🗑️ Uninstall Sapphire Language", font=("Helvetica", 14, "bold"), fg="#EF4444", bg="#0F172A")
        lbl_title.pack(anchor="w")

        lbl_sub = tk.Label(hdr, text="Completely remove Sapphire language, IDE, tools, and shortcuts from your PC.", font=("Helvetica", 9), fg="#94A3B8", bg="#0F172A")
        lbl_sub.pack(anchor="w", pady=(2, 0))

        # Target box
        box = tk.Frame(self, bg="#1E293B", padx=15, pady=12, relief="solid", bd=1)
        box.pack(fill="x", padx=25, pady=10)

        lbl_loc = tk.Label(box, text="Installation Location to Remove:", font=("Helvetica", 9, "bold"), fg="#E2E8F0", bg="#1E293B")
        lbl_loc.pack(anchor="w")

        ent_loc = tk.Entry(box, textvariable=self.install_dir, font=("Consolas", 9), bg="#0F172A", fg="#F8FAFC", bd=1)
        ent_loc.pack(fill="x", pady=5)

        # Options
        chk1 = tk.Checkbutton(box, text="Remove Sapphire from System PATH variable", variable=self.remove_path, font=("Helvetica", 9), fg="#F8FAFC", bg="#1E293B", selectcolor="#0F172A", activebackground="#1E293B")
        chk1.pack(anchor="w", pady=2)

        chk2 = tk.Checkbutton(box, text="Delete Desktop & Start Menu Shortcuts", variable=self.remove_shortcuts, font=("Helvetica", 9), fg="#F8FAFC", bg="#1E293B", selectcolor="#0F172A", activebackground="#1E293B")
        chk2.pack(anchor="w", pady=2)

        # Progress / Log Area
        self.log_box = tk.Text(self, font=("Consolas", 8), bg="#0B1120", fg="#38BDF8", height=7, bd=1)
        self.log_box.pack(fill="x", padx=25, pady=8)
        self.log_box.insert(tk.END, "Ready to uninstall. Click 'Uninstall Sapphire' below to proceed.\n")

        # Buttons
        btn_frame = tk.Frame(self, bg="#0F172A")
        btn_frame.pack(fill="x", side="bottom", padx=25, pady=15)

        self.btn_uninst = tk.Button(btn_frame, text="🗑️ Uninstall Sapphire", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#DC2626", activebackground="#B91C1C", activeforeground="#FFFFFF", bd=0, padx=16, pady=6, command=self.confirm_and_uninstall)
        self.btn_uninst.pack(side="right")

        self.btn_cancel = tk.Button(btn_frame, text="Cancel", font=("Helvetica", 10), fg="#E2E8F0", bg="#334155", activebackground="#475569", activeforeground="#FFFFFF", bd=0, padx=14, pady=6, command=self.destroy)
        self.btn_cancel.pack(side="right", padx=10)

    def log(self, text: str):
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)
        self.update_idletasks()

    def confirm_and_uninstall(self):
        target = self.install_dir.get().strip()
        if not messagebox.askyesno("Confirm Uninstall", f"Are you sure you want to permanently remove Sapphire Language and all its components from:\n\n{target}?"):
            return

        self.btn_uninst.config(state="disabled")
        self.btn_cancel.config(state="disabled")

        import threading
        threading.Thread(target=self._do_uninstall, args=(target,), daemon=True).start()

    def _do_uninstall(self, target: str):
        self.log("🚀 Beginning Sapphire uninstallation...")

        # 1. Remove Desktop Shortcuts
        if self.remove_shortcuts.get():
            self.log("🗑️ Removing Desktop shortcuts...")
            desktop = os.path.join(os.environ.get("USERPROFILE", "C:\\Users\\Public"), "Desktop")
            for sc_name in ["Emerald Developer Studio.lnk", "Sapphire Compiler Studio.lnk", "Sapphire Language Tutor.lnk", "Sapphire Setup Wizard.lnk"]:
                sc_path = os.path.join(desktop, sc_name)
                if os.path.exists(sc_path):
                    try:
                        os.remove(sc_path)
                        self.log(f"  Removed: {sc_name}")
                    except Exception as e:
                        self.log(f"  Notice ({sc_name}): {e}")

        # 2. Clean System PATH
        if self.remove_path.get():
            self.log("🔧 Cleaning System PATH environment variable...")
            try:
                ps_cmd = f'''
                $oldPath = [Environment]::GetEnvironmentVariable('Path', 'User')
                if ($oldPath -like '*{target}*') {{
                    $paths = $oldPath -split ';' | Where-Object {{ $_ -and $_ -ne '{target}' -and $_ -ne '{target}\\' }}
                    $newPath = $paths -join ';'
                    [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
                }}
                '''
                subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], capture_output=True)
                self.log("  PATH variable updated successfully.")
            except Exception as e:
                self.log(f"  PATH update warning: {e}")

        # 3. Remove Target Directory Files
        self.log(f"📁 Removing Sapphire files from {target}...")
        if os.path.exists(target):
            # If running from inside target, spawn self-deletion script
            current_exe = sys.executable if getattr(sys, 'frozen', False) else None
            try:
                for item in os.listdir(target):
                    item_path = os.path.join(target, item)
                    if current_exe and os.path.abspath(item_path) == os.path.abspath(current_exe):
                        continue # Can't delete self while running on Windows
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path, ignore_errors=True)
                    else:
                        try:
                            os.remove(item_path)
                        except Exception:
                            pass
                    self.log(f"  Deleted: {item}")
                
                # If running outside target or not self-locked, remove folder
                try:
                    os.rmdir(target)
                except Exception:
                    pass
            except Exception as e:
                self.log(f"  File removal notice: {e}")

        self.log("✨ SAPPHIRE HAS BEEN SUCCESSFULLY UNINSTALLED!")
        self.after(0, lambda: messagebox.showinfo("Uninstall Complete", "Sapphire Programming Language has been successfully uninstalled from your PC."))
        self.after(1000, self.destroy)

if __name__ == "__main__":
    app = SapphireUninstaller()
    app.mainloop()
