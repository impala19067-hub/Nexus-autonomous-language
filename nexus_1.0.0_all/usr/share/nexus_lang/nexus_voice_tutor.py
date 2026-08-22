"""
🌌 ADVANCED VOICE-GUIDED INTERACTIVE NEXUS LANGUAGE TUTOR
Learns Nexus Programming Language from 0 to Advanced Autonomous AI Development.
Features:
- Real-time Speech Voice Narration (Text-To-Speech SAPI5)
- Interactive Step-by-Step UI ("What to do next" guidance)
- 13 Chapter-wise Modules & Quizzes
- Embedded Live Nexus Code Execution Sandbox
"""

import sys
import os
import time
import threading
import queue
import traceback

# Reconfigure terminal encoding for UTF-8 compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
if hasattr(sys.stdin, 'reconfigure'):
    sys.stdin.reconfigure(encoding='utf-8')

# Robust Base Directory & Submodule Import Setup
if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NEXUS_DIR = os.path.join(BASE_DIR, "nexus_lang")

for p in [BASE_DIR, NEXUS_DIR]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

# Pre-import stdlib dependencies for PyInstaller static bundling
try:
    import requests
except ImportError:
    requests = None
try:
    import psutil
except ImportError:
    psutil = None
import urllib.request
import json
import ctypes
import subprocess
import platform

try:
    from src.lexer import Lexer
    from src.parser import Parser
    from src.interpreter import Interpreter
    NEXUS_ENGINE_AVAILABLE = True
    NEXUS_ENGINE_ERROR = None
except Exception as e:
    NEXUS_ENGINE_AVAILABLE = False
    NEXUS_ENGINE_ERROR = str(e)

# Speech Voice Engine Manager
class VoiceManager:
    def __init__(self):
        self.enabled = True
        self.speech_queue = queue.Queue()
        self.thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.engine_ready = False
        try:
            import pyttsx3
            self.pyttsx3 = pyttsx3
            self.thread.start()
            self.engine_ready = True
        except Exception:
            self.engine_ready = False

    def _speech_worker(self):
        try:
            engine = self.pyttsx3.init()
            engine.setProperty('rate', 170)
            while True:
                text = self.speech_queue.get()
                if text is None:
                    break
                if self.enabled:
                    try:
                        engine.say(text)
                        engine.runAndWait()
                    except Exception:
                        pass
                self.speech_queue.task_done()
        except Exception:
            pass

    def speak(self, text: str, wait: bool = False):
        if not self.enabled or not self.engine_ready:
            return
        clean_text = text.replace("`", "").replace("<b>", "").replace("</b>", "").replace("<i>", "").replace("</i>", "")
        self.speech_queue.put(clean_text)
        if wait:
            self.speech_queue.join()

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

voice = VoiceManager()

def print_banner(title: str):
    print("\n" + "=" * 68)
    print(f"  🌌 {title.upper()}")
    print("=" * 68)

def print_next_step(guidance: str):
    print("\n" + "👉 WHAT TO DO NEXT: " + guidance)
    voice.speak(f"What to do next: {guidance}")

def execute_nexus_code(code: str):
    if not NEXUS_ENGINE_AVAILABLE:
        print(f"⚠️ Nexus interpreter unavailable: {NEXUS_ENGINE_ERROR}")
        return None
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        return interpreter.interpret(ast)
    except Exception as e:
        print(f"❌ Execution Error: {e}")
        return None

# =========================================================================
# CHAPTER DEFINITIONS
# =========================================================================

