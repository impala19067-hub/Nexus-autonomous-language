import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from doc_helpers import get_styles, code_box, callout_box, cover_banner, make_canvas_class

def generate_coding_guide(filename="Sapphire_Coding_and_Usage_Guide.pdf"):
    styles = get_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    # ================= COVER =================
    story.append(cover_banner(
        "SAPPHIRE PROGRAMMING LANGUAGE",
        "Complete Developer Coding Manual, Deep Learning, Concurrency & AI Agent Reference",
        "Version 1.0.0 (Official Manual)", styles
    ))
    story.append(Spacer(1, 15))

    # ================= CHAPTER 1 =================
    story.append(Paragraph("Chapter 1: Executive Overview & Design Philosophy", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "<b>Sapphire</b> is an autonomous-first, statically and gradually typed programming language designed specifically for "
        "<b>PC Automation</b>, <b>Deep Neural Network Training</b>, and <b>Autonomous AI Agent Systems</b>. "
        "Modern developer workflows are severely fragmented across Python (for ML and AI scripting), Rust/C++ (for kernel performance and memory safety), "
        "JavaScript (for web APIs and async events), and Bash/PowerShell (for process orchestration). Sapphire collapses this toolchain into a single, unified runtime.",
        styles['NormalText']
    ))
    story.append(callout_box(
        "The Core Autonomous Pipeline",
        "Data → Training → Model → Reasoning → Memory → Planning → Tool Use → Autonomous Execution",
        styles, "tip"
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Key Architectural Pillars:</b>", styles['CustomH2']))
    pillars = [
        ("Colorless Concurrency", "Lightweight green fibers eliminate async function coloring and callback hell. Native parallel blocks allow concurrent execution without async/await."),
        ("Stream & Process Piping", "First-class shell commands and the |> pipe operator stream data effortlessly between OS processes, arrays, and functions."),
        ("Embedded Deep Learning Stack", "Native tensors, automatic differentiation (autograd), neural layers, and multi-worker distributed training directly in stdlib (ml module)."),
        ("Autonomous Agent Engine", "Vector/key-value memory, 4-step DAG planners, ReAct reasoning loops, dynamic tool registries, and permission policies (agent module)."),
        ("System & Hardware Automation", "Direct hardware telemetry, mouse/keyboard simulation, GUI alerts, and desktop notifications without third-party packages.")
    ]
    for name, desc in pillars:
        story.append(Paragraph(f"• <b>{name}:</b> {desc}", styles['BulletText']))
    
    story.append(PageBreak())

    # ================= CHAPTER 2 =================
    story.append(Paragraph("Chapter 2: Language Syntax, Variables & Types (.sp)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Sapphire scripts use the <code>.sp</code> file extension. Sapphire supports both dynamic type inference and optional static type annotations.",
        styles['NormalText']
    ))
    
    code_vars = """// Variable declarations and dynamic type inference
let agent_name = "Sapphire-Omni";
let max_retries = 5;
let threshold = 0.985;
let is_autonomous = true;

// Composite collections
let features = [0.12, 0.45, 0.88, 0.93];
let system_config = {
    "device": "cuda:0",
    "batch_size": 64,
    "learning_rate": 0.001,
    "model_type": "mlp"
};

// String interpolation with formatting
print("Agent {agent_name} configured with device {system_config['device']}");"""
    story.append(code_box(code_vars, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Chapter 3: Control Flow & Loops", styles['CustomH1']))
    story.append(Paragraph(
        "Sapphire provides standard structured control flow: conditional branching (<code>if/else</code>), counted loops (<code>for/in</code>), "
        "and condition-controlled loops (<code>while</code>).",
        styles['NormalText']
    ))

    code_loops = """// Conditional branching
if (system_config["batch_size"] > 32) {
    print("🚀 High throughput batching enabled.");
} else {
    print("ℹ️ Standard batching mode.");
}

// For-in loop over collections
for (val in features) {
    print("Processing feature value: {val}");
}

// While loop with break/continue
let counter = 0;
while (counter < 10) {
    counter = counter + 1;
    if (counter == 3) { continue; }
    if (counter == 8) { break; }
}"""
    story.append(code_box(code_loops, styles))
    
    story.append(PageBreak())

    # ================= CHAPTER 4 =================
    story.append(Paragraph("Chapter 4: Functions, Closures & Pipe Operator", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Functions in Sapphire are declared with the <code>fn</code> keyword and can be passed as first-class values. "
        "The <b>pipe operator (<code>|&gt;</code>)</b> passes the expression on the left as the first argument to the function on the right.",
        styles['NormalText']
    ))

    code_pipes = """// Function definition with default & typed arguments
fn compute_loss(predicted, actual) {
    let diff = predicted - actual;
    return diff * diff;
}

// Pipe Operator Pipeline Flow
fn normalize(data) {
    return ml.dataset.normalize(data);
}

fn evaluate(dataset) {
    print("Dataset evaluated successfully.");
    return dataset;
}

// Flow data through pipeline using |>
let raw_data = [10.0, 20.0, 30.0, 40.0];
let clean_data = raw_data |> normalize |> evaluate;"""
    story.append(code_box(code_pipes, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Chapter 5: Colorless Concurrency (parallel blocks)", styles['CustomH1']))
    story.append(Paragraph(
        "Sapphire eliminates function coloring. Any code block wrapped in <code>parallel { ... }</code> runs task branches concurrently across worker threads.",
        styles['NormalText']
    ))

    code_parallel = """// Structured Concurrency in Sapphire
parallel {
    // Branch 1: Sensor telemetry
    let stats = os.system_info();
    print("RAM Usage: {stats.ram_percent}%");

    // Branch 2: Web API polling
    let response = http.get("https://httpbin.org/get");
    print("API Status: {response.status_code}");

    // Branch 3: Disk workspace scan
    let files = fs.list_dir(".");
    print("Discovered {files.length} workspace files.");
}
print("✨ All parallel branches synchronized.");"""
    story.append(code_box(code_parallel, styles))

    story.append(PageBreak())

    # ================= CHAPTER 6 =================
    story.append(Paragraph("Chapter 6: Deep Learning & Tensor Standard Library (ml)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Sapphire includes a native deep learning framework with tensors, automatic differentiation, neural layers, loss functions, optimizers, and distributed data-parallel training.",
        styles['NormalText']
    ))

    code_ml = """// 1. Tensors & Matrix Multiplication
let A = ml.tensor([[1.0, 2.0], [3.0, 4.0]]);
let B = ml.tensor([[5.0, 6.0], [7.0, 8.0]]);
let C = A.matmul(B);
print("Matrix Product: {C}");

// 2. Autograd & Automatic Differentiation
let x = ml.autograd.variable(3.0);
let tape = ml.autograd.tape();
tape.watch(x);
let y = x * x + 2.0 * x + 1.0;
let dy_dx = tape.gradient(y, x);
print("d/dx (x^2 + 2x + 1) at x=3: {dy_dx}"); // Expected: 8.0

// 3. Neural Network Architecture & Model Creation
let model = ml.model.mlp([16, 64, 32, 2], "relu");

// 4. Distributed Multi-Worker Training
let dataset = ml.dataset.random(1000, 16, 2);
let split = dataset.split(0.8);

let training_results = ml.train.fit(
    model,
    split["train"],
    ml.loss.cross_entropy,
    ml.optim.adam(0.001),
    epochs=5,
    batch_size=32,
    n_workers=4,
    val_dataset=split["val"]
);
print("Final Validation Loss: {training_results.final_loss}");"""
    story.append(code_box(code_ml, styles))

    story.append(PageBreak())

    # ================= CHAPTER 7 =================
    story.append(Paragraph("Chapter 7: Autonomous Agent Architecture (agent)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "The <code>agent</code> module provides production-grade agent primitives: vector memory, 4-step DAG planners, tool registries, security permissions, and autonomous loop engines.",
        styles['NormalText']
    ))

    code_agent = """// 1. Memory Store (Short & Long Term Semantic Recall)
agent.memory.remember("model_checkpoint", "v1.2.0-prod");
agent.memory.remember("target_accuracy", 0.982);
let val = agent.memory.recall("model_checkpoint");

// 2. Tool Registration & Execution
agent.tools.register("disk_cleanup", "Deletes temporary cache files", fn(path) {
    let removed = fs.remove(path);
    return "Cleanup status: {removed}";
});

let tool_result = agent.tools.execute("disk_cleanup", "./tmp");
print("Tool Execution Result: {tool_result}");

// 3. Autonomous Loop Execution
let goal = "Train policy network, deploy to production, and alert administrator.";
let report = agent.autonomy.run_loop(goal, max_steps=5);
print("Agent Autonomous Loop Finished: {report['finished']}");"""
    story.append(code_box(code_agent, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Chapter 8: System Automation & OS Control (os, fs, gui)", styles['CustomH1']))
    code_os = """// Hardware Telemetry
let sys_info = os.system_info();
print("CPU: {sys_info.cpu_usage_percent}%, RAM: {sys_info.ram_percent}%");

// GUI Automation & Toast Alert
gui.alert("System Health Normal", "Sapphire Monitor");
os.notify("Sapphire Agent", "All systems operational.");"""
    story.append(code_box(code_os, styles))

    story.append(PageBreak())

    # ================= CHAPTER 9 =================
    story.append(Paragraph("Chapter 9: End-to-End Autonomous Autobot Script (.sp)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Below is a complete, production-ready autonomous PC autobot written entirely in Sapphire:",
        styles['NormalText']
    ))

    code_autobot = """// 05_full_pc_autobot.sp — Autonomous PC Monitor & Remediation Agent
fn pc_autobot() {
    print("🤖 SAPPHIRE AUTONOMOUS BOT INITIALIZING...");

    // Phase 1: Sense System Telemetry
    let stats = os.system_info();
    print("RAM Used: {stats.ram_percent}%, CPU: {stats.cpu_usage_percent}%");

    // Phase 2: Parallel Perception
    parallel {
        let http_check = http.get("https://httpbin.org/get");
        let workspace_files = fs.list_dir(".");
        print("Indexed {workspace_files.length} workspace items.");
    }

    // Phase 3: AI Cognitive Evaluation
    let prompt = "System RAM is {stats.ram_percent}%. Evaluate health and recommend action.";
    let ai_decision = ai.prompt(prompt);
    print("🧠 AI Decision: {ai_decision}");

    // Phase 4: Memory Persistence
    agent.memory.remember("last_pc_health_eval", ai_decision);

    // Phase 5: Autonomous Action & Notification
    os.clip_write("PC Diagnostic: RAM {stats.ram_percent}%");
    os.notify("Sapphire Autobot", "Autonomous PC Health Check Completed!");
}

pc_autobot();"""
    story.append(code_box(code_autobot, styles))

    story.append(PageBreak())

    # ================= CHAPTER 10 =================
    story.append(Paragraph("Chapter 10: Emerald Developer Studio IDE Reference", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "<b>Emerald Developer Studio</b> (launched via <code>sapphire studio</code> or <code>Emerald_Studio.exe</code>) is the official "
        "graphical integrated development environment for Sapphire.",
        styles['NormalText']
    ))
    
    studio_features = [
        ("Built-in .sp Code Editor", "High-performance syntax-aware code editor with auto-indentation and file management."),
        ("1-Click Sapphire Tool Builder", "Interactive dialog wizard to rapidly scaffold and register new autonomous agent tools."),
        ("Live Compiler Terminal", "Integrated execution terminal with live stdout/stderr capture and ANSI color formatting."),
        ("Hardware Telemetry Dashboard", "Real-time CPU load, RAM usage, and NVIDIA CUDA GPU VRAM monitoring."),
        ("Agent & Memory Inspector", "Live state inspector for agent working memory, vector embeddings, and active execution DAGs.")
    ]
    for f_title, f_desc in studio_features:
        story.append(Paragraph(f"• <b>{f_title}:</b> {f_desc}", styles['BulletText']))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Chapter 11: Standard Library Reference Table", styles['CustomH1']))

    stdlib_data = [
        [Paragraph("<b>Module</b>", styles['CalloutTitle']), Paragraph("<b>Function / API Signature</b>", styles['CalloutTitle']), Paragraph("<b>Description</b>", styles['CalloutTitle'])],
        [Paragraph("<code>ml.tensor</code>", styles['CodeText']), Paragraph("<code>ml.tensor(data, dtype, device)</code>", styles['CodeText']), Paragraph("Creates multi-dimensional tensor array.", styles['NormalText'])],
        [Paragraph("<code>ml.autograd</code>", styles['CodeText']), Paragraph("<code>ml.autograd.tape()</code>", styles['CodeText']), Paragraph("Context manager for automatic differentiation.", styles['NormalText'])],
        [Paragraph("<code>ml.train</code>", styles['CodeText']), Paragraph("<code>ml.train.fit(model, ds, loss, opt, ...)</code>", styles['CodeText']), Paragraph("Data-parallel multi-threaded neural trainer.", styles['NormalText'])],
        [Paragraph("<code>ml.gpu</code>", styles['CodeText']), Paragraph("<code>ml.gpu.info() / to_device(t, dev)</code>", styles['CodeText']), Paragraph("CUDA/GPU hardware device telemetry & tensors.", styles['NormalText'])],
        [Paragraph("<code>ai.prompt</code>", styles['CodeText']), Paragraph("<code>ai.prompt(query: str) -> str</code>", styles['CodeText']), Paragraph("LLM reasoning via local Ollama or Groq API.", styles['NormalText'])],
        [Paragraph("<code>agent.memory</code>", styles['CodeText']), Paragraph("<code>agent.memory.remember(k, v)</code>", styles['CodeText']), Paragraph("Stores vector/key-value semantic knowledge.", styles['NormalText'])],
        [Paragraph("<code>agent.tools</code>", styles['CodeText']), Paragraph("<code>agent.tools.register(name, desc, fn)</code>", styles['CodeText']), Paragraph("Registers runtime executable tool for agents.", styles['NormalText'])],
        [Paragraph("<code>agent.autonomy</code>", styles['CodeText']), Paragraph("<code>agent.autonomy.run_loop(goal, steps)</code>", styles['CodeText']), Paragraph("Runs autonomous ReAct execution loop.", styles['NormalText'])],
        [Paragraph("<code>os.system_info</code>", styles['CodeText']), Paragraph("<code>os.system_info() -> Map</code>", styles['CodeText']), Paragraph("Returns live CPU, RAM, and Disk metrics.", styles['NormalText'])],
        [Paragraph("<code>fs.write</code>", styles['CodeText']), Paragraph("<code>fs.write(path, data) -> Bool</code>", styles['CodeText']), Paragraph("Writes UTF-8 text or binary content to file.", styles['NormalText'])],
        [Paragraph("<code>http.get</code>", styles['CodeText']), Paragraph("<code>http.get(url, headers) -> Map</code>", styles['CodeText']), Paragraph("Performs HTTP GET returning status & body.", styles['NormalText'])],
    ]
    t_std = Table(stdlib_data, colWidths=[75, 200, 229])
    t_std.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
    ]))
    story.append(t_std)

    doc.build(story, canvasmaker=make_canvas_class("SAPPHIRE CODING & USAGE GUIDE"))
    print(f"[OK] Generated {filename}")

if __name__ == "__main__":
    generate_coding_guide()
