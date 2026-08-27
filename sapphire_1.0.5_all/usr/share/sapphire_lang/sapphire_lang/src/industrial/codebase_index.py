"""Small local codebase index for grounded Sapphire context."""

from __future__ import annotations

import re
from pathlib import Path


class CodebaseIndex:
    """Index source files into searchable, provenance-preserving text chunks."""

    def __init__(self, root: str | Path, extensions: tuple[str, ...] = (".sp", ".py", ".md", ".json")):
        self.root = Path(root).resolve()
        self.extensions = extensions
        self._documents: list[dict[str, str]] = []

    def rebuild(self) -> int:
        self._documents.clear()
        for path in self.root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in self.extensions:
                continue
            if any(part in {".git", "__pycache__", "build", "dist"} for part in path.parts):
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            relative = path.relative_to(self.root).as_posix()
            chunks = re.split(r"\n(?=(?:def |class |fn |##? |```))", content)
            for number, chunk in enumerate(chunks, 1):
                text = chunk.strip()
                if text:
                    self._documents.append({"source": relative, "chunk": str(number), "content": text})
        return len(self._documents)

    def search(self, query: str, limit: int = 5) -> list[dict[str, str]]:
        terms = {term.lower() for term in re.findall(r"[A-Za-z0-9_]{2,}", query)}
        scored = []
        for document in self._documents:
            words = set(re.findall(r"[A-Za-z0-9_]{2,}", document["content"].lower()))
            score = len(terms & words)
            if score:
                scored.append({**document, "score": str(score)})
        scored.sort(key=lambda item: (-int(item["score"]), item["source"], item["chunk"]))
        return scored[:limit]