CURRICULUM = [
    {
        "id": 1,
        "title": "Introduction to Nexus Architecture & Philosophy",
        "intro": "Welcome to Chapter 1! Nexus is an autonomous-first programming language built specifically for PC system control, native AI integration, and colorless parallel execution without complex boilerplate.",
        "content": """
Nexus key principles:
1. Zero Dependency System Control: Native modules (`os`, `fs`, `gui`, `http`, `ai`, `data`, `scheduler`).
2. First-class AI Primitive: `ai.prompt("...")` built into the language core.
3. Colorless Concurrency: `parallel { ... }` blocks instead of async/await hell.
""",
        "example": """// Chapter 1 Example: Hello World in Nexus
print("🌌 Welcome to Nexus Programming Language!");
print("Built for PC Automation and Autonomous AI Agents.");""",
        "quiz": {
            "question": "What is the primary architectural goal of Nexus Language?",
            "options": [
                "Building low-level device drivers",
                "PC System Automation & Autonomous AI with zero-boilerplate concurrency",
                "Writing simple HTML web pages"
            ],
            "correct": 2,
            "explanation": "Nexus is engineered specifically for system control and autonomous AI!"
        }
    },
    {
        "id": 2,
        "title": "Variables, Data Types & Printing",
        "intro": "In Chapter 2, you will learn how to declare variables and work with basic data types in Nexus.",
        "content": """
- Variables are declared using the `let` keyword:
    `let variable_name = value;`
- Supported Types: Strings, Integers, Floats, Booleans (`true`/`false`), Arrays, and Objects.
- Printing is done using the built-in `print(...)` function.
""",
        "example": """let agent_name = "Nexus-Alpha";
let agent_id = 101;
let system_health = 99.5;
let is_active = true;

print("Agent Name: " + agent_name);
print("Agent ID: " + agent_id);""",
        "quiz": {
            "question": "Which keyword is used to declare a variable in Nexus?",
            "options": [
                "var",
                "let",
                "const"
            ],
            "correct": 2,
            "explanation": "Variables in Nexus are always declared using `let`."
        }
    },
    {
        "id": 3,
        "title": "String Interpolation & Formatting",
        "intro": "In Chapter 3, you will learn how string interpolation allows you to embed variables directly into double-quoted strings.",
        "content": """
In Nexus, any double-quoted string can contain `{expression}` variables directly:
    `let user = "Alice";`
    `print("Hello {user}!");`

No string concatenation or complex formatting functions needed!
""",
        "example": """let host = "db-server-01";
let cpu_usage = 84.2;
let status = "ONLINE";

print("Server [{host}] Status: {status} (CPU: {cpu_usage}%)");""",
        "quiz": {
            "question": "How do you embed variable `score` into string 'User score is X' in Nexus?",
            "options": [
                "\"User score is $score\"",
                "\"User score is {score}\"",
                "\"User score is %score%\""
            ],
            "correct": 2,
            "explanation": "Nexus uses double quotes with curly braces `{score}` for string interpolation."
        }
    },
    {
        "id": 4,
        "title": "Decision Logic & Conditional Statements",
        "intro": "In Chapter 4, you will learn how to make decisions in your code using if and else statements.",
        "content": """
Conditionals use standard syntax:
    if (condition) {
        // execute if true
    } else if (another_condition) {
        // execute if another true
    } else {
        // fallback
    }

Logical Operators: `and`, `or`, `not`
""",
        "example": """let ram_usage = 87.5;

if (ram_usage > 90.0) {
    print("🚨 CRITICAL: High Memory Spikes!");
} else if (ram_usage > 75.0) {
    print("⚠️ WARNING: High Memory Consumption.");
} else {
    print("✅ NORMAL: Memory footprint optimal.");
}""",
        "quiz": {
            "question": "What logical operators are supported in Nexus conditional checks?",
            "options": [
                "and, or, not",
                "&&, ||, !",
                "BOTH and/or/not AND &&/||/!"
            ],
            "correct": 1,
            "explanation": "Nexus uses readable English keywords: `and`, `or`, `not`."
        }
    },
    {
        "id": 5,
        "title": "Loops & Iteration (`while`, `for ... in`)",
        "intro": "In Chapter 5, we cover repeating tasks using while loops and for-in loops.",
        "content": """
1. For-in loop over arrays:
    `for item in items { print(item); }`

2. While loop for continuous checks:
    `let count = 0; while (count < 3) { count = count + 1; }`
""",
        "example": """let modules = ["os", "fs", "http", "ai", "scheduler"];

print("Checking loaded Nexus stdlib modules:");
for mod in modules {
    print("  -> Module loaded: stdlib.{mod}");
}""",
        "quiz": {
            "question": "Which loop construct is best for iterating over elements in an array?",
            "options": [
                "for item in list { ... }",
                "loop item through list",
                "foreach (list as item)"
            ],
            "correct": 1,
            "explanation": "Nexus uses `for item in list { ... }` syntax."
        }
    },
    {
        "id": 6,
        "title": "Modular Functions (`fn`) & Scope",
        "intro": "Chapter 6 introduces reusable functions using the fn keyword.",
        "content": """
Functions are declared using `fn`:
    fn function_name(param1, param2) {
        let result = param1 + param2;
        return result;
    }
""",
        "example": """fn calculate_load_percentage(used, total) {
    let percentage = (used / total) * 100;
    return percentage;
}

let memory_load = calculate_load_percentage(14.2, 16.0);
print("Calculated Memory Load: {memory_load}%");""",
        "quiz": {
            "question": "What keyword defines a function in Nexus?",
            "options": [
                "def",
                "function",
                "fn"
            ],
            "correct": 3,
            "explanation": "Nexus uses `fn` to declare functions."
        }
    },
    {
        "id": 7,
        "title": "Standard Library: OS Telemetry & Notifications",
        "intro": "Chapter 7 demonstrates native system control using the os module.",
        "content": """
The `os` module provides native access to Windows OS:
- `os.system_info()`: Returns object with `platform`, `cpu_usage_percent`, `ram_percent`.
- `os.notify(title, message)`: Displays native Windows pop-up toast notification.
- `os.clip_write(text)`: Copies text directly to Windows Clipboard.
""",
        "example": """let sys_info = os.system_info();
print("🖥️ System Platform: {sys_info.platform}");
print("📊 CPU Usage: {sys_info.cpu_usage_percent}%");
print("💾 RAM Load: {sys_info.ram_percent}%");

os.notify("Nexus OS Audit", "System health audit completed!");""",
        "quiz": {
            "question": "Which function displays a Windows Desktop pop-up toast notification?",
            "options": [
                "os.notify(title, message)",
                "os.popup(title, message)",
                "system.alert(title, message)"
            ],
            "correct": 1,
            "explanation": "Use `os.notify(title, message)` for native toast alerts!"
        }
    },
    {
        "id": 8,
        "title": "Standard Library: File System Operations (`fs`)",
        "intro": "Chapter 8 teaches file reading, writing, and directory listing.",
        "content": """
The `fs` module handles file system operations:
- `fs.write(filepath, content)`: Writes string to file.
- `fs.read(filepath)`: Reads content from file.
- `fs.list_dir(dirpath)`: Returns list of filenames in directory.
""",
        "example": """fs.write("./nexus_audit_log.txt", "Timestamp: 2026-08-22 - System Normal");
print("✅ Log written successfully.");

let log_content = fs.read("./nexus_audit_log.txt");
print("📖 File Read Back: " + log_content);""",
        "quiz": {
            "question": "How do you list all files in a directory using Nexus `fs` module?",
            "options": [
                "fs.dir_contents(\".\")",
                "fs.list_dir(\".\")",
                "fs.ls(\".\")"
            ],
            "correct": 2,
            "explanation": "Use `fs.list_dir(path)` to retrieve directory items."
        }
    },
    {
        "id": 9,
        "title": "HTTP Networking & Data Serialization (`http`, `data`)",
        "intro": "Chapter 9 covers web requests and JSON serialization.",
        "content": """
- `http.get(url)`: Performs HTTP GET request, returns object with `ok`, `status_code`, `text`.
- `data.to_json(obj)`: Converts object to JSON string.
- `data.from_json(json_str)`: Parses JSON string to object.
""",
        "example": """let res = http.get("https://httpbin.org/get");
if (res.ok) {
    print("🌐 HTTP Request Successful! Status: {res.status_code}");
}

let report = {"timestamp": "2026-08-22", "status": "OK"};
let json_data = data.to_json(report);
print("📦 JSON Output: {json_data}");""",
        "quiz": {
            "question": "What property of `http.get()` response indicates request success?",
            "options": [
                "response.success",
                "response.ok",
                "response.status"
            ],
            "correct": 2,
            "explanation": "The `ok` boolean property indicates a 200 OK response."
        }
    },
    {
        "id": 10,
        "title": "Native AI Intelligence Primitives (`ai.prompt`)",
        "intro": "Chapter 10 teaches native AI integration using the built-in ai primitive.",
        "content": """
Nexus has built-in AI intelligence support directly in the syntax:
    `let result = ai.prompt("Your instructions or system log analysis");`

No external OpenAI SDKs or heavy dependencies required!
""",
        "example": """let system_log = "ERROR [20:05:12] High disk utilization on /dev/sda1 (94%).";
let decision = ai.prompt("Summarize risk and propose immediate fix: {system_log}");

print("🤖 AI Reasoning & Decision:");
print("   {decision}");""",
        "quiz": {
            "question": "How do you execute an AI intelligence prompt in Nexus?",
            "options": [
                "ai.prompt(\"...\")",
                "openai.Completion.create(\"...\")",
                "llm.query(\"...\")"
            ],
            "correct": 1,
            "explanation": "Nexus provides first-class `ai.prompt(\"...\")` built directly into the runtime!"
        }
    },
    {
        "id": 11,
        "title": "Colorless Concurrency (`parallel` block)",
        "intro": "Chapter 11 teaches how parallel execution blocks run multiple tasks concurrently.",
        "content": """
Nexus eliminates `async`, `await`, and promise callbacks.
Wrap any block of statements in `parallel { ... }` to execute them simultaneously!
""",
        "example": """print("⚡ Dispatching parallel subroutines...");
parallel {
    print("  -> Worker 1: Auditing network latency...");
    print("  -> Worker 2: Checking memory consumption...");
    print("  -> Worker 3: Scanning disk log files...");
}
print("✨ All concurrent workers finished!");""",
        "quiz": {
            "question": "What keyword construct is used to execute statements in parallel in Nexus?",
            "options": [
                "async { ... }",
                "parallel { ... }",
                "concurrent { ... }"
            ],
            "correct": 2,
            "explanation": "Nexus uses simple `parallel { ... }` blocks for colorless concurrency!"
        }
    },
    {
        "id": 12,
        "title": "Persistent Background Schedulers (`scheduler`)",
        "intro": "Chapter 12 teaches how to run persistent periodic tasks with the scheduler module.",
        "content": """
The `scheduler` module runs background tasks on fixed time intervals:
    `scheduler.interval(seconds, fn() { ... });`
""",
        "example": """print("⏳ Initializing periodic system health check...");
// Run audit every 10 seconds (example snippet)
scheduler.interval(10.0, fn() {
    let info = os.system_info();
    print("⏱️ [Heartbeat Audit] CPU: {info.cpu_usage_percent}%");
});""",
        "quiz": {
            "question": "Which method schedules a recurring background task in Nexus?",
            "options": [
                "scheduler.interval(seconds, callback)",
                "timer.repeat(seconds, callback)",
                "cron.schedule(seconds, callback)"
            ],
            "correct": 1,
            "explanation": "Use `scheduler.interval(seconds, callback)` for periodic autonomous jobs!"
        }
    },
    {
        "id": 13,
        "title": "Master Capstone: Building Complete Autonomous PC Autobots",
        "intro": "Congratulations on reaching Chapter 13! Now you will put everything together to build a complete Autonomous PC Autobot.",
        "content": """
An Autonomous PC Autobot combines all 12 concepts:
1. Perception (`os.system_info()`, `fs.list_dir()`)
2. Concurrency (`parallel { ... }`)
3. AI Decision Making (`ai.prompt()`)
4. System Action (`os.notify()`, `os.clip_write()`)
""",
        "example": """fn main_pc_autobot() {
    print("🤖 Launching Full Nexus Autonomous PC Autobot...");
    
    let stats = os.system_info();
    print("1. System Health: CPU {stats.cpu_usage_percent}%, RAM {stats.ram_percent}%");
    
    parallel {
        print("2. [Parallel Worker] Auditing disk log directory...");
        print("3. [Parallel Worker] Checking network connectivity...");
    }
    
    let ai_evaluation = ai.prompt("System RAM is {stats.ram_percent}%. Give 1-line health status.");
    print("4. AI Health Assessment: {ai_evaluation}");
    
    os.notify("Nexus Autobot Master", "Autonomous PC Audit Complete!");
    os.clip_write("Autobot Telemetry: RAM {stats.ram_percent}%");
    print("✨ PC Autobot Cycle Completed Successfully!");
}

main_pc_autobot();""",
        "quiz": {
            "question": "What four elements make up an Autonomous AI Agent in Nexus?",
            "options": [
                "Perception, Concurrency, AI Decision, and Action",
                "HTML, CSS, JS, and SQL",
                "Compiler, Linker, Assembler, and CPU"
            ],
            "correct": 1,
            "explanation": "Autonomous agents combine perception, parallel execution, AI reasoning, and automated action!"
        }
    }
]

