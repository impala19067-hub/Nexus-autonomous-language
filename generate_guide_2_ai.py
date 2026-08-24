import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from doc_helpers import get_styles, code_box, callout_box, cover_banner, make_canvas_class

def generate_advanced_ai_guide(filename="Building_Advanced_Autonomous_AI.pdf"):
    styles = get_styles()
    doc = SimpleDocTemplate(filename, pagesize=letter, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
    story = []

    # ================= COVER =================
    story.append(cover_banner(
        "BUILDING ADVANCED AUTONOMOUS AI WITH SAPPHIRE",
        "Architectural Blueprints, Neural Training, Memory, Planning, Tools, Multi-Agent Swarms & Self-Healing Loops",
        "Version 1.0.0 (Official Manual)", styles
    ))
    story.append(Spacer(1, 15))

    # ================= CHAPTER 1 =================
    story.append(Paragraph("Chapter 1: The Autonomous Computing Paradigm", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "An <b>Autonomous AI Agent</b> in Sapphire is not a simple chat completion prompt. "
        "It is a persistent software entity that interacts continuously with an environment, senses system state, "
        "reasons about complex goals, trains and invokes deep neural network policies, plans dynamic action DAGs, "
        "executes system tools, verifies outcomes, and self-corrects.",
        styles['NormalText']
    ))
    story.append(callout_box(
        "Chatbot vs Autonomous Agent",
        "• <b>Chatbot:</b> Reactive text responder waiting for manual prompts.<br/>"
        "• <b>Autonomous Agent:</b> Proactive goal-driven engine that continuously observes, trains, reasons, plans, uses tools, and executes 24/7.",
        styles, "note"
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>The 8-Stage Autonomous Pipeline:</b>", styles['CustomH2']))
    stages = [
        ("1. Data Ingestion", "Ingesting tabular, CSV, JSON, system telemetry, or environment state into normalized tensors."),
        ("2. Neural Training", "Fitting neural network policy and value models using ml.train.fit across parallel workers."),
        ("3. Model Evaluation", "Validating loss, accuracy, and latency metrics before deployment into live environments."),
        ("4. Cognitive Reasoning", "Analyzing high-level goal intent with local Ollama inference and Groq API cloud fallback."),
        ("5. Semantic Memory", "Persisting facts, experience tuples, and state into short and long-term vector/key-value stores."),
        ("6. Action Planning", "Decomposing high-level goals into 4-step directed acyclic graph (DAG) execution steps."),
        ("7. Tool Invocation", "Executing permission-controlled system actions, API calls, and OS automation commands."),
        ("8. Autonomous Loop", "Continuous observation, feedback validation, error recovery, and self-correction.")
    ]
    for s_name, s_desc in stages:
        story.append(Paragraph(f"• <b>{s_name}:</b> {s_desc}", styles['BulletText']))

    story.append(PageBreak())

    # ================= CHAPTER 2 =================
    story.append(Paragraph("Chapter 2: Deep Learning Policy Training in Sapphire (.sp)", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Sapphire empowers developers to train deep learning models directly in the same script where agents make autonomous decisions. "
        "Below is a complete example of training an agent policy neural network using <code>ml.train.fit</code>:",
        styles['NormalText']
    ))

    code_training = """// Training an Agent Policy Network in Sapphire (.sp)
fn train_policy_network() {
    print("📊 1. Generating synthetic state-action dataset...");
    let dataset = ml.dataset.random(2000, 12, 4); // 12 state features, 4 actions
    let split = dataset.split(0.8);

    print("🧠 2. Constructing multi-layer policy network...");
    let policy_net = ml.model.mlp([12, 64, 32, 4], "relu");
    let optimizer = ml.optim.adam(0.005);

    print("🏋️ 3. Training policy model with multi-worker data parallelism...");
    let fit_result = ml.train.fit(
        policy_net,
        split["train"],
        ml.loss.cross_entropy,
        optimizer,
        epochs=5,
        batch_size=64,
        n_workers=2,
        val_dataset=split["val"]
    );
    print("✅ Model trained. Final loss: {fit_result.final_loss}");

    // Persist trained weights
    policy_net.save("./agent_policy_v1.json");
    agent.memory.remember("active_policy", "./agent_policy_v1.json");
}

train_policy_network();"""
    story.append(code_box(code_training, styles))

    story.append(PageBreak())

    # ================= CHAPTER 3 =================
    story.append(Paragraph("Chapter 3: Cognitive Planning, Reasoning & Memory", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Sapphire's <code>agent.planning</code> and <code>agent.memory</code> modules manage the cognitive lifecycle of the agent:",
        styles['NormalText']
    ))

    code_planning = """// Cognitive Reasoning & Memory in Sapphire (.sp)
fn cognitive_decision_cycle() {
    // 1. Perception
    let stats = os.system_info();
    let memory_context = agent.memory.recall("active_policy");
    
    // 2. LLM Reasoning
    let prompt = "System RAM is {stats.ram_percent}%. Active policy: {memory_context}. Plan action.";
    let reasoning = ai.prompt(prompt);
    print("🧠 AI Reasoning: {reasoning}");

    // 3. Goal Decomposition Plan (4-Step DAG)
    let plan = agent.planning.create_plan("Scale system memory and optimize cache");
    for (step in plan.steps) {
        print("📌 Step {step.id}: {step.description} [{step.status}]");
    }
}

cognitive_decision_cycle();"""
    story.append(code_box(code_planning, styles))
    story.append(Spacer(1, 10))

    story.append(Paragraph("Chapter 4: Dynamic Tool Registration & Safe Execution", styles['CustomH1']))
    code_tools = """// Dynamic Tool Registration & Permission Policies
agent.permissions.set_policy("interactive"); // strict, interactive, or permissive

agent.tools.register("kill_heavy_processes", "Terminates memory-hogging processes", fn(threshold) {
    let procs = os.system_info();
    return "Optimized process memory for threshold {threshold}";
});

let execution_output = agent.tools.execute("kill_heavy_processes", 85.0);
print("Tool Execution: {execution_output}");"""
    story.append(code_box(code_tools, styles))

    story.append(PageBreak())

    # ================= CHAPTER 5 =================
    story.append(Paragraph("Chapter 5: Self-Healing Autonomous Loops & Swarms", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "Self-healing resilience ensures that when execution exceptions occur, the agent diagnoses the failure using AI reasoning, "
        "devises a remediation patch, and executes recovery automatically without human intervention.",
        styles['NormalText']
    ))

    code_swarm = """// Self-Healing Multi-Agent Swarm in Sapphire (.sp)
fn telemetry_worker() {
    let metrics = os.system_info();
    return "Telemetry: CPU {metrics.cpu_usage_percent}%, RAM {metrics.ram_percent}%";
}

fn security_worker() {
    return "Security Audit: All 24 firewall rules active.";
}

fn autonomous_orchestrator() {
    print("🚀 Launching Sapphire Multi-Agent Swarm...");
    
    parallel {
        let t_report = telemetry_worker();
        let s_report = security_worker();
    }
    
    let goal = "Verify swarm health, log audit, and notify administrator.";
    let swarm_result = agent.autonomy.run_loop(goal, max_steps=4);
    print("✨ Swarm Execution Completed: {swarm_result['finished']}");
}

autonomous_orchestrator();"""
    story.append(code_box(code_swarm, styles))

    story.append(PageBreak())

    # ================= CHAPTER 6 =================
    story.append(Paragraph("Chapter 6: Security Sandboxing & Permission Policies", styles['CustomH1']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0D9488"), spaceAfter=8))
    story.append(Paragraph(
        "To ensure autonomous agents cannot execute dangerous actions unsupervised, Sapphire enforces policy modes:",
        styles['NormalText']
    ))
    
    sec_data = [
        [Paragraph("<b>Policy Mode</b>", styles['CalloutTitle']), Paragraph("<b>Behavior</b>", styles['CalloutTitle']), Paragraph("<b>Use Case</b>", styles['CalloutTitle'])],
        [Paragraph("<code>strict</code>", styles['CodeText']), Paragraph("Blocks all write, process spawning, and delete actions.", styles['NormalText']), Paragraph("Production audit & read-only analysis.", styles['NormalText'])],
        [Paragraph("<code>interactive</code>", styles['CodeText']), Paragraph("Prompts user for confirmation before executing mutating actions.", styles['NormalText']), Paragraph("Supervised human-in-the-loop agents.", styles['NormalText'])],
        [Paragraph("<code>permissive</code>", styles['CodeText']), Paragraph("Grants full unconstrained system execution access.", styles['NormalText']), Paragraph("Fully autonomous background daemons.", styles['NormalText'])],
    ]
    t_sec = Table(sec_data, colWidths=[100, 220, 184])
    t_sec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_sec)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Chapter 7: 24/7 Persistent Background Daemon Agents", styles['CustomH1']))
    code_daemon = """// Persistent 24/7 Autonomous Daemon in Sapphire (.sp)
fn run_daemon() {
    print("🌌 Initializing Sapphire 24/7 Autonomous Service...");
    scheduler.interval(60.0, fn() {
        let stats = os.system_info();
        if (stats.ram_percent > 85.0) {
            let ai_eval = ai.prompt("High RAM load {stats.ram_percent}%. Immediate action?");
            os.notify("Sapphire Warning", ai_eval);
            agent.memory.remember("last_alert_time", stats.ram_percent);
        }
    });
}
run_daemon();"""
    story.append(code_box(code_daemon, styles))

    doc.build(story, canvasmaker=make_canvas_class("BUILDING ADVANCED AUTONOMOUS AI"))
    print(f"[OK] Generated {filename}")

if __name__ == "__main__":
    generate_advanced_ai_guide()
