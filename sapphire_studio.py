"""
💎 SAPPHIRE PROGRAMMING LANGUAGE — DEVELOPER STUDIO IDE & TOOL BUILDER
Graphical Coding Terminal, Tool Builder, GPU Dashboard, and Agent State Inspector.
"""
import sys
import os
import time
import subprocess
import threading
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Ensure sys.path includes sapphire_lang
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAPPHIRE_LANG_DIR = os.path.join(BASE_DIR, "sapphire_lang")
if SAPPHIRE_LANG_DIR not in sys.path:
    sys.path.insert(0, SAPPHIRE_LANG_DIR)
    sys.path.insert(0, os.path.join(SAPPHIRE_LANG_DIR, "src"))

# Reconfigure terminal encoding for UTF-8 compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Sample Sapphire Tool Templates (.sp)
TOOL_TEMPLATE_SYSTEM_AUDIT = """// 💎 System Audit Tool (system_audit.sp)
// Capability: Sense PC Telemetry & Neural Evaluation

fn audit_system() {
    print("🔍 Starting Sapphire System & ML Audit...");

    // 1. Data & Telemetry Ingestion
    let stats = os.system_info();
    print("📊 CPU: {stats.cpu_usage_percent}%, RAM: {stats.ram_percent}%");

    // 2. GPU & Tensor Allocation Test
    let gpu_list = ml.gpu.info();
    print("⚡ Available Hardware Accelerators: {gpu_list}");

    // 3. AI Reasoning & Decision
    let prompt = "System RAM load is at {stats.ram_percent}%. Recommend optimization action.";
    let opinion = ai.prompt(prompt);
    print("🤖 AI Evaluation: {opinion}");

    // 4. Memory Persistence
    agent.memory.remember("last_audit_ram", stats.ram_percent);
    os.notify("Sapphire Tool Audit", "System audit completed successfully!");
}

audit_system();
"""

TOOL_TEMPLATE_NN_TRAINER = """// 💎 Neural Network Trainer Tool (nn_trainer.sp)
// Pipeline: Data → Training → Model → Evaluation

fn train_neural_net() {
    print("🧠 Sapphire Autonomous Neural Network Trainer");

    // Step 1: Data Preparation
    let ds = ml.dataset.random(500, 8, 2);
    let split = ds.split(0.8);
    print("Dataset prepared: {split['train'].size} train, {split['val'].size} val.");

    // Step 2: Architecture Construction
    let model = ml.model.mlp([8, 32, 16, 2], "relu");
    print(model.summary());

    // Step 3: Model Training
    let result = ml.train.fit(
        model,
        split["train"],
        ml.loss.mse,
        ml.optim.adam(0.01),
        epochs=5,
        batch_size=32,
        val_dataset=split["val"]
    );

    print("✅ Final Training Loss: {result.final_loss}");
}

train_neural_net();
"""

TOOL_TEMPLATE_AUTONOMOUS_AGENT = """// 💎 Autonomous Agent Tool (auto_agent.sp)
// Pipeline: Reasoning → Memory → Planning → Tool use → Execution

fn main_agent() {
    print("🤖 Launching Sapphire Autonomous Agent...");

    let goal = "Audit GPU VRAM, train lightweight MLP model, and notify admin.";
    let result = agent.autonomy.run_loop(goal, max_steps=5);

    print("✨ Agent Execution Summary:");
    print(result["plan_summary"]);
}

main_agent();
"""


class SapphireStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("💎 Sapphire Developer Studio — AI/ML Tool Builder & IDE")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg="#0F172A") # Dark Navy

        self.current_filepath = None
        self.setup_styles()
        self.create_layout()

        # Load default sample script
        self.editor.insert("1.0", TOOL_TEMPLATE_SYSTEM_AUDIT)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#0F172A")
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"), foreground="#38BDF8", background="#0F172A")
        self.style.configure("SubHeader.TLabel", font=("Helvetica", 10), foreground="#94A3B8", background="#0F172A")

        self.style.configure("TNotebook", background="#0F172A", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#1E293B", foreground="#E2E8F0", padding=[12, 6], font=("Helvetica", 10, "bold"))
        self.style.map("TNotebook.Tab", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])

    def create_layout(self):
        # Top Title Banner
        banner = tk.Frame(self, bg="#1E293B", height=45)
        banner.pack(fill="x", side="top")
        
        lbl_title = tk.Label(banner, text="💎 SAPPHIRE DEVELOPER STUDIO", font=("Helvetica", 13, "bold"), fg="#38BDF8", bg="#1E293B")
        lbl_title.pack(side="left", padx=15, pady=8)

        lbl_subtitle = tk.Label(banner, text="Data → Training → Model → Reasoning → Memory → Planning → Tools → Autonomy", font=("Helvetica", 9), fg="#94A3B8", bg="#1E293B")
        lbl_subtitle.pack(side="left", padx=10, pady=8)

        btn_run = tk.Button(banner, text="▶ Run Script (.sp)", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#16A34A", activebackground="#15803D", activeforeground="#FFFFFF", bd=0, padx=12, pady=4, command=self.run_current_script)
        btn_run.pack(side="right", padx=10, pady=6)

        btn_new_tool = tk.Button(banner, text="+ New Sapphire Tool", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#2563EB", activebackground="#1D4ED8", activeforeground="#FFFFFF", bd=0, padx=10, pady=4, command=self.show_tool_wizard)
        btn_new_tool.pack(side="right", padx=5, pady=6)

        # Main Splitter
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg="#0F172A", bd=0, sashwidth=4)
        paned.pack(fill="both", expand=True, padx=8, pady=8)

        # Left Container: Editor & Tabs
        left_frame = tk.Frame(paned, bg="#0F172A")
        paned.add(left_frame)

        # Toolbar
        tb = tk.Frame(left_frame, bg="#0F172A")
        tb.pack(fill="x", pady=(0, 4))

        btn_open = tk.Button(tb, text="📂 Open File", font=("Helvetica", 9), fg="#E2E8F0", bg="#334155", bd=0, padx=8, pady=2, command=self.open_file)
        btn_open.pack(side="left", padx=2)

        btn_save = tk.Button(tb, text="💾 Save (.sp)", font=("Helvetica", 9), fg="#E2E8F0", bg="#334155", bd=0, padx=8, pady=2, command=self.save_file)
        btn_save.pack(side="left", padx=2)

        self.lbl_file = tk.Label(tb, text="Untitled.sp", font=("Courier", 9, "italic"), fg="#94A3B8", bg="#0F172A")
        self.lbl_file.pack(side="left", padx=10)

        # Template quick links
        lbl_tpl = tk.Label(tb, text="Templates:", font=("Helvetica", 9), fg="#64748B", bg="#0F172A")
        lbl_tpl.pack(side="right", padx=2)

        btn_tpl1 = tk.Button(tb, text="System Audit", font=("Helvetica", 8), fg="#93C5FD", bg="#1E293B", bd=0, padx=4, command=lambda: self.load_template(TOOL_TEMPLATE_SYSTEM_AUDIT))
        btn_tpl1.pack(side="right", padx=2)

        btn_tpl2 = tk.Button(tb, text="NN Trainer", font=("Helvetica", 8), fg="#93C5FD", bg="#1E293B", bd=0, padx=4, command=lambda: self.load_template(TOOL_TEMPLATE_NN_TRAINER))
        btn_tpl2.pack(side="right", padx=2)

        btn_tpl3 = tk.Button(tb, text="Auto Agent", font=("Helvetica", 8), fg="#93C5FD", bg="#1E293B", bd=0, padx=4, command=lambda: self.load_template(TOOL_TEMPLATE_AUTONOMOUS_AGENT))
        btn_tpl3.pack(side="right", padx=2)

        # Code Editor
        self.editor = scrolledtext.ScrolledText(left_frame, font=("Consolas", 11), bg="#020617", fg="#F8FAFC", insertbackground="#38BDF8", selectbackground="#1E293B", bd=1, relief="solid")
        self.editor.pack(fill="both", expand=True)

        # Right Container: Terminal & Inspector Tabs
        right_frame = tk.Frame(paned, bg="#0F172A")
        paned.add(right_frame)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill="both", expand=True)

        # Tab 1: Terminal Output
        tab_term = ttk.Frame(notebook)
        notebook.add(tab_term, text="🖥️ Terminal Output")

        self.term_output = scrolledtext.ScrolledText(tab_term, font=("Consolas", 10), bg="#090D16", fg="#4ADE80", insertbackground="#4ADE80", bd=0)
        self.term_output.pack(fill="both", expand=True)

        # Tab 2: GPU & System Dashboard
        tab_gpu = ttk.Frame(notebook)
        notebook.add(tab_gpu, text="⚡ Hardware Dashboard")

        self.lbl_gpu_info = scrolledtext.ScrolledText(tab_gpu, font=("Consolas", 10), bg="#090D16", fg="#38BDF8", bd=0)
        self.lbl_gpu_info.pack(fill="both", expand=True)
        self.refresh_gpu_dashboard()

        # Tab 3: Agent & Memory Inspector
        tab_agent = ttk.Frame(notebook)
        notebook.add(tab_agent, text="🧠 Agent & Memory Inspector")

        self.agent_inspector = scrolledtext.ScrolledText(tab_agent, font=("Consolas", 10), bg="#090D16", fg="#F472B6", bd=0)
        self.agent_inspector.pack(fill="both", expand=True)
        self.refresh_agent_inspector()

    def load_template(self, content: str):
        self.editor.delete("1.0", tk.END)
        self.editor.insert("1.0", content)

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Sapphire Script", "*.sp"), ("All Files", "*.*")])
        if filepath:
            self.current_filepath = filepath
            self.lbl_file.config(text=os.path.basename(filepath))
            with open(filepath, "r", encoding="utf-8") as f:
                self.editor.delete("1.0", tk.END)
                self.editor.insert("1.0", f.read())

    def save_file(self):
        if not self.current_filepath:
            filepath = filedialog.asksaveasfilename(defaultextension=".sp", filetypes=[("Sapphire Script", "*.sp")])
            if not filepath:
                return
            self.current_filepath = filepath
            self.lbl_file.config(text=os.path.basename(filepath))

        with open(self.current_filepath, "w", encoding="utf-8") as f:
            f.write(self.editor.get("1.0", tk.END))
        messagebox.showinfo("Saved", f"File saved to:\n{self.current_filepath}")

    def run_current_script(self):
        code = self.editor.get("1.0", tk.END)
        temp_file = os.path.join(BASE_DIR, "_temp_run.sp")
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code)

        self.term_output.delete("1.0", tk.END)
        self.term_output.insert("1.0", f"🚀 Executing Sapphire Script: {self.lbl_file.cget('text')}...\n" + "─"*50 + "\n")

        def _execute():
            cli_py = os.path.join(SAPPHIRE_LANG_DIR, "src", "cli.py")
            cmd = [sys.executable, cli_py, "run", temp_file]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate()
            
            self.term_output.insert(tk.END, stdout)
            if stderr:
                self.term_output.insert(tk.END, "\n❌ ERRORS:\n" + stderr)
            self.term_output.insert(tk.END, "\n" + "─"*50 + "\n✨ Execution Finished.\n")
            
            # Refresh inspectors
            self.after(100, self.refresh_gpu_dashboard)
            self.after(100, self.refresh_agent_inspector)

        threading.Thread(target=_execute, daemon=True).start()

    def refresh_gpu_dashboard(self):
        self.lbl_gpu_info.delete("1.0", tk.END)
        try:
            from src.stdlib.ml_mod import GPUModule
            info = GPUModule.info()
            self.lbl_gpu_info.insert(tk.END, "⚡ SAPPHIRE HARDWARE ACCELERATION DASHBOARD\n" + "═"*50 + "\n\n")
            for dev in info:
                self.lbl_gpu_info.insert(tk.END, f"• Device      : {dev['device']}\n")
                self.lbl_gpu_info.insert(tk.END, f"  Name        : {dev['name']}\n")
                self.lbl_gpu_info.insert(tk.END, f"  VRAM Total  : {dev['memory_total_mb']:.0f} MB\n")
                self.lbl_gpu_info.insert(tk.END, f"  VRAM Used   : {dev['memory_used_mb']:.0f} MB\n")
                self.lbl_gpu_info.insert(tk.END, f"  VRAM Free   : {dev['memory_free_mb']:.0f} MB\n")
                self.lbl_gpu_info.insert(tk.END, "─"*40 + "\n")
        except Exception as e:
            self.lbl_gpu_info.insert(tk.END, f"Hardware Query Error: {e}")

    def refresh_agent_inspector(self):
        self.agent_inspector.delete("1.0", tk.END)
        try:
            from src.stdlib.ai_mod import AIModule
            from src.stdlib.agent_mod import AgentModule
            status = AIModule.status()
            self.agent_inspector.insert(tk.END, "🧠 SAPPHIRE AGENT & LLM STATUS\n" + "═"*50 + "\n\n")
            
            backend_name = status.get('active_backend', 'offline').upper()
            if backend_name == "GEMINI":
                active_badge = "🟢 ONLINE — Google Gemini Cloud AI (Primary)"
            elif backend_name == "OLLAMA":
                active_badge = "🟢 ONLINE — Ollama Local Engine"
            elif backend_name == "GROQ":
                active_badge = "🟢 ONLINE — Groq Cloud Engine"
            else:
                active_badge = "⚪ OFFLINE (Smart Local Fallback Active)"

            self.agent_inspector.insert(tk.END, f"• Active Engine   : {active_badge}\n\n")
            
            # Gemini Status
            gemini_online = "🟢 Online (Active)" if status.get('gemini_online') else "⚪ Standby"
            self.agent_inspector.insert(tk.END, f"  ✦ Google Gemini Cloud : {gemini_online}\n")
            self.agent_inspector.insert(tk.END, f"    Models              : gemini-3.1-flash-lite, gemini-3.6-flash\n\n")

            # Ollama Status
            ollama_online = "🟢 Online" if status.get('ollama_online') else "⚪ Standby (Offline)"
            self.agent_inspector.insert(tk.END, f"  ✦ Ollama Local Core   : {ollama_online}\n")
            self.agent_inspector.insert(tk.END, f"    Local URL           : {status.get('ollama_url', 'http://localhost:11434')}\n\n")

            # Groq Status
            groq_online = "🟢 Online" if status.get('groq_online') else "⚪ Standby"
            self.agent_inspector.insert(tk.END, f"  ✦ Groq Cloud Fallback : {groq_online}\n\n")
            
            self.agent_inspector.insert(tk.END, "📌 Registered Agent Tools:\n")
            for tool in AgentModule.tools.list_tools():
                self.agent_inspector.insert(tk.END, f"  - {tool['name']}: {tool['description']}\n")

            self.agent_inspector.insert(tk.END, f"\n🔒 Security Policy: {AgentModule.permissions.policy.upper()}\n")
        except Exception as e:
            self.agent_inspector.insert(tk.END, f"Agent Inspector Error: {e}")


    def show_tool_wizard(self):
        wiz = tk.Toplevel(self)
        wiz.title("🔨 New Sapphire Tool Creator Wizard")
        wiz.geometry("480x360")
        wiz.configure(bg="#0F172A")

        tk.Label(wiz, text="🔨 Create New Sapphire Tool (.sp)", font=("Helvetica", 12, "bold"), fg="#38BDF8", bg="#0F172A").pack(pady=10)

        tk.Label(wiz, text="Tool Name (e.g. data_cleaner):", font=("Helvetica", 9), fg="#94A3B8", bg="#0F172A").pack(anchor="w", padx=20)
        ent_name = tk.Entry(wiz, font=("Consolas", 10), bg="#1E293B", fg="#F8FAFC", bd=1)
        ent_name.pack(fill="x", padx=20, pady=4)
        ent_name.insert(0, "custom_tool")

        tk.Label(wiz, text="Tool Description:", font=("Helvetica", 9), fg="#94A3B8", bg="#0F172A").pack(anchor="w", padx=20)
        ent_desc = tk.Entry(wiz, font=("Consolas", 10), bg="#1E293B", fg="#F8FAFC", bd=1)
        ent_desc.pack(fill="x", padx=20, pady=4)
        ent_desc.insert(0, "Custom developer tool created with Sapphire Studio")

        chk_ml = tk.BooleanVar(value=True)
        chk_agent = tk.BooleanVar(value=True)
        chk_os = tk.BooleanVar(value=True)

        tk.Checkbutton(wiz, text="Include ML & Tensor Stack (ml)", variable=chk_ml, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B").pack(anchor="w", padx=20, pady=2)
        tk.Checkbutton(wiz, text="Include AI Agent Architecture (agent & ai)", variable=chk_agent, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B").pack(anchor="w", padx=20, pady=2)
        tk.Checkbutton(wiz, text="Include System Telemetry & Automation (os)", variable=chk_os, font=("Helvetica", 9), fg="#E2E8F0", bg="#0F172A", selectcolor="#1E293B").pack(anchor="w", padx=20, pady=2)

        def _generate():
            name = ent_name.get().strip().replace(" ", "_")
            desc = ent_desc.get().strip()
            
            code = [f"// 💎 Sapphire Tool: {name}.sp", f"// Description: {desc}\n"]
            code.append(f"fn execute_{name}() {{")
            code.append(f'    print("🚀 Running {name}...");')
            if chk_os.get():
                code.append('    let stats = os.system_info();')
                code.append('    print("📊 CPU: {stats.cpu_usage_percent}%, RAM: {stats.ram_percent}%");')
            if chk_ml.get():
                code.append('    let data_tensor = ml.randn([4, 4]);')
                code.append('    print("⚡ ML Tensor: {data_tensor.shape}");')
            if chk_agent.get():
                code.append(f'    let opinion = ai.prompt("Tool {name} initialized.");')
                code.append('    print("🤖 Agent Output: {opinion}");')
                code.append(f'    agent.memory.remember("{name}_last_run", "success");')
            code.append(f'    os.notify("Sapphire Tool", "{name} execution complete!");')
            code.append("}\n")
            code.append(f"execute_{name}();")

            gen_code = "\n".join(code)
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", gen_code)
            self.lbl_file.config(text=f"{name}.sp")
            wiz.destroy()

        tk.Button(wiz, text="✨ Generate Sapphire Tool (.sp)", font=("Helvetica", 10, "bold"), fg="#FFFFFF", bg="#2563EB", bd=0, padx=12, pady=6, command=_generate).pack(pady=15)


def main():
    app = SapphireStudio()
    app.mainloop()

if __name__ == "__main__":
    main()
