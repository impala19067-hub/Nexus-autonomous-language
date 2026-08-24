"""
╔══════════════════════════════════════════════════════════════════════╗
║  ███╗  ██╗███████╗██╗  ██╗██╗   ██╗███████╗  STUDIO  v2.0          ║
║  ████╗ ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝  ─────────────────     ║
║  ██╔██╗██║█████╗   ╚███╔╝ ██║   ██║███████╗  Polymorphic  AI IDE   ║
║  ██║╚████║██╔══╝   ██╔██╗ ██║   ██║╚════██║  Autonomous  Tools     ║
║  ██║  ███║███████╗██╔╝ ██╗╚██████╔╝███████║  ─────────────────     ║
║  ╚═╝  ╚══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝  Kali  Edition        ║
╚══════════════════════════════════════════════════════════════════════╝
Nexus Studio v2.0 — Advanced Polymorphic IDE & Autonomous Compiler
Cyberpunk Dark Theme | Live System Monitor | AI Agent | Network Inspector
"""

import sys, os, io, re, time, json, threading, queue, platform, socket
import urllib.request, urllib.parse, urllib.error
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ─── ENCODING ──────────────────────────────────────────────────────────
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except: pass
if hasattr(sys.stderr, 'reconfigure'):
    try: sys.stderr.reconfigure(encoding='utf-8')
    except: pass