# =========================================================================
# TUTOR INTERACTION CONTROLLER
# =========================================================================

def run_chapter(chap_idx: int):
    chap = CURRICULUM[chap_idx]
    print_banner(f"Chapter {chap['id']}: {chap['title']}")
    
    print("\n" + chap['intro'])
    voice.speak(chap['intro'], wait=True)
    
    print("\n--- Core Concepts ---")
    print(chap['content'])
    voice.speak("Here are the core concepts for this chapter.", wait=False)
    
    print_next_step("Press Enter to review the code example and run it live...")
    input()
    
    print("\n[Code Example]:")
    print(chap['example'])
    voice.speak("Let us execute the live Nexus code snippet for this chapter.", wait=False)
    
    print("\n[Executing Code Live in Nexus Engine...]:")
    print("-" * 50)
    execute_nexus_code(chap['example'])
    print("-" * 50)
    
    # Quiz
    print_banner(f"Chapter {chap['id']} Quiz & Verification")
    quiz = chap['quiz']
    print("\n❓ QUESTION: " + quiz['question'])
    voice.speak("Quiz question: " + quiz['question'], wait=False)
    
    for i, opt in enumerate(quiz['options'], 1):
        print(f"   {i}) {opt}")
        
    print_next_step("Enter your answer choice number (1-3):")
    while True:
        ans = input("Your Choice: ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(quiz['options']):
            chosen = int(ans)
            if chosen == quiz['correct']:
                msg = f"Correct! {quiz['explanation']}"
                print("\n✅ " + msg)
                voice.speak("Correct! " + quiz['explanation'], wait=True)
            else:
                msg = f"Incorrect. The correct answer was {quiz['correct']}: {quiz['options'][quiz['correct']-1]}. {quiz['explanation']}"
                print("\n❌ " + msg)
                voice.speak("Not quite. " + quiz['explanation'], wait=True)
            break
        else:
            print("Please enter a valid choice number.")

def run_interactive_course():
    print_banner("Nexus Step-by-Step Voice-Guided Course")
    voice.speak("Welcome to the step by step voice guided course for Nexus Programming Language.", wait=True)
    
    for idx in range(len(CURRICULUM)):
        run_chapter(idx)
        if idx < len(CURRICULUM) - 1:
            print_next_step(f"Press Enter to advance to Chapter {idx+2} (or type 'q' to return to menu):")
            user_input = input().strip().lower()
            if user_input == 'q':
                break
    
    print_banner("Course Chapter Module Finished!")
    voice.speak("Great job! You have completed the curriculum modules.", wait=True)

def live_sandbox():
    print_banner("Live Nexus Interactive Sandbox")
    if not NEXUS_ENGINE_AVAILABLE:
        print(f"❌ Interpreter engine unavailable: {NEXUS_ENGINE_ERROR}")
        voice.speak("Interpreter engine unavailable.", wait=False)
        input("\nPress Enter to return to main menu...")
        return

    voice.speak("Welcome to the live interactive sandbox. You can type any Nexus code to execute it immediately.", wait=False)
    print("Type your Nexus code line or snippet below. Type 'exit' or 'quit' to return to main menu.\n")
    
    try:
        interpreter = Interpreter()
        env = interpreter.global_env
    except Exception as e:
        print(f"❌ Failed to initialize Interpreter environment: {e}")
        input("\nPress Enter to return to main menu...")
        return

    while True:
        try:
            line = input("nexus> ")
            if line.strip().lower() in ("exit", "quit"):
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
            print("\nExiting sandbox mode...")
            break
        except Exception as e:
            print(f"❌ Sandbox Execution Error: {e}")
            voice.speak("Execution error.", wait=False)

def settings_menu():
    print_banner("Voice & Audio Settings")
    current_status = "ENABLED" if voice.enabled else "DISABLED"
    print(f"Current Voice Status: {current_status}")
    print("1. Toggle Voice Speech ON/OFF")
    print("2. Return to Main Menu")
    
    print_next_step("Select option (1-2):")
    choice = input("Choice: ").strip()
    if choice == "1":
        new_state = voice.toggle()
        state_str = "ENABLED" if new_state else "DISABLED"
        print(f"\n✅ Voice Speech is now {state_str}.")
        if new_state:
            voice.speak("Voice speech enabled.")

def main_menu():
    voice.speak("Welcome to the Advanced Voice Guided Nexus Language Tutor.", wait=False)
    while True:
        print_banner("Nexus Advanced Voice-Guided Interactive Tutor")
        print("1. 🎓 Start Guided Course (13 Step-by-Step Chapters & Quizzes)")
        print("2. 📚 Select Specific Chapter")
        print("3. 🧪 Open Live Interactive Code Sandbox")
        print("4. 🔊 Voice & Speech Settings")
        print("5. 🚪 Exit")
        
        print_next_step("Select an option by entering a number from 1 to 5:")
        choice = input("Choice: ").strip()
        
        if choice == "1":
            run_interactive_course()
        elif choice == "2":
            print_banner("Chapter Selection")
            for c in CURRICULUM:
                print(f"  Chapter {c['id']}: {c['title']}")
            print_next_step("Enter Chapter number (1-13):")
            ch_num = input("Chapter: ").strip()
            if ch_num.isdigit() and 1 <= int(ch_num) <= len(CURRICULUM):
                run_chapter(int(ch_num) - 1)
        elif choice == "3":
            live_sandbox()
        elif choice == "4":
            settings_menu()
        elif choice == "5":
            print("\nThank you for learning Nexus Language! Goodbye! 🚀\n")
            voice.speak("Thank you for learning Nexus Language. Goodbye!", wait=True)
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as err:
        print(f"\n❌ Unexpected Application Error: {err}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
