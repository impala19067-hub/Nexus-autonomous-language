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
            ("Overview", [
                "Sapphire is a lightweight interpreted language designed around local scripting, automation, and experimentation. It is not marketed as a finished distributed AI platform or a certified production runtime, and the repository is intentionally transparent about what has been validated and what remains future work.",
                "The language is designed to be readable and approachable for Windows users, while still exposing enough structure for process control, file access, scheduling, and AI-assisted automation. The interpreter is intentionally compact, so the practical value comes from combining a simple syntax with controlled system access and optional integrations."
            ]),
            ("Core syntax", [
                "Variables are declared with let and const, with a syntax that supports optional type annotations when the author wants them. Functions can accept arguments, return values, and use closures or nested definitions; control flow includes if, else, loops, and exceptions. Arrays, maps, structs, and lambdas are all part of the language model used by the current interpreter.",
                "The language also supports pipeline-style expressions and indexing, plus special handling for process literals using backticks or shell-style $ access. These features are intended to make scripts feel natural for automation, especially in a local Windows environment where shell commands and file operations are common."
            ]),
            ("Stdlib namespaces", [
                "The runtime exposes several namespaces that are expected to be familiar to a developer writing local tooling: os, fs, http, ai, data, scheduler, ml, gui, and agent. Each namespace is independent and not all services are automatically available; the repo distinguishes between language features and optional runtime dependencies.",
                "For example, os gives system and process information, fs handles files, http can be used when requests is installed, and scheduler manages local tasks. The ai and ml modules depend on configured backends or installed packages, and the agent namespace adds memory and planning features that are intentionally bounded by permissions and budgets."
            ]),
            ("Command-line usage", [
                "The CLI supports running .sp scripts, REPL-style input, and interpreter inspection commands. Typical usage includes sapphire run for script execution, sapphire info for environment details, and the bundled compiler or studio tools for inspection and editing. The project does not treat the compiler as a native code generator; it is a runtime and inspection tool that is useful for development workflows.",
                "Developers should expect that the behavior of the runtime depends on the installed Python environment, the optional packages, and the local hardware. The project is transparent that capabilities can vary by machine and that notebook-style or cloud-style assumptions are not built into the core interpreter."
            ]),
            ("Example workflow", [
                "A practical script usually starts by reading system state, then performing a controlled operation, then storing or reporting the result. For example, a script can gather CPU telemetry, decide whether a condition is true, and then send a notification or write a log file. This style matches Sapphire’s emphasis on local automation tasks rather than remote orchestration or massive distributed execution.",
                "The example patterns in the project are intentionally conservative: script execution is local, tool access is tracked, and outputs are validated by direct logic rather than by assuming that a cloud or model call is always trustworthy. That approach keeps the language approachable while retaining a clear boundary between tested and untested behavior."
            ]),
        ],
    ),
    "Building_Advanced_Autonomous_AI.pdf": (
        "Building Autonomous Workflows with Sapphire",
        "A practical description of the implemented agent API, its controls, and its limits.",
        [
            ("Agent loop", [
                "The implemented agent runtime operates in a sequence that is intentionally explicit about what it does and how it decides. It observes context, retains memory, creates a plan, chooses a tool or action, executes it, verifies the result, and then decides whether to continue, recover, or stop. This makes the runtime easier to reason about than fully opaque autonomous systems.",
                "The loop is not designed to pretend it can always solve a problem without human review. Instead, it uses bounded budgets, verification steps, permissions, and recorded observations so the script can remain understandable and auditable. That is especially helpful for local PC automation or workflow orchestration where safety and debugging matter."
            ]),
            ("Memory and persistence", [
                "Sapphire provides in-process memory features that are suitable for local experimentation, as well as SQLite-backed storage through the industrial utilities. The memory model is designed to preserve short-term working context and to support later retrieval, but it is not presented as a substitute for large-scale vector infrastructure or a hosted cloud memory service.",
                "This distinction matters because many AI workflows fail when they assume persistent neural memory is cheap and infinite. Sapphire’s memory system is deliberately bounded and transparent: it stores information in local structures, keeps working context under control, and focuses on deterministic retrieval patterns rather than claiming deep external intelligence."
            ]),
            ("Permissions and budgets", [
                "Agent execution is heavily shaped by permission modes and resource budgets. The runtime tracks steps, tool calls, elapsed time, and token or metadata budget assumptions when they are relevant. This is a practical safeguard: rather than allowing an agent to run without boundaries, the design gives the host application checks and fallback paths.",
                "This approach also improves reliability. When an action fails or a result is weak, the runtime can reject the result, replan, or recover by requesting another attempt. In local automation scenarios, this is often more valuable than simply assuming that the first attempt will succeed."
            ]),
            ("What is not yet guaranteed", [
                "The project does not claim that parser-level agent declarations, event-driven automation, DAG scheduling, or production service orchestration are complete. Those are areas that could be added later, but they are not the current implementation guarantee. The explicit boundary is part of the project’s honesty and transparency statement.",
                "Similarly, the project does not claim broad security certification or complete production resilience. The aim is to provide a working, inspectable, and reasonably bounded environment for experimentation and local automation, not to provide a fully supported autonomous enterprise platform without review."
            ]),
            ("Practical automation design", [
                "A realistic advanced workflow uses Sapphire to orchestrate local tasks, collect context, and produce a plan before taking action. For example, an agent can inspect file state, query system health, and decide whether to send a notification or trigger a script. The actual work is local and inspectable, which helps the user understand what happened, why it happened, and what still needs verification.",
                "The best use of the agent APIs is as a structured helper layer, not as an unbounded autonomous black box. When combined with explicit permissions and verification logic, it becomes a robust building block for prototypes and controlled workflows."
            ]),
        ],
    ),
    "Sapphire_Autonomy_and_Performance_Benchmarks.pdf": (
        "Sapphire Local Runtime Benchmark",
        "A reproducible local measurement, not a cross-language, GPU, or cluster benchmark.",
        [
            ("Benchmark definition", [
                "The included benchmark focuses on a simple repeated parse-and-interpret workload instead of claiming supercomputer-scale performance. The idea is to provide a reproducible local measurement that can be run repeatedly on a given machine with a known Python version and environment. This keeps the benchmark useful for regression checking and local comparison without overstating global performance.",
                "The reference workload is a 100-item loop with arithmetic accumulation. The measured result is deterministic for a given test machine, but the speed numbers are not meant to be interpreted as general language rankings or proof of a production-grade runtime. They are evidence about the local implementation under one environment."
            ]),
            ("Reference run", [
                "On a reference machine running Python 3.12.10, the 100-item loop benchmark produced 4950 as the result, with a median of 0.21095 ms, a minimum of 0.2023 ms, and a maximum of 0.7817 ms. These values are useful as a data point, but they should be interpreted as local timing numbers tied to a specific hardware and software environment.",
                "The benchmark intentionally avoids claiming a wider scaling story. It does not claim a token-per-second metric, a GPU throughput number, or a cluster efficiency score, because those workloads are not part of the benchmark itself. Those claims would be misleading without the underlying infrastructure, hardware, and validation."
            ]),
            ("How to reproduce", [
                "The project includes the benchmark script under benchmarks/benchmark_runtime.py, and the easiest way to reproduce it is to run that script from the repository root. The measurement is intentionally simple, and repeated runs can be used to compare performance before and after code changes. Machine load, CPU frequency scaling, Python version, and operating system differences all affect the results.",
                "When interpreting results, it is important to remember that parsing, evaluation, and scheduling overhead are all included in the visible numbers. A benchmark like this is a useful local signal, but it is not a substitute for workload-specific testing in production, GPU-rich environments, or distributed clusters."
            ]),
            ("Benchmark ethics and scope", [
                "The project’s benchmark philosophy is conservative. It tries to provide evidence that the language can execute a specific local workload reliably, but it avoids unsupported claims such as cross-language rankings or large-scale throughput. This is a necessary safeguard: users can compare behavior under a controlled local environment without mistaking a simple benchmark for a broad systems claim.",
                "This keeps the benchmark honest and useful. It gives developers a practical measurement they can run, verify, and compare, while still telling the truth about what it does not cover."
            ]),
        ],
    ),
    "Beginners_Guide_Your_First_Autonomous_AI.pdf": (
        "Beginner's Guide to Sapphire Automation",
        "Start with a small local script and understand where AI and optional dependencies enter.",
        [
            ("First local script", [
                "A good beginner project starts with a small script that reads system information and prints the result. This helps a new user understand the language syntax, the standard library, and how commands are expressed in Sapphire. It also makes the environment feel predictable and easy to debug.",
                "The project encourages a workflow where the script is simple at first and then extended with notifications, file writes, or tool registration. This gives the user a clear path from basic syntax to automation without forcing them to jump directly into complex agent planning or external APIs."
            ]),
            ("Using AI helpers", [
                "The ai namespace is conceptually simple: send a prompt or classification request through the configured backend, then examine the result. In practice, the quality and availability of the answer depend on installed packages, credentials, and the chosen backend. This is especially important for local experimentation because a model may not be available or may be configured differently from one machine to another.",
                "For beginners, it is best to think of the AI layer as a service integration layer rather than as an automatic guarantee. A script can request an AI action, but it still needs validation, logging, and careful handling of failure or unexpected output. That keeps the system understandable and safe."
            ]),
            ("Running a basic agent", [
                "The agent runtime follows a bounded workflow: gather context, set a plan, run a tool or action, and then check the outcome. This is a good introduction to autonomy because it makes the logic explicit. It avoids the trap of treating an agent as a magical black box that always knows what to do.",
                "For example, a beginner may use a small loop to inspect system health or determine whether a file exists. A script can then either notify the user or take a limited action based on the result. This kind of use is both educational and practical."
            ]),
            ("Safety and verification", [
                "When working with external processes, file paths, tool registration, or AI outputs, it is important to validate the result. A successful call does not mean that the desired real-world outcome has been met, especially when the tool performs some side effect. This is a core lesson in local automation and is a key part of the project’s guarded design.",
                "Because the project is transparent about limitations and optional dependencies, beginners should treat the system as a practical sandbox for experimentation. The learning curve is manageable, and the combination of clear scripts, structured tools, and verification patterns makes the system easier to adopt than many opaque AI tools."
            ]),
        ],
    ),
    "Sapphire_Language_Specification_and_Automation_Manual.pdf": (
        "Sapphire Language Specification and Automation Manual",
        "Current syntax and automation behavior as implemented in the interpreter.",
        [
            ("Language model", [
                "Sapphire is implemented as a dynamically typed, tree-walk interpreter rather than as a native machine-code compiler. This means the language is intentionally easier to inspect and reason about while still being capable of practical local scripting. It is a good fit for prototypes, experimentation, and controlled automation rather than for large-scale production claims.",
                "The semantics revolve around expressions, statements, functions, control flow, structs, arrays, maps, and process results. The language aims to strike a balance between usability and practical automation features, which is why the project includes both script execution and CLI inspection tooling."
            ]),
            ("Automation primitives", [
                "The automation layer is responsible for the day-to-day operations users expect from a local scripting environment. This includes process and system queries, notifications, clipboard actions, file manipulation, HTTP support when present, scheduling, and controlled command execution. The system does not try to hide these operations; instead, it presents them as explicit capabilities with documented boundaries.",
                "This makes Sapphire useful for desktop automation and local AI-assisted workflows. The user can write a script that checks system state, reads or writes files, and either sends a notification or triggers a local action with clear control over execution."
            ]),
            ("AI, ML, and optional dependencies", [
                "The AI and ML modules provide prompt and classification helpers, plus local tensor and optimization utilities. These features operate only when the relevant dependencies, drivers, or services are installed and configured. This is one of the project’s clearest design decisions: capabilities are real when the environment supports them, not assumed by declaration alone.",
                "This means that the same source code can behave differently across machines. The user may have the needed libraries on one computer and not on another, which is why the project describes optional packages and hardware requirements in a matter-of-fact way."
            ]),
            ("Portability and usage", [
                "The runtime is fundamentally Python-based, which makes it portable and inspectable. The packaged Windows distribution adds convenience tools and installation steps, but the behavior still depends on the local interpreter, the installed dependencies, and the underlying OS. The project therefore encourages users to validate their environment rather than assume a universal runtime state.",
                "This is a strength rather than a weakness: the language is flexible enough to be useful in real machines and real developer setups, while the project keeps the documentation honest about what is and is not guaranteed."
            ]),
        ],
    ),
    "Sapphire_Capabilities_and_Transparency_Manual.pdf": (
        "Sapphire Capability and Transparency Manual",
        "What is tested, what is optional, and what remains outside the current implementation.",
        [
            ("What is validated", [
                "The repository tests cover a significant subset of the runtime: language execution, process and file helpers, concurrency behavior, agent planning and tool execution, failures, persistence, memory retrieval, sandbox boundaries, CPU and ML behavior, and reporting around CUDA capability checks. This gives the project a meaningful validation story without pretending that it covers every possible deployment scenario.",
                "The emphasis is on local correctness and bounded capability. The designers have tried to document the subset of features that are actually tested, rather than offering a broad claim that every advanced AI workflow can be executed without careful configuration."
            ]),
            ("Optional runtime layers", [
                "The project is careful to separate the core interpreter from optional extras. Packages such as NumPy, PyTorch, psutil, requests, audio libraries, AI service integrations, NVIDIA drivers, and CUDA availability may be present or absent depending on the host environment. Some features are functional with the right environment, while others are intentionally unavailable if dependencies are missing.",
                "This matters because users can easily confuse feature existence with environment readiness. A method may be implemented in the source but still fail or behave differently when a required package, driver, or service is not present. Sapphire documents this distinction instead of hiding it."
            ]),
            ("Distributed and parallel claims", [
                "The distributed package supports planning, code generation, and cluster-spec artifacts, but the project is explicit that these are not proof of successful cluster launch or performance. There is a difference between drawing up a topology or code template and actually running a real distributed job with a verified environment. The repository keeps that distinction clear.",
                "This honesty is important because advanced AI tooling often fails in subtle ways when users assume that a specification automatically equals a working system. Sapphire documents the difference between a plan and an execution result, which is exactly the right boundary for a prototype runtime."
            ]),
            ("Roadmap and future work", [
                "The project does not present native compilation, production-grade isolation, event-driven syntax, DAG scheduling, neural memory durability, verified multi-node training, cluster recovery, or broad security certification as complete features. These remain future work or not-yet-validated areas. The project is transparent about this, and that transparency is part of the trust model.",
                "In other words, Sapphire is a working local-language and automation system with clear strengths, known boundaries, and a roadmap for greater scope. The aim is not to claim the impossible, but to provide a practical foundation that developers can inspect, use, and extend responsibly."
            ]),
        ],
    ),
}