# ─── PATH RESOLUTION ───────────────────────────────────────────────────
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NEXUS_DIR = os.path.join(BASE_DIR, "nexus_lang")
for _p in [BASE_DIR, NEXUS_DIR]:
    if os.path.exists(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

# ─── OPTIONAL IMPORTS ──────────────────────────────────────────────────
try:
    import psutil; HAS_PSUTIL = True
except: HAS_PSUTIL = False
try:
    import pyttsx3; HAS_TTS = True
except: HAS_TTS = False
try:
    from src.lexer import Lexer
    from src.parser import Parser
    from src.interpreter import Interpreter
    NEXUS_OK = True; NEXUS_ERR = None
except Exception as e:
    NEXUS_OK = False; NEXUS_ERR = str(e)

# ════════════════════════════════════════════════════════════════════════
# COLOR SYSTEM — KALI CYBERPUNK (Dracula-Inspired)
# ════════════════════════════════════════════════════════════════════════
C = {
    # ── Backgrounds ──────────────────────────────────
    'void':      '#030307',   # Absolute black – window bg
    'base':      '#070710',   # Editor background
    'surface':   '#0C0C1A',   # Panel surface
    'elevated':  '#111125',   # Raised elements
    'panel':     '#09091A',   # Sidebar/panel bg
    'actbar':    '#05050E',   # Activity bar
    'sidebar':   '#09091A',   # Sidebar bg
    'gutter':    '#07070F',   # Line number gutter
    'tab_act':   '#0D0D1E',   # Active tab bg
    'tab_in':    '#07070F',   # Inactive tab bg
    'status':    '#040410',   # Status bar bg
    'hover':     '#12122A',   # Hover state
    'sel':       '#1A1A45',   # Selection highlight

    # ── Neon Accents ─────────────────────────────────
    'cyan':      '#00D4FF',   # Primary — electric cyan
    'cyan_dim':  '#006688',   # Dimmed cyan
    'cyan_dark': '#003344',   # Very dark cyan
    'purple':    '#9D4EDD',   # Secondary — neon purple
    'purple2':   '#BD93F9',   # Light purple
    'green':     '#50FA7B',   # Success — neon green
    'green2':    '#39FF14',   # Bright neon green
    'amber':     '#FFB86C',   # Warning — amber
    'red':       '#FF5555',   # Error — red
    'pink':      '#FF79C6',   # Accent — hot pink
    'orange':    '#FFB86C',   # Orange
    'blue':      '#4488FF',   # Info blue

    # ── Text Hierarchy ───────────────────────────────
    'text':      '#D8E4FF',   # Primary text
    'text2':     '#6B7A99',   # Secondary text
    'text3':     '#2A3048',   # Dimmed text
    'code':      '#F8F8F2',   # Code text (Dracula white)

    # ── Syntax Highlighting (Dracula Palette) ────────
    'syn_kw':    '#FF79C6',   # Keywords     → pink
    'syn_ctrl':  '#BD93F9',   # Control flow → purple
    'syn_fn':    '#50FA7B',   # Functions    → green
    'syn_str':   '#F1FA8C',   # Strings      → yellow
    'syn_num':   '#BD93F9',   # Numbers      → purple
    'syn_cmt':   '#6272A4',   # Comments     → blue-gray
    'syn_type':  '#8BE9FD',   # Types/Modules→ cyan
    'type':      '#8BE9FD',   # Type cyan
    'syn_op':    '#FF79C6',   # Operators    → pink
    'syn_const': '#FFB86C',   # Constants    → orange

    # ── Borders & Separators ─────────────────────────
    'border':    '#141430',   # Default border
    'border2':   '#1E1E45',   # Brighter border
    'sep':       '#1A1A35',   # Separator
}

# ─── FONTS ─────────────────────────────────────────────────────────────
FUI   = ("Segoe UI",    9)
FUIB  = ("Segoe UI",    9,  "bold")
FUIS  = ("Segoe UI",    8)
FCODE = ("Consolas",   11)
FMONO = ("Consolas",    9)
FMONO2= ("Consolas",   10)
FBIG  = ("Segoe UI",   11,  "bold")
FXBIG = ("Segoe UI",   13,  "bold")

# ════════════════════════════════════════════════════════════════════════
# SAMPLE CODE (shown on startup)
# ════════════════════════════════════════════════════════════════════════
SAMPLE_CODE = """// ╔══════════════════════════════════════════════════╗
// ║  NEXUS STUDIO v2.0  —  Autonomous Script Demo    ║
// ╚══════════════════════════════════════════════════╝

fn main() {
    print("⚡ Initializing Nexus Autonomous Agent...");

    // 1. System Hardware Audit
    let sys = os.system_info();
    print("  -> OS Platform: {sys.platform}");
    print("  -> CPU Usage:   {sys.cpu_usage_percent}%");
    print("  -> Memory Load: {sys.ram_percent}%");

    // 2. Parallel Diagnostic Workers
    parallel {
        print("  [Worker 1] Scanning file system integrity...");
        print("  [Worker 2] Checking network HTTP latency...");
        print("  [Worker 3] Profiling memory allocation...");
    }

    // 3. AI Intelligence Evaluation
    let prompt = "System RAM is {sys.ram_percent}%. Evaluate health.";
    let ai_eval = ai.prompt(prompt);
    print("  AI Eval: {ai_eval}");

    // 4. Autonomous Notification
    os.notify("Nexus Studio", "Diagnostic complete!");
    print("✅ Autonomous diagnostic finished successfully.");
}

main();
"""

EXAMPLES = {
    "01 · Basic Syntax":        '// Basic Nexus Syntax\nlet x = 42;\nlet msg = "Hello, Nexus!";\nprint("{msg} — x = {x}");\n',
    "02 · Parallel Workers":    '// Parallel Execution\nparallel {\n    print("[T1] Processing data batch...");\n    print("[T2] Scanning file system...");\n    print("[T3] Checking network...");\n}\nprint("✅ All parallel workers done.");\n',
    "03 · OS & File System":    '// OS & Filesystem Module\nlet info = os.system_info();\nprint("Platform: {info.platform}");\nprint("CPU: {info.cpu_usage_percent}%");\nlet files = fs.list_dir(".");\nprint("Files: {files}");\n',
    "04 · HTTP & Network":      '// HTTP Module\nlet res = http.get("https://httpbin.org/get");\nprint("Status: {res.status}");\nprint("Body: {res.body}");\n',
    "05 · AI Agent":            '// Autonomous AI Agent\nlet task = "Summarize: Nexus is a next-gen autonomous language.";\nlet result = ai.prompt(task);\nprint("🤖 AI Response: {result}");\nos.notify("Nexus AI", "Task complete!");\n',
    "06 · Full Autobot":        SAMPLE_CODE,
}

# ════════════════════════════════════════════════════════════════════════
# VOICE ENGINE
# ════════════════════════════════════════════════════════════════════════
class VoiceEngine:
    def __init__(self):
        self.q = queue.Queue()
        self.enabled = False
        self._ready = False
        if HAS_TTS:
            threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            import pyttsx3
            eng = pyttsx3.init()
            eng.setProperty('rate', 172)
            self._ready = True
            while True:
                text = self.q.get()
                if self.enabled and text:
                    try: eng.say(text); eng.runAndWait()
                    except: pass
        except: pass

    def say(self, text):
        if self.enabled and self._ready:
            self.q.put(text)

# ════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION CLASS
# ════════════════════════════════════════════════════════════════════════
class NexusStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("  ⚡  NEXUS STUDIO  —  Polymorphic AI IDE  v2.0  |  Kali Edition")
        self.geometry("1420x900")
        self.minsize(1100, 680)
        self.configure(bg=C['void'])

        # ── State ──────────────────────────────────────
        self.current_file   = None
        self.is_running     = False
        self.voice          = VoiceEngine()
        self.output_queue   = queue.Queue()
        self.active_tool    = tk.StringVar(value="explorer")
        self.bottom_tab     = "terminal"
        self._cpu_hist      = [0.0] * 80
        self._ram_hist      = [0.0] * 80
        self._net_bytes_old = 0
        self._net_hist      = [0.0] * 80
        self._agent_running = False
        self._status_time   = ""

        # ── Build ───────────────────────────────────────
        self._configure_styles()
        self._build_ui()
        self._bind_keys()

        # ── Timers ──────────────────────────────────────
        self.after(120,  self._poll_output)
        self.after(1500, self._update_telemetry)
        self.after(800,  self._tick_status)
        self.after(300,  self._insert_sample)

    # ════════════════════════════════════════════════════
    # TTK STYLE CONFIGURATION
    # ════════════════════════════════════════════════════
    def _configure_styles(self):
        s = ttk.Style(self)
        s.theme_use("default")

        # Notebook
        s.configure("NX.TNotebook",
            background=C['void'], borderwidth=0, tabmargins=[0,0,0,0])
        s.configure("NX.TNotebook.Tab",
            background=C['tab_in'], foreground=C['text2'],
            padding=[16, 6], font=FUI, borderwidth=0)
        s.map("NX.TNotebook.Tab",
            background=[("selected", C['tab_act']), ("active", C['hover'])],
            foreground=[("selected", C['cyan']),    ("active", C['text'])])

        # Vertical scrollbar
        s.configure("NX.Vertical.TScrollbar",
            background=C['elevated'], troughcolor=C['surface'],
            borderwidth=0, relief="flat", arrowcolor=C['text3'], width=8)
        s.map("NX.Vertical.TScrollbar",
            background=[("active", C['cyan_dim'])])
        s.configure("NX.Horizontal.TScrollbar",
            background=C['elevated'], troughcolor=C['surface'],
            borderwidth=0, relief="flat", arrowcolor=C['text3'], width=8)

        # Separator
        s.configure("NX.TSeparator", background=C['sep'])

        # Entry
        s.configure("NX.TEntry",
            fieldbackground=C['elevated'], foreground=C['text'],
            borderwidth=0, relief="flat", insertcolor=C['cyan'],
            selectbackground=C['sel'], selectforeground=C['text'],
            font=FCODE)

        # Combobox
        s.configure("NX.TCombobox",
            fieldbackground=C['elevated'], background=C['elevated'],
            foreground=C['text'], arrowcolor=C['cyan'],
            selectbackground=C['sel'], selectforeground=C['text'],
            borderwidth=0, font=FUI)
        s.map("NX.TCombobox",
            fieldbackground=[("readonly", C['elevated'])],
            selectbackground=[("readonly", C['sel'])])

        # Treeview (file explorer)
        s.configure("NX.Treeview",
            background=C['panel'], foreground=C['text2'],
            fieldbackground=C['panel'], borderwidth=0,
            rowheight=22, font=FUI)
        s.configure("NX.Treeview.Heading",
            background=C['elevated'], foreground=C['cyan'],
            relief="flat", borderwidth=0, font=FUIB)
        s.map("NX.Treeview",
            background=[("selected", C['sel'])],
            foreground=[("selected", C['cyan'])])

    # ════════════════════════════════════════════════════
    # MAIN UI BUILD
    # ════════════════════════════════════════════════════
    def _build_ui(self):
        # ── Banner strip (top) ───────────────────────────
        self._build_banner()

        # ── Body (horizontal strip) ──────────────────────
        body = tk.Frame(self, bg=C['void'])
        body.pack(fill="both", expand=True)

        # Activity bar (leftmost 50px)
        self._actbar = self._build_activity_bar(body)
        self._actbar.pack(side="left", fill="y")

        # Sidebar separator line
        tk.Frame(body, bg=C['cyan_dark'], width=1).pack(side="left", fill="y")

        # Sidebar (220px)
        self._sidebar = self._build_sidebar(body)
        self._sidebar.pack(side="left", fill="y")

        # Sidebar|Editor separator
        tk.Frame(body, bg=C['sep'], width=1).pack(side="left", fill="y")

        # Center (grows)
        center = tk.Frame(body, bg=C['void'])
        center.pack(side="left", fill="both", expand=True)
        self._build_center(center)

        # Editor|Right-panel separator
        tk.Frame(body, bg=C['sep'], width=1).pack(side="left", fill="y")

        # Right panel (280px)
        self._rpanel = self._build_right_panel(body)
        self._rpanel.pack(side="left", fill="y")

        # ── Status bar ────────────────────────────────────
        self._build_status_bar()

    # ─── BANNER ──────────────────────────────────────────
    def _build_banner(self):
        banner = tk.Frame(self, bg=C['actbar'], height=40)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        # Cyan left accent line
        tk.Frame(banner, bg=C['cyan'], width=3).pack(side="left", fill="y")

        # Logo text
        logo = tk.Label(banner,
            text="  ⚡  NEXUS STUDIO",
            bg=C['actbar'], fg=C['cyan'],
            font=("Segoe UI", 12, "bold"))
        logo.pack(side="left", padx=(8, 0))

        tk.Label(banner, text="  v2.0  ·  Polymorphic IDE  ·  Kali Edition",
            bg=C['actbar'], fg=C['text2'], font=FUIS).pack(side="left")

        # Toolbar buttons (right side)
        btn_frame = tk.Frame(banner, bg=C['actbar'])
        btn_frame.pack(side="right", padx=8)

        def tbtn(txt, cmd, color=None):
            c = color or C['cyan']
            b = tk.Button(btn_frame, text=txt, command=cmd,
                bg=C['elevated'], fg=c,
                activebackground=C['hover'], activeforeground=c,
                relief="flat", borderwidth=0, cursor="hand2",
                font=FUIB, padx=10, pady=3)
            b.pack(side="left", padx=2)
            b.bind("<Enter>", lambda e: b.config(bg=C['hover']))
            b.bind("<Leave>", lambda e: b.config(bg=C['elevated']))
            return b

        self._run_btn  = tbtn("▶  RUN  F5",     self._run_code,       C['green'])
        tbtn("⚡ EVAL SEL",    self._eval_sel,       C['cyan'])
        tbtn("📂 OPEN",        self._open_file,      C['text'])
        tbtn("💾 SAVE",        self._save_file,      C['text'])
        tbtn("🔥 FORMAT",      self._format_code,    C['amber'])
        tbtn("🧹 CLEAR OUT",   self._clear_output,   C['text2'])
        self._voice_btn = tbtn("🔊 VOICE OFF",  self._toggle_voice,   C['text2'])

    # ─── ACTIVITY BAR ────────────────────────────────────
    def _build_activity_bar(self, parent):
        bar = tk.Frame(parent, bg=C['actbar'], width=50)
        bar.pack_propagate(False)

        tools = [
            ("⊞", "explorer", "File Explorer",  C['cyan']),
            ("📊", "monitor", "System Monitor", C['green']),
            ("🌐", "network", "Net Inspector",  C['amber']),
            ("⚙",  "settings","Settings",       C['text2']),
        ]

        self._actbar_btns = {}
        for icon, key, tip, col in tools:
            btn = tk.Button(bar, text=icon,
                bg=C['actbar'], fg=C['text3'],
                activebackground=C['hover'], activeforeground=col,
                relief="flat", borderwidth=0, cursor="hand2",
                font=("Segoe UI", 14),
                width=3, height=2,
                command=lambda k=key: self._switch_sidebar(k))
            btn.pack(pady=2)
            btn.bind("<Enter>", lambda e, b=btn, c=col: b.config(fg=c, bg=C['hover']))
            btn.bind("<Leave>", lambda e, b=btn, k2=key: b.config(
                fg=C['cyan'] if self.active_tool.get()==k2 else C['text3'],
                bg=C['actbar']))
            self._actbar_btns[key] = (btn, col)

        # Separator
        tk.Frame(bar, bg=C['sep'], height=1).pack(fill="x", pady=4)

        # Run quick-button at bottom
        run_btn = tk.Button(bar, text="▶",
            bg=C['actbar'], fg=C['green'],
            activebackground=C['hover'], activeforeground=C['green2'],
            relief="flat", borderwidth=0, cursor="hand2",
            font=("Segoe UI", 16), width=3, height=2,
            command=self._run_code)
        run_btn.pack(side="bottom", pady=4)
        run_btn.bind("<Enter>", lambda e: run_btn.config(bg=C['hover']))
        run_btn.bind("<Leave>", lambda e: run_btn.config(bg=C['actbar']))

        self._update_actbar("explorer")
        return bar

    def _switch_sidebar(self, key):
        self.active_tool.set(key)
        self._update_actbar(key)
        for k, frame in self._sidebar_panels.items():
            frame.pack_forget()
        if key in self._sidebar_panels:
            self._sidebar_panels[key].pack(fill="both", expand=True)

    def _update_actbar(self, active):
        for key, (btn, col) in self._actbar_btns.items():
            if key == active:
                btn.config(fg=col, bg=C['elevated'])
            else:
                btn.config(fg=C['text3'], bg=C['actbar'])

    # ─── SIDEBAR ─────────────────────────────────────────
    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=C['sidebar'], width=220)
        sidebar.pack_propagate(False)
        self._sidebar_panels = {}

        # ── Explorer Panel ────────────────────────────────
        exp = tk.Frame(sidebar, bg=C['sidebar'])
        self._sidebar_panels["explorer"] = exp

        hdr = tk.Frame(exp, bg=C['elevated'], height=28)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['cyan'], width=2).pack(side="left", fill="y")
        tk.Label(hdr, text="  EXPLORER & EXAMPLES", bg=C['elevated'],
            fg=C['cyan'], font=FUIB).pack(side="left", pady=4)

        # Examples list
        ex_lbl = tk.Label(exp, text="  ⚡ Built-In Examples",
            bg=C['sidebar'], fg=C['purple2'], font=FUIB)
        ex_lbl.pack(anchor="w", pady=(8,2))

        for name, code in EXAMPLES.items():
            def _load(c=code, n=name):
                self._editor.delete("1.0", "end")
                self._editor.insert("1.0", c)
                self._highlight()
                self._update_line_numbers()
                self._append_out(f"  📄 Loaded: {n}\n", "info")
            btn = tk.Button(exp, text=f"  {name}",
                bg=C['sidebar'], fg=C['text2'], anchor="w",
                activebackground=C['hover'], activeforeground=C['cyan'],
                relief="flat", borderwidth=0, cursor="hand2",
                font=FUI, command=_load)
            btn.pack(fill="x", padx=4, pady=1)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=C['hover'], fg=C['cyan']))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=C['sidebar'], fg=C['text2']))

        # File tree separator
        tk.Frame(exp, bg=C['sep'], height=1).pack(fill="x", pady=6)
        tk.Label(exp, text="  📁 Open Folder",
            bg=C['sidebar'], fg=C['text2'], font=FUIS).pack(anchor="w")
        fopen = tk.Button(exp, text="  Browse...",
            bg=C['elevated'], fg=C['cyan'], anchor="w",
            activebackground=C['hover'], activeforeground=C['cyan'],
            relief="flat", borderwidth=0, cursor="hand2",
            font=FUI, command=self._open_file)
        fopen.pack(fill="x", padx=4, pady=2)

        # ── AI Panel ──────────────────────────────────────
        ai_s = tk.Frame(sidebar, bg=C['sidebar'])
        self._sidebar_panels["ai"] = ai_s
        tk.Label(ai_s, text="  🤖 AI CODE ASSISTANT", bg=C['elevated'],
            fg=C['purple2'], font=FUIB).pack(fill="x", pady=4)
        tk.Label(ai_s, text="  Ask AI about your code\n  or request code gen.",
            bg=C['sidebar'], fg=C['text2'], font=FUIS, justify="left").pack(anchor="w", padx=4)

        # ── Monitor sidebar ────────────────────────────────
        mon_s = tk.Frame(sidebar, bg=C['sidebar'])
        self._sidebar_panels["monitor"] = mon_s
        tk.Label(mon_s, text="  📊 SYSTEM MONITOR", bg=C['elevated'],
            fg=C['green'], font=FUIB).pack(fill="x", pady=4)
        tk.Label(mon_s, text="  Live metrics displayed\n  in the right panel →",
            bg=C['sidebar'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4)

        # ── Network sidebar ───────────────────────────────
        net_s = tk.Frame(sidebar, bg=C['sidebar'])
        self._sidebar_panels["network"] = net_s
        tk.Label(net_s, text="  🌐 NETWORK INSPECTOR", bg=C['elevated'],
            fg=C['amber'], font=FUIB).pack(fill="x", pady=4)
        tk.Label(net_s, text="  HTTP Inspector in the\n  bottom panel (NET tab).",
            bg=C['sidebar'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4)

        # ── Settings sidebar ──────────────────────────────
        set_s = tk.Frame(sidebar, bg=C['sidebar'])
        self._sidebar_panels["settings"] = set_s
        tk.Label(set_s, text="  ⚙ SETTINGS", bg=C['elevated'],
            fg=C['text'], font=FUIB).pack(fill="x", pady=4)
        tk.Label(set_s, text="  Font size, theme, and\n  voice settings below.",
            bg=C['sidebar'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4)
        tk.Button(set_s, text="  🔊 Toggle Voice",
            bg=C['elevated'], fg=C['text2'],
            activebackground=C['hover'], activeforeground=C['cyan'],
            relief="flat", borderwidth=0, cursor="hand2",
            font=FUI, command=self._toggle_voice).pack(fill="x", padx=4, pady=2)
        tk.Button(set_s, text="  🔆 Increase Font",
            bg=C['elevated'], fg=C['text2'],
            activebackground=C['hover'], activeforeground=C['amber'],
            relief="flat", borderwidth=0, cursor="hand2",
            font=FUI, command=lambda: self._change_font(1)).pack(fill="x", padx=4, pady=2)
        tk.Button(set_s, text="  🔅 Decrease Font",
            bg=C['elevated'], fg=C['text2'],
            activebackground=C['hover'], activeforeground=C['amber'],
            relief="flat", borderwidth=0, cursor="hand2",
            font=FUI, command=lambda: self._change_font(-1)).pack(fill="x", padx=4, pady=2)

        # Show explorer by default
        self._sidebar_panels["explorer"].pack(fill="both", expand=True)
        return sidebar

    # ─── CENTER (toolbar + editor + bottom) ──────────────
    def _build_center(self, parent):
        pane = tk.PanedWindow(parent, orient="vertical",
            bg=C['sep'], sashwidth=3, sashpad=0,
            sashrelief="flat", showhandle=False)
        pane.pack(fill="both", expand=True)

        editor_frame = tk.Frame(pane, bg=C['base'])
        self._build_editor(editor_frame)
        pane.add(editor_frame, minsize=200)

        bottom = tk.Frame(pane, bg=C['void'])
        self._build_bottom_panel(bottom)
        pane.add(bottom, minsize=150)

        pane.paneconfigure(editor_frame, stretch="always")
        pane.paneconfigure(bottom,       stretch="never")

    # ─── CODE EDITOR ─────────────────────────────────────
    def _build_editor(self, parent):
        self._font_size = 11

        hdr = tk.Frame(parent, bg=C['elevated'], height=26)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['cyan'], width=2).pack(side="left", fill="y")
        self._file_lbl = tk.Label(hdr, text="  untitled.nx",
            bg=C['elevated'], fg=C['text2'], font=FUIS)
        self._file_lbl.pack(side="left")
        self._status_lbl = tk.Label(hdr, text="  Nexus Engine: ✅ Ready" if NEXUS_OK else "  ⚠ Engine unavailable",
            bg=C['elevated'], fg=C['green'] if NEXUS_OK else C['red'], font=FUIS)
        self._status_lbl.pack(side="right", padx=8)
        self._cursor_lbl = tk.Label(hdr, text="Ln 1, Col 1",
            bg=C['elevated'], fg=C['text2'], font=FUIS)
        self._cursor_lbl.pack(side="right", padx=12)

        row = tk.Frame(parent, bg=C['base'])
        row.pack(fill="both", expand=True)

        self._ln_canvas = tk.Canvas(row, bg=C['gutter'], width=54,
            highlightthickness=0, bd=0)
        self._ln_canvas.pack(side="left", fill="y")
        tk.Frame(row, bg=C['border'], width=1).pack(side="left", fill="y")

        self._editor = tk.Text(row,
            bg=C['base'], fg=C['code'],
            insertbackground=C['cyan'], insertwidth=2,
            selectbackground=C['sel'], selectforeground=C['text'],
            relief="flat", borderwidth=0,
            font=FCODE, tabs="28p",
            undo=True, autoseparators=True, maxundo=200,
            wrap="none",
        )
        self._editor.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(row, orient="vertical", style="NX.Vertical.TScrollbar",
            command=self._on_editor_yscroll)
        vsb.pack(side="right", fill="y")
        self._editor.config(yscrollcommand=lambda *a: (vsb.set(*a), self._update_line_numbers()))
        self._ln_canvas.bind("<MouseWheel>", lambda e: self._editor.yview_scroll(-1*(e.delta//120), "units"))

        self._setup_syntax_tags()

        self._editor.bind("<KeyRelease>",   self._on_key)
        self._editor.bind("<ButtonRelease>",self._on_key)
        self._editor.bind("<Return>",       self._auto_indent, "+")

    def _on_editor_yscroll(self, *args):
        self._editor.yview(*args)
        self._update_line_numbers()

    def _setup_syntax_tags(self):
        self._editor.tag_configure("kw",    foreground=C['syn_kw'])
        self._editor.tag_configure("ctrl",  foreground=C['syn_ctrl'])
        self._editor.tag_configure("fn",    foreground=C['syn_fn'])
        self._editor.tag_configure("str",   foreground=C['syn_str'])
        self._editor.tag_configure("num",   foreground=C['syn_num'])
        self._editor.tag_configure("cmt",   foreground=C['syn_cmt'])
        self._editor.tag_configure("type",  foreground=C['syn_type'])
        self._editor.tag_configure("op",    foreground=C['syn_op'])
        self._editor.tag_configure("const", foreground=C['syn_const'])

    def _highlight(self):
        ed = self._editor
        code = ed.get("1.0", "end-1c")
        all_tags = ["kw","ctrl","fn","str","num","cmt","type","op","const"]
        for t in all_tags:
            ed.tag_remove(t, "1.0", "end")

        def apply(pattern, tag, flags=0):
            for m in re.finditer(pattern, code, flags):
                s = f"1.0+{m.start()}c"
                e = f"1.0+{m.end()}c"
                ed.tag_add(tag, s, e)

        apply(r'//[^\n]*',                             "cmt")
        apply(r'/\*[\s\S]*?\*/',                       "cmt")
        apply(r'"(?:[^"\\]|\\.)*"',                    "str")
        apply(r"'(?:[^'\\]|\\.)*'",                    "str")
        apply(r'\b\d+(\.\d+)?\b',                      "num")
        apply(r'\b(let|fn|return|true|false|null)\b',  "kw")
        apply(r'\b(if|else|for|while|break|continue|parallel|in|import)\b', "ctrl")
        apply(r'\b(os|fs|http|ai|json|net|sys|thread|async|await)\b', "type")
        apply(r'\b([a-zA-Z_]\w*)\s*(?=\()',             "fn")
        apply(r'[+\-*/%=<>!&|^~]+',                    "op")

    def _update_line_numbers(self, event=None):
        c  = self._ln_canvas
        ed = self._editor
        c.delete("all")
        i = ed.index("@0,0")
        while True:
            dline = ed.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            ln = str(i).split(".")[0]
            cur = ed.index("insert").split(".")[0]
            col = C['cyan'] if ln == cur else C['text3']
            c.create_text(48, y+7, anchor="e", text=ln, fill=col, font=("Consolas", 9))
            i = ed.index(f"{i}+1line")
            if i == ed.index(f"{i}+0c"):
                break

    def _on_key(self, event=None):
        self._highlight()
        self._update_line_numbers()
        pos = self._editor.index("insert")
        ln, col = pos.split(".")
        self._cursor_lbl.config(text=f"Ln {ln}, Col {int(col)+1}")

    def _auto_indent(self, event):
        ed = self._editor
        line = ed.get("insert linestart", "insert lineend")
        stripped = line.lstrip()
        indent = line[:len(line)-len(stripped)]
        if stripped.endswith("{"):
            indent += "    "
        ed.insert("insert", f"\n{indent}")
        return "break"

    # ─── BOTTOM PANEL ─────────────────────────────────────
    def _build_bottom_panel(self, parent):
        tabs_bar = tk.Frame(parent, bg=C['actbar'], height=32)
        tabs_bar.pack(fill="x"); tabs_bar.pack_propagate(False)
        tk.Frame(tabs_bar, bg=C['sep'], height=1).pack(side="top", fill="x")

        self._bottom_content = tk.Frame(parent, bg=C['void'])
        self._bottom_content.pack(fill="both", expand=True)

        self._bot_tabs  = {}
        self._bot_btns  = {}

        def make_tab(key, label, color=C['text2']):
            btn = tk.Button(tabs_bar, text=f"  {label}  ",
                bg=C['actbar'], fg=C['text2'],
                activebackground=C['hover'], activeforeground=color,
                relief="flat", borderwidth=0, cursor="hand2",
                font=FUIB if key==self.bottom_tab else FUI,
                command=lambda k=key: self._switch_bottom(k))
            btn.pack(side="left")
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(fg=c, bg=C['hover']))
            btn.bind("<Leave>", lambda e, b=btn, k2=key: b.config(
                fg=color if k2==self.bottom_tab else C['text2'],
                bg=C['actbar']))
            self._bot_btns[key] = (btn, color)
            return btn

        make_tab("terminal", "💻 TERMINAL",    C['green'])
        make_tab("ast",      "🔍 AST TOKENS",  C['cyan'])
        make_tab("telemetry","📊 TELEMETRY",   C['purple2'])
        make_tab("network",  "🌐 NETWORK",     C['amber'])

        # Terminal
        term_frame = tk.Frame(self._bottom_content, bg=C['void'])
        self._terminal = tk.Text(term_frame,
            bg="#020209", fg=C['green'],
            insertbackground=C['green'], insertwidth=2,
            selectbackground=C['sel'],
            relief="flat", borderwidth=0,
            font=FMONO2, wrap="none", state="disabled")
        self._terminal.pack(side="left", fill="both", expand=True)
        tsb = ttk.Scrollbar(term_frame, orient="vertical", style="NX.Vertical.TScrollbar", command=self._terminal.yview)
        tsb.pack(side="right", fill="y")
        self._terminal.config(yscrollcommand=tsb.set)
        self._setup_term_tags()
        self._bot_tabs["terminal"] = term_frame

        # AST
        ast_frame = tk.Frame(self._bottom_content, bg=C['void'])
        self._ast_out = tk.Text(ast_frame, bg=C['panel'], fg=C['type'], relief="flat", borderwidth=0, font=FMONO, wrap="none", state="disabled")
        self._ast_out.pack(side="left", fill="both", expand=True)
        asb = ttk.Scrollbar(ast_frame, orient="vertical", style="NX.Vertical.TScrollbar", command=self._ast_out.yview)
        asb.pack(side="right", fill="y")
        self._ast_out.config(yscrollcommand=asb.set)
        btn_ast = tk.Button(ast_frame, text="  🔍 Inspect AST", bg=C['elevated'], fg=C['cyan'], font=FUI, relief="flat", borderwidth=0, cursor="hand2", command=self._inspect_ast)
        btn_ast.pack(anchor="nw", padx=4, pady=4)
        self._bot_tabs["ast"] = ast_frame

        # Telemetry
        tel_frame = tk.Frame(self._bottom_content, bg=C['void'])
        self._tel_canvas = tk.Canvas(tel_frame, bg=C['base'], highlightthickness=0, bd=0)
        self._tel_canvas.pack(fill="both", expand=True)
        self._bot_tabs["telemetry"] = tel_frame

        # Network
        net_frame = self._build_network_tab(self._bottom_content)
        self._bot_tabs["network"] = net_frame

        self._switch_bottom("terminal")

    def _setup_term_tags(self):
        t = self._terminal
        t.tag_configure("info",    foreground=C['cyan'])
        t.tag_configure("success", foreground=C['green'])
        t.tag_configure("error",   foreground=C['red'])
        t.tag_configure("warn",    foreground=C['amber'])
        t.tag_configure("ai",      foreground=C['purple2'])
        t.tag_configure("dim",     foreground=C['text3'])
        t.tag_configure("prompt",  foreground=C['green2'])
        t.tag_configure("normal",  foreground=C['text'])

    def _switch_bottom(self, key):
        self.bottom_tab = key
        for k, frame in self._bot_tabs.items():
            frame.pack_forget()
        self._bot_tabs[key].pack(fill="both", expand=True)
        for k, (btn, col) in self._bot_btns.items():
            if k == key:
                btn.config(fg=col, font=FUIB, bg=C['elevated'])
            else:
                btn.config(fg=C['text2'], font=FUI, bg=C['actbar'])

    def _build_network_tab(self, parent):
        frame = tk.Frame(parent, bg=C['panel'])

        top = tk.Frame(frame, bg=C['elevated'], height=36)
        top.pack(fill="x"); top.pack_propagate(False)
        tk.Frame(top, bg=C['amber'], width=2).pack(side="left", fill="y")
        tk.Label(top, text="  🌐 HTTP REQUEST INSPECTOR", bg=C['elevated'], fg=C['amber'], font=FUIB).pack(side="left", padx=6)

        row1 = tk.Frame(frame, bg=C['panel'])
        row1.pack(fill="x", padx=6, pady=4)

        self._net_method = ttk.Combobox(row1, values=["GET","POST","PUT","DELETE","PATCH","HEAD"], width=8, font=FUI, style="NX.TCombobox", state="readonly")
        self._net_method.set("GET")
        self._net_method.pack(side="left", padx=(0,4))

        url_outer = tk.Frame(row1, bg=C['cyan'], padx=1, pady=1)
        url_outer.pack(side="left", fill="x", expand=True, padx=(0,4))
        self._net_url = tk.Entry(url_outer, bg=C['elevated'], fg=C['text'], insertbackground=C['cyan'], relief="flat", borderwidth=0, font=FMONO2)
        self._net_url.pack(fill="both", expand=True, padx=4, pady=2)
        self._net_url.insert(0, "https://httpbin.org/get")

        send_btn = tk.Button(row1, text="  ⚡ SEND", bg=C['amber'], fg=C['void'], activebackground="#CC9200", activeforeground=C['void'], relief="flat", borderwidth=0, cursor="hand2", font=FUIB, padx=10, command=self._send_request)
        send_btn.pack(side="left")

        row2 = tk.Frame(frame, bg=C['panel'])
        row2.pack(fill="x", padx=6, pady=(0,4))
        tk.Label(row2, text="Headers (JSON):", bg=C['panel'], fg=C['text2'], font=FUIS).pack(side="left")
        self._net_headers = tk.Entry(row2, bg=C['elevated'], fg=C['text'], insertbackground=C['cyan'], relief="flat", borderwidth=0, font=FMONO, width=30)
        self._net_headers.pack(side="left", padx=4)
        self._net_headers.insert(0, '{"Content-Type":"application/json"}')
        tk.Label(row2, text="Body:", bg=C['panel'], fg=C['text2'], font=FUIS).pack(side="left", padx=(8,2))
        self._net_body = tk.Entry(row2, bg=C['elevated'], fg=C['text'], insertbackground=C['cyan'], relief="flat", borderwidth=0, font=FMONO, width=24)
        self._net_body.pack(side="left")

        resp_row = tk.Frame(frame, bg=C['void'])
        resp_row.pack(fill="both", expand=True, padx=6, pady=(0,4))

        self._net_resp = tk.Text(resp_row, bg=C['base'], fg=C['text'], relief="flat", borderwidth=0, font=FMONO, wrap="none", state="disabled")
        self._net_resp.pack(side="left", fill="both", expand=True)
        nsb = ttk.Scrollbar(resp_row, orient="vertical", style="NX.Vertical.TScrollbar", command=self._net_resp.yview)
        nsb.pack(side="right", fill="y")
        self._net_resp.config(yscrollcommand=nsb.set)

        return frame

    # ─── RIGHT PANEL ──────────────────────────────────────
    def _build_right_panel(self, parent):
        panel = tk.Frame(parent, bg=C['panel'], width=295)
        panel.pack_propagate(False)

        nb = ttk.Notebook(panel, style="NX.TNotebook")
        nb.pack(fill="both", expand=True)

        mon_frame = tk.Frame(nb, bg=C['panel'])
        nb.add(mon_frame, text="  📊 Monitor  ")
        self._build_monitor_panel(mon_frame)

        agent_frame = tk.Frame(nb, bg=C['panel'])
        nb.add(agent_frame, text="  ⚙ Agent  ")
        self._build_agent_panel(agent_frame)

        return panel

    def _build_agent_panel(self, parent):
        hdr = tk.Frame(parent, bg=C['elevated'], height=28)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['green'], width=2).pack(side="left", fill="y")
        tk.Label(hdr, text="  AUTONOMOUS AGENT", bg=C['elevated'], fg=C['green'], font=FUIB).pack(side="left", pady=4)

        tk.Label(parent, text="  Task Description:", bg=C['panel'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4, pady=(6,2))

        task_outer = tk.Frame(parent, bg=C['green'], padx=1, pady=1)
        task_outer.pack(fill="x", padx=4)
        self._agent_task = tk.Text(task_outer, bg=C['elevated'], fg=C['text'], insertbackground=C['green'], relief="flat", borderwidth=0, font=FMONO, height=4, wrap="word")
        self._agent_task.pack(fill="x")
        self._agent_task.insert("1.0","Describe the autonomous task...\ne.g: scan system, list files, check network")

        presets_lbl = tk.Label(parent, text="  Quick Presets:", bg=C['panel'], fg=C['text2'], font=FUIS)
        presets_lbl.pack(anchor="w", padx=4, pady=(6,2))

        presets = [
            ("🖥 System Audit",   "Audit the system: show OS info, CPU, RAM, disk."),
            ("🌐 Network Scan",   "Check network: resolve hostname, test connectivity."),
            ("📁 File Inventory", "List all .nx files in current directory with sizes."),
        ]
        for label, task in presets:
            def _preset(t=task):
                self._agent_task.delete("1.0","end")
                self._agent_task.insert("1.0", t)
            b = tk.Button(parent, text=f"  {label}", bg=C['elevated'], fg=C['green2'], anchor="w", activebackground=C['hover'], activeforeground=C['green'], relief="flat", borderwidth=0, cursor="hand2", font=FUI, command=_preset)
            b.pack(fill="x", padx=4, pady=1)
            b.bind("<Enter>", lambda e, b2=b: b2.config(bg=C['hover']))
            b.bind("<Leave>", lambda e, b2=b: b2.config(bg=C['elevated']))

        deploy_outer = tk.Frame(parent, bg=C['green2'], padx=1, pady=1)
        deploy_outer.pack(fill="x", padx=4, pady=6)
        self._deploy_btn = tk.Button(deploy_outer, text="  🚀  DEPLOY AGENT", bg=C['elevated'], fg=C['green'], activebackground=C['hover'], activeforeground=C['green2'], relief="flat", borderwidth=0, cursor="hand2", font=FUIB, pady=5, command=self._deploy_agent)
        self._deploy_btn.pack(fill="x")

        tk.Label(parent, text="  Agent Log:", bg=C['panel'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4, pady=(4,2))
        log_frame = tk.Frame(parent, bg=C['void'])
        log_frame.pack(fill="both", expand=True, padx=4, pady=(0,4))
        self._agent_log = tk.Text(log_frame, bg="#020809", fg=C['green2'], relief="flat", borderwidth=0, font=FMONO, wrap="word", state="disabled")
        self._agent_log.pack(side="left", fill="both", expand=True)
        agsb = ttk.Scrollbar(log_frame, orient="vertical", style="NX.Vertical.TScrollbar", command=self._agent_log.yview)
        agsb.pack(side="right", fill="y")
        self._agent_log.config(yscrollcommand=agsb.set)
        self._agent_log.tag_configure("info",  foreground=C['cyan'])
        self._agent_log.tag_configure("ok",    foreground=C['green'])
        self._agent_log.tag_configure("warn",  foreground=C['amber'])
        self._agent_log.tag_configure("err",   foreground=C['red'])
        self._agent_log_write(f"  ◉ Agent standby. Deploy a task to begin.\n", "info")

    def _build_monitor_panel(self, parent):
        hdr = tk.Frame(parent, bg=C['elevated'], height=28)
        hdr.pack(fill="x"); hdr.pack_propagate(False)
        tk.Frame(hdr, bg=C['green'], width=2).pack(side="left", fill="y")
        tk.Label(hdr, text="  LIVE SYSTEM MONITOR", bg=C['elevated'], fg=C['green'], font=FUIB).pack(side="left", pady=4)

        stat_frame = tk.Frame(parent, bg=C['panel'])
        stat_frame.pack(fill="x", padx=4, pady=4)

        def stat_row(label, var_name, color):
            row = tk.Frame(stat_frame, bg=C['panel'])
            row.pack(fill="x", pady=1)
            tk.Label(row, text=f" {label}", bg=C['panel'], fg=C['text2'], font=FUIS, width=14, anchor="w").pack(side="left")
            lbl = tk.Label(row, text="--", bg=C['panel'], fg=color, font=FUIB)
            lbl.pack(side="left")
            setattr(self, var_name, lbl)

        stat_row("CPU Usage:",  "_mon_cpu",  C['cyan'])
        stat_row("RAM Usage:",  "_mon_ram",  C['purple2'])
        stat_row("Disk Read:",  "_mon_disk", C['amber'])
        stat_row("Net Speed:",  "_mon_net",  C['green'])
        stat_row("Platform:",   "_mon_os",   C['text'])
        stat_row("Uptime:",     "_mon_up",   C['text2'])

        self._mon_os.config(text=platform.system()[:18])

        tk.Label(parent, text="  CPU (cyan) / RAM (purple) history:", bg=C['panel'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4)
        self._mon_canvas = tk.Canvas(parent, bg=C['base'], highlightthickness=1, highlightbackground=C['border2'], height=120)
        self._mon_canvas.pack(fill="x", padx=4, pady=2)

        tk.Frame(parent, bg=C['sep'], height=1).pack(fill="x", pady=4)
        tk.Label(parent, text="  🖥 Process Info:", bg=C['panel'], fg=C['text2'], font=FUIS).pack(anchor="w", padx=4)
        self._proc_info = tk.Text(parent, bg=C['base'], fg=C['text2'], relief="flat", borderwidth=0, font=FMONO, height=5, state="disabled")
        self._proc_info.pack(fill="x", padx=4, pady=2)

    # ─── STATUS BAR ──────────────────────────────────────
    def _build_status_bar(self):
        bar = tk.Frame(self, bg=C['status'], height=26)
        bar.pack(fill="x", side="bottom"); bar.pack_propagate(False)
        tk.Frame(bar, bg=C['cyan'], width=2).pack(side="left", fill="y")

        self._sb_engine = tk.Label(bar, text="  ⚡ NEXUS ENGINE  ✅ Ready" if NEXUS_OK else "  ⚡ NEXUS ENGINE  ⚠ Offline", bg=C['status'], fg=C['green'] if NEXUS_OK else C['red'], font=FUIS)
        self._sb_engine.pack(side="left", padx=8)

        tk.Frame(bar, bg=C['sep'], width=1).pack(side="left", fill="y", padx=4)
        self._sb_file = tk.Label(bar, text="  untitled.nx", bg=C['status'], fg=C['text2'], font=FUIS)
        self._sb_file.pack(side="left")

        self._sb_time = tk.Label(bar, text="", bg=C['status'], fg=C['cyan'], font=FUIS)
        self._sb_time.pack(side="right", padx=12)

        self._sb_cpu = tk.Label(bar, text="CPU: --%", bg=C['status'], fg=C['text2'], font=FUIS)
        self._sb_cpu.pack(side="right", padx=8)

        self._sb_ram = tk.Label(bar, text="RAM: --%", bg=C['status'], fg=C['text2'], font=FUIS)
        self._sb_ram.pack(side="right", padx=8)

        tk.Label(bar, text="  nexus@studio:~$  ", bg=C['cyan_dark'], fg=C['cyan'], font=FUIB).pack(side="right")

    # ════════════════════════════════════════════════════════
    # EXECUTION ENGINE
    # ════════════════════════════════════════════════════════
    def _run_code(self):
        if self.is_running:
            self._append_out("  ⚠ Already running. Wait...\n", "warn")
            return
        self._switch_bottom("terminal")
        code = self._editor.get("1.0", "end-1c").strip()
        if not code:
            self._append_out("  ⚠ Nothing to run.\n", "warn"); return

        self._clear_output()
        self._append_out("  ╔══════════════════════════════════════════════╗\n", "dim")
        self._append_out("  ║  ⚡ NEXUS EXECUTION ENGINE  —  Running...    ║\n", "info")
        self._append_out("  ╚══════════════════════════════════════════════╝\n", "dim")
        self._append_out(f"  nexus@studio:~$ nexus run\n\n", "prompt")

        self.is_running = True
        self._run_btn.config(text="⏹ STOP", fg=C['red'])
        self.voice.say("Running Nexus script.")

        threading.Thread(target=self._exec_worker, args=(code,), daemon=True).start()

    def _exec_worker(self, code):
        buf = io.StringIO()
        old_out, old_err = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = buf
        start = time.time()
        try:
            if not NEXUS_OK:
                raise RuntimeError(f"Nexus engine unavailable: {NEXUS_ERR}")
            lex  = Lexer(code)
            toks = lex.tokenize()
            ast  = Parser(toks).parse()
            Interpreter().interpret(ast)
            elapsed = time.time() - start
            output = buf.getvalue()
            self.output_queue.put(("output", output))
            self.output_queue.put(("success", f"\n  ✅ Execution completed in {elapsed*1000:.2f} ms.\n"))
        except Exception as ex:
            elapsed = time.time() - start
            output = buf.getvalue()
            if output:
                self.output_queue.put(("output", output))
            self.output_queue.put(("error", f"\n  ❌ Error: {ex}\n"))
        finally:
            sys.stdout, sys.stderr = old_out, old_err
            self.output_queue.put(("done", None))

    def _eval_sel(self):
        try:
            code = self._editor.get("sel.first", "sel.last").strip()
        except tk.TclError:
            self._append_out("  ⚠ No text selected. Select code first.\n", "warn"); return
        self._clear_output()
        self._append_out(f"  ⚡ Evaluating selection...\n\n", "info")
        self.is_running = True
        threading.Thread(target=self._exec_worker, args=(code,), daemon=True).start()

    def _poll_output(self):
        while not self.output_queue.empty():
            kind, data = self.output_queue.get_nowait()
            if kind == "output":
                for line in data.split("\n"):
                    tag = "normal"
                    if any(c in line for c in ["✅","✓","success","done","complete"]):
                        tag = "success"
                    elif any(c in line for c in ["❌","error","failed","exception"]):
                        tag = "error"
                    elif any(c in line for c in ["⚠","warning","warn"]):
                        tag = "warn"
                    elif any(c in line for c in ["🤖","AI Response","ai."]):
                        tag = "ai"
                    elif any(c in line for c in ["⚡","→","[Worker","parallel"]):
                        tag = "info"
                    self._append_out(line + "\n", tag)
            elif kind == "success":
                self._append_out(data, "success")
                self.voice.say("Execution complete.")
            elif kind == "error":
                self._append_out(data, "error")
                self.voice.say("Execution error.")
            elif kind == "done":
                self.is_running = False
                self._run_btn.config(text="▶  RUN  F5", fg=C['green'])
        self.after(100, self._poll_output)

    def _append_out(self, text, tag="normal"):
        t = self._terminal
        t.config(state="normal")
        t.insert("end", text, tag)
        t.see("end")
        t.config(state="disabled")

    def _clear_output(self):
        t = self._terminal
        t.config(state="normal")
        t.delete("1.0", "end")
        t.config(state="disabled")

    # ════════════════════════════════════════════════════════
    # AST INSPECTOR
    # ════════════════════════════════════════════════════════
    def _inspect_ast(self):
        code = self._editor.get("1.0", "end-1c").strip()
        self._ast_out.config(state="normal")
        self._ast_out.delete("1.0", "end")
        if not NEXUS_OK:
            self._ast_out.insert("end", f"  ❌ Nexus engine unavailable.\n")
            self._ast_out.config(state="disabled"); return
        try:
            toks = Lexer(code).tokenize()
            self._ast_out.insert("end", "  ┌─── TOKEN STREAM ──────────────────────\n")
            for i, tok in enumerate(toks[:80]):
                self._ast_out.insert("end", f"  │  [{i:3d}]  {str(tok.type):<20} {repr(tok.value)}\n")
            if len(toks) > 80:
                self._ast_out.insert("end", f"  │  ... +{len(toks)-80} more tokens\n")
            self._ast_out.insert("end", "  └─────────────────────────────────────\n\n")
            ast = Parser(toks).parse()
            self._ast_out.insert("end", "  ┌─── AST NODES ─────────────────────────\n")
            for node in ast[:30]:
                self._ast_out.insert("end", f"  │  {repr(node)[:80]}\n")
            self._ast_out.insert("end", "  └─────────────────────────────────────\n")
        except Exception as ex:
            self._ast_out.insert("end", f"  ❌ AST Error: {ex}\n")
        self._ast_out.config(state="disabled")



    # ════════════════════════════════════════════════════════
    # AUTONOMOUS AGENT
    # ════════════════════════════════════════════════════════
    def _deploy_agent(self):
        if self._agent_running:
            self._agent_log_write("  ⚠ Agent already running.\n", "warn"); return
        task = self._agent_task.get("1.0","end").strip()
        if not task or "Describe the autonomous task" in task: return
        self._agent_running = True
        self._deploy_btn.config(text="  ⏳ RUNNING...", fg=C['amber'])
        self._agent_log_write(f"\n  ╔═══════════════════════════════╗\n", "ok")
        self._agent_log_write(f"  ║  🚀 AGENT DEPLOYED            ║\n", "ok")
        self._agent_log_write(f"  ╚═══════════════════════════════╝\n", "ok")
        self._agent_log_write(f"  Task: {task[:60]}\n\n", "info")
        threading.Thread(target=self._agent_worker, args=(task,), daemon=True).start()

    def _agent_worker(self, task):
        steps = [
            ("Initializing agent context...",     0.4),
            ("Parsing task requirements...",       0.5),
            ("Loading Nexus runtime modules...",   0.4),
            ("Executing autonomous pipeline...",   0.8),
        ]
        for msg, delay in steps:
            self.after(0, self._agent_log_write, f"  ◈ {msg}\n", "info")
            time.sleep(delay)

        task_l = task.lower()
        if "system" in task_l or "audit" in task_l or "cpu" in task_l:
            nx = 'let s = os.system_info(); print("OS: {s.platform}"); print("CPU: {s.cpu_usage_percent}%"); print("RAM: {s.ram_percent}%");'
        elif "file" in task_l or "list" in task_l or "directory" in task_l:
            nx = 'let files = fs.list_dir("."); print("Files: {files}");'
        elif "network" in task_l or "http" in task_l:
            nx = 'let r = http.get("https://httpbin.org/get"); print("Status: {r.status}");'
        else:
            nx = f'print("Agent executing: {task[:60]}..."); print("✅ Task processed via Nexus autonomous engine.");'

        buf = io.StringIO()
        old = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = buf
        try:
            if NEXUS_OK:
                Interpreter().execute(Parser(Lexer(nx).tokenize()).parse())
            result = buf.getvalue() or "Task completed."
        except Exception as ex:
            result = f"Error: {ex}"
        finally:
            sys.stdout, sys.stderr = old

        self.after(0, self._agent_log_write, f"\n  ─── OUTPUT ───\n{result}\n", "ok")
        self.after(0, self._agent_log_write, "  ✅ Agent mission complete.\n\n", "ok")
        self.after(0, lambda: self._deploy_btn.config(text="  🚀  DEPLOY AGENT", fg=C['green']))
        self._agent_running = False

    def _agent_log_write(self, text, tag="info"):
        self._agent_log.config(state="normal")
        self._agent_log.insert("end", text, tag)
        self._agent_log.see("end")
        self._agent_log.config(state="disabled")

    # ════════════════════════════════════════════════════════
    # NETWORK INSPECTOR
    # ════════════════════════════════════════════════════════
    def _send_request(self):
        url    = self._net_url.get().strip()
        method = self._net_method.get()
        body   = self._net_body.get().strip()
        headers_raw = self._net_headers.get().strip()

        self._net_resp.config(state="normal")
        self._net_resp.delete("1.0","end")
        self._net_resp.insert("end", f"  ⚡ {method} {url}\n\n")
        self._net_resp.config(state="disabled")
        threading.Thread(target=self._http_worker,
            args=(method, url, headers_raw, body), daemon=True).start()

    def _http_worker(self, method, url, headers_raw, body):
        try:
            try: headers = json.loads(headers_raw) if headers_raw else {}
            except: headers = {}
            data = body.encode() if body else None
            req  = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read()
                try:    text = raw.decode('utf-8')
                except: text = raw.decode('latin-1')
                status = resp.status
                hdrs   = dict(resp.headers)
                result = (f"  ✅ HTTP {status}\n"
                          f"  ─── Response Headers ────────────────\n")
                for k, v in list(hdrs.items())[:8]:
                    result += f"  {k}: {v}\n"
                result += f"\n  ─── Body ────────────────────────────\n"
                try:
                    parsed = json.dumps(json.loads(text), indent=2)
                    result += parsed[:3000]
                except:
                    result += text[:3000]
        except Exception as ex:
            result = f"  ❌ Request failed: {ex}"
        self.after(0, lambda r=result: self._show_net_resp(r))

    def _show_net_resp(self, text):
        self._net_resp.config(state="normal")
        self._net_resp.delete("1.0","end")
        self._net_resp.insert("end", text)
        self._net_resp.config(state="disabled")
        self._switch_bottom("network")

    # ════════════════════════════════════════════════════════
    # TELEMETRY — Live Canvas Charts
    # ════════════════════════════════════════════════════════
    def _update_telemetry(self):
        cpu = ram = disk_r = net_s = 0.0
        if HAS_PSUTIL:
            try:
                cpu   = psutil.cpu_percent(interval=None)
                ram   = psutil.virtual_memory().percent
                disk  = psutil.disk_io_counters()
                disk_r = disk.read_bytes / 1024 / 1024 if disk else 0
                net   = psutil.net_io_counters()
                nb    = net.bytes_sent + net.bytes_recv if net else 0
                net_s = max(0, (nb - self._net_bytes_old) / 1024)
                self._net_bytes_old = nb
                uptime = time.time() - psutil.boot_time()
                h, r  = divmod(int(uptime), 3600)
                m, s  = divmod(r, 60)
                self._mon_up.config(text=f"{h}h {m}m {s}s")
            except: pass
        else:
            import random
            cpu = random.uniform(5,40); ram = random.uniform(30,70)

        self._cpu_hist = self._cpu_hist[1:] + [cpu]
        self._ram_hist = self._ram_hist[1:] + [ram]
        self._net_hist = self._net_hist[1:] + [min(net_s,500)]

        self._mon_cpu.config(text=f"{cpu:.1f}%")
        self._mon_ram.config(text=f"{ram:.1f}%")
        self._mon_disk.config(text=f"{disk_r:.1f} MB/s" if HAS_PSUTIL else "--")
        self._mon_net.config(text=f"{net_s:.1f} KB/s" if HAS_PSUTIL else "--")

        self._sb_cpu.config(text=f"CPU: {cpu:.0f}%")
        self._sb_ram.config(text=f"RAM: {ram:.0f}%")

        self._draw_monitor_chart()
        self._draw_telemetry_chart()

        if HAS_PSUTIL:
            try:
                procs = sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent']),
                    key=lambda p: p.info['cpu_percent'] or 0, reverse=True)[:5]
                self._proc_info.config(state="normal")
                self._proc_info.delete("1.0","end")
                for p in procs:
                    self._proc_info.insert("end",
                        f"  PID {p.info['pid']:<6} {p.info['name'][:18]:<20}"
                        f" CPU:{p.info['cpu_percent']:.1f}%  RAM:{p.info['memory_percent']:.1f}%\n")
                self._proc_info.config(state="disabled")
            except: pass

        self.after(1500, self._update_telemetry)

    def _draw_monitor_chart(self):
        c = self._mon_canvas
        W = c.winfo_width() or 270
        H = c.winfo_height() or 120
        c.delete("all")
        if W < 10 or H < 10: return

        c.create_rectangle(0, 0, W, H, fill=C['base'], outline="")
        for i in range(1, 4):
            y = int(H * i / 4)
            c.create_line(0, y, W, y, fill=C['border2'], dash=(3,6))
        for i in range(1, 8):
            x = int(W * i / 8)
            c.create_line(x, 0, x, H, fill=C['border2'], dash=(2,8))

        N = len(self._cpu_hist)

        def draw_series(hist, color, offset=0):
            pts = []
            for i, v in enumerate(hist):
                x = int(W * i / (N-1))
                y = int(H - (H * v / 100)) + offset
                y = max(2, min(H-2, y))
                pts.extend([x, y])
            if len(pts) >= 4:
                c.create_line(*pts, fill=color, width=2, smooth=True)

        draw_series(self._cpu_hist, C['cyan'])
        draw_series(self._ram_hist, C['purple2'])

        c.create_text(4,  4,  anchor="nw", text=f"CPU {self._cpu_hist[-1]:.0f}%", fill=C['cyan'], font=("Consolas", 8))
        c.create_text(64, 4,  anchor="nw", text=f"RAM {self._ram_hist[-1]:.0f}%", fill=C['purple2'], font=("Consolas", 8))
        c.create_text(W-2, H-2, anchor="se", text="80 samples", fill=C['text3'], font=("Consolas", 7))

    def _draw_telemetry_chart(self):
        c = self._tel_canvas
        W = c.winfo_width()  or 600
        H = c.winfo_height() or 200
        c.delete("all")
        if W < 10: return

        c.create_rectangle(0, 0, W, H, fill=C['base'], outline="")

        c.create_text(W//2, 14, text="  ⚡ NEXUS STUDIO — LIVE SYSTEM TELEMETRY", fill=C['cyan'], font=("Consolas", 10, "bold"))

        charts = [
            (self._cpu_hist, C['cyan'],    "CPU %",   0,    W//3),
            (self._ram_hist, C['purple2'], "RAM %",   W//3, 2*W//3),
            (self._net_hist, C['amber'],   "NET KB/s",2*W//3, W),
        ]

        for hist, color, label, x0, x1 in charts:
            cw = x1 - x0
            ch = H - 40
            c.create_rectangle(x0+4, 30, x1-4, H-8, fill=C['surface'], outline=color)
            N = len(hist)
            peak = max(hist) if max(hist) > 0 else 1
            pts = []
            for i, v in enumerate(hist):
                x = x0 + 4 + int(cw * i / (N-1))
                y = H - 8 - int(ch * v / peak)
                y = max(32, min(H-10, y))
                pts.extend([x, y])
            if len(pts) >= 4:
                c.create_line(*pts, fill=color, width=2, smooth=True)
            c.create_text((x0+x1)//2, 22, text=f"{label}: {hist[-1]:.1f}", fill=color, font=("Consolas", 9, "bold"))

    # ════════════════════════════════════════════════════════
    # FILE OPERATIONS
    # ════════════════════════════════════════════════════════
    def _open_file(self):
        path = filedialog.askopenfilename(
            title="Open Nexus Script",
            filetypes=[("Nexus Files","*.nx"),("All Files","*.*")])
        if path:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            self._editor.delete("1.0","end")
            self._editor.insert("1.0", code)
            self._highlight()
            self._update_line_numbers()
            self.current_file = path
            name = os.path.basename(path)
            self._file_lbl.config(text=f"  {name}")
            self._sb_file.config(text=f"  {name}")

    def _save_file(self):
        if not self.current_file:
            self.current_file = filedialog.asksaveasfilename(
                defaultextension=".nx",
                filetypes=[("Nexus Files","*.nx"),("All Files","*.*")])
        if self.current_file:
            code = self._editor.get("1.0","end-1c")
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(code)
            name = os.path.basename(self.current_file)
            self._file_lbl.config(text=f"  {name}  ✅")
            self._sb_file.config(text=f"  {name}")
            self._append_out(f"  💾 Saved: {self.current_file}\n", "success")

    def _format_code(self):
        code = self._editor.get("1.0","end-1c")
        lines = code.splitlines()
        indent = 0
        result = []
        for line in lines:
            stripped = line.strip()
            if stripped.endswith("}") or stripped == "}":
                indent = max(0, indent - 1)
            result.append("    " * indent + stripped if stripped else "")
            if stripped.endswith("{"):
                indent += 1
        formatted = "\n".join(result)
        self._editor.delete("1.0","end")
        self._editor.insert("1.0", formatted)
        self._highlight()
        self._update_line_numbers()
        self._append_out("  🔥 Code formatted.\n", "success")

    def _change_font(self, delta):
        self._font_size = max(8, min(20, self._font_size + delta))
        self._editor.config(font=("Consolas", self._font_size))
        self._update_line_numbers()

    # ════════════════════════════════════════════════════════
    # MISC
    # ════════════════════════════════════════════════════════
    def _toggle_voice(self):
        self.voice.enabled = not self.voice.enabled
        label = "🔊 VOICE ON" if self.voice.enabled else "🔇 VOICE OFF"
        color = C['green'] if self.voice.enabled else C['text2']
        self._voice_btn.config(text=label, fg=color)
        if self.voice.enabled:
            self.voice.say("Nexus Studio voice assistant activated.")

    def _insert_sample(self):
        self._editor.delete("1.0","end")
        self._editor.insert("1.0", SAMPLE_CODE)
        self._highlight()
        self._update_line_numbers()

    def _tick_status(self):
        t = time.strftime("  %H:%M:%S  %d/%m/%Y")
        self._sb_time.config(text=t)
        self.after(800, self._tick_status)

    def _bind_keys(self):
        self.bind("<F5>",              lambda e: self._run_code())
        self.bind("<Control-r>",       lambda e: self._run_code())
        self.bind("<Control-s>",       lambda e: self._save_file())
        self.bind("<Control-o>",       lambda e: self._open_file())
        self.bind("<Control-Return>",  lambda e: self._eval_sel())
        self.bind("<F1>",              lambda e: self._inspect_ast())
        self.bind("<F2>",              lambda e: self._run_profiler())
        self.bind("<Control-=>",       lambda e: self._change_font(1))
        self.bind("<Control-minus>",   lambda e: self._change_font(-1))
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self):
        self.destroy()
        sys.exit(0)

# ════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = NexusStudio()
    app.mainloop()
