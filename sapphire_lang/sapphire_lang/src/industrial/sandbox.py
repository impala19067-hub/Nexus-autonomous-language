"""Workspace-confined file and process sandbox for opt-in applications."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Iterable, Sequence


class SandboxViolation(PermissionError):
    """Raised when an operation leaves the configured workspace."""


class WorkspaceSandbox:
    def __init__(self, root: str | os.PathLike[str], allowed_commands: Iterable[str] = ()):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.allowed_commands = frozenset(allowed_commands)

    def resolve(self, relative_path: str | os.PathLike[str]) -> Path:
        candidate = (self.root / relative_path).resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as error:
            raise SandboxViolation(f"Path escapes sandbox: {relative_path}") from error
        return candidate

    def read_text(self, relative_path: str) -> str:
        return self.resolve(relative_path).read_text(encoding="utf-8")

    def write_text(self, relative_path: str, content: str) -> Path:
        target = self.resolve(relative_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def run(self, command: str, args: Sequence[str] = (), timeout: float = 10.0) -> subprocess.CompletedProcess[str]:
        if self.allowed_commands and command not in self.allowed_commands:
            raise SandboxViolation(f"Command is not allowed: {command}")
        return subprocess.run(
            [command, *args], cwd=self.root, capture_output=True,
            text=True, timeout=timeout, shell=False, check=False,
        )
