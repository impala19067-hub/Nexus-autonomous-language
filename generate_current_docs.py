"""Generate conservative Sapphire manuals from the currently tested feature set."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parent

FILES = {
    "Sapphire_Coding_and_Usage_Guide.pdf": (
        "Sapphire Coding and Usage Guide",
        "Language syntax, standard-library namespaces, CLI usage, and verified boundaries.",
        [
            ("Language", "The tree-walk interpreter supports bindings, functions, control flow, arrays, maps, structs, lambdas, exceptions, pipes, process literals, and parallel blocks."),
            ("Namespaces", "The runtime exposes os, fs, http, ai, data, scheduler, ml, gui, and agent namespaces. Optional packages and services are required for some operations."),
            ("Execution", "Run .sp files with sapphire run, use the REPL or eval command, and inspect source through the compiler tools. The compiler GUI uses the interpreter and textual IR; it is not a native compiler."),
            ("Example", 'let info = os.system_info(); print("CPU: {info.cpu_usage_percent}%");'),
        ],
    ),
    "Building_Advanced_Autonomous_AI.pdf": (
        "Building Autonomous Workflows with Sapphire",
        "A practical description of the implemented agent API, its controls, and its limits.",
        [
            ("Implemented loop", "Agents retrieve bounded context, create a plan, select an action, check permissions, execute a registered or built-in action, record the observation, and report success or failure."),
            ("Memory", "Working history and an in-process long-term key/value similarity store are available. SQLite FTS5 memory is provided by the industrial utilities. These are not hosted vector search or neural memory services."),
            ("Controls", "Agent budgets cover steps, token budget metadata, elapsed time, and tool calls. Verifier and recovery callbacks can reject results or request another attempt."),
            ("Not included", "Parser-level agent declarations, event triggers, DAG execution, unattended production daemons, and verified multi-agent recovery are not current language guarantees."),
        ],
    ),
    "Sapphire_Autonomy_and_Performance_Benchmarks.pdf": (
        "Sapphire Local Runtime Benchmark",
        "A reproducible local measurement, not a cross-language, GPU, or cluster benchmark.",
        [
            ("Workload", "Parse and interpret a 100-item loop: let total = 0; for item in range(100) { total = total + item; } total;"),
            ("Reference run", "Python 3.12.10, 100 iterations, result 4950: median 0.21095 ms, minimum 0.2023 ms, maximum 0.7817 ms."),
            ("How to reproduce", "Run python benchmarks/benchmark_runtime.py from the repository root. Results vary with Python version, operating system, CPU load, and hardware."),
            ("Excluded claims", "The project does not publish fabricated MFU, tokens/second, 512-GPU throughput, or cross-language scores because those workloads are not executed by the repository benchmark."),
        ],
    ),
    "Beginners_Guide_Your_First_Autonomous_AI.pdf": (
        "Beginner's Guide to Sapphire Automation",
        "Start with a small local script and understand where AI and optional dependencies enter.",
        [
            ("First script", 'let info = os.system_info(); print("CPU: {info.cpu_usage_percent}%"); os.notify("Sapphire", "Check complete");'),
            ("AI calls", "ai.prompt sends a request through the configured backend. A working local model, cloud credentials, or offline fallback determines the result."),
            ("Agent calls", 'let report = agent.autonomy.run_loop("Inspect system health", 3); print(report.state);'),
            ("Safety", "Review permissions, tool schemas, file paths, and external commands. A successful function call is not proof that a real-world objective was achieved; add verification where it matters."),
        ],
    ),
    "Sapphire_Language_Specification_and_Automation_Manual.pdf": (
        "Sapphire Language Specification and Automation Manual",
        "Current syntax and automation behavior as implemented in the interpreter.",
        [
            ("Core semantics", "Sapphire is dynamically typed, uses a tree-walk interpreter, and supports expressions, statements, functions, member access, indexing, and structured process results."),
            ("Automation", "OS telemetry, notifications, clipboard, filesystem helpers, HTTP helpers, scheduling, and controlled process execution are exposed through standard-library modules."),
            ("AI and ML", "AI prompt/classification/JSON helpers and local tensor, dataset, model, autodiff, optimizer, and loss utilities are available subject to optional dependencies and backend configuration."),
            ("Portability", "The source runtime is Python-based. The packaged Windows distribution includes executable tools; source and optional-dependency behavior can differ by environment."),
        ],
    ),
    "Sapphire_Capabilities_and_Transparency_Manual.pdf": (
        "Sapphire Capability and Transparency Manual",
        "What is tested, what is optional, and what remains outside the current implementation.",
        [
            ("Tested", "The repository tests cover language execution, file and process helpers, parallel blocks, agent plans and tools, failures, persistence, memory retrieval, sandbox boundaries, CPU/ML behavior, and CUDA reporting."),
            ("Optional", "NumPy, PyTorch, psutil, requests, audio packages, AI services, NVIDIA drivers, and CUDA hardware are not bundled assumptions for every installation."),
            ("Distributed", "The distributed package creates planning and code-generation artifacts. It does not prove that a cluster launched, trained, recovered, or achieved any throughput figure."),
            ("Roadmap", "Native compilation, production isolation, event-driven syntax, DAG scheduling, durable neural memory, verified multi-node training, and wider security validation remain future work."),
        ],
    ),
}


def build_pdf(path: Path, title: str, subtitle: str, sections: list[tuple[str, str]]) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("Cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=24, leading=29, textColor=colors.white, alignment=1))
    styles.add(ParagraphStyle("Sub", parent=styles["Normal"], fontSize=11, leading=15, textColor=colors.HexColor("#CBD5E1"), alignment=1))
    styles.add(ParagraphStyle("H", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, textColor=colors.HexColor("#0F4C81"), spaceBefore=14, spaceAfter=6))
    styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontSize=10, leading=14, spaceAfter=8))
    doc = SimpleDocTemplate(str(path), pagesize=letter, leftMargin=.75 * inch, rightMargin=.75 * inch, topMargin=.7 * inch, bottomMargin=.75 * inch, title=title, author="Sapphire Project")
    story = [Table([[Paragraph(title, styles["Cover"])], [Paragraph(subtitle, styles["Sub"])]], colWidths=[7.1 * inch], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#102A43")), ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#2CB1BC")), ("TOPPADDING", (0, 0), (-1, -1), 20), ("BOTTOMPADDING", (0, 0), (-1, -1), 20)])), Spacer(1, 18), Paragraph("This manual describes the current local implementation. Feature names are not evidence of production scale, hardware availability, or successful external actions.", styles["Body"])]
    for heading, text in sections:
        story.extend([Paragraph(heading, styles["H"]), Paragraph(text, styles["Body"])])
    story.extend([Spacer(1, 12), Paragraph("Version 1.0.5. Reproduce local measurements with benchmarks/benchmark_runtime.py. Values depend on the machine and environment.", styles["Body"])])
    doc.build(story)


if __name__ == "__main__":
    for filename, (title, subtitle, sections) in FILES.items():
        build_pdf(ROOT / filename, title, subtitle, sections)
        print(f"Generated {filename}")