def build_pdf(path: Path, title: str, subtitle: str, sections: list[tuple[str, list[str]]]) -> None:
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("Cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=colors.white, alignment=1))
    styles.add(ParagraphStyle("Sub", parent=styles["Normal"], fontSize=10, leading=13, textColor=colors.HexColor("#CBD5E1"), alignment=1))
    styles.add(ParagraphStyle("H", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#0F4C81"), spaceBefore=14, spaceAfter=8))
    styles.add(ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9.2, leading=12.2, spaceAfter=8, textColor=colors.HexColor("#111827")))

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        leftMargin=.6 * inch,
        rightMargin=.6 * inch,
        topMargin=.55 * inch,
        bottomMargin=.55 * inch,
        title=title,
        author="Sapphire Project",
    )

    story = [
        Table(
            [[Paragraph(title, styles["Cover"])], [Paragraph(subtitle, styles["Sub"]) ]],
            colWidths=[6.8 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#102A43")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#2CB1BC")),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]),
        ),
        Spacer(1, 10),
        Paragraph("This manual describes the current local implementation, tested behavior, and honest boundaries of Sapphire. It is intentionally detailed so the document remains readable and useful beyond a short summary.", styles["Body"]),
    ]

    for idx, (heading, paragraphs) in enumerate(sections):
        story.append(Paragraph(heading, styles["H"]))
        for para in paragraphs:
            story.append(Paragraph(para, styles["Body"]))
        if (idx + 1) % 2 == 0 and idx != len(sections) - 1:
            story.append(PageBreak())

    story.append(Spacer(1, 10))
    story.append(Paragraph("Version 1.0.7. This document is intentionally longer than a brief summary to provide context, operational detail, and practical caveats for local use. Values and capabilities depend on the machine, software environment, and installed dependencies.", styles["Body"]))

    doc.build(story)


if __name__ == "__main__":
    for filename, (title, subtitle, sections) in FILES.items():
        build_pdf(ROOT / filename, title, subtitle, sections)
        print(f"Generated {filename}")
