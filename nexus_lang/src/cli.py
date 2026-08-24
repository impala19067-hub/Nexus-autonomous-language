"""
Sapphire Language Command Line Interface (CLI)
"""
import sys
import os
import argparse

# Resolve the directory that contains this file (i.e. nexus_lang/src/)
_SRC_DIR = os.path.abspath(os.path.dirname(__file__))
# Resolve nexus_lang/ (parent of src/)
_NEXUS_LANG_DIR = os.path.abspath(os.path.join(_SRC_DIR, '..'))

# Make sure both dirs are on the path so imports work regardless of cwd or
# how the script is invoked (direct script vs. python -m module).
for _p in (_NEXUS_LANG_DIR, _SRC_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

VERSION = "1.0.0 (Automation Era)"

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

def main():
    parser = argparse.ArgumentParser(description="Sapphire Language CLI Engine")
    parser.add_argument("command", nargs="?", default="repl", choices=["run", "eval", "repl", "info"], help="Command to execute")
    parser.add_argument("file_or_code", nargs="?", help="Script file path or inline code string")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug token/AST output")

    args = parser.parse_args()

    if args.command == "run":
        if not args.file_or_code:
            print("Usage: sapphire run <script.nx>")
            sys.exit(1)
        run_file(args.file_or_code, verbose=args.verbose)
    elif args.command == "eval":
        if not args.file_or_code:
            print('Usage: sapphire eval "<code>"')
            sys.exit(1)
        run_code(args.file_or_code, filename="<eval>", verbose=args.verbose)
    elif args.command == "info":
        print(f"💎 Sapphire Language v{VERSION}")
        print("Capabilities: Full PC Automation, Concurrency, Shell Piping, AI Agent Primitives,")
        print("              Tensor Engine, Automatic Differentiation, Massive Datasets,")
        print("              Model Architectures, Distributed Training, Numerical Kernels, GPU/TPU")
    elif args.command == "repl":
        start_repl()

if __name__ == "__main__":
    main()
