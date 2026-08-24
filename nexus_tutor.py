"""
🌌 NEXUS LANGUAGE AUTONOMOUS TUTOR (Interactive CLI & Executable)
Learn Nexus Language step-by-step through interactive lessons, quizzes, live REPL, and autonomous bot demos.
"""

import sys
import os
import time

# Ensure UTF-8 output encoding for terminal symbols & emojis
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# Include local nexus_lang directory in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
NEXUS_DIR = os.path.join(CURRENT_DIR, "nexus_lang")
if os.path.exists(NEXUS_DIR) and NEXUS_DIR not in sys.path:
    sys.path.insert(0, NEXUS_DIR)

try:
    from src.lexer import Lexer
    from src.parser import Parser
    from src.interpreter import Interpreter
    NEXUS_ENGINE_AVAILABLE = True
except Exception as e:
    NEXUS_ENGINE_AVAILABLE = False
    NEXUS_ENGINE_ERROR = str(e)

def print_header(title):
    print("\n" + "=" * 64)
    print(f"  🌌 {title.upper()}")
    print("=" * 64)

def print_sub(title):
    print(f"\n--- {title} ---")

def execute_nexus_snippet(code: str):
    """Utility to run inline Nexus code and display output."""
    if not NEXUS_ENGINE_AVAILABLE:
        print("⚠️ Nexus interpreter engine unavailable.")
        return None
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.interpret(ast)
    except Exception as e:
        print(f"❌ Nexus Runtime Error: {e}")
        return None

def chapter_1_basics():
    print_header("Chapter 1: Nexus Syntax, Variables & Strings")
    print("""
Nexus is a modern high-level language designed for PC Automation and Autonomous AI.

Key Concepts:
- Variables are declared with `let`: `let name = "Nexus";`
- Strings support inline variable interpolation using `{var}` syntax:
    let agent = "Autobot";
    let speed = 100;
    print("Agent {agent} speed: {speed}%");
- Basic types: strings, integers, floats, booleans (`true`/`false`), arrays, and objects/dictionaries.
""")
    input("Press Enter to run the Chapter 1 code example...")

    code = """
let language = "Nexus";
let version = 1.0;
let features = ["System Automation", "AI Integration", "Colorless Parallel"];

print("🚀 Welcome to {language} v{version}!");
for feat in features {
    print("  -> Feature: {feat}");
}
"""
    print("\n[Executing Nexus Code Snippet]:")
    print(code)
    print("-" * 40)
    execute_nexus_snippet(code)
    print("-" * 40)

    # Quiz
    print("\n🧠 QUICK QUIZ:")
    print("How do you perform string interpolation in Nexus?")
    print("1) 'Hello ' + name")
    print("2) 'Hello {name}'")
    print("3) 'Hello $name'")
    ans = input("Your choice (1-3): ").strip()
    if ans == "2":
        print("✅ Correct! Nexus evaluates {expr} directly inside double-quoted strings.")
    else:
        print("❌ In Nexus, use double quotes with braces: \"Hello {name}\".")

def chapter_2_control_flow():
    print_header("Chapter 2: Functions & Control Flow")
    print("""
Functions in Nexus are defined using the `fn` keyword:

    fn calculate_score(base, bonus) {
        let total = base + bonus;
        return total;
    }

Control Flow:
- `if (condition) { ... } else { ... }`
- `while (condition) { ... }`
- `for item in list { ... }`
""")
    input("Press Enter to run the Chapter 2 code example...")

    code = """
fn evaluate_system_load(cpu) {
    if (cpu > 80) {
        return "CRITICAL LOAD";
    } else {
        return "NORMAL OPERATING RANGE";
    }
}

let cpu_usage = 87;
let status = evaluate_system_load(cpu_usage);
print("System Load ({cpu_usage}%): {status}");
"""
    print("\n[Executing Nexus Code Snippet]:")
    print(code)
    print("-" * 40)
    execute_nexus_snippet(code)
    print("-" * 40)

