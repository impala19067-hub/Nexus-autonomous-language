"""Small reproducible runtime benchmark; reports machine-readable JSON."""
import json
import os
import statistics
import sys
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LANG = os.path.join(ROOT, 'sapphire_lang')
sys.path.insert(0, LANG)

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter

SOURCE = 'let total = 0; for item in range(100) { total = total + item; } total;'


def run(iterations=100):
    samples = []
    for _ in range(iterations):
        started = time.perf_counter_ns()
        ast = Parser(Lexer(SOURCE).tokenize()).parse()
        result = Interpreter().interpret(ast)
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
    return {
        'benchmark': 'parse_and_interpret_100_item_loop',
        'iterations': iterations,
        'result': result,
        'median_ms': statistics.median(samples),
        'min_ms': min(samples),
        'max_ms': max(samples),
        'python': sys.version.split()[0],
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
