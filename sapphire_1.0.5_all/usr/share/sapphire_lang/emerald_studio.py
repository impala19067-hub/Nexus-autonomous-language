"""Emerald Developer Studio: Sapphire's local editor, runner, and inspectors."""
from __future__ import annotations

import importlib
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_INSTANCE_MUTEX = None


def acquire_single_instance() -> bool:
    """Allow only one Emerald Studio process per Windows user session."""
    global _INSTANCE_MUTEX
    if os.name != "nt":
        return True
    import ctypes
    _INSTANCE_MUTEX = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\Sapphire.EmeraldStudio.v1")
    return bool(_INSTANCE_MUTEX) and ctypes.windll.kernel32.GetLastError() != 183
SAPPHIRE_LANG_DIR = os.path.join(BASE_DIR, "sapphire_lang")
for path in (SAPPHIRE_LANG_DIR, os.path.join(SAPPHIRE_LANG_DIR, "src")):
    if path not in sys.path:
        sys.path.insert(0, path)

TOOL_TEMPLATE_SYSTEM_AUDIT = '''// Emerald Tool: System Audit
fn audit_system() {
    let stats = os.system_info();
    print("CPU: {stats.cpu_usage_percent}%, RAM: {stats.ram_percent}%");
    let devices = ml.gpu.info();
    print("Hardware: {devices}");
    let opinion = ai.prompt("Review this system telemetry and suggest a safe next step.");
    print("AI: {opinion}");
    agent.memory.remember("last_audit_ram", stats.ram_percent);
    os.notify("Emerald Audit", "System audit completed.");
}
audit_system();
'''

TOOL_TEMPLATE_NN_TRAINER = '''// Emerald Tool: Local Neural Network Trainer
fn train_neural_net() {
    let dataset = ml.dataset.random(500, 8, 2);
    let model = ml.model.mlp([8, 32, 16, 2], "relu");
    let result = ml.train.fit(model, dataset, ml.loss.mse, ml.optim.adam(0.01), 5, 32, 2);
    print("Final loss: {result.final_loss}");
}
train_neural_net();
'''

TOOL_TEMPLATE_AUTONOMOUS_AGENT = '''// Emerald Tool: Bounded Sapphire Agent
fn main_agent() {
    let report = agent.autonomy.run_loop("Inspect system health and notify the user", 5);
    print("State: {report.state}");
    print(report.plan_summary);
}
main_agent();
'''


