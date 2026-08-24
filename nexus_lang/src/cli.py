"""
Sapphire Language Command Line Interface (CLI)
"""
import sys
import os
import argparse
import subprocess

# Resolve the directory that contains this file (i.e. nexus_lang/src/)
_SRC_DIR = os.path.abspath(os.path.dirname(__file__))
# Resolve nexus_lang/ (parent of src/)
_NEXUS_LANG_DIR = os.path.abspath(os.path.join(_SRC_DIR, '..'))
# Resolve workspace root
_WORKSPACE_ROOT = os.path.abspath(os.path.join(_NEXUS_LANG_DIR, '..'))

# Make sure both dirs are on the path so imports work regardless of cwd or
# how the script is invoked (direct script vs. python -m module).
for _p in (_NEXUS_LANG_DIR, _SRC_DIR, _WORKSPACE_ROOT):
    if _p not in sys.path:
        sys.path.insert(0, _p)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

VERSION = "1.0.0 (Automation & AI Era)"

def run_code(source: str, filename: str = "<stdin>", verbose: bool = False) -> any:
    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        if verbose:
            print("--- TOKENS ---")
            for t in tokens: print(t)

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        return result
    except Exception as e:
        print(f"❌ Error in {filename}: {e}", file=sys.stderr)
        return None

def run_file(filepath: str, verbose: bool = False):
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    run_code(source, filename=filepath, verbose=verbose)

def start_repl():
    print(f"💎 Sapphire Language REPL {VERSION}")
    print("Type 'exit' or 'quit' to exit.\n")

    interpreter = Interpreter()
    env = interpreter.global_env

    while True:
        try:
            line = input("sapphire> ")
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

def launch_studio():
    studio_py = os.path.join(_WORKSPACE_ROOT, "sapphire_studio.py")
    if not os.path.exists(studio_py):
        # Fallback check
        studio_py = os.path.join(os.getcwd(), "sapphire_studio.py")

    if os.path.exists(studio_py):
        print("🚀 Launching Sapphire Developer Studio GUI...")
        subprocess.Popen([sys.executable, studio_py])
    else:
        print("❌ sapphire_studio.py script not found.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Sapphire Language CLI Engine")
    parser.add_argument("command", nargs="?", default="repl", choices=["run", "eval", "repl", "info", "studio"], help="Command to execute")
    parser.add_argument("file_or_code", nargs="?", help="Script file path (.sp) or inline code string")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug token/AST output")

    args = parser.parse_args()

    if args.command == "run":
        if not args.file_or_code:
            print("Usage: sapphire run <script.sp>")
            sys.exit(1)
        run_file(args.file_or_code, verbose=args.verbose)
    elif args.command == "eval":
        if not args.file_or_code:
            print('Usage: sapphire eval "<code>"')
            sys.exit(1)
        run_code(args.file_or_code, filename="<eval>", verbose=args.verbose)
    elif args.command == "info":
        print(f"💎 Sapphire Language v{VERSION}")
        print("Architecture: Data → Training → Model → Reasoning → Memory → Planning → Tools → Autonomy")
        print("Capabilities: Full PC Automation, Concurrency, Shell Piping, AI Agent Architecture,")
        print("              Ollama & Groq Cloud LLMs, Tensor Engine, Autograd, Massive Datasets,")
        print("              Model Architectures, Distributed Training, Numerical Kernels, GPU/TPU")
        print("Extension   : .sp")
    elif args.command == "repl":
        start_repl()
    elif args.command == "studio":
        launch_studio()

if __name__ == "__main__":
    main()
