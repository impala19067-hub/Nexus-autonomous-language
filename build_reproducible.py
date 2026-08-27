"""Create a deterministic release manifest for Sapphire artifacts."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARTIFACTS = [
    'sapphire_cli.py', 'sapphire_compiler.py', 'emerald_studio.py',
    'sapphire_studio.py', 'INDUSTRIAL_READINESS.md',
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    manifest = {
        'source_date_epoch': os.environ.get('SOURCE_DATE_EPOCH', 'unset'),
        'python': platform.python_version(),
        'platform': platform.platform(),
        'artifacts': {
            name: sha256(ROOT / name)
            for name in ARTIFACTS if (ROOT / name).is_file()
        },
    }
    (ROOT / 'release_manifest.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n', encoding='utf-8'
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