class EmeraldStudio(tk.Tk):
    COLORS = {
        "window": "#06150F",
        "sidebar": "#082219",
        "panel": "#0D2F22",
        "panel_raised": "#123C2B",
        "border": "#1D6044",
        "accent": "#27D17F",
        "accent_bright": "#7AF2B4",
        "text": "#E9FFF2",
        "muted": "#91BCA4",
        "editor": "#03100B",
        "terminal": "#05140D",
        "warning": "#F6C85F",
    }

    def __init__(self):
        super().__init__()
        self.title("Emerald Developer Studio | Sapphire Workspace")
        self.geometry("1280x820")
        self.minsize(980, 640)
        self.configure(bg=self.COLORS["window"])
        self.current_filepath = None
        self.transparency_enabled = False
        self.script_running = False
        self._build_styles()
        self._build_shell()
        self.load_template(TOOL_TEMPLATE_SYSTEM_AUDIT)

        icon_path = os.path.join(BASE_DIR, "Emerald_Icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except tk.TclError:
                pass

    def _build_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=self.COLORS["window"])
        self.style.configure("Panel.TFrame", background=self.COLORS["panel"])
        self.style.configure("Sidebar.TFrame", background=self.COLORS["sidebar"])
        self.style.configure("TNotebook", background=self.COLORS["window"], borderwidth=0)
        self.style.configure("TNotebook.Tab", background=self.COLORS["panel_raised"], foreground=self.COLORS["muted"], padding=[16, 9], font=("Segoe UI", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", self.COLORS["accent"])], foreground=[("selected", "#032010")])

    def _build_shell(self):
        self._build_topbar()
        body = tk.Frame(self, bg=self.COLORS["window"])
        body.pack(fill="both", expand=True)
        self._build_sidebar(body)
        self._build_workspace(body)
        self._build_statusbar()

    def _build_topbar(self):
        bar = tk.Frame(self, bg=self.COLORS["panel"], height=66)
        bar.pack(fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, text="◆", font=("Segoe UI Symbol", 30, "bold"), fg=self.COLORS["accent_bright"], bg=self.COLORS["panel"]).pack(side="left", padx=(24, 12))
        title_box = tk.Frame(bar, bg=self.COLORS["panel"])
        title_box.pack(side="left", pady=10)
        tk.Label(title_box, text="EMERALD", font=("Segoe UI", 15, "bold"), fg=self.COLORS["accent_bright"], bg=self.COLORS["panel"]).pack(anchor="w")
        tk.Label(title_box, text="DEVELOPER STUDIO  /  SAPPHIRE WORKSPACE", font=("Segoe UI", 8, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["panel"]).pack(anchor="w")

        self.transparency_button = tk.Button(bar, text="Transparency: OFF", font=("Segoe UI", 9, "bold"), fg=self.COLORS["text"], bg=self.COLORS["panel_raised"], activebackground=self.COLORS["border"], activeforeground=self.COLORS["text"], bd=0, padx=12, pady=8, command=self.toggle_transparency)
        self.transparency_button.pack(side="right", padx=(6, 20), pady=13)
        tk.Button(bar, text="RUN  F5", font=("Segoe UI", 9, "bold"), fg="#032010", bg=self.COLORS["accent"], activebackground=self.COLORS["accent_bright"], bd=0, padx=15, pady=8, command=self.run_current_script).pack(side="right", padx=6, pady=13)
        tk.Button(bar, text="NEW TOOL", font=("Segoe UI", 9, "bold"), fg="#032010", bg=self.COLORS["accent_bright"], activebackground=self.COLORS["accent"], bd=0, padx=15, pady=8, command=self.show_tool_wizard).pack(side="right", padx=6, pady=13)

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, width=188, bg=self.COLORS["sidebar"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="WORKSPACE", font=("Segoe UI", 8, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["sidebar"]).pack(anchor="w", padx=20, pady=(24, 10))
        self._sidebar_button(sidebar, "Open Sapphire File", self.open_file)
        self._sidebar_button(sidebar, "Save Current File", self.save_file)
        self._sidebar_button(sidebar, "Run Current Script", self.run_current_script)
        tk.Frame(sidebar, height=1, bg=self.COLORS["border"]).pack(fill="x", padx=20, pady=18)
        tk.Label(sidebar, text="TEMPLATES", font=("Segoe UI", 8, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["sidebar"]).pack(anchor="w", padx=20, pady=(0, 10))
        self._sidebar_button(sidebar, "System Audit", lambda: self.load_template(TOOL_TEMPLATE_SYSTEM_AUDIT))
        self._sidebar_button(sidebar, "Neural Trainer", lambda: self.load_template(TOOL_TEMPLATE_NN_TRAINER))
        self._sidebar_button(sidebar, "Bounded Agent", lambda: self.load_template(TOOL_TEMPLATE_AUTONOMOUS_AGENT))
        tk.Label(sidebar, text="LOCAL RUNTIME", font=("Segoe UI", 8, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["sidebar"]).pack(anchor="w", padx=20, pady=(34, 10))
        tk.Label(sidebar, text="Interpreter online\nOptional ML detected at runtime\nF5 runs the open buffer", justify="left", font=("Segoe UI", 8), fg=self.COLORS["muted"], bg=self.COLORS["sidebar"]).pack(anchor="w", padx=20)

    def _sidebar_button(self, parent, text, command):
        button = tk.Button(parent, text=text, anchor="w", font=("Segoe UI", 9, "bold"), fg=self.COLORS["text"], bg=self.COLORS["sidebar"], activebackground=self.COLORS["panel_raised"], activeforeground=self.COLORS["accent_bright"], bd=0, padx=20, pady=8, command=command)
        button.pack(fill="x")

    def _build_workspace(self, parent):
        workspace = tk.Frame(parent, bg=self.COLORS["window"])
        workspace.pack(side="left", fill="both", expand=True, padx=(12, 16), pady=12)
        heading = tk.Frame(workspace, bg=self.COLORS["window"], height=38)
        heading.pack(fill="x")
        heading.pack_propagate(False)
        self.lbl_file = tk.Label(heading, text="Untitled.sp", font=("Segoe UI", 11, "bold"), fg=self.COLORS["text"], bg=self.COLORS["window"])
        self.lbl_file.pack(side="left", pady=6)
        tk.Label(heading, text="SAPPHIRE SOURCE", font=("Segoe UI", 8, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["window"]).pack(side="right", pady=8)

        panes = tk.PanedWindow(workspace, orient=tk.HORIZONTAL, bg=self.COLORS["border"], sashwidth=5, bd=0)
        panes.pack(fill="both", expand=True)
        editor_panel = tk.Frame(panes, bg=self.COLORS["editor"])
        right_panel = tk.Frame(panes, bg=self.COLORS["window"])
        panes.add(editor_panel, minsize=430, stretch="always")
        panes.add(right_panel, minsize=330, stretch="always")
        self.editor = scrolledtext.ScrolledText(editor_panel, wrap=tk.NONE, undo=True, font=("Cascadia Mono", 11), bg=self.COLORS["editor"], fg=self.COLORS["text"], insertbackground=self.COLORS["accent_bright"], selectbackground=self.COLORS["border"], padx=16, pady=14, bd=0)
        self.editor.pack(fill="both", expand=True)

        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill="both", expand=True)
        self.term_output = self._output_tab(notebook, "Terminal")
        self.lbl_gpu_info = self._output_tab(notebook, "Hardware")
        self.agent_inspector = self._output_tab(notebook, "Agent Memory")
        self.refresh_gpu_dashboard()
        self.refresh_agent_inspector()
        self.bind("<F5>", self._run_from_f5)

    def _output_tab(self, notebook, name):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=name)
        output = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=("Cascadia Mono", 10), bg=self.COLORS["terminal"], fg=self.COLORS["accent_bright"], insertbackground=self.COLORS["accent_bright"], padx=14, pady=14, bd=0)
        output.pack(fill="both", expand=True)
        return output

    def _build_statusbar(self):
        status = tk.Frame(self, bg=self.COLORS["sidebar"], height=28)
        status.pack(fill="x", side="bottom")
        status.pack_propagate(False)
        tk.Label(status, text="SAPPHIRE INTERPRETER", font=("Segoe UI", 8, "bold"), fg=self.COLORS["accent"], bg=self.COLORS["sidebar"]).pack(side="left", padx=18)
        tk.Label(status, text="LOCAL  |  READY  |  F5 RUN", font=("Segoe UI", 8), fg=self.COLORS["muted"], bg=self.COLORS["sidebar"]).pack(side="right", padx=18)

    def toggle_transparency(self):
        self.transparency_enabled = not self.transparency_enabled
        try:
            self.attributes("-alpha", 0.88 if self.transparency_enabled else 1.0)
            self.transparency_button.config(text=f"Transparency: {'ON' if self.transparency_enabled else 'OFF'}")
        except tk.TclError:
            self.transparency_enabled = False
            messagebox.showwarning("Transparency unavailable", "This Windows desktop does not support transparent windows.")

    def _run_from_f5(self, _event=None):
        self.run_current_script()
        return "break"

    def load_template(self, content: str):
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", content)

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Sapphire Script", "*.sp"), ("All Files", "*.*")])
        if filepath:
            self.current_filepath = filepath
            self.lbl_file.config(text=os.path.basename(filepath))
            with open(filepath, "r", encoding="utf-8") as source:
                self.load_template(source.read())

    def save_file(self):
        if not self.current_filepath:
            self.current_filepath = filedialog.asksaveasfilename(defaultextension=".sp", filetypes=[("Sapphire Script", "*.sp")])
        if self.current_filepath:
            with open(self.current_filepath, "w", encoding="utf-8") as destination:
                destination.write(self.editor.get("1.0", tk.END))
            self.lbl_file.config(text=os.path.basename(self.current_filepath))

    def run_current_script(self):
        if self.script_running:
            return
        self.script_running = True
        temp_file = os.path.join(BASE_DIR, "_temp_run.sp")
        with open(temp_file, "w", encoding="utf-8") as destination:
            destination.write(self.editor.get("1.0", tk.END))
        self.term_output.delete("1.0", tk.END)
        self.term_output.insert("1.0", f"Running {self.lbl_file.cget('text')}\n{'-' * 48}\n")

        def execute():
            cli_py = os.path.join(SAPPHIRE_LANG_DIR, "src", "cli.py")
            process = subprocess.run([sys.executable, cli_py, "run", temp_file], capture_output=True, text=True, cwd=BASE_DIR)
            output = process.stdout
            if process.stderr:
                output += f"\nERRORS:\n{process.stderr}"
            self.after(0, lambda: self._finish_run(output, process.returncode))

        threading.Thread(target=execute, daemon=True).start()

    def _finish_run(self, output: str, returncode: int):
        self.term_output.insert(tk.END, output + f"\n{'-' * 48}\nExit code: {returncode}\n")
        self.script_running = False
        self.refresh_gpu_dashboard()
        self.refresh_agent_inspector()

    def refresh_gpu_dashboard(self):
        self.lbl_gpu_info.delete("1.0", tk.END)
        try:
            gpu_module = importlib.import_module("src.stdlib.ml_mod").GPUModule
            devices = gpu_module.info()
            self.lbl_gpu_info.insert(tk.END, "EMERALD HARDWARE VIEW\n" + "=" * 42 + "\n\n")
            for device in devices:
                self.lbl_gpu_info.insert(tk.END, f"Device: {device['device']}\nName: {device['name']}\nVRAM: {device['memory_used_mb']:.0f} / {device['memory_total_mb']:.0f} MB\n\n")
        except Exception as error:
            self.lbl_gpu_info.insert(tk.END, f"Hardware data unavailable\n\n{error}\n\nCPU fallback remains available.")

    def refresh_agent_inspector(self):
        self.agent_inspector.delete("1.0", tk.END)
        try:
            ai_module = importlib.import_module("src.stdlib.ai_mod").AIModule
            agent_module = importlib.import_module("src.stdlib.agent_mod").AgentModule
            status = ai_module.status()
            self.agent_inspector.insert(tk.END, "EMERALD AGENT INSPECTOR\n" + "=" * 42 + "\n\n")
            self.agent_inspector.insert(tk.END, f"Backend: {status.get('active_backend', 'offline')}\n")
            self.agent_inspector.insert(tk.END, f"Policy: {agent_module.permissions.policy}\n\nRegistered tools:\n")
            tools = agent_module.tools.list_tools()
            self.agent_inspector.insert(tk.END, "No user tools registered.\n" if not tools else "")
            for tool in tools:
                self.agent_inspector.insert(tk.END, f"- {tool['name']}\n")
        except Exception as error:
            self.agent_inspector.insert(tk.END, f"Agent data unavailable\n\n{error}")

    def show_tool_wizard(self):
        wizard = tk.Toplevel(self)
        wizard.title("New Sapphire Tool")
        wizard.geometry("520x420")
        wizard.configure(bg=self.COLORS["window"])
        tk.Label(wizard, text="◆  NEW SAPPHIRE TOOL", font=("Segoe UI", 15, "bold"), fg=self.COLORS["accent_bright"], bg=self.COLORS["window"]).pack(anchor="w", padx=24, pady=(24, 18))
        fields = {}
        for label, key, default in (("Tool name", "name", "custom_tool"), ("Description", "description", "Local Sapphire utility")):
            tk.Label(wizard, text=label.upper(), font=("Segoe UI", 8, "bold"), fg=self.COLORS["muted"], bg=self.COLORS["window"]).pack(anchor="w", padx=24, pady=(4, 4))
            entry = tk.Entry(wizard, font=("Cascadia Mono", 10), bg=self.COLORS["panel"], fg=self.COLORS["text"], insertbackground=self.COLORS["accent_bright"], bd=0)
            entry.pack(fill="x", padx=24, ipady=7)
            entry.insert(0, default)
            fields[key] = entry
        selected = {key: tk.BooleanVar(value=True) for key in ("os", "ml", "agent")}
        for key, label in (("os", "System telemetry"), ("ml", "ML and tensor utilities"), ("agent", "AI and agent memory")):
            tk.Checkbutton(wizard, text=label, variable=selected[key], font=("Segoe UI", 9), fg=self.COLORS["text"], bg=self.COLORS["window"], selectcolor=self.COLORS["panel"], activebackground=self.COLORS["window"]).pack(anchor="w", padx=24, pady=2)

        def generate():
            name = fields["name"].get().strip().replace(" ", "_") or "custom_tool"
            lines = [f"// Emerald Tool: {name}", f"// {fields['description'].get().strip()}", "", f"fn execute_{name}() {{"]
            if selected["os"].get():
                lines.extend(["    let stats = os.system_info();", '    print("CPU: {stats.cpu_usage_percent}%");'])
            if selected["ml"].get():
                lines.extend(["    let tensor = ml.randn([4, 4]);", '    print("Tensor: {tensor}");'])
            if selected["agent"].get():
                lines.extend([f'    let opinion = ai.prompt("{name} initialized.");', '    print(opinion);', f'    agent.memory.remember("{name}_last_run", "complete");'])
            lines.extend(['    os.notify("Emerald Tool", "Execution complete.");', "}", "", f"execute_{name}();"])
            self.current_filepath = None
            self.lbl_file.config(text=f"{name}.sp")
            self.load_template("\n".join(lines))
            wizard.destroy()

        tk.Button(wizard, text="GENERATE TOOL", font=("Segoe UI", 9, "bold"), fg="#032010", bg=self.COLORS["accent"], activebackground=self.COLORS["accent_bright"], bd=0, padx=18, pady=9, command=generate).pack(anchor="e", padx=24, pady=20)


def main():
    EmeraldStudio().mainloop()


if __name__ == "__main__":
    if acquire_single_instance():
        main()