def chapter_3_stdlib():
    print_header("Chapter 3: Native PC Automation Standard Library")
    print("""
Nexus provides first-class built-in modules for OS & PC control:

- `os`: `os.system_info()`, `os.notify(title, msg)`, `os.clip_write(text)`
- `fs`: `fs.read(path)`, `fs.write(path, data)`, `fs.list_dir(path)`
- `http`: `http.get(url)`, `http.post(url, data)`
- `data`: `data.to_json(obj)`, `data.from_json(json_str)`
""")
    input("Press Enter to run the Chapter 3 code example...")

    code = """
let info = os.system_info();
print("🖥️ System Overview:");
print("  -> OS Platform: {info.platform}");
print("  -> CPU Usage: {info.cpu_usage_percent}%");
print("  -> Memory Usage: {info.ram_percent}%");

let test_data = {"status": "ACTIVE", "agents": 4};
let json_str = data.to_json(test_data);
print("📦 Serialized JSON: {json_str}");
"""
    print("\n[Executing Nexus Code Snippet]:")
    print(code)
    print("-" * 40)
    execute_nexus_snippet(code)
    print("-" * 40)

def chapter_4_parallel():
    print_header("Chapter 4: Colorless Concurrency & Parallel Execution")
    print("""
Unlike languages with async/await syntax overhead, Nexus supports native `parallel` blocks:

    parallel {
        task_a();
        task_b();
        task_c();
    }

All statements inside a `parallel` block execute concurrently!
""")
    input("Press Enter to run the Chapter 4 code example...")

    code = """
print("⚡ Launching concurrent diagnostic subroutines...");
parallel {
    print("  [Worker 1] Scanning file system integrity...");
    print("  [Worker 2] Checking HTTP endpoints...");
    print("  [Worker 3] Auditing system memory footprint...");
}
print("✨ Concurrency synchronization complete!");
"""
    print("\n[Executing Nexus Code Snippet]:")
    print(code)
    print("-" * 40)
    execute_nexus_snippet(code)
    print("-" * 40)

def chapter_5_ai():
    print_header("Chapter 5: Native AI Intelligence (`ai.prompt`)")
    print("""
Nexus has native AI primitives built into the runtime.
No heavy LLM dependencies required to structure AI tasks:

    let prompt_text = "Analyze system crash log...";
    let response = ai.prompt(prompt_text);
    print("AI Analysis: {response}");

Nexus automatically routes AI prompts to configured intelligence engines or embedded heuristic models.
""")
    input("Press Enter to run the Chapter 5 code example...")

    code = """
let telemetry_log = "WARN: Memory usage spiked to 92% during backup job.";
let analysis = ai.prompt("Summarize key risk: {telemetry_log}");
print("🤖 AI Diagnostics Output:");
print("   {analysis}");
"""
    print("\n[Executing Nexus Code Snippet]:")
    print(code)
    print("-" * 40)
    execute_nexus_snippet(code)
    print("-" * 40)

def chapter_6_autobot():
    print_header("Chapter 6: Building Your First Autonomous Agent")
    print("""
Putting it all together to create a self-monitoring PC Autobot:

An autonomous bot combines:
1. System audit (`os.system_info`)
2. AI decision making (`ai.prompt`)
3. Automated action (`os.notify`, `fs.write`, `os.clip_write`)
4. Scheduling (`scheduler.interval`)
""")
    input("Press Enter to run the full Autonomous Bot code...")

    code = """
fn autonomous_health_check() {
    let stats = os.system_info();
    let status_summary = "CPU: {stats.cpu_usage_percent}%, RAM: {stats.ram_percent}%";
    
    let decision = ai.prompt("Evaluate system state: {status_summary}");
    print("🤖 Agent Decision: {decision}");
    
    os.notify("Nexus Autonomous Agent", status_summary);
    os.clip_write(status_summary);
    print("✅ Notification posted & Telemetry copied to clipboard!");
}

autonomous_health_check();
"""
    print("\n[Executing Full Autonomous Bot Snippet]:")
    print(code)
    print("-" * 40)
    execute_nexus_snippet(code)
    print("-" * 40)

def start_guided_course():
    print_header("Nexus Interactive Guided Course")
    chapters = [
        chapter_1_basics,
        chapter_2_control_flow,
        chapter_3_stdlib,
        chapter_4_parallel,
        chapter_5_ai,
        chapter_6_autobot
    ]
    for idx, chap in enumerate(chapters, 1):
        chap()
        if idx < len(chapters):
            cont = input(f"\nPress Enter for Chapter {idx + 1} (or 'q' to return to main menu): ").strip()
            if cont.lower() == 'q':
                break

