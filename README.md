# Sapphire Programming Language

Sapphire is a small interpreted programming language and Windows distribution for scripting, local PC automation, AI service calls, and experimental ML utilities. The current implementation is a tree-walk interpreter written in Python. It is useful for learning, prototypes, and local automation; it is not a native machine-code compiler or a distributed training platform.

## Current Release

- Language and installer: `1.0.5`
- Tested interpreter: Python `3.12.10`
- Primary distribution: Windows setup wizard and bundled tools
- Optional integrations: NumPy, PyTorch, psutil, requests, audio packages, and configured AI services

## What Works

### Language

- `let` and `const` bindings with optional type annotations
- Functions, conditionals, loops, arrays, maps, structs, lambdas, return values, and exceptions
- Arithmetic, comparisons, boolean operators, member access, indexing, and pipes
- `parallel { ... }` execution blocks
- Shell/process literals using backticks or `$`, returning a `ProcessResult`
- `.sp` script execution, REPL, inline evaluation, and source inspection through the CLI

### Standard Library

- `os`: system information, processes, notifications, clipboard operations, and controlled command execution
- `fs`: UTF-8 file read, write, append, and remove operations
- `http`: HTTP helpers when the optional request dependency is available
- `ai`: prompt, classification, and JSON extraction through configured local/cloud backends or offline fallback behavior
- `ml`: tensors, basic autodiff, model helpers, datasets, losses, optimizers, CPU kernels, and optional CUDA/PyTorch paths
- `scheduler`: SQLite-backed scheduled work
- `agent`: memory, planning, tool registration, permissions, bounded execution, and orchestration

Optional integrations do not become available merely because an API exists. They depend on installed packages, credentials, services, drivers, and hardware.

## Agent Runtime

The agent module provides a runtime loop with these stages:

`observe -> remember -> plan -> select tool -> execute -> verify -> recover/replan`

The runtime currently supports:

- Recent working history and an in-process long-term key/value similarity store
- SQLite FTS5 memory through the industrial utilities
- AI-generated plans with JSON parsing and deterministic fallbacks
- Registered tools with descriptions and schemas
- Permission modes: permissive, interactive, and strict
- Bounded budgets for steps, tokens, elapsed time, and tool calls
- Optional verifier and recovery callbacks
- Sequential multi-agent orchestration

Example:

```sapphire
let report = agent.autonomy.run_loop("Inspect system health and notify the user", 5);
print(report.state);
```

The current language does not yet provide parser-level `agent "Name" { ... }` declarations, event triggers, or DAG syntax. Agent configuration is available through the runtime API and host-side Python integration.

## ML and Hardware Boundaries

- Tensor, dataset, model, loss, optimizer, and autodiff helpers run locally.
- NumPy is used for acceleration when installed; otherwise the implementation retains Python fallbacks for supported operations.
- CUDA operations require CUDA-enabled PyTorch, a compatible NVIDIA driver, and an actual CUDA device.
- `ml.distributed` describes topology, memory, communication, parallelism, and launcher plans. It does not launch or validate a multi-node or 512-GPU job.
- Generated launcher/code artifacts are plans or templates and must be reviewed and executed in an independently configured environment.

## Tools

- `Emerald_Studio.exe` is a Tk-based editor, script runner, tool template builder, hardware display, and agent information panel.
- `Sapphire_Compiler.exe` provides source execution and AST/textual IR inspection. It does not emit native Sapphire machine code.
- `Sapphire_Setup_Wizard.exe` installs the runtime, documentation, optional tools, PATH entry, `.sp` association, and shortcuts.

## Installation

On Windows, run `Sapphire_Setup_Wizard.exe`. Choose an installation directory and keep PATH and shortcuts enabled if desired. Open a new terminal after installation, then run:

```text
sapphire info
sapphire run hello.sp
sapphire studio
```

The installer also registers `.sp` files with the bundled compiler and creates Desktop and Start Menu shortcuts. Existing terminals do not automatically reload environment changes.

For source execution:

```text
python sapphire_lang/src/cli.py run path/to/script.sp
python -m unittest sapphire_lang.tests.test_sapphire sapphire_lang.tests.test_industrial_readiness
```

## Validation

The repository tests cover language evaluation, process and file helpers, concurrency blocks, agent planning and tool execution, failure handling, memory retrieval, persistence, sandbox boundaries, CPU/ML behavior, and optional CUDA reporting.

The reproducible local benchmark is run with:

```text
python benchmarks/benchmark_runtime.py
```

One reference run on Python 3.12.10 completed 100 parse-and-interpret iterations of a 100-item loop with:

- result: `4950`
- median: `0.21095 ms`
- minimum: `0.2023 ms`
- maximum: `0.7817 ms`

These values are machine-specific and are not a language-wide performance guarantee. No cross-language, large-model, cluster-throughput, or GPU-training benchmark is included because the repository does not currently run those workloads as part of its validation suite.

## Roadmap and Limitations

The following are not presented as completed features: a native compiler backend, production-grade isolation, persistent vector embeddings, event-driven agent declarations, DAG scheduling, verified multi-node training, automatic cluster recovery, and broad security certification.

See `INDUSTRIAL_READINESS.md` and `Sapphire_Capabilities_and_Transparency_Manual.pdf` for the tested scope and known limitations.
