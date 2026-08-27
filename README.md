# Sapphire Programming Language

Sapphire is a Python-based interpreted programming language and Windows distribution for local scripting, automation, AI-assisted workflows, and prototype ML tooling. It is designed for learning, experimentation, and local PC automation rather than for claiming a full production-grade distributed AI platform.

## Current release

- Language and installer version: 1.0.7
- Tested interpreter: Python 3.12.10
- Primary distribution: Windows setup wizard, CLI tools, and bundled documentation
- Bundle status: compact single-page PDF manuals regenerated and published
- Optional integrations: NumPy, PyTorch, psutil, requests, audio packages, and configured AI service backends

## What Sapphire includes

### Language features

- `let` and `const` declarations with optional type annotations
- Functions, conditionals, loops, arrays, maps, structs, lambdas, returns, and exceptions
- Arithmetic, comparisons, boolean logic, indexing, member access, and pipelines
- `parallel { ... }` execution blocks
- Shell/process literals using backticks or `$`, returning a `ProcessResult`
- `.sp` script execution, REPL mode, inline evaluation, and CLI inspection tools

### Standard library

- `os`: system information, process control, notifications, clipboard access, and bounded command execution
- `fs`: file read/write/append/remove operations
- `http`: optional HTTP helpers when the dependency is installed
- `ai`: prompt, classification, and JSON extraction flows via local/cloud backends or offline fallback behavior
- `ml`: tensor primitives, dataset helpers, optimization and loss utilities, and optional CUDA/PyTorch execution paths
- `scheduler`: SQLite-backed scheduled work
- `agent`: memory, planning, permissions, bounded execution, and orchestration support

> Optional integrations depend on installed packages, hardware, drivers, credentials, and service availability. They are not automatically available just because the API exists.

## Project tools

- `Emerald_Studio.exe`: editor, runner, template builder, hardware display, and agent runtime panel
- `Sapphire_Compiler.exe`: script execution and AST/IR inspection tool
- `Sapphire_Setup_Wizard.exe`: installer for the runtime, docs, PATH configuration, `.sp` association, and shortcuts

## Installation

On Windows, run `Sapphire_Setup_Wizard.exe` and keep PATH and shortcuts enabled if desired. After installation, open a new terminal and run:

```text
sapphire info
sapphire run hello.sp
sapphire studio
```

For source execution from the repository:

```text
python sapphire_lang/src/cli.py run path/to/script.sp
python -m unittest sapphire_lang.tests.test_sapphire sapphire_lang.tests.test_industrial_readiness
```

## Included documentation bundle

The project root includes the following compact single-page manuals and guides:

- [Sapphire_Coding_and_Usage_Guide.pdf](Sapphire_Coding_and_Usage_Guide.pdf) — practical coding reference and usage guide
- [Building_Advanced_Autonomous_AI.pdf](Building_Advanced_Autonomous_AI.pdf) — advanced automation and autonomous AI patterns
- [Sapphire_Autonomy_and_Performance_Benchmarks.pdf](Sapphire_Autonomy_and_Performance_Benchmarks.pdf) — benchmark and autonomy analysis
- [Beginners_Guide_Your_First_Autonomous_AI.pdf](Beginners_Guide_Your_First_Autonomous_AI.pdf) — beginner-facing onboarding guide
- [Sapphire_Language_Specification_and_Automation_Manual.pdf](Sapphire_Language_Specification_and_Automation_Manual.pdf) — specification and automation reference
- [Sapphire_Capabilities_and_Transparency_Manual.pdf](Sapphire_Capabilities_and_Transparency_Manual.pdf) — current scope, transparency notes, and known limitations

The bundle has been regenerated to reduce large blank areas and fit the content into a tighter one-page format for easier browsing.

Additional project documentation:

- [INSTALLATION_AND_USAGE_GUIDE.md](INSTALLATION_AND_USAGE_GUIDE.md)
- [INDUSTRIAL_READINESS.md](INDUSTRIAL_READINESS.md)

## Validation and limits

The repository includes validation around language execution, process and file helpers, concurrency, agent planning, failure handling, persistence, sandbox boundaries, CPU/ML behavior, and optional CUDA reporting.

A benchmark can be run with:

```text
python benchmarks/benchmark_runtime.py
```

One reference run on Python 3.12.10 completed 100 parse-and-interpret iterations of a 100-item loop with:

- result: 4950
- median: 0.21095 ms
- minimum: 0.2023 ms
- maximum: 0.7817 ms

Those numbers are machine-specific and are not a language-wide guarantee. This project does not currently include cross-language, cluster-scale, or large GPU-training validation.

## Roadmap and known limitations

The following are not presented as completed production features: native compiler backend, strong isolation guarantees, persistent vector embeddings, event-driven agent declarations, DAG scheduling, verified multi-node training, automatic cluster recovery, and broad security certification.

See [INDUSTRIAL_READINESS.md](INDUSTRIAL_READINESS.md) and [Sapphire_Capabilities_and_Transparency_Manual.pdf](Sapphire_Capabilities_and_Transparency_Manual.pdf) for the tested scope and known limitations.

## Quick start

```text
python -m pip install -r requirements.txt
python sapphire_lang/src/cli.py --help
```

Then run a sample script or launch the included studio tool:

```text
python sapphire_lang/src/cli.py run examples/01_basics.sp
```

If the Windows installer is used, the bundled `.sp` association and runtime tools are installed automatically.