def launch_repl():
    if not NEXUS_ENGINE_AVAILABLE:
        print("❌ Interpreter engine unavailable.")
        return
    print_header("Interactive Nexus REPL Engine")
    print("Type Nexus expressions or code blocks. Type 'exit' to return to main menu.\n")
    interpreter = Interpreter()
    env = interpreter.global_env
    while True:
        try:
            line = input("nexus> ")
            if line.strip() in ("exit", "quit"):
                break
            if not line.strip():
                continue
            lexer = Lexer(line)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ast = parser.parse()
            res = interpreter.interpret(ast, env)
            if res is not None:
                print(f"=> {interpreter._stringify(res)}")
        except KeyboardInterrupt:
            print("\nExiting REPL...")
            break
        except Exception as e:
            print(f"Error: {e}")

def run_sample_bots():
    print_header("Run Pre-Built Sample Autonomous Bots")
    examples_dir = os.path.join(NEXUS_DIR, "examples")
    if not os.path.exists(examples_dir):
        print("⚠️ Examples folder not found.")
        return
    files = [f for f in os.listdir(examples_dir) if f.endswith(".nx")]
    print("Available Sample Scripts:")
    for idx, f in enumerate(files, 1):
        print(f"  {idx}. {f}")
    
    choice = input("\nSelect script number to run (or press Enter to return): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(files):
        target_file = os.path.join(examples_dir, files[int(choice) - 1])
        print(f"\nExecuting {files[int(choice) - 1]}...")
        print("-" * 50)
        with open(target_file, 'r', encoding='utf-8') as f:
            content = f.read()
        execute_nexus_snippet(content)
        print("-" * 50)

def generate_sample_files():
    print_header("Generate Sample Nexus Scripts")
    output_path = os.path.join(CURRENT_DIR, "my_first_nexus_bot.nx")
    sample_code = """// My First Autonomous AI Agent in Nexus
fn main() {
    print("🤖 Initializing Autonomous Nexus Agent...");
    
    let info = os.system_info();
    print("System Diagnostics: RAM {info.ram_percent}%, CPU {info.cpu_usage_percent}%");
    
    let ai_opinion = ai.prompt("System RAM is at {info.ram_percent}%. Is this healthy?");
    print("AI Evaluation: {ai_opinion}");
    
    os.notify("Nexus Bot Status", "System state evaluated successfully!");
    print("✨ Agent task execution finished!");
}

main();
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(sample_code)
    print(f"✅ Generated sample script at: {output_path}")
    print("You can run this file anytime using: python nexus_lang/src/cli.py run my_first_nexus_bot.nx")

def main_menu():
    while True:
        print_header("Nexus Autonomous AI & Language Interactive Tutor")
        print("1. 🎓 Guided Chapter Lessons & Quizzes")
        print("2. 🌌 Launch Interactive Nexus REPL")
        print("3. 🤖 Run Pre-Built Sample Autonomous Bots")
        print("4. 💾 Generate Sample 'my_first_nexus_bot.nx' Script")
        print("5. ℹ️  Nexus Architecture & Language Overview")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        if choice == "1":
            start_guided_course()
        elif choice == "2":
            launch_repl()
        elif choice == "3":
            run_sample_bots()
        elif choice == "4":
            generate_sample_files()
        elif choice == "5":
            print_header("Nexus Language Overview")
            print("""
Nexus is an autonomous-first programming language created for seamless system control,
AI integration, and colorless concurrency.

Key Advantages over legacy languages:
- Built-in OS, FS, HTTP, GUI, Data, and Scheduler standard libraries.
- Native `ai.prompt()` primitive for instant intelligence tasks.
- `parallel` block construct eliminating async/await callback hell.
- Lightweight footprint and zero external setup requirements.
""")
            input("Press Enter to return to main menu...")
        elif choice == "6":
            print("\nThank you for using Nexus Language Autonomous Tutor! Happy Coding! 🚀\n")
            break
        else:
            print("Invalid selection, please try again.")

if __name__ == "__main__":
    main_menu()
