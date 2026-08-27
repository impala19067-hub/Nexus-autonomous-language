"""Repeatable lightweight security checks for the opt-in industrial utilities."""
from __future__ import annotations

import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'sapphire_lang'))
sys.path.insert(0, str(ROOT / 'sapphire_lang' / 'src'))

from industrial import SandboxViolation, WorkspaceSandbox


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        sandbox = WorkspaceSandbox(directory, allowed_commands=[])
        sandbox.write_text('audit.txt', 'sandbox ok')
        if sandbox.read_text('audit.txt') != 'sandbox ok':
            raise AssertionError('sandbox round trip failed')
        try:
            sandbox.resolve('../escape.txt')
        except SandboxViolation:
            pass
        else:
            raise AssertionError('sandbox accepted a path traversal')
    print('PASS: workspace path confinement')
    print('PASS: UTF-8 sandbox read/write')
    print('NOTE: This is an automated regression check, not an independent security audit.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
