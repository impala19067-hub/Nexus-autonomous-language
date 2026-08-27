"""Console entry point used by the packaged Sapphire compiler."""
import os
import sys
import concurrent
import concurrent.futures
import concurrent.futures.thread
import concurrent.futures.process
import multiprocessing
import threading
import queue
import platform
import urllib.request
import urllib.parse
import http.client
import ssl
import socket
import tempfile
import shutil
import math
import random
import re
import datetime
import inspect
import importlib
import types
import traceback
import io

BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
SAPPHIRE_DIR = os.path.join(BASE_DIR, "sapphire_lang")
for path in (BASE_DIR, SAPPHIRE_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)

from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


def main():
    if len(sys.argv) != 2:
        print("Usage: sapphire_runtime <script.sp>", file=sys.stderr)
        return 2
    try:
        with open(sys.argv[1], "r", encoding="utf-8") as file_handle:
            source = file_handle.read()
        ast = Parser(Lexer(source).tokenize()).parse()
        Interpreter().interpret(ast)
        return 0
    except Exception as error:
        print(f"Error in {sys.argv[1]}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
